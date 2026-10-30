cask "gds-fm" do
  version "0.2.5"
  sha256 "51db215be368e3d63dee4b1d3df2066793e6aa25f4f9321134e864087c1bbf4f"

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
