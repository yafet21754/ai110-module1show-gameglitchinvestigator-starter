"""Pure game rules, independent of Streamlit and session state."""


def get_range_for_difficulty(difficulty: str):
    """Return the starter game's inclusive ranges without changing difficulty design."""
    return {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 50)}.get(
        difficulty, (1, 100)
    )


def parse_guess(raw: str | None, low: int = 1, high: int = 100):
    """Accept a whole number in range; return (ok, value, error)."""
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."
    # FIX: Codex moved parsing here and removed float truncation; pytest checks it.
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."
    if not low <= value <= high:
        return False, None, f"Enter a number between {low} and {high}."
    return True, value, None


def check_guess(guess: int, secret: int):
    """Return the outcome string expected by the unchanged starter tests."""
    # FIX: Codex removed lexical fallback; app.py now supplies integers every turn.
    if type(guess) is not int or type(secret) is not int:
        raise TypeError("guess and secret must be integers")
    if guess == secret:
        return "Win"
    return "Too High" if guess > secret else "Too Low"


def get_hint(outcome: str):
    """Tell the player which direction their NEXT guess should go."""
    # FIX: Codex separated feedback from comparisons and tested both directions.
    return {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }[outcome]


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Wrong guesses cost 5; wins earn max(10, 100 - 10 * (attempt - 1))."""
    # FIX: Codex removed the even-attempt reward and corrected the bonus offset.
    if outcome == "Win":
        return current_score + max(10, 100 - 10 * (attempt_number - 1))
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
