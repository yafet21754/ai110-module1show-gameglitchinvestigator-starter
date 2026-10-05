# 🎮 Game Glitch Investigator: Number Guesser

A repaired Python/Streamlit game: guess a secret whole number using high/low hints before the attempts run out. Core rules live in `logic_utils.py`; `app.py` handles widgets and session state.

## Setup

Use Python 3.10 or newer. Clone your own fork:

```bash
git clone https://github.com/yafet21754/ai110-module1show-gameglitchinvestigator-starter.git
cd ai110-module1show-gameglitchinvestigator-starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` instead.

Run the tests with `python -m pytest -q` (or `pytest`).

## Rules

| Difficulty | Inclusive range | Valid guesses allowed |
|---|---|---|
| Easy | 1–20 | 6 |
| Normal | 1–100 | 8 |
| Hard | 1–50 | 5 |

The difficulty ranges are preserved from the starter. Only valid in-range integers consume an attempt; blank input, text, decimals, and out-of-range guesses show an error. Each incorrect guess costs 5 points. A win adds `max(10, 100 - 10 * (attempt_number - 1))` points to the current round score; negative scores are allowed. New Game and difficulty changes reset the score, attempts, history, feedback, and status. A win or loss disables further guessing until a new round starts.

## Document Your Experience

- [x] **Purpose:** a number guessing game with clear hints and a finite round.
- [x] **Bugs found:** reversed hints, string rather than numeric comparison on alternating turns, inconsistent score rewards, decimal truncation, attempts starting at 1, and incomplete reset behavior. The sidebar and main prompt could also disagree about the range.
- [x] **Fixes:** moved parsing, comparison, hints, scoring, and difficulty ranges into pure helpers; kept secrets as integers; validated input before counting attempts; centralized complete resets; used callbacks to update state before rendering counters.

The original README claimed the secret changed on every submission. Inspection showed this version already stored the secret in session state, so that claim was not copied into the bug log as a reproduced defect. The original three test cases remain unchanged and now pass. Their string-return contract guided the refactor: `check_guess()` returns the outcome, while `get_hint()` returns the message.

Codex performed the implementation, automated verification, and documentation in this repository. `reflection.md` distinguishes that evidence from the student's personal review, which still needs to be completed before submission.

## Demo Walkthrough

This is the deterministic scenario exercised by `test_demo_walkthrough_and_finished_game`. It uses Normal difficulty and sets the secret to **50** in the test; ordinary games generate a random secret.

1. Start a Normal game: score **0**, **8** attempts left, empty history.
2. Enter **40** and click Submit Guess. The game says **Go HIGHER!**, the score is **−5**, and **7** attempts remain.
3. Enter **70** and submit. The game says **Go LOWER!**, the score is **−10**, and **6** attempts remain.
4. Enter **50** and submit. The game announces a win and adds an **80-point** third-attempt bonus, producing a final score of **70**.
5. The history is **[40, 70, 50]** and **5** attempts remain. Further submissions are disabled; an ordinary rerun does not add the bonus again.
6. Click New Game. Score and attempts reset to **0**, history and input clear, and a new secret is generated in the selected range.
7. Enter **3.9** or **abc**. An error appears without changing score, history, or attempts.

For a manual check, use Developer Debug Info to see your random secret and try guesses below, above, and equal to it. Also use all allowed guesses incorrectly, restart, and switch difficulty.

## Test Results

Actual output from `python -m pytest -q`:

```text
.............```

The suite includes 36 pure-logic cases and 15 Streamlit AppTest cases, including all three original starter tests. AppTest executes the actual app and its callbacks, covering both win/loss endings, all difficulty attempt limits, restarts, invalid input, hints off, and difficulty changes. The Streamlit server was also started with `python -m streamlit run app.py`; its health endpoint returned **HTTP 200, `ok`**. These are automated checks, not a claim that the student manually played the game in a browser.

## Extensions and Evidence

Additional edge cases cover whitespace, decimal and nonnumeric input, range endpoints, even/odd scoring, and winning on the final allowed attempt. See `ai_interactions.md` for the actual agent/test-generation workflow; no model comparison or linting challenge is claimed. `test_results.txt` stores the captured pytest output.

## Before Submission

- [ ] Review the code diff and play a round locally.
- [ ] Complete the personal-review note in `reflection.md` section 2 with your own accepted and rejected/modified AI suggestion.
- [ ] Confirm the repository is public and the latest commits appear on GitHub.
- [ ] Submit the repository URL through the Week 3 submit button.
