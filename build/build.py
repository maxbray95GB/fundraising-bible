#!/usr/bin/env python3
"""Rebuild the encrypted Fundraising Bible page.

Usage:
  1. Export the Google Doc as HTML -> build/doc.html
  2. python3 build/build.py
  3. npx staticrypt index.html -p '<password>' -d site --short --remember 30 \
       -t build/kindred_template_built.html \
       --template-title "Fundraising Bible" --template-button "Open"
  4. npx wrangler pages deploy site --project-name=kindred-bible --branch=main
"""
import re, pathlib

base = pathlib.Path(__file__).parent
font_b64 = (base / 'saans.b64').read_text().strip()
logo_b64 = (base / 'logo.b64').read_text().strip()

# Landing template: inject font + logo
tpl = (base / 'kindred_template.html').read_text()
tpl = tpl.replace('__SAANS_B64__', font_b64).replace('__LOGO_B64__', logo_b64)
(base / 'kindred_template_built.html').write_text(tpl)

# Doc page: head injection + logo swap
html = (base / 'doc.html').read_text(encoding='utf-8')
inject = (
    '<title>Kindred \u2014 Fundraising Bible</title>'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    '<meta name="robots" content="noindex, nofollow">'
    '<style>'
    '@font-face{font-family:"Saans";src:url(data:font/otf;base64,' + font_b64 + ') format("opentype");'
    'font-weight:400;font-style:normal;font-display:swap;}'
    'body,body *{font-family:"Saans","Helvetica Neue",Arial,sans-serif !important;}'
    'body{margin:0 auto !important;}'
    '.kindred-logo{display:block;height:44px;width:auto;margin:8px auto 16px;}'
    '@media(max-width:640px){body{padding:24px 20px !important;max-width:100% !important;}}'
    '</style>'
)
html = html.replace('<head>', '<head>' + inject, 1)

logo_tag = '<img class="kindred-logo" src="data:image/png;base64,' + logo_b64 + '" alt="Kindred">'
wrappers = re.findall(r'<span style="overflow: hidden;[^"]*"><img[^>]*src="data:image/[^"]*"[^>]*></span>', html)
if len(wrappers) == 1:
    html = html.replace(wrappers[0], logo_tag)
else:
    print(f'WARNING: found {len(wrappers)} logo wrappers (expected 1) - logo not swapped')

(base.parent / 'index.html').write_text(html, encoding='utf-8')
print('built: kindred_template_built.html and index.html')
