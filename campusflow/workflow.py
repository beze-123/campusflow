from campusflow.ticket import normalize_status


def _find_ticket(tickets: list[dict], ticket_id: str) -> dict:
	if not isinstance(ticket_id, str) or not ticket_id.strip():
		raise ValueError("Ticket ID must not be blank.")
	normalized_id = ticket_id.strip().casefold()
	for ticket in tickets:
		if ticket["id"].casefold() == normalized_id:
			return ticket
	raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_ticket(tickets: list[dict], ticket_id: str, assignee: str) -> dict:
	ticket = _find_ticket(tickets, ticket_id)
	if not isinstance(assignee, str) or not assignee.strip():
		raise ValueError("Assignee name must not be blank.")
	if ticket["status"] == "closed":
		raise ValueError("Closed tickets must be reopened before they can be changed.")

	ticket["assigned_to"] = assignee.strip()
	return ticket


def update_ticket_status(tickets: list[dict], ticket_id: str, status: str) -> dict:
	ticket = _find_ticket(tickets, ticket_id)
	new_status = normalize_status(status)
	current_status = ticket["status"]

	if new_status == "open":
		raise ValueError("Use the reopen action to move a closed ticket to open.")
	next_status = {"open": "in_progress", "in_progress": "closed"}.get(
		current_status
	)
	if new_status != next_status:
		raise ValueError(
			f"Cannot move ticket from {current_status} to {new_status}."
		)
	if current_status == "open" and not ticket["assigned_to"]:
		raise ValueError("Assign the ticket before moving it to in_progress.")

	ticket["status"] = new_status
	return ticket


def reopen_ticket(tickets: list[dict], ticket_id: str) -> dict:
	ticket = _find_ticket(tickets, ticket_id)
	if ticket["status"] != "closed":
		raise ValueError("Only closed tickets can be reopened.")

	ticket["status"] = "open"
	return ticket


def get_work_queue(tickets: list[dict]) -> list[dict]:
	priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
	open_tickets = [
		ticket for ticket in tickets if ticket["status"] in {"open", "in_progress"}
	]

	def sort_key(ticket: dict) -> tuple[int, int]:
		priority = ticket["priority"]
		if priority not in priority_order:
			raise ValueError(f"Ticket {ticket['id']} has an invalid priority.")
		ticket_id = ticket["id"]
		if (
			not isinstance(ticket_id, str)
			or not ticket_id.startswith("T")
			or not ticket_id[1:].isdigit()
		):
			raise ValueError(f"Ticket ID {ticket_id!r} is not in T<number> format.")
		return priority_order[priority], int(ticket_id[1:])

	return sorted(open_tickets, key=sort_key)
