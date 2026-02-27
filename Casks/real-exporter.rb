cask "real-exporter" do
  version "0.1.2"
  sha256 "f30af6c70f80bac28adec0ae20bf2d7b37b70121d02169828433aa32151d7372"

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
