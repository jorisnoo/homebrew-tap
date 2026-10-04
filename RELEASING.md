# Release policy

This tap has no independent package releases or semantic version tags. App releases in Harvie and RealExporter update their own casks after the signed DMG is published. Keep each cask’s version, SHA-256, download URL and app name tied to that app’s exact release without a `v` prefix. Do not update another app’s cask. For a manual update, download and verify the published DMG, calculate its SHA-256, update only the intended cask, and check it with Homebrew’s cask lint/audit tools before committing. The app repositories document their release commands in `RELEASING.md`.
