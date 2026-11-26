# Digesta TEI: source and transformation provenance

This file records the workflow behind the current working TEI document,
`phi2806.phi002.humanitext-lat1.xml`. It is intended to be released with the
dataset and expanded into the Zenodo release documentation.

## Source and workflow

The project used the Mommsen--Krueger *editio maior* of the *Digesta* (two
volumes, Berlin: Weidmann, 1868--1870) as its principal Latin source, as
recorded in the TEI header.

The physical copy digitised was not the Weidmann original but the reprint
published at Goldbach by Keip in 2001 (ISBN 3-8051-0884-2), **bound in four
volumes**. That reprint reproduces the 1868--1870 text together with the
prefaces of 1868 and 1870 and the later *Berichtigungen und Ergänzungen*. Any
reader collating the dataset against a Weidmann original should note that the
corrections and additions carried by the reprint are part of the digitised
source.

**Pagination.** The reprint keeps the pagination of the two-volume original,
which restarts once, between book 29 and book 30. Its own division into four
physical volumes does not restart it: the page numbers run on across the
binding at books 15/16 and 40/41.

| 復刻版の冊 | books | *editio maior* の巻 | 頁 |
| --- | --- | --- | --- |
| Vol. 1 | 1--15 | I | 1 以降 |
| Vol. 2 | 16--29 | I（続き） | …889 まで |
| Vol. 3 | 30--40 | II | 1 以降 |
| Vol. 4 | 41--50 | II（続き） | …900 前後まで |

Page references in this repository therefore cite the volume of the *editio
maior* (I or II) rather than the physical volume of the reprint, since the
latter varies between printings while the pagination does not.

> **訂正（2026-10-22）** 本文書と TEI ヘッダーの `sourceDesc` は、復刻版を
> 「二巻本（two-volume reprint）」と記していた。RA が底本で頁番号を調べた際に
> **物理的には四分冊**であることが判明したため、本文書を訂正した。
> TEI ヘッダーの該当箇所は未修正であり、
> `docs/review/2026-10-22_TEI修正提案書O_底本の巻数.md` で承認を仰ぐ。
> 原本（Weidmann, 1868--1870）が 2 巻であることに変わりはなく、原稿の
> 「two volumes, 1868--1870」および `monogr` の `2 vols.` は原本を指すため正しい。

A representative part of that source is retained at
`../../papers/source-edition/mommsen_editio-maior_book-1_keip-2001-reprint.pdf`
(39 pages; SHA-256
`8705b7f1609c3dfb721103cbeb4db9e63fd954aeed4d17d9c38d077253c04714`). Alan
Watson's English edition is recorded in the TEI header as a reference edition.

The working textual data followed this sequence:

1. OCR was applied to the printed source edition.
2. The OCR output was checked and corrected by a human reader.
3. The reviewed text was organized as 50 book-level XML inputs.
4. Those inputs were consolidated and structurally transformed into the
   current TEI P5 document.
5. The project then applied recorded structural enrichment and deterministic
   normalizations, including Greek-language tagging, attribution-key
   corrections, and proem identifier corrections. These later actions are
   recorded in the TEI `revisionDesc`.

The PDF is evidence for the source and workflow; it is not by itself a claim
that every page of the release is newly transcribed from that single file.
The release documentation should identify any additional source files,
OCR-engine/version, review scope, reviewers, dates, transformation scripts,
and validation reports before public deposition.

## Scope

The TEI is a structured, citable representation of the reviewed textual
input. It is not a new critical edition and does not claim to encode a full
apparatus of manuscript variants.

## 2026-08-16 の承認済み修正

指導教員の承認のもと、`docs/review/2026-08-15_TEI修正提案書.md` の A〜E を実施した。
根拠は `docs/review/2026-08-15_底本照合結果.md`（2026-08-15、Keip 2001 復刻版との照合）。

