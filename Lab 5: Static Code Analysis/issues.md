# Lab 5 – Issues Found

| # | Issue | Type | Tool / Code | Severity | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|----------|---------|-------------|--------------|
| 1 | Unsafe deserialization with pickle | Security | Bandit B301, B403 | Medium | 2, 44, 49 | `pickle.load` can execute arbitrary code if the backup file is tampered with | Replace pickle with JSON for backup/restore; convert keys back to int on restore |
| 2 | try/except/pass hides errors | Security / Bug | Bandit B110, Pylint W0702, Flake8 E722 | Low (Bandit) / Warning | 22–25 | Bare `except: pass` silently ignores all errors (e.g. updating nonexistent order 42) | Catch only `KeyError` and raise a clear error instead of passing |
| 3 | Mutable default argument | Bug | Pylint W0102 | Warning | 11 | `order_history=[]` is shared across every call | Default to `None` and create a new list inside the function |
| 4 | Too broad exception | Bug | Pylint W0718 | Warning | 32 | `except Exception` hides unexpected errors while loading the menu | Catch only `FileNotFoundError` and `json.JSONDecodeError` |
| 5 | Files not closed / no encoding | Resource leak | Pylint R1732, W1514 | Refactor / Warning | 30, 43, 49 | Files opened without `with`, some never closed; no encoding given | Use `with open(..., encoding="utf-8")` |
| 6 | Global statements | Design | Pylint W0603, C0103 | Warning / Convention | 7, 12, 28, 48 | Functions reassign module globals | Mutate the dicts in place (`clear`/`update`) and derive the next ID from existing orders |
| 7 | Non-snake_case function name | Style | Pylint C0103 | Convention | 51 | `printQueue` breaks PEP 8 naming | Rename to `print_queue` |
| 8 | Old-style string formatting | Style | Pylint C0209 | Convention | 52 | `%` formatting instead of f-string | Use an f-string |
| 9 | Missing docstrings | Documentation | Pylint C0114, C0116 | Convention | 1, 11, 21, 27, 35, 42, 47, 51, 56 | Module and functions have no docstrings | Add docstrings |
| 10 | Blank lines / line length | Style | Flake8 E302, E305, E501 | Style | 11–56, 16, 54, 70 | Only 1 blank line between functions; lines over 79 chars | Add 2 blank lines; wrap long lines |
| 11 | Invalid status accepted | Logic bug | Not flagged | High (functional) | 21–23 | `VALID_STATUSES` is never used, so "teleported" is accepted | Validate status against `VALID_STATUSES` and raise `ValueError` |
| 12 | Unknown dish silently costs 99 | Logic bug | Not flagged | High (functional) | 15 | "sushi" isn't on the menu but is charged 99 | Raise `ValueError` for items not on the menu |
| 13 | Empty order accepted | Logic bug | Not flagged | Medium (functional) | 60 | Order with no customer and no items is created and "delivered" | Validate customer name and items before creating an order |
| 14 | Script runs on import | Design | Not flagged | Low | 70 | `main()` runs whenever the module is imported | Wrap in `if __name__ == "__main__":` |