cask "harvest-qr-bill" do
  version "0.4.2"
  sha256 "083053741be1c2e183d6e9cd6df75d1869210d7145a69361cbe40f84b4933bd6"

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
