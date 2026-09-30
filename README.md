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

## Notes

- The Lab 4 commit history was imported from its original repository, so the individual commits for the fix and each feature are preserved in this repo's log.
- No pull requests were raised to the course's main repository.
