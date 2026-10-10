import argparse

from campusflow.storage import StorageError
from campusflow.storage import TicketStorage
from campusflow.ticket import (
	create_ticket,
	normalize_category,
	normalize_urgency,
	validate_affected_users,
)


def build_parser():
	parser = argparse.ArgumentParser(description="Manage campus technical support tickets.")
	parser.add_argument("--data", default="tickets.json", help="ticket data file")
	commands = parser.add_subparsers(dest="command")

	add = commands.add_parser("add", help="record a support request")
	add.add_argument("--title", required=True)
	add.add_argument("--category", required=True)
	add.add_argument("--urgency", required=True)
	add.add_argument("--affected-users", required=True, type=int)

	commands.add_parser("list", help="list all support requests")

	return parser


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


def interactive_menu(storage):
	while True:
		print("\nCampusFlow Ticket Manager")
		print("1. Create a ticket")
		print("2. Show all tickets")
		print("3. View ticket details")
		print("4. Quit")
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
				print("Goodbye.")
				return
			else:
				print("Choose 1, 2, 3, or 4.")
		except (StorageError, ValueError) as error:
			print(f"Error: {error}")
		except EOFError:
			print("\nGoodbye.")
			return


def main(argv=None):
	parser = build_parser()
	args = parser.parse_args(argv)
	storage = TicketStorage(args.data)
	try:
		if args.command is None:
			interactive_menu(storage)
		elif args.command == "add":
			ticket = add_ticket(
				storage,
				args.title,
				args.category,
				args.urgency,
				args.affected_users,
			)
			print(f"Created {ticket['id']} ({ticket['priority']}).")
		elif args.command == "list":
			print(format_tickets(storage.load()))
	except (StorageError, ValueError) as error:
		parser.error(str(error))


if __name__ == "__main__":
	main()
