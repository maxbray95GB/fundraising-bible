# bible

Password-protected static page served at https://bible.kindredcapital.vc via **Cloudflare Pages** (project `kindred-bible`, account Max@kindredcapital.vc). DNS: CNAME `bible` → `kindred-bible.pages.dev` at OnlyDomains.

The page content is AES-256 encrypted with [StatiCrypt](https://github.com/robinmoisson/staticrypt) — this repo contains only ciphertext.

## Updating the page

1. Export the "Fundraising Bible" Google Doc as HTML.
2. Inject the Saans font, Kindred logo, and mobile CSS into the exported HTML (see session notes / ask Claude — the build also uses a customised StatiCrypt template with Kindred branding).
3. Re-encrypt: `npx staticrypt index.html -p '<password>' -d site --short --remember 30 -t kindred_template_built.html --template-title "Fundraising Bible" --template-button "Open"`
4. Deploy: `npx wrangler pages deploy site --project-name=kindred-bible --branch=main` (needs `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`), and commit the new `index.html` here.

GitHub Pages previously hosted this (cert provisioning got permanently stuck in "new"); the Pages site may still exist as a legacy fallback.
