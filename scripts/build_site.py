#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import shutil
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
SITE = ROOT / "site"

NAV = [
    ("review", "/", "Wiederholen"),
    ("progress", "/progress/", "Fortschritt"),
    ("sessions", "/sessions/", "Sitzungen"),
    ("teacher", "/teacher/", "Für die Lehrkraft"),
]

SKILL_LABELS = {
    "kennenlernen": "Kennenlernen",
    "foto_beschreiben": "Foto beschreiben",
    "situation_besprechen": "Situation besprechen",
    "schreiben": "Schreiben",
    "lesen": "Lesen",
    "wortschatz": "Wortschatz",
    "grammatik": "Grammatik",
    "fluessigkeit": "Flüssigkeit",
    "aufgabenverstaendnis": "Aufgabenverständnis",
}


def esc(value: object) -> str:
    return html.escape(str(value))


def display_date(value: object) -> str:
    if isinstance(value, (date, datetime)):
        return value.strftime("%d.%m.%Y")
    raw = str(value)
    try:
        return datetime.strptime(raw, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return raw


def md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def nav(active: str) -> str:
    links = []
    for key, href, label in NAV:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    return "".join(links)


def page(title: str, active: str, body: str, description: str = "Training für den Berliner Sprachtest B1") -> str:
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#176b4d">
  <title>{esc(title)} · Deutsch B1</title>
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
  <header class="site-header">
    <nav class="nav" aria-label="Hauptnavigation">
      <a class="brand" href="/"><span class="brand-mark">B1</span><span>Deutsch Training</span></a>
      <div class="nav-links">{nav(active)}</div>
    </nav>
  </header>
  <main>{body}</main>
  <footer class="footer">Berliner Sprachtest · Aus dem Lernfortschritt erstellt</footer>
  <script src="/assets/app.js" defer></script>
</body>
</html>"""


def write(route: str, content: str) -> None:
    target = OUT / route / "index.html" if route else OUT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def section(markdown_text: str, name: str) -> str:
    match = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", markdown_text, re.M | re.S)
    return match.group(1).strip() if match else ""


def plain(markdown_text: str) -> str:
    text = re.sub(r"[`*_>#]", "", markdown_text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_review(progress: dict, review: dict) -> None:
    cards = []
    for index, item in enumerate(review.get("items", []), start=1):
        cards.append(f"""
        <article class="review-card flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-face flip-card-front">
              <span class="card-number">KARTE {index:02d} · FRAGE</span>
              <p class="prompt" lang="ru">{esc(item['prompt'])}</p>
              <button class="reveal" type="button" data-flip aria-pressed="false" aria-label="Antwort für Karte {index} anzeigen">Antwort anzeigen</button>
            </div>
            <div class="flip-card-face flip-card-back">
              <span class="card-number">KARTE {index:02d} · ANTWORT</span>
              <div class="answer">
                <p class="answer-de" lang="de">{esc(item['answer'])}</p>
                <p class="answer-note" lang="ru">{esc(item.get('note', ''))}</p>
              </div>
              <button class="reveal" type="button" data-flip aria-pressed="false" aria-label="Zur Frage von Karte {index}">Zurück zur Frage</button>
            </div>
          </div>
        </article>""")

    priorities = "".join(f"<li>{esc(item)}</li>" for item in progress.get("current_priorities", []))
    body = f"""
    <section class="hero">
      <div>
        <span class="eyebrow">3–5 Minuten vor der Sitzung</span>
        <h1>{esc(review.get('title', 'Wiederholen'))}</h1>
        <p>{esc(review.get('intro', ''))}</p>
      </div>
      <div class="updated">Aktualisiert am {display_date(review.get('updated', ''))}</div>
    </section>
    <section class="grid" aria-label="Karten zum Wiederholen">{''.join(cards)}</section>
    <section class="card panel" style="margin-top:18px">
      <h2>Aktueller Fokus</h2>
      <ol class="priority-list">{priorities}</ol>
    </section>"""
    write("", page("Wiederholen", "review", body))


def build_progress(progress: dict, gaps_text: str) -> None:
    rows = []
    for key, data in progress.get("skills", {}).items():
        score = data.get("score")
        unknown = score is None
        width = 0 if unknown else int(score) * 20
        score_text = "—" if unknown else f"{score}/5"
        cls = "skill-row unknown" if unknown else "skill-row"
        rows.append(f"""
        <div class="{cls}">
          <span class="skill-name">{esc(SKILL_LABELS.get(key, key))}</span>
          <span class="bar" aria-label="{score_text}"><span style="width:{width}%"></span></span>
          <span class="score">{score_text}</span>
        </div>""")
    priorities = "".join(f"<li>{esc(item)}</li>" for item in progress.get("current_priorities", []))
    body = f"""
    <div class="section-head"><div><span class="eyebrow">Aktueller Stand</span><h1>Fortschritt</h1></div><p>Aktualisiert am {display_date(progress.get('updated', ''))}</p></div>
    <div class="content-grid">
      <section class="card panel"><h2>Fertigkeiten</h2><div class="skill-list">{''.join(rows)}</div></section>
      <section class="card panel"><h2>Nächste Prioritäten</h2><ol class="priority-list">{priorities}</ol></section>
    </div>
    <section class="card panel prose"><h2>Aktuelle Schwierigkeiten</h2>{md(gaps_text.replace('# Current Gaps', '', 1))}</section>"""
    write("progress", page("Fortschritt", "progress", body))


def session_data(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    goal = plain(section(text, "Goals"))
    time = plain(section(text, "Time available"))
    return {"date": path.stem.split("-")[0:3], "slug": path.stem, "text": text, "goal": goal, "time": time}


def build_sessions() -> None:
    sessions = [session_data(path) for path in sorted((ROOT / "sessions").glob("*.md"), reverse=True)]
    cards = []
    for item in sessions:
        label = display_date("-".join(item["date"]))
        cards.append(f"""
        <a class="card session-link" href="/sessions/{esc(item['slug'])}/">
          <span class="session-meta">{label} · {esc(item['time'])}</span>
          <h2>{esc(item['goal'] or 'Trainingseinheit')}</h2>
          <p>Aufgaben, Ergebnisse und Wiederholungsziele öffnen →</p>
        </a>""")
        body = f'<article class="card panel prose">{md(item["text"])}</article>'
        write(f"sessions/{item['slug']}", page(f"Sitzung {label}", "sessions", body))
    body = f"""
    <div class="section-head"><div><span class="eyebrow">Trainingsverlauf</span><h1>Sitzungen</h1></div><p>{len(sessions)} gespeichert</p></div>
    <div class="session-list">{''.join(cards)}</div>"""
    write("sessions", page("Sitzungen", "sessions", body))


def build_teacher(text: str) -> None:
    checkpoint = re.search(r"\*\*Berücksichtigt bis:\*\*\s*(.+)", text)
    checkpoint_text = checkpoint.group(1) if checkpoint else "Kein Stand angegeben"
    body = f"""
    <div class="section-head"><div><span class="eyebrow">Informationen vor dem Unterricht</span><h1>Übersicht für die Lehrkraft</h1></div></div>
    <div class="teacher-banner"><strong>Berücksichtigter Stand</strong><span>{esc(checkpoint_text)}</span></div>
    <article class="card panel prose">{md(text)}</article>"""
    write("teacher", page("Für die Lehrkraft", "teacher", body, "Aktuelle Übersicht für die Deutschlehrkraft"))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "assets").mkdir()
    shutil.copy2(SITE / "styles.css", OUT / "assets" / "styles.css")
    shutil.copy2(SITE / "app.js", OUT / "assets" / "app.js")

    progress = yaml.safe_load((ROOT / "state" / "progress.yaml").read_text(encoding="utf-8"))
    review = yaml.safe_load((ROOT / "state" / "review.yaml").read_text(encoding="utf-8"))
    gaps = (ROOT / "state" / "gaps.md").read_text(encoding="utf-8")
    teacher = (ROOT / "teacher" / "next_lesson.md").read_text(encoding="utf-8")

    build_review(progress, review)
    build_progress(progress, gaps)
    build_sessions()
    build_teacher(teacher)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built site in {OUT}")


if __name__ == "__main__":
    main()
