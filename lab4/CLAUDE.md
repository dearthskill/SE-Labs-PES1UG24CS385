# CLAUDE.md — Scenario 16: Hangman Challenge

A multi-round terminal word-guessing game with categories, hints, scoring, and streaks.
Run with: `python main.py`

## Project files

- `main.py` — entry point
- `game.py` — round state, guesses, hints, scoring, session flow
- `words.py` — in-memory word and hint data
- `stats.py` — session statistics support (supplied, must be integrated)
- `requirements.txt` — dependency declaration

## Hard constraints

- Keep ALL state in memory. Do NOT add CSV, JSON, SQLite, or any other persistence.
- Do NOT add unnecessary external dependencies.
- Do NOT replace the project with an unrelated implementation; modify the existing code.
- Keep the code understandable and modular, preserving the existing file structure.
- Inspect the existing code before making changes.
- Explain every change made so it can be understood and tested.
- The whole assignment must be completed within 4 prompts, so batch related work in each response and avoid unnecessary clarifying questions.

## Tasks

### Task 1 — Guess-state correctness
- A previously attempted wrong letter must not consume another life.
- A previously accepted correct letter must not be counted as a new guess.
- **Done when:** each distinct letter affects the round exactly once.
- The original defect must be reproduced before it is fixed.

### Task 2 — Complete the session model
- Integrate `stats.py` so that rounds played, rounds won, and best streak are tracked correctly across multiple rounds.
- **Done when:** starting a new round resets only round-specific state; session statistics continue across the whole run.

### Task 3 — Difficulty and scoring
- Add difficulty choices that change the available lives and scoring.
- Preserve category selection.
- Hint usage must affect scoring consistently.
- **Done when:** difficulty changes round rules without leaking state between rounds.

### Task 4 — Robust input and feedback
- Improve handling of invalid letters, repeated commands, category selection, and hint usage.
- Feedback must describe actual player actions, once.
- **Done when:** malformed input never changes game state and feedback is not duplicated.

## Required testing

Test all of the following:
- repeated correct guesses
- repeated incorrect guesses
- hints
- category changes
- multiple rounds
- streak resets
- difficulty changes
- invalid input
- quitting
- boundary cases

## Submission (only these three items)

1. A 10-second gameplay video **before** changes, showing the bug/broken behavior.
2. A 10-second gameplay video **after** changes, showing the bug fixed and new features working.
3. The link to the LLM chat page with the complete chat history.
