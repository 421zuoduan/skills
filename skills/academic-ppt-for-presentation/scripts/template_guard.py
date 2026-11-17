#!/usr/bin/env python3
"""Read-only, conservative OOXML style guard for cloned PowerPoint text shapes.

inventory TEMPLATE prints an identity provenance map. Edit that map to describe
the output's actual slide/shape/paragraph donors, then check TEMPLATE OUTPUT --map
MAP. This checks structural style preservation, not layout or visual fidelity.
Exit codes: 0 pass, 1 style mismatch, 2 invalid/unsupported input.
"""

import argparse
import copy
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
R = "{" + NS["r"] + "}"
RUN_PATH = r"(?:a:r\[[1-9][0-9]*\]/a:rPr|a:fld\[[1-9][0-9]*\]/a:rPr|a:pPr/a:defRPr|a:endParaRPr)"
LAYOUT_ISSUES = {"overflow", "overlap", "grouping", "spacing_imbalance"}
ADJUSTMENT_FIELDS = {"slide", "shape", "paragraph", "path", "attribute", "before", "after",
                     "issue", "reason", "alternatives", "before_render", "after_render"}


class Unsupported(ValueError):
    pass


def signature(node):
    """Namespace-prefix/attribute-order independent; preserve absent properties."""
    if node is None:
        return None
    return (node.tag, tuple(sorted(node.attrib.items())),
            node.text if node.text and node.text.strip() else None,
            tuple(signature(child) for child in node))


def pick(node, path):
    return signature(node.find(path, NS))


def require(condition, message):
    if not condition:
        raise Unsupported(message)


def number(value, limit, label):
    require(type(value) is int and 1 <= value <= limit,
            f"{label}: expected integer in 1..{limit}, got {value!r}")
    return value - 1


