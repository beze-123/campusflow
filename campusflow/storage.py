import json
import os
import tempfile
from pathlib import Path

from campusflow.ticket import validate_ticket_data


class StorageError(Exception):
	"""Raised when the ticket file cannot be read or written safely."""


def _validate_collection(data):
	if not isinstance(data, list):
		raise ValueError("The ticket file must contain a JSON list.")

	tickets = [validate_ticket_data(ticket) for ticket in data]
	ids = [ticket["id"] for ticket in tickets]
	if len(ids) != len(set(ids)):
		raise ValueError("The ticket file contains duplicate IDs.")
	return tickets


class TicketStorage:
	def __init__(self, path="tickets.json"):
		self.path = Path(path)

	def load(self) -> list[dict]:
		if not self.path.exists():
			return []
		try:
			with self.path.open(encoding="utf-8") as file:
				data = json.load(file)
			return _validate_collection(data)
		except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
			raise StorageError(f"Could not read {self.path}: {error}") from error

	def save(self, tickets: list[dict]) -> None:
		temporary_path = None
		try:
			validated_tickets = _validate_collection(tickets)
			self.path.parent.mkdir(parents=True, exist_ok=True)
			with tempfile.NamedTemporaryFile(
				mode="w",
				encoding="utf-8",
				dir=self.path.parent,
				prefix=f".{self.path.name}.",
				suffix=".tmp",
				delete=False,
			) as file:
				temporary_path = Path(file.name)
				json.dump(validated_tickets, file, indent=2)
				file.write("\n")

			os.replace(temporary_path, self.path)
			
		except (OSError, TypeError, ValueError) as error:
			raise StorageError(f"Could not write {self.path}: {error}") from error
		finally:
			if temporary_path is not None and temporary_path.exists():
				temporary_path.unlink()
