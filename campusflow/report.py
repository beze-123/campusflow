def build_report(tickets: list[dict]) -> dict:
	return {
		"total": len(tickets),
		"by_status": {
			status: sum(ticket["status"] == status for ticket in tickets)
			for status in ("open", "in_progress", "resolved")
		},
		"by_priority": {
			priority: sum(ticket["priority"] == priority for ticket in tickets)
			for priority in ("critical", "high", "medium", "low")
		},
	}


def format_report(tickets: list[dict]) -> str:
	report = build_report(tickets)
	lines = [f"Total tickets: {report['total']}", "By status:"]
	lines.extend(
		f"  {status}: {count}" for status, count in report["by_status"].items()
	)
	lines.append("By priority:")
	lines.extend(
		f"  {priority}: {count}"
		for priority, count in report["by_priority"].items()
	)
	return "\n".join(lines)
