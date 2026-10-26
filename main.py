from campusflow.storage import (StorageError, TicketStorage)
from campusflow.search import search_tickets, sort_search_results
from campusflow.notes import add_note, get_ticket_notes
from campusflow.understanding_check import run_understanding_check


from campusflow.report import format_report
from campusflow.ticket import (
	CATEGORIES,
	PRIORITIES,
	create_ticket,
	normalize_category,
	normalize_status,
	normalize_urgency,
	validate_affected_users,
)
from campusflow.workflow import (
	assign_ticket,
	get_work_queue,
	reopen_ticket,
	update_ticket_status,
)


def next_ticket_id(tickets):
	largest_id = max(
		(
			int(ticket["id"][1:])
			for ticket in tickets
			if ticket["id"].startswith("T") and ticket["id"][1:].isdigit()
		),
		default=0,
	)
	return f"T{largest_id + 1:03d}"


def add_ticket(storage, title, category, urgency, affected_users):
	tickets = storage.load()
	ticket = create_ticket(
		next_ticket_id(tickets), title, category, urgency, affected_users
	)
	tickets.append(ticket)
	storage.save(tickets)
	return ticket


def prompt_for_ticket(storage):
	def prompt_value(label, normalize):
		while True:
			value = input(f"{label}: ")
			try:
				return normalize(value)
			except ValueError as error:
				print(error)

	def normalize_title(title):
		if not title.strip():
			raise ValueError("Title must not be blank.")
		return title.strip()

	def normalize_user_count(value):
		try:
			count = int(value)
		except ValueError as error:
			raise ValueError("Affected users must be a positive integer.") from error
		return validate_affected_users(count)

	title = prompt_value("Title", normalize_title)
	category = prompt_value("Category (Network, Hardware, Software, Other)", normalize_category)
	urgency = prompt_value("Urgency (low, medium, high)", normalize_urgency)
	affected_users = prompt_value("Affected users", normalize_user_count)
	ticket = add_ticket(storage, title, category, urgency, affected_users)
	print(f"Created {ticket['id']} ({ticket['priority']}).")
	return ticket