- **A** 欠損標示の是正。D.48.20.9 と D.48.22.12–18 で、底本が inscriptio に一箇所だけ
  示す欠損を本文側にも重複符号化していた 8 件を削除。変換時に失われていた
  D.36.1.83–85 の末尾欠損 3 件を追加。`gap` は 26 件から **21 件**になった。
- **B** 法学者名の一部が `bibl/title` の先頭に混入していた 25 件を `bibl/author` へ移した。
  あわせて `ABURNIUS` を `UALENS` へ、`UOLUSIUS` を `MAECIANUS` へ統合し、
  `FURIUS` を `FURIUS ANTHIANUS`、`RUTILIUS` を `RUTILIUS MAXIMUS` に改めた。
  統制された帰属キーは 41 から **39** になった。
  表層形は底本の綴りを保持している（例: `LICINIUS RUFINUS` は n が一つのまま）。
- **C** D.30 の見出しの綴りを `FIDEICOMMISSIDE` から `FIDEICOMMISSIS` に訂正した。
- **D** rubric を持たない D.31・D.32 を、D.30 および他の 49 巻と同じ形式に揃えた。
  title の `@n` を `0` から `1` とし、配下の `xml:id` 756 件を 4 階層表記に改めた
  （`Dig.31.62` → `Dig.31.1.62` など）。旧新対応は本リリースに同梱する。
- **E** 底本で inscriptio 自体が失われており編者が復元した 5 件
  （D.36.1.45、36.1.84、36.1.85、36.4.16、36.4.17）について、`author` と `title` の
  内容を `<supplied reason="lost" cert="low">` で囲んだ。
  当初 `bibl/@cert` を用いたが、EpiDoc 8.19 の `att.global` は `att.responsibility` を
  含まず `@cert` を許容しないため、`supplied`（`model.pPart.transcriptional`）に改めた。
  D.36.4.16・36.4.17 の `UALENS` は直前断片からの継承であり、
  他の 3 件と同様に底本には印刷されていない。**これら 5 件の帰属は編者の復元であって、
  底本の証言ではない。**

修正後のファイル: 9,650,600 bytes、SHA-256 `c77522c0beee3f096de1ba71e9548bff0f1981e372c0a0304d1a20b72d8e460d`
（修正前は 9,647,938 bytes、`10bf3e2e9a4c7e88f134dd30d5b777187df3c069fb1ff5aeb6f89fe41cca150a`）。
XML は整形式であり、`xml:id` 30,688 件はすべて一意、
book/title/fragment/section の CTS 参照は D.31・D.32 を含めて解決する。

### 検証の状況

実施済み — XML 整形式、`xml:id` 30,688 件の一意性、構造数値（50/432/9,139/21,067/495）、
`gap` 21 件、帰属キー 39 件、`bibl/title` 先頭の人名残存 0 件、
book/title/fragment/section の CTS 参照解決（D.31・D.32 を含む）。

**EpiDoc 8.19 Relax NG による全文検証は、2026-10-13 に実施して VALID を得た**
（下記 2026-10-13 の項を参照）。本項を記した時点では未実施で、作業環境の検証器が
スキーマのコンパイル段階で完了しなかった（system xmllint／lxml とも異常終了、
Java 未導入のため jing も不可）。当時の代替として、導入した構造がスキーマ定義上
許容されることを個別に確認していた。

- `<gap>` は `model.global.edit` → `model.global` → `macro.paraContent` により `p` 内で許容
- `<supplied>` は `model.pPart.transcriptional` → `model.pPart.edit` → `model.phrase`
  → `macro.phraseSeq`／`macro.paraContent` により `author`・`title` 内で許容。
  `@reason="lost"`・`@cert` はいずれも `supplied` の属性として定義されている

（この課題は 2026-10-13 に salve で解消した。下記 2026-10-13 の項を参照。）

## Ribary (2020) との対応表

`data/crosswalk/digesta-tei__ribary-digest-db__crosswalk.csv`

Ribary の `digest.db`（CC BY 4.0、figshare DOI 10.6084/m9.figshare.12333290）の
text unit と、本データセットの section を突き合わせた対応表。
論文が「対応表なしに直接比較すべきではない」と述べている、その対応表にあたる。

