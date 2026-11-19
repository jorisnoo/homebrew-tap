# Release policy

This tap has no independent package releases or semantic version tags. A cask update follows the corresponding signed DMG release in GDSPlayer, Harvie or RealExporter. Keep its version, SHA-256, URL and app name tied to that exact release (no `v` prefix). Do not update another app's cask. Each app documents its release commands in `RELEASING.md`.

GDSPlayer, Harvie and RealExporter submit cask updates through the `update-cask` action pinned to a tap commit in each producer's release workflow. The action checks the DMG against the published release asset, changes only that app's cask on a release branch, and opens or reuses a pull request. It requests GitHub's native squash auto-merge at the verified head commit. **Cask audit** runs on the PR; a failing check holds the PR open. Inspect the failure rather than pushing to `main` or using an administrator bypass. The same check runs again after merge.

The producer's `HOMEBREW_TAP_PAT` must be a fine-grained token for this tap with **Contents: read and write**, **Pull requests: read and write**, and the default **Metadata: read**. The producer releases and their asset digests are public. The action does not require Administration or Workflows permission. `main` must require **Cask audit** from GitHub Actions, including for administrators, and the tap must allow squash merges and auto-merge.

For a manual bump, verify the published DMG and its SHA-256, change only the intended cask, and open a pull request against `main`. The audit checks every cask with Homebrew style and strict online audit, fetches the assets without installing them, verifies the legacy token and runs the producer action's tests.

When changing a `zap` stanza, verify each path against the released bundle identifier and app source. Use only app-owned paths, never a shared default database, a wildcard for a store, or a user-selected folder.
