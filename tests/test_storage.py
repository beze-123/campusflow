import json
import tempfile
import unittest
from pathlib import Path

from campusflow.notes import add_note
from campusflow.storage import StorageError, TicketStorage
from campusflow.ticket import create_ticket
from main import next_ticket_id


class StorageTests(unittest.TestCase):
	def test_round_trip_preserves_notes_and_next_ids(self):
		with tempfile.TemporaryDirectory() as directory:
			storage = TicketStorage(Path(directory) / "tickets.json")
			ticket = create_ticket("T001", "Wi-Fi issue", "Network", "high", 1)
			add_note([ticket], "T001", "Mentor", "Router reboot tried")
			storage.save([ticket])

			loaded = storage.load()
			self.assertEqual(loaded[0]["notes"][0]["note_id"], "N001")
			self.assertEqual(next_ticket_id(loaded), "T002")
			self.assertEqual(
				add_note(loaded, "T001", "Mentor", "Switch ports checked")["note_id"],
				"N002",
			)

	def test_legacy_ticket_without_notes_loads_with_empty_notes(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "tickets.json"
			ticket = create_ticket("T001", "Legacy issue", "Other", "low", 1)
			del ticket["notes"]
			path.write_text(json.dumps([ticket]), encoding="utf-8")

			self.assertEqual(TicketStorage(path).load()[0]["notes"], [])

	def test_invalid_json_is_rejected_without_changing_existing_records(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "tickets.json"
			path.write_text("{broken", encoding="utf-8")
			current_tickets = [create_ticket("T010", "Current", "Other", "low", 1)]
			original = [ticket.copy() for ticket in current_tickets]

			with self.assertRaises(StorageError):
				TicketStorage(path).load()

			self.assertEqual(current_tickets, original)

	def test_duplicate_ticket_ids_are_rejected(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "tickets.json"
			ticket = create_ticket("T001", "Issue", "Other", "low", 1)
			path.write_text(json.dumps([ticket, ticket]), encoding="utf-8")

			with self.assertRaisesRegex(StorageError, "duplicate IDs"):
				TicketStorage(path).load()

	def test_invalid_save_does_not_replace_existing_file(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "tickets.json"
			storage = TicketStorage(path)
			valid_ticket = create_ticket("T001", "Valid", "Other", "low", 1)
			storage.save([valid_ticket])
			original_contents = path.read_text(encoding="utf-8")
			invalid_ticket = create_ticket("T002", "Invalid", "Other", "low", 1)
			invalid_ticket["notes"] = [{"note_id": "N001", "author": " ", "message": "bad"}]

			with self.assertRaises(StorageError):
				storage.save([invalid_ticket])

			self.assertEqual(path.read_text(encoding="utf-8"), original_contents)


if __name__ == "__main__":
	unittest.main()
