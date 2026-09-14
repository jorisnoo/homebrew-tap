cask "real-exporter" do
  version "0.2.1"
  sha256 "d3d2e53fbc36dc91f9de884d6a4c4bf71ce78a4d7bcc8c1faceddecb9edc1e4a"

  url "https://github.com/jorisnoo/RealExporter/releases/download/#{version}/RealExporter-#{version}.dmg"
  name "RealExporter"
  desc "Export and convert BeReal data"
  homepage "https://github.com/jorisnoo/RealExporter"

  depends_on macos: ">= :sonoma"
  auto_updates true

  app "RealExporter.app"

  zap trash: [
    "~/Library/Application Support/app.realexporter",
    "~/Library/Caches/app.realexporter",
    "~/Library/Preferences/app.realexporter.plist",
  ]
end
