"""Publish one verified cask change. All tap reads are data, never executable code."""

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


TAP = "jorisnoo/homebrew-tap"
APPS = {
    "jorisnoo/GDSPlayer": ("gds-fm", "GDS.FM"),
    "jorisnoo/Harvie": ("harvie", "Harvie"),
    "jorisnoo/RealExporter": ("real-exporter", "RealExporter"),
}
VERSION = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gh(*args, data=None):
    output = subprocess.run(["gh", *args], check=True, text=True, stdout=subprocess.PIPE,
                            input=None if data is None else json.dumps(data)).stdout
    return output


def api(endpoint, data=None):
    args = ["api", endpoint]
    if data is not None:
        args.extend(["--input", "-"])
    return json.loads(gh(*args, data=data))


def tap(endpoint, data=None):
    return api(f"repos/{TAP}/{endpoint}", data)


def cask_at(path, sha):
    blob = tap(f"contents/{path}?ref={sha}")
    require(blob["type"] == "file" and blob["encoding"] == "base64", "Expected a cask file")
    return base64.b64decode(blob["content"]).decode("utf-8")


def updated(text, version, digest):
    pattern = rf'^  version "({VERSION})"\n  sha256 "([0-9a-f]{{64}})"$'
    matches = list(re.finditer(pattern, text, re.MULTILINE))
    require(len(matches) == 1 and len(re.findall(r'^\s*(?:version|sha256)\s', text, re.MULTILINE)) == 2,
            "Expected exactly one literal version and sha256 in the cask")
    match = matches[0]
    old_version, old_digest = match.groups()
    key = lambda value: tuple(map(int, value.split(".")))
    require(key(version) >= key(old_version), "Refusing to downgrade the cask")
    require(old_version != version or old_digest == digest, "Digest changed for the same cask version")
    return text[:match.start()] + f'  version "{version}"\n  sha256 "{digest}"' + text[match.end():]


def published_digest(repo, version, dmg, name):
    filename = f"{name}-{version}.dmg"
    require(dmg.name == filename and dmg.is_file(), f"Expected released asset {filename}")
    sha = hashlib.sha256()
    with dmg.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    digest = sha.hexdigest()
    release = api(f"repos/{repo}/releases/tags/{version}")
    require(not release["draft"] and not release["prerelease"] and release["tag_name"] == version,
            "Expected a published stable release at the exact tag")
    assets = [a for a in release["assets"] if a["name"] == filename]
    require(len(assets) == 1 and assets[0]["state"] == "uploaded" and assets[0]["digest"] == f"sha256:{digest}",
            "DMG does not match the published release asset digest")
    return digest


def branch_head(branch):
    ref = f"refs/heads/{branch}"
    matches = tap(f"git/matching-refs/heads/{branch}")
    return next((r["object"]["sha"] for r in matches if r["ref"] == ref), None)


def commit_cask(branch, base, path, text, title):
    mutation = """mutation($input: CreateCommitOnBranchInput!) {
      createCommitOnBranch(input: $input) { commit { oid } }
    }"""
    input_data = {
        "branch": {"repositoryNameWithOwner": TAP, "branchName": branch},
        "expectedHeadOid": base,
        "message": {"headline": title},
        "fileChanges": {"additions": [{"path": path, "contents": base64.b64encode(text.encode()).decode()}]},
    }
    result = api("graphql", {"query": mutation, "variables": {"input": input_data}})
    return result["data"]["createCommitOnBranch"]["commit"]["oid"]


def propose(repo, version, dmg):
    require(repo in APPS, "Unsupported release producer")
    require(re.fullmatch(VERSION, version), "Expected stable X.Y.Z version without a prefix")
    cask, name = APPS[repo]
    digest = published_digest(repo, version, dmg, name)
    path = f"Casks/{cask}.rb"
    branch = f"release/{cask}/{version}"
    main = tap("branches/main")
    base = main["commit"]["sha"]
    original = cask_at(path, base)
    desired = updated(original, version, digest)
    if original == desired:
        print(f"{TAP} already contains {cask} {version} with the published digest")
        return

    # gh --auto may merge immediately when no check is required. Fail closed
    # before making changes; this public endpoint needs no Administration scope.
    checks = main.get("protection", {}).get("required_status_checks", {})
    require(main["protected"] and checks.get("enforcement_level") == "everyone" and
            {"context": "Cask audit", "app_id": 15368} in checks.get("checks", []),
            "main must require GitHub Actions' Cask audit check, including for admins")
    title = f"Update {cask} to {version}"
    pulls = tap(f"pulls?base=main&head=jorisnoo:{branch}&state=all")
    require(len(pulls) <= 1 and all(p["state"] == "open" for p in pulls),
            "Refusing to replace a closed or ambiguous release PR")
    head = branch_head(branch)
    if not head:
        require(not pulls, "Existing PR head is missing")
        tap("git/refs", {"ref": f"refs/heads/{branch}", "sha": base})
        head = base

    if head != base:
        # GitHub's three-dot comparison covers everything this PR introduces,
        # even if main has advanced on unrelated files. Never trust a branch name.
        comparison = tap(f"compare/{base}...{head}")
        ahead = comparison["ahead_by"]
        if ahead:
            files = [(f["filename"], f["status"]) for f in comparison["files"]]
            require(ahead == 1 and files == [(path, "modified")] and cask_at(path, head) == desired,
                    "Existing release branch differs from the intended one-file update")
            tree = tap(f"git/trees/{head}?recursive=1")
            require(any(entry["path"] == path and entry["mode"] == "100644" for entry in tree["tree"]),
                    "Expected a regular non-executable cask file")
        else:
            require(cask_at(path, head) == original, "Recovered branch has stale cask contents")
    else:
        ahead = 0
    if not ahead:
        require(not pulls, "Refusing to modify an unexpected open PR")
        head = commit_cask(branch, head, path, desired, title)

    if not pulls:
        pulls = [tap("pulls", {"head": branch, "base": "main", "title": title,
                              "body": f"Published release: https://github.com/{repo}/releases/tag/{version}\n\nSHA-256: `{digest}`"})]
    pr = pulls[0]
    require(pr["base"]["ref"] == "main" and pr["head"]["repo"]["full_name"] == TAP and
            pr["head"]["ref"] == branch and pr["head"]["sha"] == head and not pr["draft"],
            "Unexpected release PR base, head or state")
    number = str(pr["number"])
    auto = pr["auto_merge"]
    if auto:
        require(auto["merge_method"] == "squash", "Existing PR uses a different merge method")
    else:
        gh("pr", "merge", number, "--repo", TAP, "--auto", "--squash", "--match-head-commit", head)
    print(f"https://github.com/{TAP}/pull/{number}")


if __name__ == "__main__":
    try:
        require(os.environ.get("GITHUB_EVENT_NAME") == "push", "Only push-triggered app releases are supported")
        require(os.environ.get("GH_TOKEN"), "Missing tap token")
        propose(os.environ["GITHUB_REPOSITORY"], os.environ["RELEASE_VERSION"], Path(os.environ["RELEASE_DMG"]))
    except (KeyError, OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
