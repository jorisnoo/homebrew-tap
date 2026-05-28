cask "harvie" do
  version "0.7.2"
  sha256 "aaac6421997cda01f7ffab5223c1046475e250397b71a5cdcc190695d266d82c"

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
