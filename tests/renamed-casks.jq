# Check Homebrew's resolved artifacts, not the Ruby source. In particular,
# Harvie's unscoped default.store and user-selected folders must stay untouched.
def zap($token):
  [.casks[] | select(.token == $token) | .artifacts[] | .zap? // empty | .[]];

def per_bundle($id):
  ["~/Library/Caches/\($id)", "~/Library/HTTPStorages/\($id)", "~/Library/Preferences/\($id).plist"];

(zap("harvie") == [{trash: (["~/Library/Application Support/Harvie"] + per_bundle("app.harvie") + ["~/Library/WebKit/app.harvie"])}]) and
(zap("real-exporter") == [{trash: per_bundle("ch.noordermeer.RealExporter")}])
