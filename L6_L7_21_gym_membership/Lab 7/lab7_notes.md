# Lab 7 notes: Fuzzing for Input Validation Bugs

## Setup notes

- The Lab 7 files were in the instructor repo (`SETAPESU26/L6_L7_21_gym_membership`), not in my fork. I merged the instructor's `Add Lab 7 files` commit into `main`.
- The handout and playbook call the module `processor.py` / `test_processor.py`. In this repo they are `Lab 7/gym_membership.py` and `Lab 7/test_gym_membership.py`, with the functions `parse_plan`, `calculate_bmi` and `average_workout`.
- Environment: Python 3.11 venv at the repo root, with Hypothesis and pytest.
- `gym_membership.py` reads its inputs with `input()`. For the logged runs the inputs are passed on stdin and listed in the log header. For the screenshots they were typed into a real Terminal window.
- The screenshots in `evidence/screenshots/` are real macOS captures of Terminal windows (`screencapture`). The full text of each run is in `evidence/*.txt`.

## Contract

The test skeleton names every test `*_no_crash`, so the policy is the same for all three functions: they never raise, and they return `None` for any input they cannot handle. `main()` prints an "Invalid input" message when it gets `None`.

| Function | Valid input | Expected output | Behaviour on invalid input |
|---|---|---|---|
| `parse_plan(code)` | A string `PLAN-MONTHS`: exactly one `-`, PLAN is ASCII letters, MONTHS is a positive whole number (whitespace around either part is ignored) | `(PLAN.upper(), MONTHS)`, e.g. `"gold-12"` gives `("GOLD", 12)` | `None` for non-strings, a missing or extra `-`, an empty or non-letter plan, months that are not a whole number (`"abc"`, `"1.5"`, `"²"`), months of 0, or input longer than 100 characters |
| `calculate_bmi(data)` | A string `WEIGHT,HEIGHT` with two finite positive numbers | `round(weight / height**2, 1)` as a float | `None` for non-strings, the wrong number of fields, non-numbers, zero or negative values, NaN or infinity, a result that is not finite (overflow), or input longer than 100 characters |
| `average_workout(minutes)` | A string of whole numbers of minutes (0 or more) separated by whitespace, at least one value | `sum // count` as an int | `None` for non-strings, empty or whitespace-only input, non-integer tokens (`"sixty"`, `"²"`), negative minutes, or input longer than 10,000 characters |

## Bugs found

Falsifying examples taken from `evidence/step4_tests_fail_buggy.txt`. 9 tests failed and the 3 valid-input property tests passed.

| Function | Falsifying input | Exception or wrong result on the buggy code |
|---|---|---|
| `parse_plan` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `parse_plan` | `''`, `'GOLD12'` | `ValueError: not enough values to unpack (expected 2, got 1)` |
| `parse_plan` | `'GOLD--5'` | `ValueError: too many values to unpack (expected 2)` |
| `parse_plan` | `'GOLD-abc'` | `ValueError: invalid literal for int() with base 10: 'abc'` |
| `parse_plan` | `'GOLD-²'` | `ValueError: invalid literal for int() with base 10: '²'` |
| `parse_plan` | `'-12'` | Returned `('', 12)`, a plan with no name |
| `parse_plan` | `b''` | `TypeError: a bytes-like object is required, not 'str'` |
| `calculate_bmi` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `calculate_bmi` | `''` | `ValueError: not enough values to unpack (expected 2, got 1)` |
| `calculate_bmi` | `'70,0'` | `ZeroDivisionError: float division by zero` |
| `calculate_bmi` | `'70.0,1e+200'` | `OverflowError: (34, 'Result too large')` |
| `calculate_bmi` | `'-70,1.75'` | Returned `-22.9`, a negative BMI |
| `calculate_bmi` | `b''` | `TypeError: a bytes-like object is required, not 'str'` |
| `average_workout` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `average_workout` | `''` | `ZeroDivisionError: integer division or modulo by zero` |
| `average_workout` | `'²'`, `':'` | `ValueError: invalid literal for int() with base 10` |
| `average_workout` | `'-30 -40'`, `'-1'` | Returned `-35` and `-1`, negative workout minutes |

## Fixes

Each function now checks its input type and length first, then validates every field before using it. There is no bare `except` or blanket `except Exception`: only the specific errors that `int()`, `float()` and the BMI arithmetic can raise are caught.

| Function | Falsifying input | Root cause | Fix |
|---|---|---|---|
| `parse_plan` | `None`, `b''` | Called `.split()` without checking the type | Return `None` unless the input is a `str` of at most 100 characters |
| `parse_plan` | `''`, `'GOLD12'`, `'GOLD--5'` | Unpacked `split('-')` straight into two names | Split first and return `None` unless there are exactly 2 parts |
| `parse_plan` | `'-12'` | Never checked the plan name | Plan must be non-empty ASCII letters (`isascii() and isalpha()`) |
| `parse_plan` | `'GOLD-abc'`, `'GOLD-²'` | Unguarded `int()` (`'²'` passes `isdigit()` but `int()` rejects it) | `int()` inside `try`/`except ValueError`, returning `None` |
| `parse_plan` | `'GOLD-0'` | Accepted 0 months | Months must be greater than 0 |
| `calculate_bmi` | `None`, `b''`, `''` | Same type and unpacking problems | Type and length check, exactly 2 comma-separated fields |
| `calculate_bmi` | `'70,0'` | Division by zero | Weight and height must be greater than 0; `ZeroDivisionError` from underflow is also caught |
| `calculate_bmi` | `'70.0,1e+200'` | `height ** 2` overflows | Catch `OverflowError`, and reject a result that is not finite |
| `calculate_bmi` | `'nan,1.75'`, `'70,inf'` | `float()` accepts NaN and infinity | Reject non-finite values with `math.isfinite` |
| `calculate_bmi` | `'-70,1.75'` | Negative weight gave a negative BMI | Weight and height must be positive |
| `average_workout` | `None`, `b''` | Called `.split()` without checking the type | Return `None` unless the input is a `str` of at most 10,000 characters |
| `average_workout` | `''`, whitespace only | Divided by `len([])` | Return `None` when there are no values |
| `average_workout` | `'²'`, `':'`, `'45 sixty 30'` | Unguarded `int()` | `int()` inside `try`/`except ValueError`, returning `None` |
| `average_workout` | `'-30 -40'`, `'-1'` | Negative minutes accepted | Each value must be 0 or more |
| `main()` | Any bad input | Printed whatever came back, or crashed | Prints `Invalid input` when a function returns `None` |

Behaviour on valid input is unchanged: `GOLD-12` gives `('GOLD', 12)`, `70,1.75` gives `22.9` and `45 60 30` gives `45`. The three valid-input property tests passed both before and after the fix.

Results: 12 passed on the fixed code, stable across 3 extra runs with new random examples. See `evidence/step6_tests_pass_fixed.txt`.