def format_tickets(tickets):
	if not tickets:
		return "No tickets found."
	headings = ("ID", "TITLE", "CATEGORY", "URGENCY", "USERS", "PRIORITY", "STATUS", "ASSIGNED TO")
	rows = [
		(
			ticket["id"],
			ticket["title"],
			ticket["category"],
			ticket["urgency"],
			str(ticket["affected_users"]),
			ticket["priority"],
			ticket["status"],
			ticket["assigned_to"] or "-",
		)
		for ticket in tickets
	]
	widths = [max(len(heading), *(len(row[index]) for row in rows)) for index, heading in enumerate(headings)]
	lines = ["  ".join(heading.ljust(widths[index]) for index, heading in enumerate(headings))]
	lines.extend("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)) for row in rows)
	return "\n".join(lines)


def format_ticket_details(ticket):
	fields = (
		("ID", "id"),
		("Title", "title"),
		("Category", "category"),
		("Urgency", "urgency"),
		("Affected users", "affected_users"),
		("Priority", "priority"),
		("Status", "status"),
		("Assigned to", "assigned_to"),
	)
	return "\n".join(
		f"{label}: {ticket[key] if ticket[key] is not None else '-'}"
		for label, key in fields
	)


def format_search_results(tickets):
	if not tickets:
		return "No matching tickets."

	headings = ("ID", "TITLE", "CATEGORY", "PRIORITY", "STATUS", "ASSIGNED TO")
	rows = [
		(
			ticket["id"],
			ticket["title"],
			ticket["category"],
			ticket["priority"],
			ticket["status"],
			ticket["assigned_to"] or "-",
		)
		for ticket in tickets
	]
	widths = [
		max(len(heading), *(len(row[index]) for row in rows))
		for index, heading in enumerate(headings)
	]
	lines = ["  ".join(heading.ljust(widths[index]) for index, heading in enumerate(headings))]
	lines.extend(
		"  ".join(value.ljust(widths[index]) for index, value in enumerate(row))
		for row in rows
	)
	return "\n".join(lines)


def prompt_for_search(storage, sort_by_priority=False):
	title = input("Title contains (blank for any): ")
	category = None
	while True:
		value = input("Category (Network, Hardware, Software, Other; blank for any): ")
		if not value.strip():
			break
		try:
			category = normalize_category(value)
			break
		except ValueError as error:
			print(error)

	status = None
	while True:
		value = input("Status (open, in_progress, resolved; blank for any): ")
		if not value.strip():
			break
		try:
			status = normalize_status(value)
			break
		except ValueError as error:
			print(error)

	priority = None
	while True:
		value = input("Priority (critical, high, medium, low; blank for any): ")
		if not value.strip():
			break
		priority = value.strip().casefold()
		if priority in PRIORITIES:
			break
		print("Priority must be critical, high, medium, or low.")

	results = search_tickets(
		storage.load(),
		title=title,
		category=category,
		status=status,
		priority=priority,
	)
	if sort_by_priority:
		results = sort_search_results(results)
	print(format_search_results(results))


def prompt_for_add_note(storage):
	ticket_id = input("Ticket ID: ").strip()
	author = input("Author: ")
	message = input("Note (5-300 characters): ")
	tickets = storage.load()
	note = add_note(tickets, ticket_id, author, message)
	storage.save(tickets)
	print(f"Added note {note['note_id']} to {ticket_id}.")


def prompt_for_view_notes(storage):
	ticket_id = input("Ticket ID: ").strip()
	notes = get_ticket_notes(storage.load(), ticket_id)
	if not notes:
		print(f"No notes for ticket {ticket_id}.")
		return
	for note in notes:
		print(f"{note['note_id']} | {note['author']} | {note['message']}")


def prompt_for_assignment(storage):
	ticket_id = input("Ticket ID: ").strip()
	assignee = input("Staff member: ")
	tickets = storage.load()
	ticket = assign_ticket(tickets, ticket_id, assignee)
	storage.save(tickets)
	print(f"Assigned {ticket['id']} to {ticket['assigned_to']}.")


def prompt_for_status_update(storage):
	ticket_id = input("Ticket ID: ").strip()
	status = input("New status (in_progress or resolved): ").strip()
	tickets = storage.load()
	ticket = update_ticket_status(tickets, ticket_id, status)
	storage.save(tickets)
	print(f"Ticket {ticket['id']} is now {ticket['status']}.")


def prompt_for_reopen(storage):
	ticket_id = input("Ticket ID: ").strip()
	tickets = storage.load()
	ticket = reopen_ticket(tickets, ticket_id)
	storage.save(tickets)
	print(f"Ticket {ticket['id']} has been reopened.")


def interactive_menu(storage):
	while True:
		print("\nCampusFlow Ticket Manager")
		print("1. Create a ticket")
		print("2. Show all tickets")
		print("3. View ticket details")
		print("4. Assign a ticket")
		print("5. Update ticket status")
		print("6. Reopen a resolved ticket")
		print("7. Show work queue")
		print("8. Show ticket report")
		print("9. Search tickets")
		print("10. Search results by priority")
		print("11. Add follow-up note")
		print("12. View ticket notes")
		print("13. Engineering Understanding Check")
		print("14. Quit")
		try:
			choice = input("Choose an option: ").strip()
			if choice == "1":
				prompt_for_ticket(storage)
			elif choice == "2":
				print(format_tickets(storage.load()))
			elif choice == "3":
				ticket_id = input("Ticket ID: ").strip()
				ticket = next(
					(
						item
						for item in storage.load()
						if item["id"].casefold() == ticket_id.casefold()
					),
					None,
				)
				if ticket is None:
					print(f"Ticket {ticket_id} was not found.")
				else:
					print(format_ticket_details(ticket))
			elif choice == "4":
				prompt_for_assignment(storage)
			elif choice == "5":
				prompt_for_status_update(storage)
			elif choice == "6":
				prompt_for_reopen(storage)
			elif choice == "7":
				print(format_tickets(get_work_queue(storage.load())))
			elif choice == "8":
				print(format_report(storage.load()))
			elif choice == "9":
				prompt_for_search(storage)
			elif choice == "10":
				prompt_for_search(storage, sort_by_priority=True)
			elif choice == "11":
				prompt_for_add_note(storage)
			elif choice == "12":
				prompt_for_view_notes(storage)
			elif choice == "13":
				run_understanding_check()
			elif choice == "14":
				print("Goodbye.")
				return
			else:
				print("Choose a number from 1 to 14.")
		except (StorageError, ValueError) as error:
			print(f"Error: {error}")
		except EOFError:
			print("\nGoodbye.")
			return


def main():

	interactive_menu(TicketStorage())


if __name__ == "__main__":
	main()