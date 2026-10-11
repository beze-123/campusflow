# AI Learning Log — CampusFlow

## Task: Ticket Validation and Storage

* **Project:** CampusFlow
* **Language:** Python
* **Feature:** Ticket validation, priority calculation, and JSON storage

---

## What I Worked On

I worked on the **ticket validation and storage system** for CampusFlow.

The main responsibilities were:

* Validating and normalizing ticket information.
* Calculating ticket priority.
* Loading tickets from a JSON file.
* Saving tickets safely to a JSON file.
* Detecting invalid or duplicate stored tickets.

---

## What I Learned

### Ticket Validation

I learned how to create small validation functions with clear responsibilities.

* `normalize_category()` validates and formats categories.
* `normalize_urgency()` validates urgency levels.
* `normalize_status()` validates ticket statuses.
* `validate_affected_users()` ensures affected users is a positive integer.

I also learned that `casefold()` helps normalize text regardless of capitalization.

For example, `"HIGH"` can safely become `"high"`.

### Priority Calculation

I used `calculate_priority()` to calculate priority from **urgency and impact**.

* High urgency + 10 or more affected users → `critical`
* High urgency or 10+ affected users → `high`
* Medium urgency or 3+ affected users → `medium`
* Otherwise → `low`

This helped me understand how business requirements become Python conditional logic.

---

## JSON Storage

I created the `TicketStorage` class for persistent ticket storage.

### `load()`

The method:

* Returns an empty list when the file does not exist.
* Reads ticket data using `json.load()`.
* Ensures the JSON contains a list.
* Validates every stored ticket.
* Detects duplicate ticket IDs.

### `save()`

The method:

* Creates directories when necessary.
* Writes tickets to a temporary file.
* Uses `json.dump()` to create formatted JSON.
* Uses `os.replace()` to safely replace the original file.
* Cleans up temporary files after the operation.

---

## Error Handling

I created a custom `StorageError` for storage-related failures.

I learned how `try`, `except`, and `finally` work together and how:

`raise StorageError(...) from error`

preserves the original error while providing a clearer application-level message.

---

## How AI Helped Me

I used AI as a **learning and code-review assistant**.

AI helped me understand:

* JSON file handling.
* Input normalization and validation.
* Custom exceptions and exception chaining.
* Safe file writing with temporary files.
* Duplicate ID detection.
* Why Boolean values need special handling when validating integers.

I reviewed and understood the suggestions before applying them.

---

## How I Verified the Work

I checked both valid and invalid scenarios.

* Valid tickets are normalized correctly.
* Priorities follow the required business rules.
* Invalid categories, urgency, and statuses are rejected.
* `affected_users` must be a positive integer.
* Invalid stored tickets and duplicate IDs are rejected.
* Valid tickets can be saved and loaded successfully.

---

## Key Takeaway

I learned that persistent storage is more than simply reading and writing JSON.

A reliable system must **validate data, enforce business rules, handle errors, prevent corrupted writes, and verify stored information**.

AI supported my learning, while I remained responsible for understanding and verifying the final implementation.