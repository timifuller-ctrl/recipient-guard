import re
from dataclasses import dataclass
from typing import List

@dataclass
class TicketContext:
    requester_domain: str
    employee_name: str
    is_internal_document: bool = False

@dataclass
class OutboundDraft:
    recipient_domains: List[str]
    attachment_filenames: List[str]
    reply_all: bool = False
    extra_external_recipients: bool = False

def score_risk(ticket: TicketContext, draft: OutboundDraft) -> dict:
    reasons = []
    risk = "Low"

    # Rule 1: Wrong school domain
    for domain in draft.recipient_domains:
        if domain and domain != ticket.requester_domain and "school" in domain.lower():
            reasons.append(f"Recipient domain '{domain}' does not match expected '{ticket.requester_domain}'")
            risk = "High"

    # Rule 2: Attachment for different employee
    for filename in draft.attachment_filenames:
        if re.search(r"Employee[_\s]?(\d+)", filename, re.I):
            extracted = re.search(r"Employee[_\s]?(\d+)", filename, re.I).group(1)
            expected_num = re.search(r"(\d+)", ticket.employee_name)
            if expected_num and extracted != expected_num.group(1):
                reasons.append(f"Attachment '{filename}' appears to reference a different employee than '{ticket.employee_name}'")
                risk = "High" if risk != "High" else risk

    # Rule 3: Internal document to external
    if ticket.is_internal_document and any("school" in d.lower() or "sch.uk" in d.lower() for d in draft.recipient_domains):
        reasons.append("Internal document being sent to an external school domain")
        risk = "High"

    # Rule 4: Reply-all to unexpected external
    if draft.reply_all and draft.extra_external_recipients:
        reasons.append("Reply-all includes unexpected external recipients")
        risk = "Medium" if risk == "Low" else risk

    if risk in ("Medium", "High"):
        reasons.append("Recommended: pause and complete a documented recipient + content check before sending")

    return {
        "risk": risk,
        "reasons": reasons if reasons else ["No significant issues detected"],
        "action": "Allow" if risk == "Low" else ("Require confirmation" if risk == "Medium" else "Block or require manager approval")
    }
