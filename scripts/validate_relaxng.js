// Relax NG validation of a TEI/EpiDoc document with salve (pure-JS Relax NG validator).
// Usage: npm install salve saxes
//        node scripts/validate_relaxng.js <schema.rng> <document.xml> <report.txt>
// Rationale: libxml2 (lxml, xmllint) does not finish compiling the EpiDoc schema; salve takes seconds.

const fs = require("fs");
const { pathToFileURL, fileURLToPath } = require("url");
const loader = { load(url) { const u = new URL(url); return Promise.resolve({ url: u, getText() { return Promise.resolve(fs.readFileSync(fileURLToPath(u), "utf8")); } }); } };
const salve = require("salve");
const { SaxesParser } = require("saxes");
const [rngPath, xmlPath, outPath] = process.argv.slice(2);
(async () => {
  const t0 = Date.now();
  const { pattern, warnings } = await salve.convertRNGToPattern(pathToFileURL(rngPath), { resourceLoader: loader });
  console.log("schema converted in", ((Date.now()-t0)/1000).toFixed(1), "s; warnings:", warnings.length);
  const walker = pattern.newWalker(new salve.DefaultNameResolver());
  const errors = [];
  let count = 0;
  const parser = new SaxesParser({ xmlns: true, position: true });
  function fire(name, params) {
    const r = walker.fireEvent(name, params);
    if (r) { for (const e of r) { if (errors.length < 500) errors.push({ line: parser.line, col: parser.column, event: name, params: params.join(" "), msg: e.toString() }); } count += r.length; }
  }
  parser.on("opentag", (tag) => {
    fire("enterStartTag", [tag.uri, tag.local]);
    for (const attr of Object.values(tag.attributes)) {
      if (attr.prefix === "xmlns" || attr.name === "xmlns") continue;
      fire("attributeName", [attr.uri, attr.local]); fire("attributeValue", [attr.value]);
    }
    fire("leaveStartTag", []);
  });
  parser.on("text", (t) => { if (t.trim() !== "") fire("text", [t]); });
  parser.on("closetag", (tag) => { fire("endTag", [tag.uri, tag.local]); });
  parser.on("error", (e) => { throw e; });
  const xml = fs.readFileSync(xmlPath, "utf8");
  const CH = 1 << 20;
  for (let i = 0; i < xml.length; i += CH) parser.write(xml.slice(i, i + CH));
  parser.close();
  const endErr = walker.end();
  if (endErr) for (const e of endErr) errors.push({ line: -1, col: -1, event: "end", params: "", msg: e.toString() });
  const total = count + (endErr ? endErr.length : 0);
  const lines = [
    "Relax NG validation with salve " + require("salve/package.json").version + " (pure-JS Relax NG validator)",
    "schema: " + rngPath, "document: " + xmlPath,
    "result: " + (total === 0 ? "VALID" : "INVALID"), "error count: " + total, ""
  ];
  for (const e of errors) lines.push(`line ${e.line} col ${e.col} [${e.event} ${e.params}]: ${e.msg}`);
  fs.writeFileSync(outPath, lines.join("\n") + "\n");
  console.log(total === 0 ? "VALID" : "INVALID", "errors:", total, "in", ((Date.now()-t0)/1000).toFixed(1), "s");
  for (const e of errors.slice(0, 15)) console.log(`line ${e.line}: [${e.event} ${e.params}] ${e.msg}`);
})().catch(e => { console.error("FAILED:", e); process.exit(2); });
