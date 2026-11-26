# Validation of the Digesta TEI v1.0.0

The 26 November 2026 edition includes an updated TEI header. All nine contributors have one responsibility statement each and a shared key for their English and Japanese names. Their order matches the English and Japanese manuscripts, CITATION.cff and the Zenodo creator list. EpiDoc validation passed after the header revision. The text element is byte-identical to the 27 October revision. The distributed XML is 9,655,308 bytes. Its SHA-256 is `63e4d85f093793cfde64afcde8b4e3c3290571fd04f031556f3823bdfa322f16`, as recorded in the [editorial provenance](../data/tei/PROVENANCE.md).

| Check | Result |
| --- | --- |
| EpiDoc 8.19 Relax NG, salve 9.1.2 | Valid. Zero schema-conversion warnings and zero document errors. |
| Books, titles, fragments, sections | 50, 432, 9,139 and 21,077 respectively. |
| Identifiers | All 30,698 XML IDs are unique. |
| Inscriptions | Each of the 9,139 fragments has one inscription with one keyed author. The attribution table has 39 keys and 108 key/form pairs. The two forms *IDEM* and *Idem* occur 2,119 times in total. |
| Markup | 346 Greek spans, 21 gaps and 11 editorial supplements. |
| Editorial scans | Zero empty sections, stray text directly under a division, or Greek/Latin script placement flags. The six OCR-pattern scans returned one hit, the printed dash at `Dig.10.4.5.pr`. |
| Migration tables | All target IDs resolve in this XML across the 756 August rows and the 337 October rows. |
| Ribary crosswalk | Recomputed from the packaged XML and Ribary’s distributed SQLite file. All six columns agree across all 21,099 rows. Each TEI section occurs once and the table covers 21,055 distinct Ribary units. |

## Repeat the checks

Run the commands from the repository root. The schema used for this check has SHA-256 `62515cf420d1eb3488289021a30f1efb5315c4084afe22b5969737a24a4a1e42`.

```sh
curl -fL https://epidoc.stoa.org/schema/8.19/tei-epidoc.rng -o tei-epidoc.rng
npm install --no-save salve@9.1.2 saxes@6.0.0
node scripts/validate_relaxng.js tei-epidoc.rng data/tei/phi2806.phi002.humanitext-lat1.xml report.txt
```

The report records the validity result and error count. The editorial scans and crosswalk builder use Python 3 with `lxml`. Run `python scripts/scan_k8.py` for the editorial scans. To reproduce the crosswalk, place [Ribary’s digest.db](https://doi.org/10.6084/m9.figshare.12333290) at `papers/comparison-datasets/ribary-2020_digest-db/digest.db` (Figshare file 25829474, MD5 `2c5f3eb6409bddd23031a0d6b3a7d4f3`). Then run `python scripts/build_crosswalk.py` and `sha256sum -c SHA256SUMS`.

## Editorial limits

The October quotation review left the closing quotation marks at `Dig.9.4.21.2` and `Dig.13.5.16.2` in place. The 369 wording differences in the Ribary comparison can reflect readings of different printed editions or residual OCR errors. The comparison checks opening words.