## 2026-09-08 の承認済み修正（本文の校訂）

指導教員の承認のもと、`docs/review/2026-09-08_進捗報告_本文校訂.md` の F〜J を実施した。
Ribary (2020) `digest.db` との本文比較で候補を機械的に抽出し、**全件を Keip 復刻版と照合**
したうえでの修正である。

- **F** 本文の脱落 16 件を復元した（D.2.14.21、3.1.1、4.4.3、8.2.20、8.5.19、9.2.51、
  9.2.54、22.5.14、30.1.50、30.1.89、33.2.28、38.17.2、41.1.65、41.2.10、42.1.16、45.3.11）。
  うち D.9.2.54 は誤混入の `P` の削除を伴う。
  当方の現行本文は多くが文法的に成立しておらず（`sunt hi parens`／`hoc ceteris de dolo`／
  `adquisiit ex personae`）、脱落であることは内的にも裏付けられた。
- **G** `v` を `u` に統一した（130 語。本文・inscriptio・head）。底本は本文を通じて `u` を
  用いる。ローマ数字は `V` が正しいため除外した。
  inscriptio の `VARUS`(6) は `@key="ALFENUS UARUS"`、`IAVOLENUS`(2) は `@key="IAUOLENUS"` と
  綴りが割れていたが、これも解消した。
- **H** 本文に混入していた写本記号 `F[P(VU)]` を削除した（D.18.4.10 pr）。
  本文全体を走査し、同種の混入はこの 1 件のみであることを確認している。

  > **訂正（2026-10-15）** この確認は不十分だった。当時は角括弧の形 `F[...]` のみを
  > 探しており、丸括弧の形を見落としていた。2026-10-15 の再走査で
  > `F(XYMOC)`（D.48.16.11 pr、D.48.5.39.9）と `F(XYMC)`（D.50.17.178 pr）の 3 件、
  > および法学者名の略記 `(Scaeu.)`（D.36.1.80.1）を新たに検出した。
  > 対応は `docs/review/2026-10-13_TEI修正提案書M_機械的修正.md` の M-17。
- **I** D.49 の見出し 18 件を、他の 49 書と同じ総大文字に改めた。
- **J** D.7.1.12.2 の 3 件を修正した。`fructum, sed` が `frucsed` と接合していたもの、
  `locauero` が `locavtum` となっていたもの、`Iulianus` が小文字だったもの。

**構造は一切変わっていない。** books 50 / titles 432 / fragments 9,139 / sections 21,067 /
inscriptio 9,139 / 帰属キー 39 / ギリシア語 495 / gap 21 / `supplied` 10 /
`xml:id` 30,688 件はすべて一意で、CTS 参照も解決する。

修正後のファイル: 9,652,417 bytes、SHA-256 `d0e13eaa5c0cc6d6cb5cc86d1289a85da35a5dc8777e83ef2ef3c2326939ff98`
（修正前は `c77522c0beee3f096de1ba71e9548bff0f1981e372c0a0304d1a20b72d8e460d`）。

### 検出手法の限界

Ribary との本文比較で拾えるのは「Ribary にあって当方にない」箇所に限られる。
両版とも欠く箇所や、Ribary 側が脱落している箇所は原理的に対象外であり、
**網羅性を主張できる調査ではない。**

なお D.7.1.12.2 の `frucsed` は、脱落した 4 字が語の接合で吸収され section 全体の長さが
ほとんど変わらなかったため、長さ差による絞り込みでは検出できなかった。長さに依存しない
方法で全 21,023 section を再走査したところ、同種の破損はこの 1 件のみであった。

### 修正しなかったもの

- `Dig.28.3.2` の「superius rumpitur.」— Ribary にはあるが底本には見当たらず、
  editio stereotypa 側の読みと解した。
- `Dig.19.5.26.1` の `[Ianuariis?]` — **底本の角括弧**であり、編者の推定を示す。
  削除してはならない。符号化は下記 2026-09-10 の項で実施した。

