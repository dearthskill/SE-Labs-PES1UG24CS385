# Reflection — Lab 5: Static Code Analysis

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest fixes were the mechanical ones. These were renaming `logSighting`, `observerId` and `zoneSummary` to snake_case, renaming `l`, adding docstrings, and switching `hashlib.md5` to `hashlib.sha256`. Each was a one-line change and the tool told me exactly where to make it. The hardest was the module-level `conn`. Fixing it meant restructuring the program: I moved the connection into `main()`, added a `create_schema` helper and added the `if __name__ == "__main__":` guard, and then had to check that the output was still the same. Line length was also trickier than I expected, because fixes interacted. The Bandit fix (adding a parameter tuple to the INSERT) made that line longer, at 105 characters, so Pylint flagged a new C0301 and the score was 9.70 instead of 10.00 until I wrapped the line.

## 2. Did the static analysis tools report any false positives? If so, how did you identify them?

I didn't find any clear false positives. I checked each finding against the code. The B608 SQL injection was real, since the values were inserted straight into the SQL string with `str.format`. The closest thing to a false positive was B324 for MD5. The hash only makes a short display ID, not a password or signature, so in practice the risk is low, and Bandit itself suggests `usedforsecurity=False` as an option. I still switched to SHA-256 because it's simple and costs nothing. Bandit's B101 `assert` warning was valid too, because the check would be removed under `python -O`. The tools also missed something: none of them flagged that `rarest` crashes with `ValueError` on an empty table. I only found that by reading the code.

## 3. How would you integrate static analysis tools into your actual software development workflow?

Locally, I would set up Flake8 and Pylint in my editor so problems show up as I type instead of in one big report at the end. I would add a pre-commit hook that runs Flake8 and Bandit, so formatting problems and things like string-built SQL can't be committed. In CI, I would run all three tools on every pull request, with a minimum Pylint score (for example 9.5) and a rule that fails the build on any Bandit High or Medium finding. This lab showed why the tools should be re-run after every fix. A fix for one tool (the Bandit query change) created a new warning in another tool (Pylint line length).

## 4. What tangible improvements in code quality, readability, security or robustness did you observe after fixing the issues?

The Pylint score went from 3.46/10 to 10.00/10. Bandit went from 3 issues (1 High, 1 Medium, 1 Low) to 0, and Flake8 went from 6 issues to 0. For security, the INSERT is now parameterised, so a name like `O'Brien's owl` is stored correctly and can't break the SQL. I tested this after the fix. For robustness, `rarest` now returns `None` on an empty table instead of crashing. Separate calls to `log_sighting` no longer share one hidden dictionary, and the module can be imported without opening a database or running `main()`. The program still prints `25 Leopard` as before. Only the observer ID changed, because of the hash switch.
