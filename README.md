# PES1UG24CS310_SE_LAB_SUBMISSIONS

Software Engineering lab submissions.

| | |
|---|---|
| **Name** | Omkar |
| **SRN** | PES1UG24CS310 |
| **Semester / Section** | V / 5F |
| **Course** | Software Engineering |

Labs 1 to 3 use one running case study, **Problem Statement #05: Academic Elective Bidding & Allocation System**. Lab 4 is a separate Python game project. Labs 5, 6 and 7 each work on a separate assigned Python program.

## Repository Structure

```
PES1UG24CS310_SE_LAB_SUBMISSIONS/
├── Lab 1: Requirements Engineering & UML Use-Case Modelling/
├── Lab 2: Jira hands on – Agile Backlog Creation & Sprint Simulations/
├── Lab 3: Component Modelling & Architectural Pattern Selection/
├── Lab 4: VibeCoding/
├── Lab 5: Static Code Analysis/
├── Lab 6: Code & Branch Coverage Analysis/
├── Lab 7: Fuzzing for Input Validation Bugs/
└── README.md
```

## Lab Summaries

### Lab 1: Requirements Engineering & UML Use-Case Modelling
Captures the requirements for the Academic Elective Bidding & Allocation System. Actors are the Student, Academic Registrar and System Administrator.

- `Requirements_Table.docx`: functional and non-functional requirements (FR-001 to FR-005, NFR-001, NFR-002), each with priority, acceptance criteria and rationale
- `UseCase_Diagram.pdf`: UML use-case diagram
- `UseCase_Flow.pdf`: use-case flow description

### Lab 2: Jira Hands-on, Agile Backlog Creation & Sprint Simulations
Agile planning for the same system in Jira (project: *Elective-Bidding*).

- `PES1UG24CS310_OMKAR_LAB2.pdf`: sprint reflection report
- Screenshots: backlog with Epics and User Stories, story point assignments, active sprint board, burndown chart

### Lab 3: Component Modelling & Architectural Pattern Selection
Selects an architecture for the system and justifies it.

- `PES1UG24CS310_Component_Diagram.pdf`: component diagram
- `PES1UG24CS310_Architectural_Justification.docx`: justification for choosing a **Layered Architecture** (Presentation, Business and Data layers). It covers separation of concerns, a deployment model suited to short bidding windows, security (all requests pass through the Business layer) and performance (in-process calls support the 30-second allocation target in NFR-001).

### Lab 4: VibeCoding
Used ChatGPT to fix a bug in a Pygame **Balloon Pop** game and add new features through prompting.

- **Bug fixed:** click detection compared squared distance to an unsquared radius, so only clicks near a balloon's center registered
- **Features added:** balloon types (normal, bonus, penalty), a 3-lives system, a 30-second timed round, and a Game Over screen with restart
- `balloon-pop/`: updated source code
- `Recording_before.mp4` and `Recording_after.mp4`: gameplay before and after the changes
- `Chat history.pdf`: full ChatGPT conversation
- `README.md`: setup instructions and details for the game

To run the game:

```bash
cd "Lab 4: VibeCoding/balloon-pop"
pip install -r requirements.txt
python main.py
```
### Lab 5: Static Code Analysis
Used **Pylint**, **Bandit** and **Flake8** to find and fix quality, security and style issues in a **Food Delivery Order Queue Manager** script (assigned repo: `L5_05_food_delivery`).

- **Security fixed:** replaced unsafe `pickle` backup/restore with JSON (Bandit B301/B403) and removed a silent `try/except/pass` (B110)
- **Quality fixed:** mutable default argument, broad and bare `except`, files opened without `with`, `global` statements, naming and missing docstrings
- **Logic bugs found by running the program:** invalid statuses such as "teleported" were accepted, unknown dishes silently cost 99, and empty orders were created and marked delivered
- **Results:** Pylint 6.27 → **10.00/10**, Flake8 12 → **0** issues, Bandit 1 Medium + 2 Low → **0**
- `delivery_system.py`: cleaned source code
- `issues.md`: table of the 14 issues found and how each was fixed
- `*_report_before.txt` and `*_report.txt`: tool reports before and after the fixes