## 2026-09-10 の承認済み修正（編者推定の符号化）

指導教員の指示により、`Dig.19.5.26.1` の編者推定を符号化した。

底本は `Quod kalendis [Ianuariis?] dari solet medicis et artificibus` と印刷する。
角括弧の中身は編者が補ったもので、疑問符はその不確かさを示す。
これを削除せず、E の 5 件（inscriptio の編者復元）と同じ書式で符号化した。

```xml
Quod kalendis <supplied reason="lost" cert="low">Ianuariis</supplied> dari solet
```

疑問符が担っていた不確かさは `@cert="low"` が引き受ける。
これにより **本文中に符号化されていない角括弧は残っていない**
（もう 1 件の `F[P(VU)]` は 2026-09-08 に写本記号として削除済み）。

構造は変わっていない。`supplied` が 10 から **11** になった以外は、
books 50 / titles 432 / fragments 9,139 / sections 21,067 / inscriptio 9,139 /
帰属キー 39 / ギリシア語 495 / gap 21 / `xml:id` 30,688 件すべて一意で不変である。

修正後のファイル: 9,652,851 bytes、SHA-256 `632996ab9ac05b0b981e550e2e873eb93197f7f78d556188cacb335dcb43bfec`
（修正前は `d0e13eaa5c0cc6d6cb5cc86d1289a85da35a5dc8777e83ef2ef3c2326939ff98`）。

> **確認をお願いしたい点** Mommsen の角括弧が「編者による補い」を示すのか
> 「削除すべき挿入」を示すのかは版によって慣行が異なる。`<supplied>` は前者の解釈である。
> 後者であれば `<surplus>` が適切になる。疑問符を伴う点からは補いと解されるが、
> 底本の凡例でご確認いただきたい。

## 2026-10-13 の承認済み修正（残存 OCR 痕跡とヘッダー）

指導教員の承認のもと、`docs/review/2026-10-13_TEI修正提案書K_残存OCR痕跡.md` の
A〜F および G、計 61 件を実施した。**全件を RA が Keip 復刻版と照合したうえでの修正である。**

- **A** 本文に残っていた行割れ記号 `||` を 16 件削除した。底本では改行位置にあたる。
- **B** 校訂註の上付き番号 24 件を削除した。本プロジェクトは校訂註を採らない方針であり、
  OCR が本文に取り込んでいたもの。
- **C** 本文に混入した数字・丁付け参照 4 件を削除した。
- **D** 文字が三重化していた 6 語を修正した。
- **E** OCR がラテン語に持ち込んだアクセント付き文字 6 件を置き換えた。
  うち **D.32.1.101 pr** では、ラテン文字の `c`・`í` がギリシア語範囲を 3 つに分断していた。
  これを 1 つの `<foreign>` に統合したため、**ギリシア語範囲は 495 から 493 になった**。
  本文の字数は変わっていない。
- **F** 誤認された記号 4 件を整えた。**D.10.4.5 pr のダッシュと `transscribendis` の綴りは
  底本どおりとして維持した。**
- **G** `Dig.2.14.21.2` の `</div>` 直後にあった重複文を削除した。
  2026-09-08 の F #1 の挿入作業の残骸で、section にも `<p>` にも属さない浮遊テキストだった。
  **これが EpiDoc 8.19 スキーマ不適合の唯一の原因であった。**

TEI ヘッダーには `<funder>Institutes of Innovation for Future Society, Nagoya University</funder>` を
`titleStmt` 末尾に追加した。

### 構造

books 50 / titles 432 / fragments 9,139 / sections 21,067 / inscriptio 9,139 /
帰属キー 39 / gap 21 / `supplied` 11 / `xml:id` 30,688 件はすべて一意で不変。
**ギリシア語範囲のみ 495 → 493**（上記 E による）。

