# Use-Case Flow Specification
## Vaccination Cohort & Dose Scheduling System
**Problem Statement #17 | PES University — SE Lab 1**

---

## Use Case: UC-03 — Book Vaccination Slot

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-03 |
| **Use Case Name** | Book Vaccination Slot |
| **Primary Actor** | Citizen Registrant |
| **Secondary Actor** | Vaccination Officer (notified on booking confirmation) |
| **Description** | Allows a registered and cohort-eligible citizen to search for available vaccination center slots and confirm a booking for their current due dose. |
| **Trigger** | Citizen logs in and navigates to the "Book Appointment" section. |

---

### Preconditions
1. The Citizen Registrant has a verified account in the system (FR-001 completed).
2. The citizen has been assigned to a vaccination cohort.
3. If booking for Dose 2 or later, the mandatory minimum interval since the previous dose has elapsed (FR-002 satisfied).
4. At least one vaccination center has available slots published for the citizen's eligible date range.

---

### Postconditions
**On success:**
- A slot is reserved and marked unavailable to other citizens.
- The citizen receives a booking confirmation (SMS/email) with center details, date, time, and dose number.
- The Vaccination Officer's queue at the selected center is updated with the new appointment.

**On failure:**
- No slot is reserved; system state is unchanged.
- Citizen is shown an appropriate error message.

---

### Main Success Scenario

| Step | Actor | Action |
|------|-------|--------|
| 1 | Citizen | Logs into the system using registered credentials. |
| 2 | System | Authenticates the citizen and loads their profile, cohort, and current dose stage. |
| 3 | Citizen | Selects "Book Appointment" and applies filters (preferred date range, district/city, vaccine type). |
| 4 | System | Queries available slots matching the citizen's cohort eligibility and dose stage; displays results sorted by proximity and date. |
| 5 | Citizen | Selects a preferred slot from the list. |
| 6 | System | **«include»** Validates Dose Interval — confirms the mandatory minimum days since the last dose have been met. |
| 7 | System | Displays slot summary (center name, address, date, time, vaccine brand, dose number) and prompts for confirmation. |
| 8 | Citizen | Confirms the booking. |
| 9 | System | Reserves the slot, creates a booking record linked to the citizen's profile, and sends a confirmation notification. |
| 10 | System | Updates the Vaccination Officer's appointment queue at the selected center. |

---

### Alternate Flow A — No Slots Available

| Step | Description |
|------|-------------|
| A1 | At Step 4, the system finds no available slots matching the citizen's filters. |
| A2 | System displays a "No slots available" message with suggested alternative nearby centers or dates. |
| A3 | **«extend»** Citizen may optionally enable "Notify Me" — the system registers the citizen for an alert when a slot matching their criteria opens. |
| A4 | Use case ends without a booking being made. |

---

### Alternate Flow B — Dose Interval Not Yet Met

| Step | Description |
|------|-------------|
| B1 | At Step 6, the interval validation finds that the minimum days since Dose 1 have not elapsed. |
| B2 | System blocks the booking and displays a message: *"Dose 2 is not yet available. You are eligible from [date]."* |
| B3 | The citizen is returned to the slot search screen; no slot is reserved. |
| B4 | Use case ends without a booking being made. |
