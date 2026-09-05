#!/usr/bin/env python3
"""
Extract the metadata AltStore/SideStore need out of a raw .ipa:
- CFBundleIdentifier
- CFBundleShortVersionString (fallback if the GitHub tag is ever missing)
- MinimumOSVersion
- file size in bytes
- sha256 of the file

Usage: read_ipa_metadata.py plezy.ipa   (prints JSON to stdout)
"""
import hashlib
import json
import plistlib
import sys
import zipfile
from pathlib import Path


def main() -> None:
    ipa_path = Path(sys.argv[1])
    data = ipa_path.read_bytes()

    with zipfile.ZipFile(ipa_path) as zf:
        # Info.plist always lives at Payload/<Something>.app/Info.plist
        info_plist_name = next(
            n for n in zf.namelist()
            if n.startswith("Payload/") and n.endswith(".app/Info.plist")
        )
        with zf.open(info_plist_name) as f:
            # plistlib handles both XML and binary plists transparently
            info = plistlib.load(f)

    meta = {
        "bundle_identifier": info.get("CFBundleIdentifier"),
        "bundle_version": info.get("CFBundleShortVersionString"),
        "min_os_version": info.get("MinimumOSVersion", "15.0"),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
