cask "harvie" do
  version "0.8.3"
  sha256 "742e8816385210ea57bea64f1d93a3a6b2ccd1a09916c51c1d3f59a4bda00f3d"

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
