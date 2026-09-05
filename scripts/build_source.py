#!/usr/bin/env python3
"""
Combine release info (from env vars, set by the workflow) and ipa_meta.json
(from read_ipa_metadata.py) into an AltStore/SideStore-compatible source.json.

Reads:  ipa_meta.json, env vars VERSION / IPA_URL / NOTES
Writes: source.json
"""
import datetime
import json
import os

with open("ipa_meta.json") as f:
    meta = json.load(f)

version = os.environ["VERSION"]
ipa_url = os.environ["IPA_URL"]
notes = os.environ.get("NOTES", "").strip() or "See upstream release notes."
today = datetime.date.today().isoformat()

source = {
    "name": "Plezy (unofficial, auto-updated)",
    "identifier": "io.github.am133.plezy-altstore-source",
    "sourceURL": "https://am133.github.io/plezy-altstore-source/source.json",
    "apps": [
        {
            "name": "Plezy",
            "bundleIdentifier": meta["bundle_identifier"],
            "developerName": "edde746",
            "subtitle": "Plex & Jellyfin client",
            "localizedDescription": (
                "Modern cross-platform Plex & Jellyfin client. "
                "This source is an unofficial mirror that tracks the IPA "
                "attached to each GitHub release automatically."
            ),
            "iconURL": "https://raw.githubusercontent.com/edde746/plezy/main/assets/plezy.png",
            "tintColor": "#1e2327",
            "size": meta["size"],
            "versions": [
                {
                    "version": version,
                    "date": today,
                    "localizedDescription": notes,
                    "downloadURL": ipa_url,
                    "size": meta["size"],
                    "sha256": meta["sha256"],
                    "minOSVersion": meta["min_os_version"],
                }
            ],
        }
    ],
    "news": [],
}

with open("source.json", "w") as f:
    json.dump(source, f, indent=2)
    f.write("\n")

print(f"Wrote source.json for Plezy {version}")
