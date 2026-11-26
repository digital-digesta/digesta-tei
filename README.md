# Digesta TEI

A TEI P5 / EpiDoc edition of all 50 books of Justinian’s *Digest*, prepared by the Digital Digesta project at Nagoya University. Each fragment records its attributed jurist and source work. Books, titles, fragments and sections have stable identifiers for citation and alignment.

**Digesta TEI v1.0.0.** The XML incorporates the corrections of 27 October 2026 and the contributor-name and licence updates of 26 November 2026. The [validation report](docs/validation.md) documents checks on the packaged files on 26 November 2026.

## Read and cite the text

Download the [TEI XML](data/tei/phi2806.phi002.humanitext-lat1.xml). To locate the opening paragraph of fragment 1 in title 1 of book 1, search for `xml:id="Dig.1.1.1.pr"`. Its CTS reference is `urn:cts:latinLit:phi2806.phi002.humanitext-lat1:1.1.1.pr`. The TEI header describes the source edition, editors, encoding conventions and citation levels. The nine dataset creators and citation metadata are listed in [CITATION.cff](CITATION.cff).

The team digitised the four-volume Keip reprint (Goldbach, 2001) of the two-volume Mommsen–Krüger *editio maior* (Berlin, Weidmann, 1868–1870). The team checked the Humanitext OCR output against the printed text. The [provenance record](data/tei/PROVENANCE.md) documents the workflow and subsequent corrections.

| Feature | Count |
| --- | ---: |
| Books / titles / fragments / sections | 50 / 432 / 9,139 / 21,077 |
| Juristic inscriptions / distinct attribution keys | 9,139 / 39 |
| Greek spans / marked losses / editorial supplements | 346 / 21 / 11 |
| Unique XML identifiers | 30,698 |

## Reuse the tables

- [Jurist attribution keys](data/attribution/jurist-keys.csv). Each row gives an inscription author’s controlled `author_key`, the written `surface_form` (case preserved, whitespace normalised), and the number of fragments with that pairing. The 108 pairs cover all 9,139 fragments. Forms such as *IDEM* and *Idem* retain the key of the jurist to whom the inscription refers.
- [Ribary crosswalk](data/crosswalk/digesta-tei__ribary-digest-db__crosswalk.csv). The columns distinguish alignment by reference from comparison of the opening words. Of 21,077 TEI sections, 21,033 have a matching numbered unit in Ribary’s database. See the [column guide and limitations](data/crosswalk/README.md).
- [August identifier migration](data/crosswalk/xmlid-migration_2026-08-16.csv) and [October identifier migration](data/crosswalk/xmlid-migration_2026-10-20.csv). Use the tables in date order to update references from earlier working versions. A split can map one earlier reference to several sections.

## Verify the files

From the repository root, run `sha256sum -c SHA256SUMS` with GNU coreutils to verify the XML and all five data tables. The distributed files use UTF-8 and LF line endings. The [validation report](docs/validation.md) lists the schema, commands and results. The [October quotation-mark review](docs/review/2026-10-27_引用符位置の一覧.csv) records 70 corrections and two retained cases.

## Licence and funding

The dataset and its documentation are licensed under [CC BY 4.0](LICENSE). Credit Marton Ribary when reusing identifiers from his [CC BY 4.0 dataset](https://doi.org/10.6084/m9.figshare.12333290).

Digital Digesta was funded by the Future Society Creation Project (International Academia Formation Seed Fund) of the Institutes of Innovation for Future Society, Nagoya University (principal investigator Yukiko Kawamoto). The work continues within the Humanitext programme.
