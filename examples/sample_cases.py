#!/usr/bin/env python3
"""Run the Recipient Guard prototype against sample cases."""

import sys
from pathlib import Path

# Allow running this script directly without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from recipient_guard.guard import TicketContext, OutboundDraft, score_risk

if __name__ == "__main__":
    print("=== Recipient Guard Prototype Demo ===\n")

    cases = [
        (
            "Wrong school domain",
            TicketContext("school-a.sch.uk", "Employee 123"),
            OutboundDraft(["school-b.sch.uk"], ["payroll_Employee123.pdf"])
        ),
        (
            "Attachment for different employee",
            TicketContext("school-a.sch.uk", "Employee 456"),
            OutboundDraft(["school-a.sch.uk"], ["Employee_123_payroll.pdf"])
        ),
        (
            "Internal document to school",
            TicketContext("school-a.sch.uk", "Employee 123", is_internal_document=True),
            OutboundDraft(["school-a.sch.uk"], ["internal_staff_list.xlsx"])
        ),
        (
            "Reply-all to external",
            TicketContext("school-a.sch.uk", "Employee 123"),
            OutboundDraft(["school-a.sch.uk", "other-school.sch.uk"], [], reply_all=True, extra_external_recipients=True)
        ),
        (
            "Clean send",
            TicketContext("school-a.sch.uk", "Employee 123"),
            OutboundDraft(["school-a.sch.uk"], ["Employee_123_payroll.pdf"])
        ),
    ]

    for title, ticket, draft in cases:
        result = score_risk(ticket, draft)
        print(f"Case: {title}")
        print(f"  Risk: {result['risk']}")
        print(f"  Action: {result['action']}")
        print(f"  Reasons: {'; '.join(result['reasons'])}")
        print()
