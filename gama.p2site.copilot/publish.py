"""Assemble immutable release repositories behind a stable composite p2 site."""

import argparse
import hashlib
import lzma
from pathlib import Path
import re
import shutil
import time
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


def assemble(incoming, site, release):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", release):
        raise ValueError("Invalid release directory name")
    for kind in ("content", "artifacts"):
        with ZipFile(incoming / f"{kind}.jar") as archive:
            ET.fromstring(archive.read(f"{kind}.xml"))
    if not (incoming / "plugins").is_dir() or not (incoming / "features").is_dir():
        raise ValueError("The incoming repository has no plugins or features")
    releases = site / "releases"
    releases.mkdir(parents=True, exist_ok=True)
    destination = releases / release
    if destination.exists():
        raise ValueError(f"Refusing to overwrite immutable release {release}")
    for folder in ("plugins", "features", "binary"):
        source = incoming / folder
        if not source.exists():
            continue
        for artifact in source.iterdir():
            target = site / folder / artifact.name
            target.parent.mkdir(exist_ok=True)
            if target.exists():
                with artifact.open("rb") as left, target.open("rb") as right:
                    if hashlib.file_digest(left, "sha256").digest() != hashlib.file_digest(right, "sha256").digest():
                        raise ValueError(f"Different bytes for retained artifact: {target}")
            else:
                shutil.copy2(artifact, target)
    shutil.copytree(incoming, destination, ignore=shutil.ignore_patterns("plugins", "features", "binary"))
    with ZipFile(destination / "artifacts.jar") as archive:
        artifacts = ET.fromstring(archive.read("artifacts.xml"))
    for rule in artifacts.findall("mappings/rule"):
        output = rule.get("output")
        if not output.startswith("${repoUrl}/"):
            raise ValueError(f"Unexpected artifact mapping: {output}")
        rule.set("output", output.replace("${repoUrl}/", "${repoUrl}/../../", 1))
    metadata = (
        b'<?xml version="1.0" encoding="UTF-8"?>\n<?artifactRepository version="1.1.0"?>\n'
        + ET.tostring(artifacts, encoding="utf-8") + b"\n")
    with ZipFile(destination / "artifacts.jar", "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("artifacts.xml", metadata)
    (destination / "artifacts.xml.xz").write_bytes(lzma.compress(metadata))
    if (destination / "artifacts.xml").exists():
        (destination / "artifacts.xml").write_bytes(metadata)
    children = sorted(p for p in releases.iterdir() if p.is_dir())
    for child in children:
        if not (child / "content.jar").is_file() or not (child / "artifacts.jar").is_file():
            raise ValueError(f"Incomplete retained repository: {child}")
    for kind in ("Metadata", "Artifact"):
        root = ET.Element("repository", {
            "name": "GitHub Copilot for GAMA",
            "type": f"org.eclipse.equinox.internal.p2.{kind.lower()}.repository.Composite{kind}Repository",
            "version": "1.0.0",
        })
        properties = ET.SubElement(root, "properties", size="1")
        ET.SubElement(properties, "property", name="p2.timestamp", value=str(int(time.time() * 1000)))
        entries = ET.SubElement(root, "children", size=str(len(children)))
        for child in children:
            ET.SubElement(entries, "child", location=f"releases/{child.name}")
        ET.indent(root)
        filename = "compositeContent.xml" if kind == "Metadata" else "compositeArtifacts.xml"
        instruction = "compositeMetadataRepository" if kind == "Metadata" else "compositeArtifactRepository"
        (site / filename).write_bytes(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<?{instruction} version="1.0.0"?>\n'.encode()
            + ET.tostring(root, encoding="utf-8") + b"\n")
    (site / "p2.index").write_text(
        "version=1\nmetadata.repository.factory.order=compositeContent.xml,!\n"
        "artifact.repository.factory.order=compositeArtifacts.xml,!\n", encoding="utf-8")
    (site / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("incoming", type=Path)
    parser.add_argument("site", type=Path)
    parser.add_argument("release")
    args = parser.parse_args()
    assemble(args.incoming, args.site, args.release)