修正後のファイル: 9,653,601 bytes、SHA-256 `e96d8392ffaa310bc694dd90e3967bbcbd52c20913ca811c255380198a2f3a62`
（修正前は 9,652,851 bytes、`632996ab9ac05b0b981e550e2e873eb93197f7f78d556188cacb335dcb43bfec`）。
チェックサムは LF の内容に対して計算している。

### 検証 — EpiDoc 8.19 Relax NG 検証に合格

**2026-08-16 の項で「未実施」としていた全文の Relax NG 検証を実施し、VALID を得た。**

| 項目 | 値 |
| --- | --- |
| スキーマ | `https://epidoc.stoa.org/schema/8.19/tei-epidoc.rng`（2026-10-13 取得、519,816 bytes、SHA-256 `62515cf4…`） |
| 検証器 | salve 9.1.2（純 JavaScript の Relax NG 検証器）、Node.js v22.20.0 |
| 判定 | **VALID（エラー 0 件、警告 0 件）** |
| 所要時間 | スキーマ変換 0.3 秒、全文検証 1.8 秒 |

同一の検証器・スキーマで修正前後を比較し、エラーが G 項の 1 件だけであったこと、
およびそれが解消したことを確認している。

| 対象 | 判定 |
| --- | --- |
| K 適用前（`632996ab…`） | INVALID（1 件、3382 行 `text not allowed here`） |
| K 適用後（`e96d8392…`） | **VALID（0 件）** |

libxml2（lxml 6.0.2、xmllint）は EpiDoc スキーマのコンパイル段階で完了しない。
これは環境の問題ではなく、libxml2 の Relax NG 実装が TEI 系の大規模スキーマで
極端に遅くなる既知の性質による。詳細は
`docs/review/2026-10-13_スキーマ検証報告.md`。

このほか、`xml:id` の一意性、構造数値、A〜F パターンの再走査（ヒット 0。底本にある
D.10.4.5 pr のダッシュを除く）、`body` 配下の全 `div` について浮遊テキストが 0 件であること、
`<foreign>` 外のギリシア文字 0 件、`<foreign>` 内のラテン文字 0 件、空の section 0 件、
book/title/fragment/section の CTS 参照解決（17 件すべて一意）を確認した。



## 2026-10-15 の修正（提案書 L・M・N、371 件）

`docs/review/2026-10-13_TEI修正提案書M_機械的修正.md` と
`docs/review/2026-10-15_TEI修正提案書N_区切り位置のずれ.md` に基づく。
**うち 47 件は RA が Keip 復刻版で個別に照合して確定したものである。**

### 内訳

| 分類 | 件数 | 判定の根拠 |
| --- | --- | --- |
| M-5 Unicode 正規化（oxia → tonos） | 89 | Unicode の正規等価。字形は不変 |
| M-6〜M-9 ギリシア語の語形 | 53 | ギリシア語の正書法 |
| M-10 ギリシア語とラテン語の境界 | 5 | 字形の似たラテン文字が `foreign` を分断 |
| M-11 ラテン語として成立しない語形 | 45 | 成立せず、かつ Ribary が想定形を持つ |
| M-12・M-15 行末で割れた語 | 40 | 繋げた形が本文に多数あり |
| M-13 引用符の混入 | 14 | 語中・二重・空白欠落 |
| M-14 Ribary との先頭照合で検出 | 14 | 同上 |
| M-16 見出し | 16 | ローマ数字の重複ほか |
| M-17 注釈・写本記号の混入 | 6 | 底本では本文外に印刷される |
| M-1〜M-4 文字の置換 | 42 | キリル文字・ダイアクリティカル・引用符・行割れ記号 |
| **提案書 L・N 底本確定分** | **47** | **RA による底本照合** |
| 合計 | **371** | |

### 底本どおりとして修正しなかったもの

RA の照合により、OCR 誤りに見えて実は底本の読みであると確認された 17 件は修正していない。
`promissit`・`occassione`・`promisserat`・`excussatus`・`inpendia`（子音の重複と `inp-`）、
`casa`・`sinus`・`pane`・`quali`・`situ`・`nomino`・`imus`・`manumissit`・`quaccumque`・`aute` ほか。

