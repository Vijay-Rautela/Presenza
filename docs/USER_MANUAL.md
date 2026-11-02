# Presenza User Manual

## Start the application

1. Install the dependencies with `py -m pip install -r requirements.txt`.
2. Start the program with `py main.py`.
3. On the first run, the database and starter data are created automatically.

## Admin guide

1. Sign in with `admin` and `Admin@123`.
2. Replace the default password when prompted.
3. Use **Students**, **Teachers**, **Courses**, and **Subjects** to maintain master data.
4. Use **Assignments** to connect each teacher with subject, semester, and section.
5. Use **Import** for the provided CSV templates or a matching Excel file.
6. Use **Reset selected account** when a Teacher or Student must activate again.
7. Use **Settings** to change the minimum attendance percentage.
8. Use **Reports** for all-system report views and CSV export.
9. Use **Backup** to create a timestamped database copy.

## Teacher guide

1. Activate your account first from the login screen using your employee ID and date of birth.
2. Sign in and open **Mark attendance**.
3. Select one assigned class/subject, choose a date, and click **Load class**.
4. Keep students as Present or change them to Absent/Late, then click **Save attendance**.
5. Use **Corrections** only for valid changes. Enter a reason before saving; the system creates an audit record.
6. Use **Leave requests** to approve or reject requests only from your assigned classes.
7. Use **Reports** to view or export your own class data.

## Student guide

1. Activate your account from the login screen using your roll number and date of birth.
2. Sign in to view the overall percentage and subject-wise attendance on the dashboard.
3. Open **My records** for date-wise attendance.
4. Open **Apply for leave**, enter valid dates and a reason, then submit.
5. The leave status table shows Pending, Approved, or Rejected requests.

## Validation messages

- Use dates as `YYYY-MM-DD`.
- Passwords need at least eight characters, one letter, and one number.
- Attendance cannot be saved for future dates or duplicated for the same student, subject, and date.
- Attendance corrections need a reason and must be inside the configured edit period.
- Leave request dates cannot be reversed or overlap another pending request.

## Recovery

If the application closes unexpectedly, check `logs/presenza.log`. An Admin can restore data manually by replacing a damaged database with a known-good copy from the `backups/` folder while the app is closed.
