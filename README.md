# PES1UG24CS310_SE_LAB_SUBMISSIONS

Software Engineering lab submissions.

| | |
|---|---|
| **Name** | Omkar |
| **SRN** | PES1UG24CS310 |
| **Semester / Section** | V / 5F |
| **Course** | Software Engineering |

Labs 1 to 3 use one running case study, **Problem Statement #05: Academic Elective Bidding & Allocation System**. Lab 4 is a separate Python game project.

## Repository Structure

```
PES1UG24CS310_SE_LAB_SUBMISSIONS/
├── Lab 1: Requirements Engineering & UML Use-Case Modelling/
├── Lab 2: Jira hands on – Agile Backlog Creation & Sprint Simulations/
├── Lab 3: Component Modelling & Architectural Pattern Selection/
├── Lab 4: VibeCoding/
├── Lab 5: Static Code Analysis/
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

The intro line near the top says *"Lab 4 is a separate Python game project."* If you want Lab 5 mentioned there too, change it to *"Lab 4 is a separate Python game project, and Lab 5 is a static code analysis exercise."* This is optional.

Then commit from the repo's root folder in the Codespace:

````bash
cd /workspaces/PES1UG24CS310_SE_LAB_SUBMISSIONS
git add README.md
git commit -m "Add Lab 5 to README"
git push
````

## Notes

- The Lab 4 commit history was imported from its original repository, so the individual commits for the fix and each feature are preserved in this repo's log.
- No pull requests were raised to the course's main repository.
