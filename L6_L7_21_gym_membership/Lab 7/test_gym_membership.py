import math

from hypothesis import given, example, settings, strategies as st
from gym_membership import parse_plan, calculate_bmi, average_workout

FUZZ = settings(max_examples=300, deadline=None)

# Anything a caller might pass in: not just text, but None and other types too.
any_input = st.one_of(
    st.none(), st.text(), st.integers(),
    st.floats(allow_nan=True, allow_infinity=True), st.booleans(), st.binary(),
    st.lists(st.text()), st.dictionaries(st.text(), st.integers()),
)


# ---------- parse_plan ----------

def check_plan_result(result):
    assert result is None or (
        isinstance(result, tuple) and len(result) == 2
        and isinstance(result[0], str) and result[0].isascii()
        and result[0].isalpha() and result[0].isupper()
        and isinstance(result[1], int) and result[1] > 0
    )


@FUZZ
@given(st.text() | st.none())
@example(None)
@example("")
@example("   ")
@example("GOLD12")
@example("GOLD-12-3")
@example("GOLD-abc")
@example("GOLD-" + "9" * 5000)
def test_parse_plan_no_crash(s):
    check_plan_result(parse_plan(s))


@FUZZ
@given(any_input)
def test_parse_plan_any_type_no_crash(x):
    check_plan_result(parse_plan(x))


@FUZZ
@given(st.text(alphabet="GOLDsilver-0123456789 +.\u00b2\u0663\t", max_size=15))
@example("GOLD-0")
@example("GOLD--5")
@example("-12")
@example("GOLD-²")
@example("GOLD-1.5")
def test_parse_plan_near_valid(s):
    check_plan_result(parse_plan(s))


@FUZZ
@given(st.from_regex(r"[A-Za-z]{1,10}", fullmatch=True), st.integers(1, 120))
def test_parse_plan_round_trip(plan, months):
    assert parse_plan(f"{plan}-{months}") == (plan.upper(), months)


# ---------- calculate_bmi ----------

def check_bmi_result(result):
    assert result is None or (
        isinstance(result, float) and math.isfinite(result) and result >= 0
    )


@FUZZ
@given(st.text() | st.none())
@example(None)
@example("")
@example("70")
@example("70,0")
@example("70,1.75,3")
@example("nan,1.75")
@example("70,inf")
@example("-70,1.75")
def test_calculate_bmi_no_crash(s):
    check_bmi_result(calculate_bmi(s))


@FUZZ
@given(any_input)
def test_calculate_bmi_any_type_no_crash(x):
    check_bmi_result(calculate_bmi(x))


@FUZZ
@given(st.floats(allow_nan=True, allow_infinity=True),
       st.floats(allow_nan=True, allow_infinity=True))
@example(70.0, 0.0)
@example(1e308, 1e-300)
@example(70.0, 1e200)
def test_calculate_bmi_extreme_numbers(weight, height):
    check_bmi_result(calculate_bmi(f"{weight},{height}"))


@FUZZ
@given(st.floats(20, 300), st.floats(0.5, 2.5))
def test_calculate_bmi_matches_formula(weight, height):
    assert calculate_bmi(f"{weight},{height}") == round(weight / height ** 2, 1)


# ---------- average_workout ----------

def check_average_result(result):
    assert result is None or (isinstance(result, int) and result >= 0)


@FUZZ
@given(st.text() | st.none())
@example(None)
@example("")
@example("   ")
@example("45 sixty 30")
@example("-30 -40")
@example("²")
def test_average_workout_no_crash(s):
    check_average_result(average_workout(s))


@FUZZ
@given(any_input)
def test_average_workout_any_type_no_crash(x):
    check_average_result(average_workout(x))


@FUZZ
@given(st.lists(st.integers(-1000, 1000), max_size=10).map(lambda xs: " ".join(map(str, xs))))
def test_average_workout_integer_lists(s):
    check_average_result(average_workout(s))


@FUZZ
@given(st.lists(st.integers(0, 600), min_size=1, max_size=50))
def test_average_workout_bounds(values):
    result = average_workout(" ".join(map(str, values)))
    assert result == sum(values) // len(values)
    assert min(values) <= result <= max(values)
