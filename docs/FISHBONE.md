# Fishbone Analysis: Incorrect or Unreliable Attendance Data

This is the root-cause framework for Presenza. After real defect logs exist, highlight only causes supported by the recorded evidence.

```text
People ───────────────┐  Teacher chooses wrong status; user skips activation instructions
Process ──────────────┤  Late correction; incomplete class register; unclear leave workflow
Software code ────────┼──────────────► Incorrect or unreliable attendance data
Infrastructure ───────┤  Missing Python environment; local device failure; missing backup
Data ─────────────────┤  Duplicate import; incorrect DOB; wrong assignment mapping
Measurement ──────────┘  No real test log; report interpreted without correct filters
```

## Existing preventive controls

| Cause area | Presenza control |
|---|---|
| People / Process | Friendly messages, simple role portals, mandatory correction reason |
| Software code | Parameterized SQL, unique attendance constraint, service-level role checks |
| Infrastructure | Timestamped Admin backup and error log |
| Data | CSV column validation, duplicate checks, account activation DOB verification |
| Measurement | Defect checksheet, report exports, and Pareto generator based on actual log data |
