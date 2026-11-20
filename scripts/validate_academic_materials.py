#!/usr/bin/env python3
"""Validate the published academic project source and research materials."""

import re
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ACADEMIC = ROOT / "projects"

REQUIRED = [
    "README.md",
    "academic-projects.html",
    "02-advanced-book-shop/README.md",
    "02-advanced-book-shop/index.html",
    "02-advanced-book-shop/docs/database-design.md",
    "02-advanced-book-shop/docs/php-source-guide.md",
    "02-advanced-book-shop/sql/schema.sql",
    "03-fire-smoke-cse360/README.md",
    "03-fire-smoke-cse360/index.html",
    "03-fire-smoke-cse360/arduino/code.ino",
    "03-fire-smoke-cse360/arduino/B_proto.ino",
    "03-fire-smoke-cse360/materials/CSE360 Project Report - Group 5.pdf",
    "03-fire-smoke-cse360/materials/Project V1.zip",
    "04-assembly-password-checker/src/password_checker.asm",
    "04-assembly-password-checker/tests/test.sh",
]

for path in REQUIRED:
    item = ACADEMIC / path
    if not item.is_file() or item.stat().st_size == 0:
        raise AssertionError(f"Missing academic artifact: {path}")

sql = (ACADEMIC / "02-advanced-book-shop/sql/schema.sql").read_text(encoding="utf-8")
tables = set(re.findall(r"CREATE TABLE `([^`]+)`", sql, re.IGNORECASE))
expected_tables = {
    "cart", "categories", "clients", "inventory", "orders", "order_list",
    "products", "sales", "sub_categories", "system_info", "users",
}
if tables != expected_tables:
    raise AssertionError(f"Unexpected bookshop schema tables: {tables ^ expected_tables}")
if re.search(r"\bINSERT\s+INTO\b", sql, re.IGNORECASE):
    raise AssertionError("Bookshop schema should contain table definitions only")

report = ACADEMIC / "03-fire-smoke-cse360/materials/CSE360 Project Report - Group 5.pdf"
if not report.read_bytes().startswith(b"%PDF-"):
    raise AssertionError("Invalid CSE360 report PDF")

archive = ACADEMIC / "03-fire-smoke-cse360/materials/Project V1.zip"
with ZipFile(archive) as source:
    names = source.namelist()
    if not any(name.endswith("B_proto.ino") for name in names):
        raise AssertionError("Arduino serial prototype missing in original archive")
    if not any(name.endswith("/code.ino") for name in names):
        raise AssertionError("Arduino detection sketch missing in original archive")
    bad_file = source.testzip()
    if bad_file:
        raise AssertionError(f"Invalid entry in Arduino archive: {bad_file}")

for name in ("code.ino", "B_proto.ino"):
    source = (ACADEMIC / "03-fire-smoke-cse360/arduino" / name).read_text(encoding="utf-8")
    if "void setup()" not in source or "void loop()" not in source:
        raise AssertionError(f"Arduino sketch entry points missing: {name}")

overview = (ACADEMIC / "README.md").read_text(encoding="utf-8")
for project in (
    "Advanced School Management", "Advanced Book Shop Management",
    "Advanced Fire and Smoke Detection", "Assembly Password",
    "Contextual Hate Speech", "Enhancing Infrastructure Detection",
):
    if project not in overview:
        raise AssertionError(f"Project absent from index: {project}")

print("Academic project files, SQL schema, Arduino sketches, source ZIP, PDF and index verified.")