To run the program and the tools:

````bash
cd "Lab 5: Static Code Analysis"
pip install pylint bandit flake8
python delivery_system.py
pylint delivery_system.py
````

### Lab 6: Code & Branch Coverage Analysis
Used **coverage.py** with **pytest** to measure and improve test coverage for a **Blood Donation Screening** module (assigned repo: `L6_L7_05_blood_donation_screening`). The module screens donor cohorts by age, weight and hemoglobin, and checks centrifuge runs for RPM drops.

- **Starting point:** the single starter test reached 47% line and 43% branch coverage, and never called `verify_storage_centrifuge`
- **Line vs. branch:** the code coverage tests run every line (100%) but still miss one branch, `26->15`: a low-hemoglobin donor in a *standard* cohort, where screening carries on instead of stopping. The branch coverage tests add this case along with boundary values (age 17, weight 50 kg, Hb 12.5 and 18.0, 3000 rpm, exactly 4 deferrals), empty donor lists, empty centrifuge runs and missing dictionary keys
- **Results:** line coverage 47% → **100%** (11 tests); branch coverage 43% → **100%**, 32/32 branches (38 tests)
- **Observation:** a low-hemoglobin donor in a `high_altitude` cohort resets the *running* total to 0, which also discards what earlier cohorts collected. A test records this behaviour
- `blood_donation_screening.py`: module under test (unchanged)
- `test_blood_donation.py`: starter test from the assigned repo
- `CodeCoverageTest_PES1UG24CS310_application.py`: line coverage tests
- `BranchCoverageTest_PES1UG24CS310_application.py`: branch coverage tests
- `code_coverage.png` and `branch_coverage.png`: terminal screenshots of the coverage reports

To run the tests and reports:

````bash
cd "Lab 6: Code & Branch Coverage Analysis"
pip install coverage pytest
coverage run -m pytest CodeCoverageTest_PES1UG24CS310_application.py
coverage report -m
coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS310_application.py
coverage report -m
````
### Lab 7: Fuzzing for Input Validation Bugs
Used **Hypothesis** property-based fuzzing with **pytest** to find and fix input validation bugs in a **Blood Donation Screening** processor (assigned repo: `L6_L7_05_blood_donation_screening`). The module validates ABO/Rh blood codes, calculates pulse pressure from a BP string and parses pipe-delimited donor records.

- **Bugs found by fuzzing:** each of the 3 functions crashed on 3 distinct inputs, 9 in total. The crashes came from `None` (AttributeError), empty strings (IndexError / ValueError) and malformed input such as `'0'`, `'/'` and `'|'` (KeyError / ValueError)
- **Other issues fixed while hardening:** `'XYZ+'` was accepted as a blood group, `'120/0'` raised ZeroDivisionError and huge numbers raised OverflowError. A diastolic higher than systolic gave a negative pulse pressure, and `'inf'` for weight and hemoglobin marked a donor Eligible. NaN values, negative weights, empty donor IDs and extra fields were also accepted
- **Results:** 3 failed → **3 passed**. Every function now returns an "Invalid input" message instead of raising an exception
- `processor.py`: fixed script
- `test_processor.py`: completed Hypothesis tests (`st.text() | st.none()`, with try/except for each function)
- `PES1UG24CS310_Lab7_FuzzTesting.pdf`: screenshots of each step

To run the program and the tests:

````bash
cd "Lab 7: Fuzzing for Input Validation Bugs"
pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py
````
## Notes

- The Lab 4 commit history was imported from its original repository, so the individual commits for the fix and each feature are preserved in this repo's log.
- No pull requests were raised to the course's main repository.
