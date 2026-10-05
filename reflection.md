# Reflection: Game Glitch Investigator

**Evidence-based draft prepared by Codex.** The user supplied the assignment and their fork. The debugging and tests below were performed by the assistant; this document does not claim the student personally ran them or reviewed the changes. The personal-review note in section 2 must be completed by the student before submission.

## 1. What was broken when you started?

The initial Streamlit AppTest run displayed only seven remaining attempts in a Normal game that should allow eight. Executing the original functions showed that a high guess told the player to go higher and a low guess told the player to go lower. Alternating conversion of the secret to a string could also cause lexical comparisons, so 9 incorrectly compared as greater than "50". Scoring could reward a wrong answer, decimals were silently truncated, and New Game did not clear the won status or history. The baseline pytest run had three failures because the imported helpers were unimplemented.

### Bug Reproduction Log

| Input / action | Expected behavior | Actual behavior before repair | Observed output / evidence |
|---|---|---|---|
| `check_guess(60, 50)` | Too High; go lower | Go HIGHER | `('Too High', '📈 Go HIGHER!')` |
| `check_guess(40, 50)` | Too Low; go higher | Go LOWER | `('Too Low', '📉 Go LOWER!')` |
| `check_guess(9, "50")` | App should compare integers; 9 is too low | Lexical comparison says too high | `('Too High', '📈 Go HIGHER!')` |
| `update_score(0, "Too High", 2)` | Deduct five for a wrong answer | Rewards five points | `5` |
| `parse_guess("3.9")` | Reject a decimal | Accepts 3 | `(True, 3, None)` |
| Start Normal game | Eight attempts available | Starts with one attempt already counted | AppTest: attempts `1`, display `Attempts left: 7` |
| Win with 50, then New Game | Playing status, empty history | Remains won with old history | AppTest: status `won`, history `[50]` |
| `python -m pytest -q` | Runnable helper implementations | Three tests fail | `3 failed`; `NotImplementedError` in `logic_utils.py` |

The function results were reproduced by extracting the original function definitions with Python's AST and executing them; the UI results came from Streamlit AppTest. There was no syntax error observed. The README's claim of a secret regenerating every submit was not supported by this starter version, so it was not treated as a reproduced bug.

## 2. How did you use AI as a teammate?

The user asked ChatGPT/Codex to complete the supplied debugging assignment, and Codex inspected the fork, proposed repairs, edited the code, generated tests, and recorded the results. A correct AI suggestion was to move the game rules into `logic_utils.py` and keep both the guess and secret as integers; the unchanged starter tests, numeric-comparison test, and complete-game AppTest verify that approach. An alternative AI suggestion presented for review was to keep the starter app's combined `(outcome, message)` return and change the original tests; the implemented version instead preserves their string-return contract and uses a separate `get_hint()` helper, so comparison rules and presentation can be verified separately. All three original tests and both hint-direction cases pass, which supports the implemented choice. That design selection was made by Codex; no response to the student's review question was received, so it is not represented as a rejection personally made by the student.

**Personal review still required:** After inspecting the changes, replace this note with your own explanation of one AI suggestion you accept and one you reject or modify, why, and how you checked your decision. You may review the return-format alternative above, the proposed scoring rule, or the input-handling design; record what you actually decide rather than claiming an action you did not take.

## 3. Debugging and testing your fixes

Verification used concrete expected outputs and state transitions instead of assuming that code which runs is correct. The baseline had three failing tests; after the repairs, `python -m pytest -q` reported **51 passed in 2.12s**, including all three original cases. For example, a guess of 60 against 50 must return Too High and a LOWER hint, and the 40 → 70 → 50 AppTest sequence must finish with a score of 70 and status won. Codex generated the additional test set for invalid input, exact attempt limits, final-attempt wins, difficulty changes, and restarting after both winning and losing, and reviewed the changed code. Starting the Streamlit server also produced a healthy HTTP 200 response; browser play by the student remains a separate review step.

### Debugging/test evidence

- `tests/test_game_logic.py`: 36 cases for comparisons, hint directions, input validation, boundaries, difficulty ranges, and score rules.
- `tests/test_app.py`: 15 cases exercising real Streamlit callbacks and reruns with controlled secrets.
- `test_results.txt`: captured output of the final pytest run.
- Before repairs: `check_guess(9, "50")` incorrectly said Too High; after repairs the UI never creates string secrets, `check_guess(9, 50)` returns Too Low, and an accidentally supplied string raises a clear TypeError.
- The game starts at zero used attempts; invalid input leaves state unchanged; the final allowed guess can still win; terminal rounds cannot award points again.
- The repair commit contains the logic/UI changes and tests; the earlier investigation commit preserves the FIXME markers and initial reproduction log.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script when someone interacts with a widget, like redrawing a scoreboard after each play. Session state is the notebook that remembers the secret, score, attempts, and history between those redraws. The secret should be generated when a round starts, and a reset must update every field that belongs to that round. Callbacks update state before the page is rendered, so the displayed score and remaining attempts immediately match the accepted guess.

## 5. Looking ahead: your developer habits

A useful habit illustrated here is to reproduce a bug with a specific input before changing code, then keep a regression test for that behavior. A future improvement would be to agree on scoring and return-value contracts with the human reviewer before implementing them. An AI hallucination can look like a confident claim about a bug that is not actually present, such as assuming the README's secret-reset description applied to this version without checking it. A human-in-the-loop process combines the test set and verification evidence with the student's own review; automated success alone does not establish that the student understands or approves every change.
