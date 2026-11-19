import base64
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_cask as action


class CaskProposal(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dmg = Path(tmp.name) / 'Harvie-1.10.0.dmg'
        self.dmg.write_bytes(b'published asset fixture')
        self.digest = hashlib.sha256(self.dmg.read_bytes()).hexdigest()
        self.base = 'a' * 40
        self.head = 'b' * 40
        self.branch = 'release/harvie/1.10.0'
        self.path = 'Casks/harvie.rb'
        self.release = {'draft': False, 'prerelease': False, 'tag_name': '1.10.0', 'assets': [
            {'name': self.dmg.name, 'state': 'uploaded', 'digest': 'sha256:' + self.digest}]}
        self.main = {'commit': {'sha': self.base}, 'protected': True, 'protection': {'required_status_checks': {
            'enforcement_level': 'everyone', 'checks': [{'context': 'Cask audit', 'app_id': 15368}]}}}
        self.original = f'cask "harvie" do\n  version "1.9.0"\n  sha256 "{"0" * 64}"\n\n  app "Harvie.app"\nend\n'
        self.desired = self.original.replace('1.9.0', '1.10.0').replace('0' * 64, self.digest)
        self.blobs = {self.base: self.original, self.head: self.desired}
        self.remote = None
        self.pulls = []
        self.pr = {'number': 42, 'state': 'open', 'draft': False, 'auto_merge': None, 'base': {'ref': 'main'},
                   'head': {'sha': self.head, 'ref': self.branch, 'repo': {'full_name': action.TAP}}}
        self.diff = {'ahead_by': 1, 'files': [{'filename': self.path, 'status': 'modified'}]}
        self.mode = '100644'
        self.writes = []
        for name, replacement in [('api', self.api), ('gh', self.merge)]:
            p = patch.object(action, name, replacement)
            p.start()
            self.addCleanup(p.stop)

    def api(self, endpoint, data=None):
        if data is not None:
            self.writes.append((endpoint, data))
        if endpoint == 'repos/jorisnoo/Harvie/releases/tags/1.10.0' and data is None:
            return self.release
        if endpoint == 'graphql':
            change = data['variables']['input']
            self.assertIn('createCommitOnBranch', data['query'])
            self.assertEqual(change['branch'], {'repositoryNameWithOwner': action.TAP, 'branchName': self.branch})
            self.assertEqual(change['expectedHeadOid'], self.remote)
            self.assertEqual(change['fileChanges'], {'additions': [
                {'path': self.path, 'contents': base64.b64encode(self.desired.encode()).decode()}]})
            self.remote = self.head
            return {'data': {'createCommitOnBranch': {'commit': {'oid': self.head}}}}
        prefix = f'repos/{action.TAP}/'
        self.assertTrue(endpoint.startswith(prefix))
        endpoint = endpoint[len(prefix):]
        if endpoint == 'branches/main' and data is None:
            return self.main
        for sha, text in self.blobs.items():
            if endpoint == f'contents/{self.path}?ref={sha}' and data is None:
                return {'type': 'file', 'encoding': 'base64', 'content': base64.b64encode(text.encode()).decode()}
        if endpoint == f'pulls?base=main&head=jorisnoo:{self.branch}&state=all' and data is None:
            return self.pulls
        if endpoint == f'git/matching-refs/heads/{self.branch}' and data is None:
            return [] if not self.remote else [{'ref': f'refs/heads/{self.branch}', 'object': {'sha': self.remote}}]
        if endpoint == 'git/refs':
            self.assertEqual(data, {'ref': f'refs/heads/{self.branch}', 'sha': self.base})
            self.remote = self.base
            return {}
        if endpoint == f'compare/{self.base}...{self.remote}' and data is None:
            return self.diff
        if endpoint == f'git/trees/{self.head}?recursive=1' and data is None:
            return {'tree': [{'path': self.path, 'mode': self.mode}]}
        if endpoint == 'pulls':
            self.assertEqual((data['base'], data['head']), ('main', self.branch))
            self.pulls = [self.pr]
            return self.pr
        self.fail(f'Unexpected API call: {endpoint}')

    def merge(self, *args):
        self.assertEqual(args, ('pr', 'merge', '42', '--repo', action.TAP, '--auto', '--squash',
                                '--match-head-commit', self.head))
        self.writes.append(('merge', args))

    def propose(self):
        action.propose('jorisnoo/Harvie', '1.10.0', self.dmg)

    def test_new_and_rerun_use_the_same_matching_pr(self):
        self.propose()
        self.assertEqual([w[0].split('/')[-1] for w in self.writes], ['refs', 'graphql', 'pulls', 'merge'])
        self.writes.clear()
        self.propose()
        self.assertEqual([w[0] for w in self.writes], ['merge'])
        self.writes.clear()
        self.pr['auto_merge'] = {'merge_method': 'squash'}
        self.propose()
        self.assertFalse(self.writes)

    def test_recover_branch_after_partial_failure(self):
        for head, expected in [(self.base, ['graphql', 'pulls', 'merge']), (self.head, ['pulls', 'merge'])]:
            with self.subTest(head=head):
                self.remote, self.pulls, self.writes = head, [], []
                self.propose()
                self.assertEqual([w[0].split('/')[-1] for w in self.writes], expected)

    def test_already_shipped_is_read_only(self):
        self.blobs[self.base] = self.desired
        self.propose()
        self.assertFalse(self.writes)

    def test_downgrade_and_same_version_replacement(self):
        for version in ('2.0.0', '1.10.0'):
            with self.subTest(version=version), self.assertRaises(ValueError):
                self.blobs[self.base] = self.original.replace('1.9.0', version)
                self.propose()
        self.assertFalse(self.writes)

    def test_require_exact_asset_and_stable_producer(self):
        for repo, version in [('different/Harvie', '1.10.0'), ('jorisnoo/Harvie', '1.10.0-beta.1'),
                              ('jorisnoo/Harvie', 'v1.10.0'), ('jorisnoo/Harvie', '01.10.0')]:
            with self.subTest(repo=repo, version=version), self.assertRaises(ValueError):
                action.propose(repo, version, self.dmg)
        self.release['prerelease'] = True
        with self.assertRaisesRegex(ValueError, 'stable release'):
            self.propose()
        self.release['prerelease'] = False
        self.dmg.write_bytes(b'different')
        with self.assertRaisesRegex(ValueError, 'asset digest'):
            self.propose()
        self.assertFalse(self.writes)

    def test_missing_or_bypassable_required_check(self):
        required = self.main['protection']['required_status_checks']
        for level, app in [('off', 15368), ('non_admins', 15368), ('everyone', 1)]:
            with self.subTest(level=level), self.assertRaisesRegex(ValueError, 'must require'):
                required.update(enforcement_level=level, checks=[{'context': 'Cask audit', 'app_id': app}])
                self.propose()
        self.assertFalse(self.writes)

    def test_unrelated_or_different_pending_changes_are_not_merged(self):
        self.remote, self.pulls = self.head, [self.pr]
        self.diff['files'].append({'filename': 'README.md', 'status': 'modified'})
        with self.assertRaisesRegex(ValueError, 'one-file update'):
            self.propose()
        self.diff['files'].pop()
        self.mode = '100755'
        with self.assertRaisesRegex(ValueError, 'non-executable'):
            self.propose()
        self.mode = '100644'
        self.blobs[self.head] = self.desired + '# unrelated\n'
        with self.assertRaisesRegex(ValueError, 'one-file update'):
            self.propose()
        self.assertFalse(self.writes)

    def test_closed_or_mismatching_pr_is_left_alone(self):
        self.remote, self.pulls = self.head, [self.pr]
        self.pr['state'] = 'closed'
        with self.assertRaisesRegex(ValueError, 'closed'):
            self.propose()
        self.pr['state'] = 'open'
        self.pr['head']['sha'] = 'c' * 40
        with self.assertRaisesRegex(ValueError, 'head or state'):
            self.propose()
        self.assertFalse(self.writes)
