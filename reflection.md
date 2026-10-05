# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret 50; guess 60 / 40 | Ask the player to go lower / higher | Messages say HIGHER / LOWER, respectively | Direct execution: `(Too High, Go HIGHER!)` / `(Too Low, Go LOWER!)` |
| Guess 9; secret converted to `"50"` | Too Low (numeric comparison) | Too High (string comparison) | Direct execution: `check_guess(9, "50")` returns Too High |
| Score 0; Too High; attempt 2 | Deduct 5 points | Adds 5 points | Direct execution: `update_score(0, "Too High", 2) == 5` |
| Input `3.9` | Reject a non-integer | Silently accepts 3 | Direct execution: `(True, 3, None)` |
| New Game after winning | Reset to playing and empty history | Reset handler only updates attempts/secret | Streamlit AppTest: status remains `won`, history remains `[50]` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

## Investigation notes — before repairs

The assistant extracted and executed the original functions without modifying their behavior. The first targets are hint/comparison correctness and score correctness, followed by input validation and round lifecycle repairs. The existing three tests import unimplemented helpers and expect `check_guess` to return a string, whereas app.py currently returns a tuple; preserve the starter tests and align the implementation with their contract. The README claims that the secret changes on every submit, but this version initializes it only when absent from session state; that claim is not supported by the source.

Baseline verification: `python -m pytest -q` reports **3 failed**, all due to unimplemented helpers. Streamlit AppTest shows an initial attempt count of 1 (only 7 of 8 displayed), a first submitted winning guess scores 70, and New Game leaves the status as won. AppTest produced no application exceptions.
