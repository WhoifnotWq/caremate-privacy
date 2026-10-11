"""Offline authoring tool. Published pages need only a static web server."""

import json
from datetime import date
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = {"en": "index.html", "ru": "privacy-ru.html"}
MONTHS = {
    "en": (
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ),
    "ru": (
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    ),
}


def text(value):
    return escape(value, quote=True)


def brand_mark():
    return '<span class="brand-mark" aria-hidden="true">✿</span>'


def paragraphs(values):
    return "\n".join(f"<p>{text(value)}</p>" for value in values)


def links(values):
    return '<ul class="link-list">\n' + "\n".join(
        f'<li><a href="{text(item["url"])}" rel="noreferrer">'
        f'{text(item["label"])}</a></li>' for item in values
    ) + "\n</ul>"


def render_section(section, language, contact):
    content = [
        f'<section class="policy-section" aria-labelledby="{text(section["id"])}">',
        f'<h2 id="{text(section["id"])}">{text(section["title"])}</h2>',
        paragraphs(section.get("paragraphs", [])),
    ]
    if "items" in section:
        content.append("<ul>\n" + "\n".join(
            f"<li>{text(item)}</li>" for item in section["items"]
        ) + "\n</ul>")
    content.append(paragraphs(section.get("after", [])))
    for service in section.get("services", []):
        purpose = "Purpose" if language == "en" else "Назначение"
        categories = "Information categories" if language == "en" else "Категории информации"
        content.append(
            f'<div class="service"><h3>{text(service["name"])}</h3>'
            f'<dl><dt>{purpose}</dt><dd>{text(service["purpose"])}</dd>'
            f'<dt>{categories}</dt><dd>{text(service["data"])}</dd></dl>'
            f'{links(service["links"])}</div>'
        )
    if "links" in section:
        content.append(links(section["links"]))
    if section["id"] == "contact":
        content.append(f'<p><a href="mailto:{text(contact)}">{text(contact)}</a></p>')
    content.append("</section>")
    return "\n".join(item for item in content if item)


def shell(language, title, description, body, labels, contact, current_file):
    nav_items = []
    for lang, filename in FILES.items():
        current = ' aria-current="page"' if filename == current_file else ""
        label = "English" if lang == "en" else "Русский"
        nav_items.append(
            f'<a href="{filename}" lang="{lang}" hreflang="{lang}"{current}>'
            f'{label}</a>'
        )
    nav = "\n".join(nav_items)
    return f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{text(description)}">
  <meta name="referrer" content="no-referrer">
  <title>{text(title)} — CareMate Plants</title>
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48x48.png">
  <link rel="stylesheet" href="styles.css">
</head>
<body id="top">
  <a class="skip-link" href="#main">{text(labels["skip_label"])}</a>
  <div class="site-wrap">
    <header class="site-header">
      <div class="brand">
        {brand_mark()}<span>CareMate Plants</span>
      </div>
      <nav class="language-nav" aria-label="{text(labels["language_label"])}">
        {nav}
      </nav>
    </header>
    <main id="main" tabindex="-1">
{body}
    </main>
    <footer class="site-footer">
      <nav class="footer-nav" aria-label="{text(labels["footer_label"])}">
        <a href="mailto:{text(contact)}">{text(labels["contact_label"])}</a>
        <a href="#top">{text(labels["back_label"])}</a>
      </nav>
      <div class="footer-brand">
        <svg class="footer-mark" viewBox="215 167 594 720" width="43" height="52" aria-hidden="true" focusable="false">
          <image href="assets/caremate-plant-mark.png" width="1024" height="1024" />
        </svg>
      </div>
    </footer>
  </div>
</body>
</html>
'''


def dated_line(language, labels, effective):
    readable = f"{effective.day} {MONTHS[language][effective.month - 1]} {effective.year}"
    return (
        f'<p class="effective-date">{text(labels["effective_label"])}: '
        f'<time datetime="{effective.isoformat()}">{readable}</time></p>'
    )


def main():
    data = json.loads((ROOT / "policy.json").read_text(encoding="utf-8"))
    effective = date.fromisoformat(data["effective_date"])
    english_ids = [section["id"] for section in data["languages"]["en"]["sections"]]
    for language, labels in data["languages"].items():
        sections = labels["sections"]
        ids = [section["id"] for section in sections]
        if ids != english_ids or len(ids) != len(set(ids)):
            raise ValueError("Section identifiers must be unique and match across translations")
        toc = "\n".join(
            f'<li><a href="#{text(section["id"])}">{text(section["title"])}</a></li>'
            for section in sections
        )
        body = f'''      <article class="paper">
        <header class="policy-heading">
          <p class="eyebrow">CareMate Plants</p>
          <h1>{text(labels["title"])}</h1>
          {dated_line(language, labels, effective)}
          <p class="canonical-notice">{text(labels["canonical_notice"])}</p>
        </header>
        <nav class="contents" aria-label="{text(labels["contents_label"])}">
          <h2>{text(labels["contents_label"])}</h2>
          <ol>{toc}</ol>
        </nav>
        {chr(10).join(render_section(section, language, data["contact"]) for section in sections)}
      </article>'''
        output = shell(language, labels["title"], labels["description"], body, labels,
                       data["contact"], FILES[language])
        (ROOT / FILES[language]).write_text(output, encoding="utf-8", newline="\n")

    print("Rendered index.html, privacy-ru.html")


if __name__ == "__main__":
    main()
