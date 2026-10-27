import unittest

from campusflow.search import search_tickets, sort_search_results
from campusflow.ticket import create_ticket


class SearchTests(unittest.TestCase):
	def setUp(self):
		self.tickets = [
			create_ticket("T006", "Wi-Fi router reboot", "Network", "low", 1),
			create_ticket("T007", "Wi-Fi outage", "Network", "high", 12),
			create_ticket("T002", "Wi-Fi software setup", "Software", "medium", 4),
		]
		self.tickets[1]["status"] = "in_progress"

	def test_title_search_is_case_insensitive_substring(self):
		results = search_tickets(self.tickets, title="wI-fI")

		self.assertEqual([ticket["id"] for ticket in results], ["T006", "T007", "T002"])

	def test_all_supplied_filters_must_match(self):
		results = search_tickets(
			self.tickets,
			title="WI-FI",
			category="network",
			status="open",
			priority="low",
		)

		self.assertEqual([ticket["id"] for ticket in results], ["T006"])

	def test_empty_filters_match_all_tickets(self):
		self.assertEqual(search_tickets(self.tickets), self.tickets)

	def test_invalid_filter_is_rejected(self):
		with self.assertRaisesRegex(ValueError, "Priority"):
			search_tickets(self.tickets, priority="urgent")

	def test_priority_sorted_view_uses_numeric_ticket_id(self):
		results = sort_search_results([self.tickets[0], self.tickets[2], self.tickets[1]])

		self.assertEqual([ticket["id"] for ticket in results], ["T007", "T002", "T006"])
		self.assertEqual([ticket["id"] for ticket in self.tickets], ["T006", "T007", "T002"])


if __name__ == "__main__":
	unittest.main()
