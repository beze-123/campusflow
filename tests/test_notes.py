def next_note_id(ticket):
    notes = ticket["notes"]

    if not notes:
        return "N001"

    numbers = [
        int(note["note_id"][1:])
        for note in notes
    ]

    return f"N{max(numbers) + 1:03d}"