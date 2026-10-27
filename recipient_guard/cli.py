#!/usr/bin/env python3
"""Simple interactive CLI for Recipient Guard."""

import sys
from pathlib import Path

# Allow running directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from recipient_guard.guard import TicketContext, OutboundDraft, score_risk

def main():
    print("=== Recipient Guard CLI ===")
    print("Enter ticket details (press Enter for defaults where shown)\n")

    requester_domain = input("Expected requester domain [school-a.sch.uk]: ").strip() or "school-a.sch.uk"
    employee_name = input("Employee name [Employee 123]: ").strip() or "Employee 123"
    internal = input("Is this an internal document? (y/N): ").strip().lower() == "y"

    print("\nNow the outbound draft:")
    recipients = input("Recipient domain(s), comma-separated [school-a.sch.uk]: ").strip() or "school-a.sch.uk"
    recipient_domains = [d.strip() for d in recipients.split(",") if d.strip()]

    attachments = input("Attachment filename(s), comma-separated (or blank): ").strip()
    attachment_filenames = [a.strip() for a in attachments.split(",") if a.strip()] if attachments else []

    reply_all = input("Is this a reply-all? (y/N): ").strip().lower() == "y"
    extra_external = False
    if reply_all:
        extra_external = input("Does reply-all include unexpected external addresses? (y/N): ").strip().lower() == "y"

    ticket = TicketContext(
        requester_domain=requester_domain,
        employee_name=employee_name,
        is_internal_document=internal,
    )
    draft = OutboundDraft(
        recipient_domains=recipient_domains,
        attachment_filenames=attachment_filenames,
        reply_all=reply_all,
        extra_external_recipients=extra_external,
    )

    result = score_risk(ticket, draft)

    print("\n" + "=" * 40)
    print(f"Risk:    {result['risk']}")
    print(f"Action:  {result['action']}")
    print("Reasons:")
    for reason in result["reasons"]:
        print(f"  - {reason}")
    print("=" * 40)

if __name__ == "__main__":
    main()
