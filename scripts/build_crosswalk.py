#!/usr/bin/env python3
"""Digesta TEI と Ribary (2020) digest.db の対応表を生成する。

    python3 scripts/build_crosswalk.py

決定的。同じ入力から同じ出力を得る。詳細は data/crosswalk/README.md。
"""
import csv, re, sqlite3, sys, unicodedata as ud
from pathlib import Path
import lxml.etree as ET

ROOT = Path(__file__).resolve().parent.parent
TEI_FILE = ROOT / "data/tei/phi2806.phi002.humanitext-lat1.xml"
DB_FILE = ROOT / "papers/comparison-datasets/ribary-2020_digest-db/digest.db"
OUT_FILE = ROOT / "data/crosswalk/digesta-tei__ribary-digest-db__crosswalk.csv"

NS = {"t": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
# D.30-32 は rubric を持たず、Ribary は階層を一段ずらして当てている。
RUBRICLESS = {30, 31, 32}
STATUS_ORDER = {"matched": 0, "tei_only": 1, "tei_only_subdivision": 2, "ribary_only": 3}


def ribary_index(db_path):
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, book_no, section_no, passage_no, textunit_no FROM text"
        )
        return {(b, s, p, u): tid for tid, b, s, p, u in rows}


def ribary_texts(db_path):
    """text.id → 本文。Ribary が ^…^ で埋め込む異読は除く。"""
    with sqlite3.connect(db_path) as conn:
        out = {}
        for tid, txt in conn.execute("SELECT id, text FROM text"):
            out[tid] = re.sub(r"\s*\^[^^]*\^", "", txt or "")
        return out


def words(s):
    s = ud.normalize("NFD", s.lower())
    s = "".join(c for c in s if not ud.combining(c))
    return re.findall(r"[a-z]+", s.replace("v", "u").replace("j", "i"))


def content_check(tei_text, rib_text, neighbours):
    """section 先頭の本文が一致するかを判定する。

    match          先頭 8 語が相手に含まれる
    boundary_shift 隣の unit の先頭と一致する（区切り位置のずれ）
    wording_diff   対応はするが字句が違う
    not_compared   比較できない
    """
    a, b = words(tei_text), words(rib_text)
    if not a or not b:
        return "not_compared"
    if " ".join(b).startswith(" ".join(a[:8])) or " ".join(a).startswith(" ".join(b[:8])):
        return "match"
    for nb in neighbours:
        nw = words(nb)
        if nw and " ".join(nw).startswith(" ".join(a[:8])):
            return "boundary_shift"
    return "wording_diff"


def ribary_key(book, title, fragment, section_n):
    """section の @n を Ribary の4つ組へ写す。対応不能なら None。"""
    if section_n == "pr":
        section = 0
    elif section_n.isdigit():
        section = int(section_n)
    else:
        return None  # モムゼンの文字付き細分（4a など）
    if book in RUBRICLESS:
        return (book, fragment, section, 0)
    return (book, title, fragment, section)


def build(tei_file, db_path):
    index = ribary_index(db_path)
    texts = ribary_texts(db_path)
    tree = ET.parse(str(tei_file))
    rows, matched = [], set()
    for book_div in tree.findall(".//t:div[@subtype='book']", NS):
        book = int(book_div.get("n"))
        for title_div in book_div.findall("./t:div[@subtype='title']", NS):
            title = int(title_div.get("n"))
            for frag_div in title_div.findall("./t:div[@subtype='fragment']", NS):
                fragment = int(frag_div.get("n"))
                for sec in frag_div.findall("./t:div[@subtype='section']", NS):
                    section_n = sec.get("n")
                    key = ribary_key(book, title, fragment, section_n)
                    text_id = index.get(key) if key else None
                    if text_id is not None:
                        matched.add(key)
                        status = "matched"
                    elif key is None:
                        status = "tei_only_subdivision"
                    else:
                        status = "tei_only"
                    tei_text = " ".join("".join(sec.itertext()).split())
                    if text_id is not None:
                        nb = []
                        for delta in (-2, -1, 1, 2):
                            k2 = (key[0], key[1], key[2], key[3] + delta)
                            if k2 in index:
                                nb.append(texts.get(index[k2], ""))
                        cc = content_check(tei_text, texts.get(text_id, ""), nb)
                    elif key is None:
                        # モムゼンの文字付き細分（4a など）。Ribary は親 unit の中に
                        # ^a^ の記号で記録しているため、親 unit と照合する
                        m = re.fullmatch(r"(\d+)[a-z]", section_n or "")
                        pk = ribary_key(book, title, fragment, m.group(1)) if m else None
                        if section_n and section_n.startswith("pr"):
                            pk = ribary_key(book, title, fragment, "pr")
                        pid = index.get(pk) if pk else None
                        cc = ("match" if pid is not None
                              and " ".join(words(texts.get(pid, ""))).find(
                                  " ".join(words(tei_text)[:8])) >= 0
                              else "not_compared")
                    else:
                        cc = "not_compared"
                    rows.append({
                        "tei_xml_id": sec.get(XML_ID),
                        "tei_ref": f"{book}.{title}.{fragment}.{section_n}",
                        "ribary_text_id": "" if text_id is None else text_id,
                        "ribary_ref": "" if text_id is None else ".".join(map(str, key)),
                        "status": status,
                        "content_check": cc,
                    })
    for key, text_id in index.items():
        if key not in matched:
            rows.append({
                "tei_xml_id": "", "tei_ref": "",
                "ribary_text_id": text_id,
                "ribary_ref": ".".join(map(str, key)),
                "status": "ribary_only",
                "content_check": "not_compared",
            })
    rows.sort(key=lambda r: (STATUS_ORDER[r["status"]], r["tei_ref"] or "~", str(r["ribary_ref"])))
    return rows


def main():
    for path in (TEI_FILE, DB_FILE):
        if not path.exists():
            sys.exit(f"見つかりません: {path}")
    rows = build(TEI_FILE, DB_FILE)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, lineterminator="\n", fieldnames=["tei_xml_id", "tei_ref", "ribary_text_id", "ribary_ref",
                            "status", "content_check"]
        )
        writer.writeheader()
        writer.writerows(rows)
    counts, cc = {}, {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
        cc[row["content_check"]] = cc.get(row["content_check"], 0) + 1
    print(f"{OUT_FILE.relative_to(ROOT)}: {len(rows):,} 行")
    for status in sorted(counts, key=lambda s: STATUS_ORDER[s]):
        print(f"  {status:22s} {counts[status]:6,}")
    print("  --- content_check ---")
    for k in ("match", "boundary_shift", "wording_diff", "not_compared"):
        if k in cc:
            print(f"  {k:22s} {cc[k]:6,}")


if __name__ == "__main__":
    main()