**記入いただいた 58 行のうち 30 行（51%）で当方の想定が誤っていた。**
子音の重複は語によって扱いが分かれ、辞書的な規則では決まらない。

### 構造

books 50 / titles 432 / fragments 9,139 / sections 21,067 / inscriptio 9,139 /
帰属キー 39 / gap 21 / `supplied` 11 / `xml:id` 30,688 件はすべて一意で不変。
**ギリシア語範囲のみ 493 → 490。** M-10 で、ラテン文字に誤認されていた文字を直して
`<foreign>` を繋げた結果である（D.34.1.4 pr で 3 要素を 1 つに、D.38.17.1.6 で
ラテン語 `eius` を囲っていた要素を削除）。本文の字数は変わっていない。

修正後のファイル: 9,655,138 bytes、SHA-256
`56681fd09fac678b3aaa7c9d2f3b4b27ab463a757652988f4afb620143968b7f`
（修正前は 9,653,601 bytes、`e96d8392ffaa310bc694dd90e3967bbcbd52c20913ca811c255380198a2f3a62`）。
チェックサムは LF の内容に対して計算している。

### 検証

| 項目 | 結果 |
| --- | --- |
| EpiDoc 8.19 Relax NG（salve 9.1.2 / Node.js v22.20.0） | **VALID、エラー 0 件** |
| `xml:id` の一意性 | 30,688 件すべて一意 |
| CTS 参照（book/title/fragment/section） | 17 件すべて一意に解決 |
| 提案書 K 第 8 節の走査 A〜F | すべて 0 件（底本にある D.10.4.5 pr のダッシュを除く） |
| `<foreign>` 外のギリシア文字／内のラテン文字 | 0 / 0 |
| 空の section・`div` 直下の浮遊テキスト | 0 / 0 |

適用は `scripts/apply_proposal_m.py` による。決定論的であり、`--dry-run` で差分のみ確認できる。
段階間でアンカーが壊れないことを検査する処理を含む。

### 未実施 — section の区切り位置（提案書 N）

**底本照合により、24 fragment・約 97 section で section の区切り位置が誤っていることが
確定しているが、本修正には含めていない。** `xml:id` の変更を伴い、旧新対応表の作成と
humanitext 側の派生データの移行が必要なためである。あわせて枝番号の 3 件
（D.45.1.5 の付け替え、D.23.2.57 pr・D.29.3.2.4 の分割）も未実施。

### 走査の限界

- 本修正は文字・語の層に限られる。**section の区切りは上記のとおり未修正である。**
- Ribary との照合で拾えるのは対応づいた 21,023 section に限られ、
  両版とも誤る箇所、Ribary 側が誤る箇所は原理的に対象外である。
- Ribary の `text` 列には `^…^` の形で異読が埋め込まれている（21,055 unit のうち 199）。
  当初の比較はこれを本文として扱っており、「脱落」21 件のうち 16 件が偽陽性だった。
  現在の走査は除去してから比較している。


## 2026-10-20 の修正（提案書 N・ギリシア語の符号化）

`docs/review/2026-10-19_指導教員の判断_提案書L-N以降.md` と
`docs/review/2026-10-20_RAへの依頼_N以降.md` による。提案書 L・M・N の 371 件は
2026-10-19 に指導教員が事後承認し、独立に検証（VALID、`xml:id` 一意、構造数値不変）している。

### section の区切り位置（提案書 N）

**RA が 25 fragment すべてを Keip 復刻版で照合し、23 fragment で当方の区切りが
誤っていると確定した**（当方が正しいのは D.5.3.40 と D.9.2.2 の 2 件）。
指導教員も D.11.5.1 を底本 346 頁で確認している。

