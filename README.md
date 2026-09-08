# Berliner Sprachtest zur Einbürgerung — Training Repository

Persistent training system for systematic preparation for the **Berliner Sprachtest zur Einbürgerung**.

The repository is designed to be used primarily with **Codex CLI**. A German teacher is the main speaking partner twice per week. ChatGPT / Voice is optional and used for occasional additional practice, e.g. while driving.

## Core principle

Do not "study German in general". Train the ability to **produce useful B1 German spontaneously under exam conditions**.

The system continuously tracks:

- exam skills;
- topic coverage;
- recurring errors;
- active vs passive vocabulary;
- useful Redemittel;
- teacher feedback;
- handwritten writing tasks;
- evidence of improvement.

## Normal commands to Codex

You should usually be able to start with one sentence:

- `Начинаем сегодняшнюю тренировку.`
- `У меня сегодня 30 минут.`
- `Давай сегодня только Sprechen.`
- `Подготовь контекст для следующего занятия с преподавателем.`
- `Проведи mock exam.`
- `Сделай ревью прогресса за последние две недели.`
- `Сгенерируй промпт для ChatGPT Voice на 20 минут практики за рулем.`

Codex must read `AGENTS.md` and the state files before selecting exercises.

## Recommended weekly rhythm

A reasonable default is:

- 4–6 independent sessions per week;
- about 60 minutes when time allows;
- 2 speaking-heavy lessons with the native German teacher;
- occasional ChatGPT Voice sessions for extra spontaneous speaking.

The schedule is not a target by itself. Quality and repeated retrieval matter more than clock time.

## Daily session

Typical ~60 minute session:

1. 5–10 min — retrieval warm-up from older material
2. 15–20 min — speaking / exam task
3. 15–20 min — handwritten Schreiben or another productive task
4. 10 min — targeted gap drill
5. 5 min — active recall + state update

Codex should vary this structure and adapt it to the current weaknesses.

## Handwritten Schreiben workflow

Writing tasks are done **by hand on paper**.

1. Codex gives the task.
2. The learner writes it on paper without a prepared model answer.
3. A photo is uploaded to ChatGPT/Codex for review.
4. The attempt is evaluated and logged.
5. Important errors and reusable phrases are added to the state.
6. A writing task is NOT marked successful until the actual handwritten attempt has been reviewed.

## Teacher workflow

Before a lesson:

`Подготовь контекст для преподавателя.`

Codex updates:

`teacher/next_lesson.md`

It should be usable directly by a native German teacher and should prioritize dialogue, spontaneous follow-up questions, role play, and the learner's actual recent gaps.

After a lesson, tell Codex what happened and any teacher feedback. It should integrate that evidence into the state.

## ChatGPT Voice workflow

Voice is optional, not the source of truth.

Ask Codex:

`Сгенерируй промпт для ChatGPT Voice на 20 минут.`

Codex creates/updates:

`prompts/chatgpt_voice_next.md`

Paste that prompt into a fresh ChatGPT chat and practice. Afterwards, if useful, summarize notable mistakes/successes back to Codex.

## Source of truth

Persistent state lives in this repository.

Important files:

- `state/progress.yaml`
- `state/gaps.md`
- `state/dashboard.md`
- `vocabulary/learning.md`
- `vocabulary/active.md`
- `vocabulary/weak.md`
- `vocabulary/constructions.md`
- `sessions/`
- `teacher/`

Git history provides a long-term record of changes.

## Web dashboard

The static dashboard is generated directly from the repository state, session logs, vocabulary, and teacher summary.

Local preview:

```sh
make setup
make preview
```

Open `http://localhost:8000`. A GitHub Actions workflow rebuilds and deploys the site to GitHub Pages after every push to `main`.
