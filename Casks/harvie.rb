cask "harvie" do
  version "0.4.4"
  sha256 "4ca56bc55bcea67b133000f981f1fe579d5061de594a380fe7ae157393af12f9"

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
