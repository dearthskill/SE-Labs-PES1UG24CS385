# Issues Found — `wildlife_sightings.py`

Line numbers refer to the **original** file (commit `fd57197`) and come from the reports in `reports/before/`.
Tools: Pylint 3.3.9, Bandit 1.8.6, Flake8 7.3.0 (Python 3.9.6).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak MD5 hash (Bandit B324) | Security | 15 | **High** severity / High confidence. `observerId` used `hashlib.md5`, a broken hash algorithm (CWE-327). | Switched to `hashlib.sha256`. The printed observer ID changes from `5455c3` to `e753d3` as a result. This is expected and is the only change in the output. |
| SQL injection (Bandit B608) | Security | 9 | **Medium** severity / Medium confidence. The INSERT was built with `str.format`, so a species or zone value with a quote in it could change the SQL (CWE-89). | Used a parameterised query, `VALUES (?, ?, ?)`, with the values passed as a tuple. |
| Dangerous mutable default (Pylint W0102) | Bug | 8 | `extras={}` is created once and shared by every call that leaves out `extras`, so totals leak between unrelated calls. | Default is now `None`, and a new dict is created inside the function. |
| Global connection at import time (Pylint W0621 ×3) | Quality | 4, 5, 8, 18, 26, 40 | A module-level `conn` was created and its table built on import, and `main()` ran on import too. Every function parameter `conn` shadowed the global. | Moved the connection into `main()`, added a `create_schema(conn)` helper, closed the connection at the end and guarded the call with `if __name__ == "__main__":`. |
| `rarest` crashes on an empty table | Bug | 27–29 | `min()` of an empty list raises `ValueError` when there are no sightings. No tool reported this; I found it while reading the code. | Return `None` when there are no rows. The result is the same as before whenever rows exist. |
| `assert` used for a runtime check (Bandit B101) | Security | 36 | Low severity. The `assert` disappears under `python -O`, so the check would silently stop running. | Replaced with `if len(totals) != 3: raise RuntimeError(...)`. |
| Non-snake_case names (Pylint C0103) | Style | 8, 14, 18 | `logSighting`, `observerId` and `zoneSummary` don't follow PEP 8 naming. | Renamed to `log_sighting`, `observer_id` and `zone_summary`. |
| Ambiguous variable name `l` (Flake8 E741) | Style | 28 | `l` is easy to confuse with `1` or `I`. | Renamed to `rarest_row`. |
| Missing docstrings (Pylint C0114, C0116 ×5) | Quality | 1, 8, 14, 18, 26, 32 | There was no module docstring and no function docstrings. | Added short docstrings to the module and to every function. |
| Unnecessary `else` after `return` (Pylint R1705) | Style | 20–23 | `zoneSummary` had an `if/else` where both branches returned. | Replaced with a single conditional-expression `return`. |
| Old-style string formatting (Pylint C0209) | Style | 9 | `str.format` could have been an f-string. | Went away with the B608 fix, since the query is now parameterised. |
| Line too long (Pylint C0301, Flake8 E501) | Style | 5, 9, 19, 27 | Pylint flagged lines 5 and 9 (over 100 characters). Flake8 flagged all four (over 79). | Split the SQL strings and calls across several lines. |
| Missing whitespace around operator (Flake8 E225) | Style | 28 | `l=min(...)` | Changed to `rarest_row = min(...)`. |

## Before / after summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 3.46/10 (17 messages) | 10.00/10 |
| Bandit | 3 issues (1 High, 1 Medium, 1 Low) | 0 issues |
| Flake8 | 6 issues | 0 issues |

Program output before: `5455c3 25 Leopard`. After: `e753d3 25 Leopard`. Only the observer ID changed, because of the switch from MD5 to SHA-256.
