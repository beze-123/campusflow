from campusflow.ticket import PRIORITIES, normalize_category, normalize_status
from campusflow.validation import validate_ticket_id


_PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def search_tickets(tickets, title="", category=None, status=None, priority=None):
	if not isinstance(title, str):
		raise ValueError("Title search must be text.")

	title_filter = title.strip().casefold()
	category_filter = None
	if category is not None and (not isinstance(category, str) or category.strip()):
		category_filter = normalize_category(category)
	status_filter = None
	if status is not None and (not isinstance(status, str) or status.strip()):
		status_filter = normalize_status(status)
	priority_filter = None
	if priority is not None and (not isinstance(priority, str) or priority.strip()):
		if not isinstance(priority, str):
			raise ValueError("Priority must be critical, high, medium, or low.")
		priority_filter = priority.strip().casefold()
	if priority_filter is not None and priority_filter not in PRIORITIES:
		raise ValueError("Priority must be critical, high, medium, or low.")

	return [
		ticket
		for ticket in tickets
		if title_filter in ticket["title"].casefold()
		and (category_filter is None or ticket["category"] == category_filter)
		and (status_filter is None or ticket["status"] == status_filter)
		and (priority_filter is None or ticket["priority"] == priority_filter)
	]


def sort_search_results(tickets):
	def sort_key(ticket):
		priority = ticket["priority"]
		if priority not in _PRIORITY_ORDER:
			raise ValueError(f"Ticket {ticket['id']} has an invalid priority.")
		ticket_id = validate_ticket_id(ticket["id"])
		return _PRIORITY_ORDER[priority], int(ticket_id[1:])

	return sorted(tickets, key=sort_key)