def keys(value, allowed, label):
    require(isinstance(value, dict), f"{label}: expected an object")
    require(not set(value) - set(allowed),
            f"{label}: unknown keys {sorted(set(value) - set(allowed))}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def adjustment_index(records, slide_count):
    require(isinstance(records, list), "adjustments must be a list")
    grouped, seen = {}, set()
    for record in records:
        keys(record, ADJUSTMENT_FIELDS, "adjustment")
        require(set(record) == ADJUSTMENT_FIELDS, "adjustment: all fields are required")
        number(record["slide"], slide_count, "adjustment slide")
        require(type(record["paragraph"]) is int and record["paragraph"] >= 1,
                "adjustment paragraph must be a positive integer")
        for field in ADJUSTMENT_FIELDS - {"slide", "paragraph"}:
            require(isinstance(record[field], str) and record[field].strip(),
                    f"adjustment {field} must be a nonempty string")
        require(record["before_render"].strip() != record["after_render"].strip(),
                "adjustment: before_render and after_render must differ")
        require(record["before"] != record["after"], "adjustment must change the property")
        target = (record["slide"], record["shape"], record["paragraph"])
        prop = target + (record["path"], record["attribute"])
        require(prop not in seen, f"Duplicate adjusted property: {prop}")
        seen.add(prop)
        grouped.setdefault(target, []).append(record)
    return grouped


def explicit_value(paragraph, path, attribute, label):
    nodes = paragraph.findall(path, NS)
    require(len(nodes) == 1 and attribute in nodes[0].attrib,
            f"{label}: property must exist explicitly at exactly one node: {path} @{attribute}")
    return nodes[0], nodes[0].get(attribute)


def unsigned(value, label):
    require(isinstance(value, str) and re.fullmatch(r"[0-9]+", value) is not None,
            f"{label}: expected a nonnegative XML integer")
    return int(value)


def adjust_paragraph(source, output, records, label, palette):
    """Build an expected copy; only registered, bounded properties may differ."""
    expected = copy.deepcopy(source)
    spacing_delta = 0
    for rec in records:
        path, attribute, issue = rec["path"], rec["attribute"], rec["issue"]
        spacing = re.fullmatch(r"a:pPr/a:(spcBef|spcAft)/a:spcPts", path)
        line = re.fullmatch(r"a:pPr/a:lnSpc/a:(spcPct|spcPts)", path)
        size = re.fullmatch(RUN_PATH, path) and attribute == "sz"
        font = re.fullmatch(RUN_PATH + r"/a:(latin|ea|cs)", path)
        color = re.fullmatch(RUN_PATH + r"/a:solidFill/a:(srgbClr|schemeClr)", path)
        require((spacing or line or color) and attribute == "val" or size or font and attribute == "typeface",
                f"{label}: property is outside the adjustment whitelist: {path} @{attribute}")
        node, before = explicit_value(expected, path, attribute, label)
        _, after = explicit_value(output, path, attribute, label)
        require(before == rec["before"] and after == rec["after"],
                f"{label}: declared before/after do not match source/output")
        if spacing or line or size:
            require(issue in LAYOUT_ISSUES, f"{label}: numeric adjustment requires a layout issue")
            old, new = unsigned(before, label), unsigned(after, label)
            require(old != new, f"{label}: numeric adjustment has no actual change")
            if spacing:
                spacing_delta += abs(new - old)
                require(spacing_delta <= 600, f"{label}: total paragraph-spacing change exceeds 6 pt")
            elif line:
                require(old > 0 and new > 0 and abs(new - old) * 10 <= old,
                        f"{label}: line-spacing change exceeds 10%")
                require(line.group(1) != "spcPct" or new >= 100000,
                        f"{label}: proportional line spacing must remain at least single")
            else:
                require(old > 0 and new > 0 and abs(new - old) <= 200 and abs(new - old) * 10 <= old,
                        f"{label}: font-size change exceeds 2 pt or 10%")
        elif font:
            require(issue in {"missing_glyph", "font_substitution"},
                    f"{label}: font change requires missing_glyph or font_substitution")
        else:
            require(issue == "low_contrast", f"{label}: color change requires low_contrast")
            kind = color.group(1)
            require(after in palette[kind], f"{label}: color is absent from the template's {kind} values")
        node.set(attribute, after)
    return expected


def spacing_boundaries(source_paragraphs, output_paragraphs, records, label):
    edges = set()
    for j, items in enumerate(records):
        for rec in items:
            if rec["path"] == "a:pPr/a:spcBef/a:spcPts" and j > 0:
                edges.add(j - 1)
            if rec["path"] == "a:pPr/a:spcAft/a:spcPts" and j + 1 < len(records):
                edges.add(j)
    for j in edges:
        totals = []
        for ps in [source_paragraphs, output_paragraphs]:
            total = 0
            for index, side in [(j, "spcAft"), (j + 1, "spcBef")]:
                path = f"a:pPr/a:{side}/a:spcPts"
                _, value = explicit_value(ps[index], path, "val", label + " adjacent gap")
                total += unsigned(value, label)
            totals.append(total)
        require(abs(totals[1] - totals[0]) <= 600,
                f"{label} paragraphs {j + 1}/{j + 2}: combined adjacent gap change exceeds 6 pt")


class Deck:
    def __init__(self, path):
        self.data = Path(path).read_bytes()
        self.sha256 = hashlib.sha256(self.data).hexdigest()
        self.zip = zipfile.ZipFile(path)
        self.cache = {}
        self.pres = self.xml("ppt/presentation.xml")
        require(self.pres.tag == "{" + NS["p"] + "}presentation",
                "Only transitional OOXML PPTX is supported")
        rels = self.rels("ppt/presentation.xml")
        self.slides = []
        for item in self.pres.findall("p:sldIdLst/p:sldId", NS):
            rel = rels.get(item.get(R + "id"))
            require(rel is not None and rel[0] == "slide" and not rel[2],
                    "Invalid presentation slide relationship")
            self.slides.append(rel[1])
        require(self.slides, "Presentation has no slides")

    def xml(self, part):
        if part not in self.cache:
            raw = self.zip.read(part)
            require(b"<!DOCTYPE" not in raw.upper(), f"DTD unsupported: {part}")
            self.cache[part] = ET.fromstring(raw)
        return self.cache[part]

    def rels(self, part):
        folder, base = posixpath.split(part)
        name = posixpath.join(folder, "_rels", base + ".rels")
        if name not in self.zip.namelist():
            return {}
        result = {}
        for rel in self.xml(name):
            external = rel.get("TargetMode") == "External"
            target = rel.get("Target", "")
            if not external:
                target = (target.lstrip("/") if target.startswith("/") else
                          posixpath.normpath(posixpath.join(folder, target)))
                require(target in self.zip.namelist(), f"Missing part: {target}")
            result[rel.get("Id")] = (rel.get("Type", "").rsplit("/", 1)[-1],
                                     target, external)
        return result

    def related(self, part, kind, required=False):
        matches = [r for r in self.rels(part).values() if r[0] == kind]
        require(len(matches) <= 1 and (matches or not required),
                f"{part}: expected {'one' if required else 'at most one'} {kind}")
        if not matches:
            return None
        require(not matches[0][2], f"External {kind} unsupported")
        return matches[0][1]

    def inherited(self, part):
        layout = self.related(part, "slideLayout", required=True)
        master = self.related(layout, "slideMaster", required=True)
        theme = self.related(master, "theme", required=True)
        pieces = {"layout": signature(self.xml(layout)),
                  "master": signature(self.xml(master)),
                  "theme": signature(self.xml(theme))}
        for label, source in [("slide", part), ("layout", layout), ("master", master)]:
            override = self.related(source, "themeOverride")
            pieces[label + ".themeOverride"] = signature(self.xml(override)) if override else None
        return pieces

    def global_styles(self):
        result = {name: pick(self.pres, "p:" + name) for name in
                  ["sldSz", "defaultTextStyle", "embeddedFontLst"]}
        result["fontEmbeddingFlags"] = tuple(self.pres.get(n) for n in
                                            ["embedTrueTypeFonts", "saveSubsetFonts"])
        theme = self.related("ppt/presentation.xml", "theme")
        result["presentationTheme"] = signature(self.xml(theme)) if theme else None
        fonts = []
        for rid, (kind, target, external) in self.rels("ppt/presentation.xml").items():
            if kind == "font":
                require(not external, "External embedded font unsupported")
                fonts.append((rid, hashlib.sha256(self.zip.read(target)).hexdigest()))
        result["embeddedFontData"] = tuple(sorted(fonts))
        return result

    def shapes(self, part):
        root = self.xml(part)
        require(root.find(".//p:graphicFrame", NS) is None,
                f"{part}: table/chart/SmartArt/graphicFrame is not covered")
        require(not any(n.tag.endswith("}AlternateContent") for n in root.iter()),
                f"{part}: AlternateContent is not covered")
        result = {}
        covered = set()
        for shape in root.findall(".//p:sp", NS):
            body = shape.find("p:txBody", NS)
            if body is None:
                continue
            meta = shape.find("p:nvSpPr/p:cNvPr", NS)
            require(meta is not None and meta.get("id"), f"{part}: shape lacks ID")
            key = meta.get("id")
            require(key not in result, f"{part}: duplicate text shape ID {key}")
            result[key] = shape
            covered.add(id(body))
            for paragraph in body.findall("a:p", NS):
                allowed = {"pPr", "r", "br", "fld", "endParaRPr"}
                require(all(n.tag in {"{" + NS["a"] + "}" + t for t in allowed}
                            for n in paragraph),
                        f"{part} shape {key}: unsupported paragraph content (e.g. native math)")
        bodies = {id(n) for n in root.iter() if n.tag.endswith("}txBody")}
        require(bodies == covered, f"{part}: text outside supported p:sp shapes")
        return result


def shape_style(shape):
    return {name: pick(shape, path) for name, path in {
        "bodyPr": "p:txBody/a:bodyPr", "lstStyle": "p:txBody/a:lstStyle",
        "fontRef": "p:style/a:fontRef", "placeholder": "p:nvSpPr/p:nvPr/p:ph",
    }.items()}


def paragraph_style(paragraph, strict_runs=False):
    runs = []
    for child in paragraph:
        if child.tag in {"{" + NS["a"] + "}" + n for n in ["r", "fld", "br"]}:
            style = (child.tag, child.get("type"), pick(child, "a:rPr"), pick(child, "a:pPr"))
            if strict_runs or not runs or runs[-1] != style:
                runs.append(style)
    return {"pPr": pick(paragraph, "a:pPr"),
            "endParaRPr": pick(paragraph, "a:endParaRPr"), "runStyles": tuple(runs)}


def slide_style(deck, part):
    root = deck.xml(part)
    result = deck.inherited(part)
    result["clrMapOvr"] = pick(root, "p:clrMapOvr")
    result["background"] = pick(root, "p:cSld/p:bg")
    return result


def inventory(deck):
    slides = []
    for index, part in enumerate(deck.slides, 1):
        shapes = {}
        for sid, shape in deck.shapes(part).items():
            paragraphs = shape.findall("p:txBody/a:p", NS)
            shapes[sid] = {
                "paragraphs": list(range(1, len(paragraphs) + 1)),
                "name": shape.find("p:nvSpPr/p:cNvPr", NS).get("name", ""),
                "text": ["".join(p.itertext())[:120] for p in paragraphs],
            }
        slides.append({"source_slide": index, "shapes": shapes})
    return {"version": 1, "template_sha256": deck.sha256, "slides": slides}


def compare(expected, actual, label, errors):
    for key in expected:
        if expected[key] != actual[key]:
            errors.append(f"{label}: {key} changed")


def check(source, output, mapping, accepted_adjustments=None):
    keys(mapping, ["version", "template_sha256", "slides", "adjustments"], "map")
    require(type(mapping.get("version")) is int and mapping.get("version") == 1,
            "Map must be an object with version: 1")
    require(mapping.get("template_sha256") == source.sha256,
            "Map template_sha256 does not match TEMPLATE; use its inventory")
    entries = mapping.get("slides")
    require(isinstance(entries, list) and len(entries) == len(output.slides),
            "Map slides must cover every output slide in presentation order")
    adjustments = adjustment_index(mapping.get("adjustments", []), len(output.slides))
    used, accepted = set(), []
    palette = {"srgbClr": set(), "schemeClr": set()}
    if any("solidFill" in r["path"] for records in adjustments.values() for r in records):
        for part in source.zip.namelist():
            if part.endswith(".xml"):
                for kind in palette:
                    palette[kind].update(n.get("val") for n in source.xml(part).iter("{" + NS["a"] + "}" + kind))
    errors = []
    compare(source.global_styles(), output.global_styles(), "presentation", errors)
    for i, (part, entry) in enumerate(zip(output.slides, entries), 1):
        keys(entry, ["source_slide", "shapes"], f"slide {i}")
        src_index = number(entry.get("source_slide"), len(source.slides), f"slide {i} source_slide")
        src_part = source.slides[src_index]
        actual = output.shapes(part)
        shape_map = entry.get("shapes")
        require(isinstance(shape_map, dict), f"slide {i}: shapes must be an object")
        require(set(shape_map) == set(actual),
                f"slide {i}: mapping must cover all text shapes exactly; "
                f"unmapped={sorted(set(actual) - set(shape_map))}, stale={sorted(set(shape_map) - set(actual))}")
        compare(slide_style(source, src_part), slide_style(output, part), f"slide {i}", errors)
        for sid, shape in actual.items():
            rule = shape_map[sid]
            label = f"slide {i} shape {sid}"
            keys(rule, ["source_slide", "source_shape", "paragraphs", "name", "text"], label)
            donor_index = number(rule.get("source_slide", src_index + 1), len(source.slides),
                                 label + " source_slide")
            donor_part = source.slides[donor_index]
            donor_id = str(rule.get("source_shape", sid))
            donors = source.shapes(donor_part)
            require(donor_id in donors, f"{label}: source shape {donor_id} missing")
            donor = donors[donor_id]
            context = slide_style(source, donor_part)
            context.pop("background")
            compare(context, slide_style(output, part), label + " inheritance", errors)
            compare(shape_style(donor), shape_style(shape), label, errors)
            src_ps = donor.findall("p:txBody/a:p", NS)
            out_ps = shape.findall("p:txBody/a:p", NS)
            paragraphs = rule.get("paragraphs")
            require(isinstance(paragraphs, list) and len(paragraphs) == len(out_ps),
                    f"{label}: paragraphs must map each output paragraph")
            mapped_sources, local_records = [], []
            for j, (p, origin) in enumerate(zip(out_ps, paragraphs), 1):
                p_index = number(origin, len(src_ps), f"{label} paragraph {j} donor")
                records = adjustments.get((i, sid, j), [])
                expected = adjust_paragraph(src_ps[p_index], p, records, f"{label} paragraph {j}", palette)
                mapped_sources.append(src_ps[p_index])
                local_records.append(records)
                if records:
                    used.add((i, sid, j))
                    accepted.extend({**r, "source": {"slide": donor_index + 1, "shape": donor_id,
                                                      "paragraph": origin}} for r in records)
                compare(paragraph_style(expected, strict_runs=bool(records)),
                        paragraph_style(p, strict_runs=bool(records)),
                        f"{label} paragraph {j} (source {donor_index + 1}/{donor_id}/{origin})", errors)
            spacing_boundaries(mapped_sources, out_ps, local_records, label)
    require(used == set(adjustments), f"Unmatched/stale adjustment targets: {sorted(set(adjustments) - used)}")
    if accepted_adjustments is not None:
        accepted_adjustments.extend(accepted)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("inventory", help="Print source shape/paragraph IDs and identity map")
    inv.add_argument("template")
    chk = sub.add_parser("check", help="Compare output styles to explicit source donors")
    chk.add_argument("template")
    chk.add_argument("output")
    chk.add_argument("--map", required=True, dest="mapping")
    args = parser.parse_args()
    try:
        source = Deck(args.template)
        if args.command == "inventory":
            print(json.dumps(inventory(source), ensure_ascii=False, indent=2))
            return 0
        output = Deck(args.output)
        mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        accepted = []
        errors = check(source, output, mapping, accepted)
        status = "FAIL" if errors else ("PASS_WITH_ADJUSTMENTS" if accepted else "PASS")
        print(json.dumps({"status": status, "errors": errors, "accepted_adjustments": accepted,
                          "scope": "mapped native text styles and inheritance only; adjustment records are not visual approval; visual QA still required"},
                         ensure_ascii=False, indent=2))
        return 1 if errors else 0
    except (Unsupported, OSError, KeyError, ET.ParseError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "UNSUPPORTED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
