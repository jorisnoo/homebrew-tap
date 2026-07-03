cask "harvie" do
  version "0.8.0"
  sha256 "e95c385149db0835e8aaf2d7e6abf566fdfe4d74b25660319e09d797f3ca3d9b"

  url "https://github.com/jorisnoo/Harvie/releases/download/#{version}/Harvie-#{version}.dmg"
  name "Harvie"
  desc "Generate Swiss QR Bills for Harvest invoices"
  homepage "https://github.com/jorisnoo/Harvie"

  depends_on macos: ">= :sonoma"
  auto_updates true

  app "Harvie.app"

  zap trash: [
    "~/Library/Application Support/app.harvie",
    "~/Library/Caches/app.harvie",
    "~/Library/Preferences/app.harvie.plist",
  ]
end
