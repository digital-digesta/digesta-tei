#!/usr/bin/env python3
"""提案書 K 第 8 節の走査法を再実行する。

本文（<text> 配下）を section ごとに取り出し、提案書 K が用いた正規表現でヒットを列挙する。
あわせて <foreign> 外のギリシア文字、<foreign> 内のラテン文字、空の section、
div 直下の浮遊テキスト（提案書 K 第 7 節）も確認する。

使い方: python3 scripts/scan_k8.py [TEI ファイル]
"""
import re, sys
import lxml.etree as ET

NS = {"t": "http://www.tei-c.org/ns/1.0"}
T = "{http://www.tei-c.org/ns/1.0}"
XID = "{http://www.w3.org/XML/1998/namespace}id"
XL = "{http://www.w3.org/XML/1998/namespace}lang"

PATTERNS = [
    ("A  行割れ記号 ||",    r"\|\|"),
    ("B  上付きの脚注番号",   r"[¹²³⁴⁵⁶⁷⁸⁹⁰]"),
    ("C  本文に混入した数字",  r"\b\d+\b'?|f\. \d+'?"),
    ("D  文字の三重化",      r"\b\w*(sss|ttt|uuu)\w*\b"),
    ("E  アクセント付き文字",  r"[íáéóú]"),
    ("F  記号の誤認",        r"[&`‛—…]"),
]
GRK = re.compile(r"[Ͱ-Ͽἀ-῿]")


def flow(e):
    """(文字列, ギリシア語タグ内か) の列を返す。"""
    out = []
    def walk(x, g):
        gg = g or (x.tag == T + "foreign" and x.get(XL) == "grc")
        if x.text:
            out.append((x.text, gg))
        for ch in x:
            walk(ch, gg)
            if ch.tail:
                out.append((ch.tail, g))
    walk(e, False)
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/tei/phi2806.phi002.humanitext-lat1.xml"
    d = ET.parse(path)
    body = d.xpath("//t:body", namespaces=NS)[0]
    secs = {s.get(XID): flow(s) for s in body.iter(T + "div")
            if s.get("subtype") == "section"}
    print(f"対象: {path}")
    print(f"section {len(secs)} 件を走査\n")

    total = 0
    for name, pat in PATTERNS:
        rx = re.compile(pat)
        hits = []
        for sid, parts in secs.items():
            for txt, ingrc in parts:
                if ingrc:
                    continue
                for m in rx.finditer(txt):
                    hits.append((sid, m.group(0),
                                 " ".join(txt[max(0, m.start() - 45):m.end() + 45].split())))
        total += len(hits)
        print(f"  {name:24s} {len(hits):4d} 件" + ("  OK" if not hits else ""))
        for sid, g, c in hits[:6]:
            print(f"       {sid:22s} {g!r}  …{c}…")
        if len(hits) > 6:
            print(f"       …ほか {len(hits) - 6} 件")

    out_grk, in_lat = [], []
    for sid, parts in secs.items():
        for txt, ingrc in parts:
            if ingrc:
                in_lat += [(sid, m.group(0)) for m in re.finditer(r"[A-Za-z]", txt)]
            else:
                out_grk += [(sid, m.group(0)) for m in GRK.finditer(txt)]
    empty = [sid for sid, parts in secs.items()
             if not "".join(t for t, _ in parts).strip()]
    floating = []
    for dv in body.iter(T + "div"):
        if dv.text and dv.text.strip():
            floating.append((dv.get(XID), "text"))
        for ch in dv:
            if ch.tail and ch.tail.strip():
                floating.append((dv.get(XID), "tail"))

    for label, items in (("foreign 外のギリシア文字", out_grk),
                         ("foreign 内のラテン文字", in_lat),
                         ("空の section", empty),
                         ("div 直下の浮遊テキスト", floating)):
        print(f"\n  {label:26s} {len(items):4d} 件" + ("  OK" if not items else ""))
        for x in items[:6]:
            print(f"       {x}")

    print(f"\n  A〜F の合計 {total} 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
