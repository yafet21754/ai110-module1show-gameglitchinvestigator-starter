"""Streamlit UI and round state for the number guessing game."""

import random

import streamlit as st

from logic_utils import check_guess, get_hint, get_range_for_difficulty, parse_guess, update_score

ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}


def reset_game():
    """Start a complete new round using the selected difficulty."""
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    # FIX: Codex centralized resets; AppTest verifies restart and difficulty changes.
    st.session_state.update(
        secret=random.randint(low, high),
        attempts=0,
        score=0,
        status="playing",
        history=[],
        guess_input="",
        last_outcome=None,
        input_error=None,
    )


def submit_guess():
    """Apply one valid guess before rendering the updated UI."""
    if st.session_state.status != "playing":
        return
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    ok, guess, error = parse_guess(st.session_state.guess_input, low, high)
    st.session_state.input_error = error
    if not ok:
        return

    # FIX: Codex moved counting after validation and removed alternating string secrets.
    st.session_state.attempts += 1
    st.session_state.history.append(guess)
    outcome = check_guess(guess, st.session_state.secret)
    st.session_state.last_outcome = outcome
    st.session_state.score = update_score(
        st.session_state.score, outcome, st.session_state.attempts
    )
    if outcome == "Win":
        st.session_state.status = "won"
    elif st.session_state.attempts >= ATTEMPT_LIMITS[st.session_state.difficulty]:
        st.session_state.status = "lost"


st.set_page_config(page_title="Number Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number before your attempts run out.")

st.sidebar.header("Settings")
st.sidebar.selectbox(
    "Difficulty", list(ATTEMPT_LIMITS), index=1, key="difficulty", on_change=reset_game
)
if "secret" not in st.session_state:
    reset_game()

low, high = get_range_for_difficulty(st.session_state.difficulty)
attempt_limit = ATTEMPT_LIMITS[st.session_state.difficulty]
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.sidebar.caption("Changing difficulty starts a new round.")
st.sidebar.caption("Wrong guess: −5. Win bonus: 100, minus 10 per previous attempt (minimum 10).")

st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
st.metric("Score", st.session_state.score)
st.write("Guess history:", st.session_state.history)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", st.session_state.difficulty)
    st.write("History:", st.session_state.history)

finished = st.session_state.status != "playing"
st.text_input("Enter your guess:", key="guess_input", disabled=finished)
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Submit Guess 🚀", on_click=submit_guess, disabled=finished)
with col2:
    st.button("New Game 🔁", on_click=reset_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.session_state.input_error:
    st.error(st.session_state.input_error)

if st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Start a new game to try again."
    )
elif show_hint and st.session_state.last_outcome:
    st.warning(get_hint(st.session_state.last_outcome))

st.divider()
st.caption("AI-assisted repairs verified with automated logic and Streamlit tests.")
