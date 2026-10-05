# AI Interactions Log

## Agent workflow

**Tool:** ChatGPT/Codex. One assistant session was used; separate bug-specific chat sessions were not created. No second AI model was used.

**Actual user request:** "do this for me", followed by the full Game Glitch Investigator assignment; the user then supplied a screenshot identifying their fork.

**Work performed:** cloned the fork; read its source and starter tests; reproduced original function/UI failures; marked FIXME locations and made an investigation commit; refactored helpers and callbacks; generated unit and Streamlit AppTest regressions; reviewed diffs; ran tests and a server health check; completed an evidence-based README and reflection draft.

**Human review status:** the assistant presented two return-format options for review, but no selection was received. The code uses a string outcome plus a separate hint helper. The student must review the diff and supply their own accepted/rejected-suggestion explanation; no human testing or approval is fabricated.

## Test generation / edge cases

The supplied assignment requested: "Ask your AI coding assistant to generate a pytest case ... that specifically targets the bug you just fixed." The assistant expanded that requirement into the cases below; these are not invented quotations of separate student prompts.

| Edge case | Generated test / expectation | Result |
|---|---|---|
| Guess 60 or 40 against 50 | Correct numeric outcome and LOWER/HIGHER message | Passed |
| Blank, whitespace, text, decimals, infinity, scientific notation | Reject invalid input without silently truncating | Passed |
| Inclusive range endpoints | Accept valid endpoints; reject above maximum | Passed |
| Wrong high guesses on even turns | Deduct five consistently | Passed |
| First win / late win | Bonus starts at 100 and bottoms out at 10 | Passed |
| All three difficulties at final allowed attempt | Correct final guess wins; incorrect final guess loses | Passed |
| New Game after won/lost | Clear round state and allow play again | Passed |
| Invalid submission in actual app | No change to score, attempts, secret, or history | Passed |
| Difficulty change / ordinary rerun | Reset only on new round; preserve secret and prevent duplicate scoring on reruns | Passed |

Full output is in `test_results.txt` and README.md. No formal linting or model-comparison stretch challenge is claimed.
