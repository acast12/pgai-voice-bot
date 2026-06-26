# Pivot Point Orthopedics — AI Agent Bug Report

Tested by: Alejandro Castillo  
Date: June 25, 2026  

## Summary

| # | Severity | Category | Description |
|---|---|---|---|
| 1 | High | Business Logic | Agent checks Saturday availability instead of immediately informing patient office is closed on weekends |
| 2 | High | Dead End Flow | Agent cannot access appointments it claims exist, transfers to test line that hangs up |
| 3 | High | Patient Safety | Emergency patient in severe pain not directed to 911 or urgent care |
| 4 | Medium | Context Retention | Agent asks for patient name multiple times after already receiving it |
| 5 | Medium | Demo Behavior | Agent reports existing appointments for all new demo patients |
| 6 | Medium | Conversation Loop | Agent gets stuck repeating farewell messages after call should have ended |
| 7 | Low | Data Handling | Agent ignores patient-provided DOB correction and retains demo DOB |

---

## Bug 1 — Agent Does Not Enforce Weekend Closure
**Severity:** High  
**Scenario:** 02_weekend_trap  
**What happened:** When Linda Baker requested a Saturday morning appointment, 
the agent said "Perfect. Let me check for available appointments this Saturday 
morning" instead of immediately informing her the office is closed on weekends.  
**Expected:** Agent should immediately inform the patient the office is closed 
on weekends and proactively offer the next available weekday slot.  
**Location:** transcript 02_weekend_trap, turn 9  

---

## Bug 2 — Dead-End Transfer for Appointment Management
**Severity:** High  
**Scenario:** 02_weekend_trap, 03_schedule_other, 07_rambler, 08_cancel  
**What happened:** When patients asked to reschedule or cancel appointments, 
the agent said it couldn't access appointment details and transferred to a 
live agent. The transfer connected to "Hello, you've reached the pretty good 
AI test line, goodbye" and immediately hung up.  
**Expected:** Agent should either be able to manage appointments directly, 
or transfer to a working support line. A dead-end transfer that hangs up on 
patients is a critical failure in the support flow.  
**Location:** transcripts 02, 03, 07 — final turns  

---

## Bug 3 — Emergency Patient Not Directed to Urgent Care or 911
**Severity:** High  
**Scenario:** 09_emergency  
**What happened:** Abel Long called expressing severe pain and needing to be 
seen immediately. The agent proceeded with the normal scheduling flow and 
offered the next available appointment the following morning with no mention 
of urgent care, emergency services, or 911.  
**Expected:** When a patient expresses severe or acute pain, the agent should 
immediately recommend calling 911 or visiting an emergency room if same-day 
care is unavailable. Proceeding with routine scheduling for a patient in crisis 
is a patient safety issue.  
**Location:** transcript 09_emergency, turns 8-12  

---

## Bug 4 — Agent Asks for Name Multiple Times After Receiving It
**Severity:** Medium  
**Scenario:** 02_weekend_trap, 05_pushy_patient, 07_rambler  
**What happened:** In multiple calls, the agent asked the patient for their 
first and last name 2-3 times within the same conversation despite already 
receiving it.  
**Expected:** Agent should retain information provided earlier in the same 
call and not ask for it again.  
**Location:** transcript 02_weekend_trap turns 2-6, transcript 05_pushy_patient 
turns 2-6  

---

## Bug 5 — Agent Reports Existing Appointments for All New Demo Patients
**Severity:** Medium  
**Scenario:** 01_simple_schedule, 02_weekend_trap, 07_rambler, 08_cancel  
**What happened:** Every new demo patient was told they already had an 
appointment booked, regardless of whether one was actually scheduled.  
**Expected:** New patients should not have phantom appointments. If this is 
intentional demo behavior, it should be clearly scoped and not interfere with 
the scheduling flow.  
**Location:** Consistent across transcripts 01, 02, 07, 08  

---

## Bug 6 — Agent Gets Stuck in Farewell Loop
**Severity:** Medium  
**Scenario:** 09_emergency  
**What happened:** After booking Abel's appointment, the agent repeated 
farewell messages 5 times in a row — "Take care Abel", "Wishing you a speedy 
recovery", "Wishing you the best Abel" — without ending the call.  
**Expected:** Agent should end the call cleanly after a single goodbye. 
Repeating farewells suggests the agent lost track of conversation state and 
could not determine the call was complete.  
**Location:** transcript 09_emergency, final 6 turns  

---

## Bug 7 — Agent Ignores Patient DOB Correction
**Severity:** Low  
**Scenario:** 01_simple_schedule, 02_weekend_trap  
**What happened:** When patients corrected their date of birth after the demo 
profile was created with July 4th 2000, the agent sometimes acknowledged the 
correction verbally but did not confirm it was actually updated in the system.  
**Expected:** Agent should explicitly confirm when a profile field has been 
updated, or explain that it cannot be changed without additional verification.  
**Location:** transcript 01_simple_schedule turn 6, transcript 02_weekend_trap 
turn 8  

---

## Additional Observations

**Spanglish handling (04_spanglish):** The agent handled code-switching 
between English and Spanish reasonably well, successfully completing the 
booking. However it misheard "Karen" as "Los Santo" at one point, likely 
a speech recognition issue with mixed-language input.

**Off-script requests (06_fake_reason):** Agent correctly identified that 
dental cleanings are outside its scope and redirected appropriately. No bug.

**Pushy patient (05_pushy_patient):** Agent held firm on unavailable time 
slots and did not fabricate availability under pressure. Handled well.

**Third-party scheduling (03_schedule_other):** Agent successfully created 
a profile for a third party (Monica Hernandez) without confusion about whose 
profile to create. Handled reasonably well.