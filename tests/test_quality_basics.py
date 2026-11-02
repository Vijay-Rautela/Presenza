"""Focused tests for Phase 7 validation and password-quality features."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from services.import_service import _normalise_value
from services.report_service import export_csv
from utils.security import hash_password, verify_password
from utils.validators import validate_date_of_birth, validate_password


class PasswordSecurityTests(unittest.TestCase):
    def test_hash_is_not_plain_text_and_verifies(self):
        password_hash = hash_password("Secure123")
        self.assertNotEqual(password_hash, "Secure123")
        self.assertTrue(verify_password("Secure123", password_hash))
        self.assertFalse(verify_password("Wrong123", password_hash))

    def test_password_validation_rejects_weak_passwords(self):
        self.assertIsNotNone(validate_password("short1", "short1"))
        self.assertIsNotNone(validate_password("abcdefgh", "abcdefgh"))
        self.assertIsNotNone(validate_password("12345678", "12345678"))
        self.assertIsNone(validate_password("Secure123", "Secure123"))


class InputValidationTests(unittest.TestCase):
    def test_date_of_birth_requires_standard_date(self):
        self.assertTrue(validate_date_of_birth("2004-08-15"))
        self.assertFalse(validate_date_of_birth("15/08/2004"))
        self.assertFalse(validate_date_of_birth("not-a-date"))

    def test_import_normalises_semester_and_date_of_birth(self):
        import pandas as pd

        self.assertEqual(_normalise_value(5.0, "semester", pd), "5")
        self.assertEqual(_normalise_value(pd.Timestamp("2004-08-15"), "dob", pd), "2004-08-15")


class ReportExportTests(unittest.TestCase):
    def test_csv_formula_values_are_escaped(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "report.csv"
            export_csv([{"name": "=SUM(A1:A2)", "percentage": 75}], str(output))
            self.assertIn("'=SUM(A1:A2)", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
