cask "real-exporter" do
  version "0.2.0"
  sha256 "e3f2c33c978a3c2658c5b8555815d315866f36ea3ed3170592cd5d37c83a374d"

  url "https://github.com/jorisnoo/RealExporter/releases/download/#{version}/RealExporter-#{version}.dmg"
  name "RealExporter"
  desc "Export and convert BeReal data"
  homepage "https://github.com/jorisnoo/RealExporter"

  depends_on macos: ">= :sonoma"
  auto_updates true

  app "RealExporter.app"

  zap trash: [
    "~/Library/Application Support/ch.noordermeer.RealExporter",
    "~/Library/Caches/ch.noordermeer.RealExporter",
    "~/Library/Preferences/ch.noordermeer.RealExporter.plist",
  ]
end
