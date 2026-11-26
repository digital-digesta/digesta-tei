# Digesta TEI ⇄ Ribary (2020) `digest.db` 対応表

`digesta-tei__ribary-digest-db__crosswalk.csv`

本データセットの section と、Marton Ribary の SQLite データベース `digest.db` の
text unit とを1対1で突き合わせた対応表。論文 §Context が「両リソースは異なる印刷底本と
異なるデータモデルに立脚するため、報告された unit 数を、公開された対応表なしに直接
比較すべきではない」と述べている、その対応表にあたる。

## 対象

| | Digesta TEI | Ribary `digest.db` |
| --- | --- | --- |
| 底本 | Mommsen–Krüger *editio maior*（1868–1870、Keip 2001 復刻） | Mommsen–Krüger *editio stereotypa* 第5版（Weidmann, 1889） |
| 本文取得 | 新規 OCR ＋人手校正 | ROMTEXT → Amanuensis |
| 単位 | 21,077 sections | 21,055 text units |
| 出典 | 本リポジトリ | figshare DOI 10.6084/m9.figshare.12333290（CC BY 4.0） |

## 列

| 列 | 内容 |
| --- | --- |
| `tei_xml_id` | 本データセットの `xml:id`（例 `Dig.1.1.1.pr`） |
| `tei_ref` | book.title.fragment.section（例 `1.1.1.pr`） |
| `ribary_text_id` | `digest.db` の `text.id` |
| `ribary_ref` | `book_no.section_no.passage_no.textunit_no` |
| `status` | 参照番号による対応。下表参照 |
| `content_check` | **本文の内容による検証。** 下表参照（2026-10-20 追加） |

## 対応状況

| status | 件数 | 意味 |
| --- | --- | --- |
| `matched` | 21,033 | 参照番号に双方の対応がある |
| `tei_only_subdivision` | 23 | モムゼンの細分（`4a`, `6b` 等）。Ribary は整数の unit 番号のみを持つ |
| `ribary_only` | 22 | Ribary にのみ存在 |
| `tei_only` | 21 | 本データセットにのみ存在 |

対応表は全21,099行。

TEI 21,077 sections のうち **21,033 件（99.8%）**、
Ribary 21,055 text units のうち **21,033 件（99.9%）** が参照番号で対応する。

## 本文の内容による検証（`content_check`）

**2026-10-20 より前の対応表は、参照番号だけで突き合わせており本文を照合していなかった。**
そのため、番号は一致するが本文がずれている箇所を `matched` と記録していた。
`content_check` 列はこれを是正するもので、section 冒頭の語列を比較する。ラテン文字を小文字化し、アクセントを除き、u/v と i/j を統一して先頭8語までを使う。番号で対応する行は冒頭の一致を調べ、文字付き細分は親 unit の中を探す。

| `content_check` | 件数 | 意味 |
| --- | --- | --- |
| `match` | 20,570 | 先頭の本文が一致する |
| `wording_diff` | 369 | 対応はするが字句が異なる（下記） |
| `not_compared` | 158 | 比較に使える冒頭語列が得られない場合など。番号で対応する115行と、片側のみにある43行 |
| `boundary_shift` | **2** | 区切り位置が異なる |

`boundary_shift` の 2 件（`Dig.5.3.40.3`、`Dig.9.2.2.1`）は、**底本照合により当方が正しいと
確認された箇所**である（`docs/review/2026-10-15_提案書N_照合票2.xlsx` シート 1）。
Ribary 側の区切りが底本と異なる。

2026-10-20 より前は `boundary_shift` が **97 件**あった。提案書 N
（`docs/review/2026-10-15_TEI修正提案書N_区切り位置のずれ.md`）で 23 fragment の区切りを
底本どおりに直した結果、2 件になった。

全20,570件の `match` の内訳は、番号で対応する行が20,547件、親 unit の本文中で一致する細分が23件。

### `wording_diff` 369 件について

Ribary のテクストは editio stereotypa 系であり、底本（editio maior）と字句が異なる箇所がある。
369 件はその差と、当方に残る OCR 誤りの両方を含む。**どちらであるかは本対応表では区別していない。**
標本を見るかぎり、

- Ribary 側に本文が多い／少ない（版の差）例: `Dig.1.2.2.27`、`Dig.1.5.7.pr`
- 当方の OCR 誤りと見られる例: `Dig.1.2.2.28`（`co praetore` / `eo praetore`）、
  `Dig.1.7.21.pr`（`ad rogari` / `adrogari`）

の双方がある。**後者は公開後の版で扱う**（2026-10-19 指導教員の判断 §7）。

なお Ribary の `text` 列には `^…^` の形で異読が埋め込まれている（21,055 unit のうち 199）。
`content_check` はこれを除去してから比較している。

## 対応の規則

**通常の書（D.30–32 以外）**

```
TEI (book, title, fragment, section)  ⇄  Ribary (book_no, section_no, passage_no, textunit_no)
section の "pr" は textunit_no = 0 に対応する
```

**D.30–32**

この3書のみ rubric（title）を持たない（Kaiser 2015, p. 127）。
両者は階層の当て方が異なる。

```
TEI    : book → title(=1) → fragment → section
Ribary : book → section_no(= TEI の fragment) → passage_no(= TEI の section) → textunit_no(常に0)
```

したがって対応は次のとおり。

```
TEI (b, 1, f, s)  ⇄  Ribary (b, f, s', 0)      ただし s'=0 if s=="pr" else int(s)
```

## 未対応が生じる理由

- **底本の系統差** — 本データセットは editio maior、Ribary は editio stereotypa。
  校訂者の断片区分の判断が異なる箇所がある。とくに `D.46.8.26` は
  *fragmentum incertum*（帰属不確実な断片）であり、editio maior に固有。
- **細分の粒度** — モムゼンの `4a`・`6b` のような文字付き細分を、
  本データセットは `@n` に保持するが、Ribary の `textunit_no` は整数のみ。
  ただし Ribary は親 unit の本文中に `^a^` の記号でこの細分を記録しており、
  `content_check` はその親 unit と照合している（23 件中 23 件が `match`）。

## 再現方法

```
python3 scripts/build_crosswalk.py
```

Python 3 と `lxml` を使う。[Ribary の配布ページ](https://doi.org/10.6084/m9.figshare.12333290) から `digest.db` を取得し、`papers/comparison-datasets/ribary-2020_digest-db/digest.db` に置く。入力は本リポジトリの TEI とこのデータベース。決定的であり、同じ入力から同じ出力を得る。

## ライセンス

対応表そのものは本データセットと同じ CC BY 4.0。
`ribary_text_id` / `ribary_ref` 列は Ribary の CC BY 4.0 データに由来する識別子であり、
利用にあたっては Ribary (2020) の帰属表示を行うこと。

> Ribary, M. (2020). A Relational Database of Roman Law Based on Justinian's *Digest*.
> *Journal of Open Humanities Data*, 6(1): 5. DOI: 10.5334/johd.17


## 変更履歴

| 日付 | 内容 |
| --- | --- |
| 2026-08-16 | 初版。参照番号による突き合わせ |
| **2026-10-20** | `content_check` 列を追加。提案書 N による区切りの修正を反映し、section 数が 21,067 → 21,077 に。`boundary_shift` 97 → 2 |
