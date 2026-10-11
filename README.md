# CareMate Plants Privacy Site

## Purpose

A static privacy-information site for CareMate Plants. English is the canonical
notice for app-store publication; Russian is a convenience translation.

This bundle is prepared for review. Creating these files does not publish a site.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Canonical English Privacy Policy, served at the site root |
| `privacy-ru.html` | Russian translation |
| `styles.css` | Responsive styles using system fonts |
| `assets/caremate-plant-mark.png` | Local transparent app-icon foreground used in the footer |
| `policy.json` | Authoring source: effective date, contact, and both policy texts |
| `render.py` | Optional offline authoring tool that regenerates the two HTML pages |
| `.nojekyll` | Serves the static bundle without Jekyll processing |
| `README.md` | Publication and update instructions |

The HTML pages are already generated. Hosting requires no Python, JavaScript,
package installation, or custom build workflow.

The footer PNG is an unmodified copy of CareMate's transparent
`caremate_icon_foreground.png`, rather than a recreated symbol or a full icon tile.
An inline SVG viewport excludes its empty canvas margins without modifying the
image pixels. The visible plant is 52 px high, with a 22 px gap below footer
navigation and 28 px below the mark. It is decorative and hidden from assistive
technology; the header mark is unchanged.

## How to publish with GitHub Pages

After reviewing and approving the policy:

1. Create a separate public repository named `caremate-privacy` under `whoifnotwq`.
2. Copy the **contents** of this bundle into that repository's root, including
   `.nojekyll`. Publish only the website bundle, not any other project's contents.
3. Commit and push the reviewed files in that separate repository.
4. Open **Settings → Pages → Build and deployment**.
5. Select **Deploy from a branch**, choose `main` and `/(root)`, then save.
6. Wait for the Pages deployment to complete and enable **Enforce HTTPS** if needed.
7. Open both pages while signed out. Check the language links, section links,
   contact link, vendor links, and mobile layout before submitting a URL to a store.

See the official instructions for
[configuring a Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
and [HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https).

## Expected URL

These are intended future URLs, not confirmation of a live deployment:

- Canonical English policy: <https://whoifnotwq.github.io/caremate-privacy/>
- Russian translation: <https://whoifnotwq.github.io/caremate-privacy/privacy-ru.html>

Keep the root URL stable for store use. Use the hosted HTTPS URL rather than a
GitHub repository, branch, blob, or raw-file URL.

## Update procedure

1. Edit the English and corresponding Russian text in `policy.json` together.
2. Set its single `effective_date` value to the actual effective date in ISO format
   (`YYYY-MM-DD`). The contact address also has a single source in this file.
3. From this bundle's directory, run `python render.py` with Python 3.10 or newer.
   Python is an **offline editing tool**, never a visitor-side runtime dependency.
4. Review both generated HTML pages. Do not edit generated HTML directly;
   regeneration would replace those edits.
5. Check relative links and mobile/desktop layout. If the app's behavior changed,
   verify that both notices still accurately describe it.
6. Publish the reviewed source and generated files to the separate website repo.

For a local preview, run `python -m http.server 8765 --bind 127.0.0.1` in this
directory and open `http://127.0.0.1:8765/`. Stop the server when finished. Directly
opening `index.html` also works because the website is entirely static.

## No analytics or cookies

The site code adds no cookies, analytics, JavaScript, tracking pixels, forms,
advertising SDKs, external fonts, or third-party widgets. No cookie banner is used.
CSS is local, and fonts are supplied by the visitor's system.

GitHub Pages hosting is separate: GitHub states that visitors' IP addresses are
logged and stored for security purposes. The policy discloses this and links to
[GitHub Pages data collection](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)
and the [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

## Contact

Privacy and support: <nikitawq.dev@gmail.com>.
