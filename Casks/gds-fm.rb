cask "gds-fm" do
  version "0.2.7"
  sha256 "a6fc87de36d4ff0a30c685072aec698315987d2b6fea1db91e9672ee4828ee21"

  url "https://github.com/jorisnoo/GDSPlayer/releases/download/#{version}/GDS.FM-#{version}.dmg"
  name "GDS.FM"
  desc "Menu bar player for GDS.FM radio"
  homepage "https://github.com/jorisnoo/GDSPlayer"

  auto_updates true
  depends_on macos: :sequoia

  app "GDS.FM.app"

  zap trash: [
    "~/Library/Caches/ch.noordermeer.GDSPlayer",
    "~/Library/HTTPStorages/ch.noordermeer.GDSPlayer",
    "~/Library/Preferences/ch.noordermeer.GDSPlayer.plist",
  ]
end
