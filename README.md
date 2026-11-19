# Homebrew Tap

Custom Homebrew tap for macOS apps by [jorisnoo](https://github.com/jorisnoo).

## Installation

```sh
brew tap jorisnoo/tap
```

## Casks

| App                                                      | Description                                  | Install                                   |
|----------------------------------------------------------|----------------------------------------------|-------------------------------------------|
| [GDS.FM](https://github.com/jorisnoo/GDSPlayer)          | Menu bar player for GDS.FM radio             | `brew install jorisnoo/tap/gds-fm`        |
| [Harvie](https://github.com/jorisnoo/Harvie)             | Generate Swiss QR Bills for Harvest invoices | `brew install jorisnoo/tap/harvie`        |
| [RealExporter](https://github.com/jorisnoo/RealExporter) | Export and convert BeReal data               | `brew install jorisnoo/tap/real-exporter` |

The `harvest-qr-bill` cask was renamed to `harvie`. Homebrew uses the tap's rename map to resolve the old token.

`brew uninstall --zap` also removes the app's listed settings and data. For Harvie this includes its logo and templates in `~/Library/Application Support/Harvie`. Harvie 0.9.0 uses an unnamed SwiftData store: the tap deliberately leaves `~/Library/Application Support/default.store` and its sidecars alone because other apps can use that path. User-selected template folders and exported documents are not zap targets.

## Maintenance

See [RELEASING.md](RELEASING.md) for this repository’s release policy.
