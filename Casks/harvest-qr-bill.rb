cask "harvest-qr-bill" do
  version "0.3.0"
  sha256 "PLACEHOLDER"

  url "https://github.com/jorisnoo/HarvestQRBill/releases/download/#{version}/HarvestQRBill-#{version}.dmg"
  name "HarvestQRBill"
  desc "Generate Swiss QR Bills for Harvest invoices"
  homepage "https://github.com/jorisnoo/HarvestQRBill"

  depends_on macos: ">= :sequoia"

  app "HarvestQRBill.app"

  zap trash: [
    "~/Library/Application Support/ch.noordermeer.HarvestQRBill",
    "~/Library/Caches/ch.noordermeer.HarvestQRBill",
    "~/Library/Preferences/ch.noordermeer.HarvestQRBill.plist",
  ]
end
