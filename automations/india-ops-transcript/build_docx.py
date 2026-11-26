# Builds a Teams-style transcript .docx (stdlib only, small output).
# Usage: python3 build_docx.py input.json output.docx
# input.json: {"title": str, "date": str, "duration": str, "started_by": str|null,
#              "entries": [{"speaker": str, "ts": "1:51", "text": str}, ...]}
import json, sys, zipfile
from xml.sax.saxutils import escape as e

def run(t, bold=False, color=None, size=None):
    rpr = ""
    if bold: rpr += "<w:b/>"
    if color: rpr += f'<w:color w:val="{color}"/>'
    if size: rpr += f'<w:sz w:val="{size}"/>'
    return f'<w:r>{"<w:rPr>"+rpr+"</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{e(t)}</w:t></w:r>'

def para(*runs, after=120):
    return f'<w:p><w:pPr><w:spacing w:after="{after}"/></w:pPr>{"".join(runs)}</w:p>'

d = json.load(open(sys.argv[1], encoding="utf-8"))
body = [para(run(d["title"], bold=True, size=32), after=60),
        para(run(d["date"], color="616161"), after=0),
        para(run(d["duration"], color="616161"), after=240)]
if d.get("started_by"):
    body.append(para(run(d["started_by"], bold=True), run("   started transcription", color="616161"), after=240))
for x in d["entries"]:
    body.append(para(run(x["speaker"], bold=True), run("   " + x["ts"], color="616161"), after=40))
    body.append(para(run(x["text"]), after=240))

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
       + "".join(body) +
       '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>')
styles = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W}><w:docDefaults><w:rPrDefault><w:rPr>'
          '<w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI" w:cs="Segoe UI"/><w:sz w:val="21"/></w:rPr></w:rPrDefault></w:docDefaults></w:styles>')
ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
with zipfile.ZipFile(sys.argv[2], "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", doc); z.writestr("word/_rels/document.xml.rels", drels)
    z.writestr("word/styles.xml", styles)
import os; print(os.path.getsize(sys.argv[2]), "bytes")
