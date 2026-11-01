"""Download and verify the locked, unmodified upstream p2 archive before Tycho starts."""

import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def prepare():
    lock = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
    feature = ET.parse(ROOT / "gama.feature.copilot/feature.xml").getroot()
    include = feature.find("includes[@id='com.microsoft.copilot.eclipse.feature']")
    if include is None or include.get("version") != lock["version"]:
        raise ValueError("The wrapper feature and upstream.lock.json must pin the same version")
    cache = ROOT / ".build"
    cache.mkdir(exist_ok=True)
    archive = cache / "upstream.zip"
    if not archive.exists():
        temporary = cache / "upstream.zip.part"
        with urllib.request.urlopen(lock["url"], timeout=120) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        if digest(temporary) != lock["sha256"]:
            raise ValueError("Downloaded upstream archive does not match the locked SHA-256")
        temporary.replace(archive)
    if digest(archive) != lock["sha256"]:
        raise ValueError("Cached upstream archive does not match the locked SHA-256")
    destination = cache / "upstream"
    destination.mkdir(exist_ok=True)
    with ZipFile(archive) as source:
        for entry in source.infolist():
            path = destination / entry.filename
            if not path.resolve().is_relative_to(destination.resolve()):
                raise ValueError(f"Unsafe archive entry: {entry.filename}")
        source.extractall(destination)
    with ZipFile(destination / "content.jar") as metadata:
        units = ET.fromstring(metadata.read("content.xml")).find("units")
    if units.find(
        f"unit[@id='com.microsoft.copilot.eclipse.feature.feature.group'][@version='{lock['version']}']"
    ) is None:
        raise ValueError("Pinned feature version is absent from upstream metadata")
    print(f"Verified Copilot {lock['version']} ({lock['sha256']})")


if __name__ == "__main__":
    prepare()
