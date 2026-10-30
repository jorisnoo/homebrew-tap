cask "gds-fm" do
  version "0.2.6"
  sha256 "7589f11217e99f429b193091e757984dba8ba38577f9e6425fc563f153e4250a"

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
