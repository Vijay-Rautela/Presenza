# CTQ Tree: Presenza Attendance Management

## Customer need

**Reliable, fast, and accountable attendance management.**

```text
Reliable attendance management
├── Accurate attendance data
│   ├── One record per student / subject / date
│   ├── Only assigned teacher can mark a class
│   ├── No future-date attendance
│   └── Corrections have a mandatory reason and audit log
├── Useful visibility
│   ├── Student sees own percentage and records
│   ├── Teacher sees only assigned classes
│   ├── Admin sees system dashboard and defaulters
│   └── Reports can be exported to CSV
├── Safe and recoverable system
│   ├── Passwords are PBKDF2 hashed
│   ├── Portals and services apply role controls
│   ├── User-friendly validation messages are shown
│   └── Admin can create timestamped database backups
└── Continuous improvement evidence
    ├── Test checksheet and defect log capture real results
    ├── Pareto chart uses logged defect frequencies
    └── PDCA log records verified changes
```

## CTQ measures

| CTQ | Measure | Target | Evidence source |
|---|---|---|---|
| Duplicate prevention | Duplicate attendance saved | 0 | Test checksheet / database constraint |
| Proxy prevention | Unauthorized teacher saves attendance | 0 | Test checksheet |
| Traceability | Corrections with audit log | 100% | `attendance_logs` |
| Report availability | Requested report/export completes | Functional | Manual test record |
| Recoverability | Backup created when requested | Functional | Backup file / test record |
