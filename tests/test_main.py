import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from campusflow.storage import TicketStorage
from campusflow.ticket import create_ticket
from main import interactive_menu


class MenuTests(unittest.TestCase):
	def test_menu_integrates_ticket_lifecycle_reporting_and_persistence(self):
		with tempfile.TemporaryDirectory() as directory:
			storage = TicketStorage(Path(directory) / "tickets.json")
			user_inputs = [
				"1",
				"Wi-Fi outage",
				"Network",
				"high",
				"12",
				"4",
				"T001",
				"Alex",
				"5",
				"T001",
				"in_progress",
				"8",
				"5",
				"T001",
				"resolved",
				"6",
				"T001",
				"9",
			]
			output = io.StringIO()
			with patch("builtins.input", side_effect=user_inputs):
				with redirect_stdout(output):
					interactive_menu(storage)

			ticket = storage.load()[0]
			self.assertEqual(ticket["status"], "open")
			self.assertEqual(ticket["assigned_to"], "Alex")
			self.assertIn("Total tickets: 1", output.getvalue())
			self.assertIn("in_progress: 1", output.getvalue())
			self.assertIn("has been reopened", output.getvalue())

	def test_invalid_transition_is_reported_without_saving_a_change(self):
		with tempfile.TemporaryDirectory() as directory:
			storage = TicketStorage(Path(directory) / "tickets.json")
			storage.save(
				[create_ticket("T001", "Unassigned issue", "Other", "low", 1)]
			)
			output = io.StringIO()
			with patch(
				"builtins.input",
				side_effect=["5", "T001", "in_progress", "8", "9"],
			):
				with redirect_stdout(output):
					interactive_menu(storage)

			ticket = storage.load()[0]
			self.assertEqual(ticket["status"], "open")
			self.assertIsNone(ticket["assigned_to"])
			self.assertIn("Error: Assign the ticket", output.getvalue())
			self.assertIn("open: 1", output.getvalue())


if __name__ == "__main__":
	unittest.main()
