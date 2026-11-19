# Release policy

This tap has no independent package releases or semantic version tags. A cask update follows the corresponding signed DMG release in GDSPlayer, Harvie or RealExporter. Keep its version, SHA-256, URL and app name tied to that exact release (no `v` prefix). Do not update another app's cask. Each app documents its release commands in `RELEASING.md`.

For a manual bump, verify the published DMG and its SHA-256, change only the intended cask and open a pull request against `main`. Wait for **Cask audit** before merging. The same check also runs after pushes to `main`, including direct updates from the existing app release workflows. It checks every cask with Homebrew style and strict online audit, fetches the assets without installing them, and checks the legacy token. A post-push check reports a bad direct update; it does not prevent one.

When changing a `zap` stanza, verify each path against the released bundle identifier and app source. Use only app-owned paths, never a shared default database, a wildcard for a store, or a user-selected folder.
