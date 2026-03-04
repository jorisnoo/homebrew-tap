cask "harvest-qr-bill" do
  version "0.4.0"
  sha256 "b2e682e8844abf7b278f34d9eb5a518314b192fd773ea8cceca19421490b408b"

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