底本は、section が始まる行の欄外に番号を印刷する。section が行の途中や行末から
始まっていても番号はその行に置かれるため、読み取りが難しい箇所がある。
D.2.14.1 は RA が提供した底本の写真（`docs/review/source-images/底本_D-2-14_DE-PACTIS.jpg`）で
決着した。欄外の `2` は `et est pactio duorum` を含む行にあり、この行で文が改まるのは
そこだけである。

| 操作 | 件数 |
| --- | --- |
| 分割 | 48 |
| 統合 | 14 |
| 番号の付け替え | 78 |
| 変更なし（対象 fragment 内） | 197 |

あわせて文字付き細分（枝番号）を 3 件直した。**当方の TEI は以前から枝番号を
20 件持っており**（`Dig.5.3.20.6a` など）、新しい形式ではない。

- **D.45.1.5** — 区切り位置は正しく番号だけがずれていた。`4` → `3a`、`5` → `4`。
  底本の写真（`docs/review/source-images/底本_D-45-1-5_枝番号3a.jpg`）で確認
- **D.23.2.57 pr** — `Diuus Marcus et Lucius imperatores…` から `pra` に分割
- **D.29.3.2.4** — `Inspici tabulas est…` から `4a` に分割

**本文は 1 文字も変えていない。** 適用スクリプト `scripts/apply_proposal_n.py` は、
fragment ごとに適用前後の語列を突き合わせ、一致しなければ書き込まない。

旧新対応表は `data/crosswalk/xmlid-migration_2026-10-20.csv`（337 行）としてリリースに同梱する。
`old_xml_id` / `new_xml_id` / `action` / `boundary_words` / `source_page` / `note` の列を持つ。
`source_page` は底本の頁で、照合時の記録から RA が記入する。

### ギリシア語の符号化

指導教員の判断 §3 による。

- **省音符を U+2019 に統一した**（53 件）。内訳は U+1FBD 29、U+0027 22、U+1FBF 2。
  前後がギリシア文字である位置のみを対象とし、ラテン語の引用符（5,753 件）には触れていない
- **ギリシア語自身の句読点だけで隔てられた隣接する `<foreign>` を 144 箇所で統合した。**
  対象は文末ピリオド 104、省音符 33、行末ハイフン 3、コロン 2、疑問符 2。
  ラテン語・括弧・開き引用符が介在する 63 箇所は統合していない。
  **`<foreign xml:lang="grc">` は 490 から 346 になった**
- いずれも `editorialDecl/normalization` に記載した

### 構造

| | 修正前 | 修正後 |
| --- | --- | --- |
| books / titles / fragments | 50 / 432 / 9,139 | 変更なし |
| **sections** | 21,067 | **21,077**（+10） |
| inscriptio / 帰属キー / gap / supplied | 9,139 / 39 / 21 / 11 | 変更なし |
| **`<foreign xml:lang="grc">`** | 490 | **346**（−144） |
| **`xml:id`** | 30,688 | **30,698**（すべて一意） |

修正後のファイル: 9,653,095 bytes、SHA-256
`978652d9580137d4f025309f6dfbc5d33b0f69e908ef53bc1eca8b98cc3cb115`
（修正前は 9,655,138 bytes、`56681fd09fac678b3aaa7c9d2f3b4b27ab463a757652988f4afb620143968b7f`）。
チェックサムは LF の内容に対して計算している。

### 検証

| 項目 | 結果 |
| --- | --- |
| **EpiDoc 8.19 Relax NG**（salve 9.1.2 / Node.js v22.20.0） | **VALID、エラー 0 件** |
| `xml:id` の一意性 | 30,698 件すべて一意 |
| `@n` と `xml:id` の整合 | 不整合 0 件 |
| CTS 参照（book/title/fragment/section、枝番号を含む） | すべて一意に解決 |
| 提案書 K 第 8 節の走査 A〜F | すべて 0 件（底本にある D.10.4.5 pr のダッシュを除く） |
| `<foreign>` 外のギリシア文字／内のラテン文字 | 0 / 0 |
| 空の section・`div` 直下の浮遊テキスト | 0 / 0 |
| 移行表 337 行の検証 | 新 `xml:id` の不在 0、`boundary_words` の不一致 0 |

