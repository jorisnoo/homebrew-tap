cask "harvie" do
  version "0.7.0"
  sha256 "5dfe0fb66aa99c388552fa079559abe838e718a1d8b3425db02dcc2961f7ac57"

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
