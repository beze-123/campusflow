import unittest

from campusflow.validation import (
    validate_affected_users,
    validate_category,
)


class TestValidation(unittest.TestCase):

    def test_valid_category_is_normalized(self):
        self.assertEqual(
            validate_category("nEtWoRk"),
            "Network"
        )

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_negative_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-2)

    def test_float_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(2.5)

    def test_boolean_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(True)


if __name__ == "__main__":
    unittest.main()