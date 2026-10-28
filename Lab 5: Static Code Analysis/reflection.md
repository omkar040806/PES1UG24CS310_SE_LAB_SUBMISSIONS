# Lab 5 – Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the style issues from Flake8 (E302/E305 blank lines, E501 long lines)
and simple Pylint conventions like renaming `printQueue` to `print_queue`, using f-strings
and adding docstrings. They were mechanical and didn't change how the program behaves.

The hardest was removing the `global` statements (W0603). It needed a small redesign:
mutating the `orders` and `menu` dicts in place and deriving the next order ID from
existing orders instead of a global counter. Replacing `pickle` with JSON (Bandit B301)
was also tricky, because JSON stores dictionary keys as strings, so order IDs had to be
converted back to integers when restoring.

## 2. Did the static analysis tools report any false positives? If so, describe one.

No real false positives. The closest was Bandit's B403 on `import pickle`: importing
pickle is not dangerous by itself, and in this script the backup file was written by the
program itself. Still, the warning was worth acting on because the backup file could be
tampered with on disk, and JSON was a safe drop-in replacement.

The bigger gap was false negatives. The tools did not catch the logic bugs: an invalid
status like "teleported" being accepted, unknown dishes silently costing 99, and an empty
order with no customer being created and marked delivered. I only found these by running
the program and reading the output.

## 3. How would you integrate static analysis tools into your software development workflow?

- Run Flake8 and Pylint automatically in the editor and as a pre-commit hook, so style and
  quality issues are caught before code is committed.
- Add Pylint, Flake8 and Bandit to a CI pipeline (e.g. GitHub Actions) on every push and pull
  request, failing the build on Bandit findings of medium severity or higher, or if the
  Pylint score drops below a threshold such as 9.5.
- Keep a shared configuration file (`.pylintrc`, `.flake8`) so the whole team uses the same rules.

## 4. What tangible improvements did you observe in code quality, readability and robustness after the fixes?

- **Security:** the unsafe `pickle` deserialization was replaced with JSON, so Bandit went
  from 1 Medium and 2 Low issues to none.
- **Robustness:** errors are no longer silently swallowed. Updating a missing order prints
  "Order 42 not found", and invalid statuses, unknown dishes and empty orders are rejected
  with clear messages. Files are always closed using `with`.
- **Readability and maintainability:** docstrings, snake_case names, f-strings and PEP 8
  formatting make the code easier to read. Pylint improved from 6.27/10 to 10.00/10 and
  Flake8 went from 12 issues to 0.
- **Correctness:** revenue and order totals can now be trusted, because bad input is rejected
  instead of producing wrong values like the 249 total for an order containing "sushi".