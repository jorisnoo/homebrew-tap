cask "harvest-qr-bill" do
  version "0.4.3"
  sha256 "4a1cf55b056662163a0e29b33d7697ca217d0d8ba225b65fd87a03a5f3b2c47e"

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
