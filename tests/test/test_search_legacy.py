from campusflow.search import search_tickets


def test_search_can_combine_filters():
	tickets = [
		{
			"id": "T006",
			"title": "wIFI",
			"category": "Network",
			"priority": "low",
			"status": "open",
		},
		{
			"id": "T007",
			"title": "Wi-Fi outage",
			"category": "Network",
			"priority": "critical",
			"status": "open",
		},
	]

	results = search_tickets(
		tickets,
		title="wifi",
		category="Network",
		status="open",
		priority="low",
	)

	assert [ticket["id"] for ticket in results] == ["T006"]
