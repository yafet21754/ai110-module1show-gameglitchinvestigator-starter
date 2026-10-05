import pytest

from logic_utils import check_guess, get_hint, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


@pytest.mark.parametrize("guess, direction", [(60, "LOWER"), (40, "HIGHER")])
def test_hint_tells_player_correct_direction(guess, direction):
    assert direction in get_hint(check_guess(guess, 50))


def test_numeric_comparison_not_lexical():
    assert check_guess(9, 50) == "Too Low"
    with pytest.raises(TypeError):
        check_guess(9, "50")


@pytest.mark.parametrize("raw", [None, "", "   ", "hello", "3.9", "50.0", "nan", "inf", "1e2", "0", "101"])
def test_invalid_input(raw):
    ok, value, error = parse_guess(raw)
    assert not ok
    assert value is None
    assert error


@pytest.mark.parametrize("raw, expected", [("1", 1), ("100", 100), (" 50 ", 50)])
def test_valid_input(raw, expected):
    assert parse_guess(raw) == (True, expected, None)


@pytest.mark.parametrize("difficulty, bounds", [("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 50))])
def test_difficulty_bounds(difficulty, bounds):
    assert get_range_for_difficulty(difficulty) == bounds
    low, high = bounds
    assert parse_guess(str(low), low, high)[0]
    assert parse_guess(str(high), low, high)[0]
    assert not parse_guess(str(high + 1), low, high)[0]


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_every_wrong_guess_costs_five(outcome, attempt):
    assert update_score(0, outcome, attempt) == -5


@pytest.mark.parametrize("attempt, bonus", [(1, 100), (2, 90), (3, 80), (10, 10), (20, 10)])
def test_win_bonus(attempt, bonus):
    assert update_score(-10, "Win", attempt) == -10 + bonus
