# Requirements Specification
## Vaccination Cohort & Dose Scheduling System
**Problem Statement #17 | PES University — SE Lab 1**

---

## Functional Requirements

| ID | Description | Priority | Acceptance Criteria | Rationale |
|----|-------------|----------|---------------------|-----------|
| FR-001 | The system shall allow a Citizen Registrant to create a profile by submitting personal details (name, date of birth, Aadhaar/ID number, contact information, and pre-existing health conditions) to be enrolled in the appropriate vaccination cohort. | High | **Pass:** Citizen profile is created and assigned to a cohort; duplicate ID numbers are rejected with an error message. **Fail:** System accepts duplicate registrations or enrolls citizen in an incorrect cohort. | Accurate cohort assignment is the foundation for scheduling and eligibility checks. |
| FR-002 | The system shall enforce minimum dose interval rules — blocking Dose 2 booking if fewer than the mandated minimum days (e.g., 28 days) have elapsed since the previous dose administration date. | High | **Pass:** Dose 2 booking UI remains locked and displays remaining wait days if interval < 28 days; booking proceeds normally once interval is met. **Fail:** System permits early Dose 2 booking regardless of interval. | Prevents medically unsafe early administration and ensures vaccination protocol compliance. |
| FR-003 | The system shall allow a Citizen Registrant to browse available vaccination center slots filtered by date, location, and vaccine type, and book a slot subject to cohort eligibility and dose interval validation. | High | **Pass:** Only eligible slots for the citizen's cohort and dose stage are displayed; booking confirms and reserves the slot. **Fail:** Ineligible slots are shown or a slot can be double-booked. | Ensures equitable, structured access to vaccination infrastructure. |
| FR-004 | The system shall allow a Vaccination Officer to record dose administration details (vaccine batch number, dose number, date, and administering officer ID) against a citizen's booking, updating the citizen's vaccination status. | High | **Pass:** Administration record is saved; citizen status updates to reflect dose received; booking is marked complete. **Fail:** Record is saved without linking to a citizen, or citizen status is not updated. | Maintains an accurate, auditable vaccination history per citizen. |
| FR-005 | The system shall automatically generate a digitally signed, verifiable QR-code vaccination certificate upon successful recording of the final dose, accessible by the Citizen Registrant via download or email. | High | **Pass:** Certificate is generated within 60 seconds of final dose recording; QR code decodes to valid citizen and vaccination metadata; digital signature passes verification. **Fail:** Certificate is not generated, or QR code contains incorrect/unverifiable data. | Provides citizens with a portable, tamper-evident proof of vaccination status. |

---

## Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|----|------|-------------|----------|---------------------|-----------|
| NFR-001 | Performance & Security | The vaccination certificate verification endpoint shall authenticate digitally signed QR codes both online and offline in under 150 ms, even under peak load simulating 10,000 concurrent verification requests. | High | **Pass:** Load tests confirm p95 latency ≤ 150 ms; QR codes verified without network access return correct results. **Fail:** Latency exceeds threshold under simulated load, or offline verification is unavailable. | Certificates must be verifiable instantly at checkpoints without network dependency. |
| NFR-002 | Availability & Scalability | The system shall maintain 99.9% uptime during active vaccination drive windows, with horizontal scaling triggered automatically when concurrent user sessions exceed 5,000. | High | **Pass:** Uptime monitoring confirms ≥ 99.9% over a 30-day drive window; auto-scaling provisions new instances within 60 seconds of threshold breach. **Fail:** System experiences downtime > 0.1% or fails to scale under load, causing booking failures. | Vaccination drives have concentrated peak demand; downtime directly prevents citizens from booking doses. |
