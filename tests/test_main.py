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
	def test_search_reprompts_invalid_filters_and_displays_matching_ticket(self):
		with tempfile.TemporaryDirectory() as directory:
			storage = TicketStorage(Path(directory) / "tickets.json")
			storage.save([create_ticket("T001", "Wi-Fi outage", "Network", "low", 1)])
			output = io.StringIO()
			with patch(
				"builtins.input",
				side_effect=["9", "wi-fi", "Invalid", "Network", "open", "urgent", "low", "14"],
			):
				with redirect_stdout(output):
					interactive_menu(storage)

		self.assertIn("Invalid category.", output.getvalue())
		self.assertIn("Priority must be critical", output.getvalue())
		self.assertIn("T001", output.getvalue())
		self.assertIn("Wi-Fi outage", output.getvalue())

	def test_add_and_view_note_through_menu(self):
		with tempfile.TemporaryDirectory() as directory:
			storage = TicketStorage(Path(directory) / "tickets.json")
			storage.save([create_ticket("T001", "Wi-Fi outage", "Network", "low", 1)])
			output = io.StringIO()
			with patch(
				"builtins.input",
				side_effect=[
					"11",
					"T001",
					"Mentor A",
					"Wi-Fi router reboot attempted",
					"12",
					"T001",
					"14",
				],
			):
				with redirect_stdout(output):
					interactive_menu(storage)
			self.assertEqual(storage.load()[0]["notes"][0]["note_id"], "N001")
			self.assertIn(
				"N001 | Mentor A | Wi-Fi router reboot attempted", output.getvalue()
			)

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
				"",
				"",
				"",
				"",
				"14",
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
				 side_effect=["5", "T001", "in_progress", "8", "14"],
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