走査は `scripts/scan_k8.py` で再現できる。

### Ribary との対応表

`content_check` 列を加えて再生成した（`scripts/build_crosswalk.py`）。
**参照番号だけで突き合わせていた従来の欠陥を是正するものである。**

| `content_check` | 件数 |
| --- | --- |
| `match` | 20,570 |
| `wording_diff` | 369 |
| `not_compared` | 158 |
| **`boundary_shift`** | **2**（提案書 N の実施前は 97） |

残る 2 件は、底本照合で当方が正しいと確認された D.5.3.40 と D.9.2.2 である。
`wording_diff` 369 件は版の差と当方に残る OCR 誤りの両方を含み、本対応表では区別していない。
**後者は公開後の版で扱う**（指導教員の判断 §7）。詳細は `data/crosswalk/README.md`。


## 2026-10-27 の修正（引用符の位置・底本の巻数）

指導教員の最終チェック（`docs/review/2026-10-26_最終チェック結果と残りの修正.md`）による。

### 引用符の位置（70 件）

section の区切りで、新しい section が引用で始まる場合に、**開き引用符 `'` が直前の
section の末尾に取り残されていた**。提案書 N の分割で生じたもの 6 件と、元の変換に
由来するもの 64 件がある。末尾の「空白＋`'`」を削り、次の section の冒頭に付け直した。

**本文の字は変えておらず、引用符の総数も 5,777 のまま変わらない。**
一覧は `docs/review/2026-10-27_引用符位置の一覧.csv`（72 行）。

**2 件は適用していない。** `Dig.9.4.21.2` と `Dig.13.5.16.2` は、次の section が引用では
なく閉じ引用符も持たないため、末尾の `'` は当該 section 自身の閉じ引用符と見られる。
正しい処置は「次へ移す」ではなく「手前の空白を詰める」であり、承認された規則と異なるため、
指示に従い適用せず一覧に残した。

### 底本の巻数（提案書 O、承認済み）

`sourceDesc` の `note` を訂正した。Keip 2001 復刻版は**四分冊**であり、二巻本ではない。
あわせて、復刻版が原本（Weidmann 2 巻）の頁付けを保ち、book 29/30 の 1 箇所でのみ
振り直されることを記した。

### 構造と検証

books 50 / titles 432 / fragments 9,139 / sections 21,077 / inscriptio 9,139 /
帰属キー 39 / `foreign` 346 / gap 21 / `supplied` 11 / `xml:id` 30,698 件すべて一意 —
**すべて変更なし。**

| 項目 | 結果 |
| --- | --- |
| EpiDoc 8.19 Relax NG | **VALID、エラー 0 件** |
| CTS 参照（枝番号を含む） | すべて一意に解決 |
| 提案書 K 第 8 節の走査 A〜F | 0 件（底本にある D.10.4.5 pr のダッシュを除く） |
| 末尾が「空白＋`'`」の section | 72 → **2**（保留の 2 件のみ） |

修正後のファイル: 9,654,285 bytes、SHA-256
`a4e239ae3f16f2b6743a4fcdce38bdde432723b8d360bb7f8617b4357f278104`
（修正前は 9,653,095 bytes、`978652d9580137d4f025309f6dfbc5d33b0f69e908ef53bc1eca8b98cc3cb115`）。

## 2026-11-26　公開版 v1.0.0

統括3名・本文作成6名の各人に一つの `respStmt` を割り当て、日英の `persName` に共通の人物識別キーを付けた。9名の順序は引用情報およびZenodoの著者一覧と一致する。公開ライセンスは CC BY 4.0。10月27日版と公開版の `text` 要素はバイト単位で一致する。

公開XMLは EpiDoc 8.19 Relax NG に適合（エラー0件）。UTF-8・LFで 9,655,308 bytes、SHA-256 `63e4d85f093793cfde64afcde8b4e3c3290571fd04f031556f3823bdfa322f16`。
