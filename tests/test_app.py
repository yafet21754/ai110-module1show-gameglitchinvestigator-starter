"""Exercise real Streamlit callbacks and reruns with deterministic secrets."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def start_game(difficulty="Normal", secret=50):
    app = AppTest.from_file(str(APP)).run()
    if difficulty != "Normal":
        app.selectbox[0].select(difficulty).run()
    app.session_state["secret"] = secret
    assert not app.exception
    return app


def guess(app, raw):
    app.text_input[0].set_value(raw)
    app.button[0].click().run()
    assert not app.exception
    return app


def test_demo_walkthrough_and_finished_game():
    app = start_game()
    assert "Attempts left: 8" in app.info[0].value
    guess(app, "40")
    assert "HIGHER" in app.warning[0].value
    assert app.session_state["score"] == -5
    guess(app, "70")
    assert "LOWER" in app.warning[0].value
    assert app.session_state["score"] == -10
    assert app.session_state["secret"] == 50
    guess(app, "50")
    assert app.session_state["status"] == "won"
    assert app.session_state["score"] == 70
    assert app.session_state["history"] == [40, 70, 50]
    assert "Attempts left: 5" in app.info[0].value
    assert app.button[0].disabled
    app.run()
    assert app.session_state["score"] == 70


@pytest.mark.parametrize("raw", ["", " ", "abc", "3.9", "0", "101"])
def test_invalid_guesses_do_not_change_round(raw):
    app = start_game()
    guess(app, raw)
    assert app.error
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert app.session_state["status"] == "playing"
    assert app.session_state["secret"] == 50


def test_first_guess_win_with_hints_off():
    app = start_game()
    app.checkbox[0].uncheck().run()
    guess(app, "50")
    assert app.success
    assert app.session_state["score"] == 100
    assert app.session_state["attempts"] == 1


@pytest.mark.parametrize("difficulty, limit, secret", [("Easy", 6, 20), ("Normal", 8, 50), ("Hard", 5, 50)])
@pytest.mark.parametrize("win_last", [True, False])
def test_exact_attempt_limit_and_restart(difficulty, limit, secret, win_last):
    app = start_game(difficulty, secret)
    for _ in range(limit - 1):
        guess(app, "1")
        assert app.session_state["status"] == "playing"
    guess(app, str(secret) if win_last else "1")
    assert app.session_state["status"] == ("won" if win_last else "lost")
    assert "Attempts left: 0" in app.info[0].value
    assert app.button[0].disabled
    app.button[1].click().run()
    assert not app.exception
    assert app.session_state["status"] == "playing"
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert app.text_input[0].value == ""
    assert 1 <= app.session_state["secret"] <= (20 if difficulty == "Easy" else 100 if difficulty == "Normal" else 50)
    assert not app.button[0].disabled
    guess(app, str(app.session_state["secret"]))
    assert app.session_state["status"] == "won"


def test_difficulty_change_resets_active_round():
    app = start_game()
    guess(app, "40")
    app.selectbox[0].select("Easy").run()
    assert not app.exception
    assert 1 <= app.session_state["secret"] <= 20
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert "between 1 and 20" in app.info[0].value
    guess(app, "21")
    assert app.session_state["attempts"] == 0
    assert app.error
