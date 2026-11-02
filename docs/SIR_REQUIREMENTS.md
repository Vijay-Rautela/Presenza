# What Sir Requires: BBAT104 TQM Project Checklist

Built from the Course Project Guidelines (Session 2026-27) and the Project Synopsis or Report Template (2026-27). Tick each item only when it is really done.

## 1. Basics

- Course: BBAT104 Fundamentals of TQM. Max assessment: 70 raw marks.
- Baseline system from last digit of roll number. Digit 0: Attendance Management System. Goal: automate tracking and minimize proxy entries.
- One assigned Quality Goal (Q01 to Q20), see `quality-goals.md`. Implement any 5 of its suggested features.
- Public GitHub repository named `BBAT104_TQM_[RegNo]`, with an initial README.md that has project details.
- Tools named by sir: VS Code, GitHub account, GitHub Desktop, and Python with Tkinter or CustomTkinter, SQLite3 or Pandas, and Matplotlib or Seaborn. 
- Presenza implements Python 3 (Flask REST API) with SQLite3 and Matplotlib/Pandas for the core data engine and SQC artifacts, paired with a React (Vite) web interface for modern responsive usability. Charts and defect metrics are completely reproducible from real data.

## 2. Marking scheme (70 marks)

| Milestone | Marks | COs | What must be shown |
|---|---|---|---|
| Review 1: Setup and SRS | 10 | CO1 | GitHub repo started, System Architecture Flowchart, SRS document, scope definition |
| Review 2: Base system and CRUD | 15 | CO1, CO2 | Base CRUD modules working plus the 5 quality goal features |
| Review 3: FMEA and risk audit | 15 | CO2 | FMEA matrix with RPN scores, SIPOC process map, CTQ tree, defect logging |
| Review 4: SQC and continuous improvement | 15 | CO2, CO3 | Pareto chart (80/20), Fishbone diagram, checksheets, PDCA cycle log |
| Final demo and viva | 10 | CO3 | Live software demo, bug-handling defense, oral viva on TQM tool selection |
| Documentation and GitHub health | 5 | CO3 | Comprehensive README.md, user manual, at least 30 meaningful commits, GitHub Issues |

## 3. Core TQM principles that must be visible

- Customer Focus: features that solve real pain points of teachers, students, admin.
- Continuous Improvement (Kaizen): improve through PDCA cycles.
- Process-Centric Approach: SIPOC diagrams of inputs and outputs.
- Fact-Based Decision Making: bug fixes chosen using real defect metrics.
- Error Prevention (Poka-Yoke): strict input validation, field masks, dropdowns.

## 4. SQC tools that must be produced

- Pareto analysis (80/20): defect frequencies, vital few causes.
- Ishikawa (Fishbone) diagram: categories People, Process, Software Code, Infrastructure.
- Checksheets and defect logs: occurrence, severity, resolution status.
- FMEA matrix: RPN = Severity x Occurrence x Detection, with mitigation steps.
- Also required: System Architecture Flowchart, SRS, CTQ tree, SIPOC, PDCA log.

## 5. Step-by-step process sir expects

1. Environment setup and repository initialization.
2. Requirement analysis and SRS: identify baseline system, architecture flowchart, CTQ parameters, SRS.
3. Base system and CRUD (Create, Read, Update, Delete) with database storage.
4. Integrate the 5 assigned quality goal features.
5. Process mapping and risk audit: SIPOC, then FMEA with failure modes, RPN, mitigation.
6. SQC and continuous improvement: log bugs on a checksheet, generate Pareto and Fishbone, run one PDCA cycle.
7. GitHub sync and documentation: at least 30 commits, README with architecture diagram, user manual, setup instructions.
8. Final submission and viva: repository link, live demo, defend choice of TQM tools.

## 6. What gets the Excellent band (80 to 100 percent)

- System and CRUD: all modules fully functional, robust architecture, zero breaking errors.
- FMEA: accurate RPN calculations, logical Severity and Occurrence ratings, actionable mitigation plan.
- SQC and PDCA: flawless Pareto and Fishbone, clear data checksheets, verified PDCA log.
- Viva and GitHub: confident defense, 30 or more commits, interactive README with screenshots and manual.
- Lower bands: 20 to 29 commits is Good, 10 to 19 is Satisfactory, under 10 is Needs Work. A default or missing README is the lowest band.

## 7. Project report structure (from the template)

Use the college template exactly. Title in passive voice. Cover and title page with "BBAT104: TQM PROJECT", Amrapali Institute of Technology and Sciences, Haldwani (Uttarakhand), December 2026.

Front matter, in this order:
- Title page, second title page with supervisor and moderator names, Certificate, Abstract, Acknowledgement, Contents, List of Figures, List of Tables.
- Abstract fields: university roll number, student name, project carried at, guide name, guide's email, dissertation title, abstract text, broad academic area (Total Quality Management), keywords, signatures and date.

Chapters:
1. Introduction: background of the problem, organization or system overview, problem statement, need for the project, objectives, scope, expected outcomes.
2. Review of Literature: TQM, quality in the selected industry, customer satisfaction and requirements, relevant quality tools, existing systems or previous studies, project gap.
3. Materials and Method: project methodology, data collection, customer requirements, process mapping and flowchart, SIPOC, voice of customer, CTQ requirements, quality tools used, software and system design (SRS, DFD, ER diagram, database design, system architecture, user interface design).
4. Results and Discussions: existing process analysis, problems found, root cause analysis, improved process, system developed, functional results, quality improvement results, KPIs, user feedback, before versus after, discussion.
5. Conclusion: objectives achieved, quality improvement, limitations, future scope.

Back matter:
- References in this order: 1) books, 2) research papers, 3) conference papers, 4) dissertations, 5) articles on government websites. Use the template's format (authors, title, publisher or journal, place, date, page numbers).
- Abbreviations table: replace the template's Taguchi and ANOVA terms with this project's terms (for example TQM, SRS, CTQ, SIPOC, FMEA, RPN, PDCA, SQC, CRUD, JWT, API).
- Appendix I.

## 8. Things I must not do

- Do not invent defect data, test results, user feedback, or references. Every chart and score comes from real logs.
- Do not copy FMEA or other artefacts from someone else. Copied or irrelevant FMEA lands in the lowest band.
- Do not leave the default README.

## 9. Final submission check

- [ ] Repo public and named `BBAT104_TQM_[RegNo]`
- [ ] README with description, setup steps, architecture diagram, screenshots, user manual link
- [ ] At least 30 meaningful commits and GitHub Issues (open and closed)
- [ ] Base CRUD working without breaking errors
- [ ] 5 quality goal features working and demo-ready
- [ ] SRS, architecture flowchart, CTQ tree, SIPOC
- [ ] FMEA with correct RPN and mitigation
- [ ] Defect log and checksheet with real entries
- [ ] Pareto chart and Fishbone diagram from real data
- [ ] PDCA log with at least one full cycle
- [ ] User manual for Admin, Teacher, Student
- [ ] Report written in the college template
- [ ] Viva prepared on why each TQM tool was used
