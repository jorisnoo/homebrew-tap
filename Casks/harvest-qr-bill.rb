cask "harvest-qr-bill" do
  version "0.3.0"
  sha256 "8cab6a08789e368895366c035bf8d6294ae0aff2542f2556addb3f840f05dfc6"

  url "https://github.com/jorisnoo/HarvestQRBill/releases/download/#{version}/HarvestQRBill-#{version}.dmg"
  name "HarvestQRBill"
  desc "Generate Swiss QR Bills for Harvest invoices"
  homepage "https://github.com/jorisnoo/HarvestQRBill"

  depends_on macos: ">= :sonoma"
  auto_updates true

  app "HarvestQRBill.app"

  zap trash: [
    "~/Library/Application Support/ch.noordermeer.HarvestQRBill",
    "~/Library/Caches/ch.noordermeer.HarvestQRBill",
    "~/Library/Preferences/ch.noordermeer.HarvestQRBill.plist",
  ]
end
