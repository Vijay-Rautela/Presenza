# FMEA: Presenza Attendance Management

Scores use 1 (low) to 10 (high). RPN = Severity × Occurrence × Detection. These are **pre-release risk-assessment scores**, not measured defect frequencies. Reassess them after real test evidence is collected.

| Process step | Failure mode | Effect | Cause | Existing control | S | O | D | RPN | Recommended action |
|---|---|---|---|---|---:|---:|---:|---:|---|
| Teacher marks attendance | Duplicate record saved | Wrong percentage/report | Double submission | Database unique constraint and service check | 8 | 3 | 2 | 48 | Run duplicate-save test and log outcome. |
| Teacher marks attendance | Unauthorized class marked | Proxy/incorrect class data | Wrong assignment access | Assignment ownership check in service | 9 | 3 | 3 | 81 | Test with a second teacher account. |
| Teacher marks attendance | Future date used | False attendance data | Manual date entry | Future-date validation | 7 | 3 | 2 | 42 | Test one future-date rejection. |
| Teacher corrects record | Change lacks traceability | Cannot explain data change | Missing reason/log | Mandatory reason and audit log | 8 | 2 | 2 | 32 | Verify log after a real correction test. |
| Student account access | Password exposed | Account misuse | Plain-text storage | PBKDF2 hashing | 10 | 2 | 3 | 60 | Verify stored value is hash, not password. |
| Reporting | Teacher sees another class | Privacy breach | Missing report scope | Assignment-scoped report query | 9 | 3 | 3 | 81 | Test report scope with two teachers. |
| Database storage | Data unavailable after local issue | Loss of attendance history | Hardware/app failure | Admin timestamped backup | 9 | 4 | 4 | 144 | Highest planned risk: create and verify a backup before review. |

## Priority

The highest pre-release RPN is database recovery (144), followed by unauthorized class marking and report-scope leakage (81 each). These should receive early real test evidence in the checksheet.
