#!/usr/bin/env python3
"""Builds the static Kodi repository (addons.xml, zips, assets) into _dist/.

The output of this script is published as-is to GitHub Pages. Each entry in
ADDONS is a path (relative to the repo root) to a directory containing an
addon.xml. "." refers to the repo root itself (the skin addon).
"""
import hashlib
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

REPO_ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
).strip()
OUT_DIR = os.path.join(REPO_ROOT, "_dist")

ADDONS = [".", "repository.gettuh"]


def read_addon_id_version(addon_dir):
    tree = ET.parse(os.path.join(REPO_ROOT, addon_dir, "addon.xml"))
    root = tree.getroot()
    return root.attrib["id"], root.attrib["version"]


def archive_addon(addon_dir, addon_id, out_zip):
    treeish = f"HEAD:{addon_dir}" if addon_dir != "." else "HEAD"
    subprocess.check_call(
        [
            "git",
            "archive",
            "--format=zip",
            f"--prefix={addon_id}/",
            "-o",
            out_zip,
            treeish,
        ],
        cwd=REPO_ROOT,
    )


def copy_if_exists(addon_dir, filename, dest_dir):
    src = os.path.join(REPO_ROOT, addon_dir, filename)
    if os.path.isfile(src):
        shutil.copy2(src, os.path.join(dest_dir, filename))


def build_addons_xml(addon_xml_paths, out_path):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<addons>"]
    for p in addon_xml_paths:
        with open(p, encoding="utf-8") as f:
            content = f.read().strip()
        if content.startswith("<?xml"):
            content = content.split("?>", 1)[1].strip()
        parts.append(content)
    parts.append("</addons>")
    xml_str = "\n".join(parts) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    return xml_str


def write_directory_listings(root_dir):
    """Writes an index.html per directory listing its entries.

    GitHub Pages serves no directory listing of its own (a bare folder URL
    404s without an index.html). Kodi's HTTP file-source browser needs an
    actual browsable listing to validate a source and to enumerate zips for
    "Install from zip file", so every directory gets one.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames.sort()
        entries = []
        if os.path.abspath(dirpath) != os.path.abspath(root_dir):
            entries.append(("../", "../"))
        for name in dirnames:
            entries.append((f"{name}/", f"{name}/"))
        for name in sorted(filenames):
            if name == "index.html":
                continue
            entries.append((name, name))

        links = "\n".join(
            f'<li><a href="{href}">{label}</a></li>' for href, label in entries
        )
        html = (
            "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\">"
            "<title>Index</title></head><body>\n<ul>\n"
            f"{links}\n</ul>\n</body></html>\n"
        )
        with open(os.path.join(dirpath, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)


def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    addon_xml_paths = []

    for addon_dir in ADDONS:
        addon_id, version = read_addon_id_version(addon_dir)
        dest_dir = os.path.join(OUT_DIR, addon_id)
        os.makedirs(dest_dir, exist_ok=True)

        zip_path = os.path.join(dest_dir, f"{addon_id}-{version}.zip")
        archive_addon(addon_dir, addon_id, zip_path)

        addon_xml_dest = os.path.join(dest_dir, "addon.xml")
        shutil.copy2(
            os.path.join(REPO_ROOT, addon_dir, "addon.xml"), addon_xml_dest
        )
        for asset in ("icon.png", "fanart.jpg", "changelog.txt"):
            copy_if_exists(addon_dir, asset, dest_dir)

        addon_xml_paths.append(addon_xml_dest)
        print(f"Packaged {addon_id} {version} -> {zip_path}")

    addons_xml_path = os.path.join(OUT_DIR, "addons.xml")
    xml_str = build_addons_xml(addon_xml_paths, addons_xml_path)

    md5 = hashlib.md5(xml_str.encode("utf-8")).hexdigest()
    with open(addons_xml_path + ".md5", "w", encoding="utf-8") as f:
        f.write(md5)

    print(f"Wrote {addons_xml_path} (md5 {md5})")

    write_directory_listings(OUT_DIR)
    print("Wrote index.html directory listings")


if __name__ == "__main__":
    main()
