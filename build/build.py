#!/usr/bin/env python3
"""Rebuild the encrypted Fundraising Bible page.

Usage:
  1. Export the Google Doc as HTML -> build/doc.html
  2. python3 build/build.py          (writes build/index_plain.html + build/kindred_template_built.html)
  3. cd build && npx staticrypt index_plain.html -p '<password>' -d out --short --remember 30 \
       -t kindred_template_built.html \
       --template-title "Fundraising Bible" --template-button "Open"
  4. cp build/out/index_plain.html <deploy-dir>/index.html
     npx wrangler pages deploy <deploy-dir> --project-name=kindred-bible --branch=main
     (also commit the new encrypted index.html to this repo root)

NEVER commit build/doc.html or build/index_plain.html - they are plaintext (gitignored).
"""
import re, pathlib

base = pathlib.Path(__file__).parent
font_b64 = (base / 'saans.b64').read_text().strip()   # landing page only
logo_b64 = (base / 'logo.b64').read_text().strip()

# Landing template: inject font + logo
tpl = (base / 'kindred_template.html').read_text()
tpl = tpl.replace('__SAANS_B64__', font_b64).replace('__LOGO_B64__', logo_b64)
(base / 'kindred_template_built.html').write_text(tpl)

# Doc page: Helvetica Neue, 12pt body / 14pt section heads, cream bg,
# title block: logo -> FUNDRAISING BIBLE -> rule -> FIRST THINGS FIRST:
html = (base / 'doc.html').read_text(encoding='utf-8')
inject = (
    '<title>Kindred \u2014 Fundraising Bible</title>'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    '<meta name="robots" content="noindex, nofollow">'
    '<style>'
    'body,body *{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif !important;}'
    'body{margin:0 auto !important;max-width:540pt !important;background-color:#faf8f2 !important;}'
    'body p,body li,body span{font-size:12pt !important;}'
    'body p,body li{line-height:1.3 !important;}'
    '.section-head{font-size:14pt !important;font-weight:700 !important;}'
    '.sub-head{font-size:12pt !important;font-weight:700 !important;}'
    '.kindred-logo{display:block;height:44px;width:auto;margin:8px auto 20px;}'
    '.title-rule{border:none;border-top:1px solid rgba(0,0,0,0.3);width:100%;margin:18px 0;}'
    '@media(max-width:700px){body{padding:24px 20px !important;max-width:100% !important;}}'
    '</style>'
)
html = html.replace('<head>', '<head>' + inject, 1)

count = 0
def tag(m):
    global count; count += 1
    return m.group(0).replace('<span ', '<span class="section-head" ', 1)
html = re.sub(r'<span style="[^"]*font-family:&quot;Lora&quot;[^"]*">(BEFORE|AFTER)</span>', tag, html)
assert count == 2, f'tagged {count} section heads, expected 2'

m = re.search(r'<p[^>]*text-align:center[^>]*><span style="[^"]*font-family:&quot;Lora&quot;[^"]*">FIRST THINGS FIRST</span></p>', html)
assert m, 'FIRST THINGS FIRST paragraph not found'
replacement = (
    '<p style="padding:0;margin:0;line-height:1.15;text-align:center">'
    '<span class="section-head" style="color:#000000;font-weight:700">FUNDRAISING BIBLE</span></p>'
    '<hr class="title-rule">'
    '<p style="padding:0;margin:0 0 6px;line-height:1.15;text-align:center">'
    '<span class="sub-head" style="color:#000000;font-weight:700">FIRST THINGS FIRST:</span></p>'
)
html = html.replace(m.group(0), replacement)

logo_tag = '<a href="https://kindredcapital.vc" style="display:block"><img class="kindred-logo" src="data:image/png;base64,' + logo_b64 + '" alt="Kindred"></a>'
wrappers = re.findall(r'<span style="overflow: hidden;[^"]*"><img[^>]*src="data:image/[^"]*"[^>]*></span>', html)
assert len(wrappers) == 1, f'found {len(wrappers)} logo wrappers'
html = html.replace(wrappers[0], logo_tag)

(base / 'index_plain.html').write_text(html, encoding='utf-8')
print('built: kindred_template_built.html and index_plain.html')
