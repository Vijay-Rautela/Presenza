# PDCA Log: Presenza

Use this log only when the stated test evidence is available. The first row is a planned cycle, not a claimed completed result.

| Cycle | Plan | Do | Check evidence | Act decision | Status |
|---|---|---|---|---|---|
| 1 | Verify that future-date attendance cannot be saved, because it would reduce data accuracy. | Run the future-date case using a real Teacher account after Python setup. | Add the exact result to `DEFECT_CHECKSHEET.csv`. | If it fails, fix validation and rerun; if it passes, retain the current control. | Pending real test |
| 2 | Verify that an Admin backup produces a restorable database copy. | Create backup from the Admin portal and inspect the generated file. | Record file name, time, and restore check in the checksheet. | Improve instructions or code only from real result. | Pending real test |
| 3 | Verify core validation and safe data handling before live portal testing. | Run `py -m unittest discover -s tests -v`. | Five tests passed on 2026-10-25: password hash verification, password strength/DOB validation, import normalisation, and CSV formula protection. | Retain the controls; record future live-screen tests separately. | Complete |

## Completed-cycle rule

Change a row to Complete only after the test result, action, and verification are recorded. This prevents made-up PDCA evidence.
