def build_report(tickets: list[dict]) -> dict:
	by_status = {
		status: sum(ticket["status"] == status for ticket in tickets)
		for status in ("open", "in_progress", "resolved")
	}
	total = len(tickets)
	resolved = by_status["resolved"]

	return {
		"total": total,
		"by_status": by_status,
		"by_priority": {
			priority: sum(ticket["priority"] == priority for ticket in tickets)
			for priority in ("critical", "high", "medium", "low")
		},
		"by_category": {
			category: sum(ticket["category"] == category for ticket in tickets)
			for category in ("Network", "Hardware", "Software", "Other")
		},
		"unresolved": by_status["open"] + by_status["in_progress"],
		"resolved": resolved,
		"resolution_percentage": (resolved / total * 100) if total else 0,
	}


def format_report(tickets: list[dict]) -> str:
	report = build_report(tickets)
	resolution_percentage = report["resolution_percentage"]
	resolution_text = (
		"0%" if resolution_percentage == 0 else f"{resolution_percentage:.1f}%"
	)
	lines = [f"Total tickets: {report['total']}", "By status:"]
	lines.extend(
		f"  {status}: {count}" for status, count in report["by_status"].items()
	)
	lines.append("By priority:")
	lines.extend(
		f"  {priority}: {count}"
		for priority, count in report["by_priority"].items()
	)
	lines.append("By category:")
	lines.extend(
		f"  {category}: {count}"
		for category, count in report["by_category"].items()
	)
	lines.append(f"Unresolved tickets: {report['unresolved']}")
	lines.append(f"Resolved tickets: {report['resolved']}")
	lines.append(f"Resolution percentage: {resolution_text}")
	return "\n".join(lines)
