import pytest
from recipient_guard.guard import TicketContext, OutboundDraft, score_risk

def test_wrong_school_domain():
    ticket = TicketContext("school-a.sch.uk", "Employee 123")
    draft = OutboundDraft(["school-b.sch.uk"], ["payroll_Employee123.pdf"])
    result = score_risk(ticket, draft)
    assert result["risk"] == "High"
    assert any("does not match expected" in r for r in result["reasons"])
    assert result["action"] == "Block or require manager approval"

def test_attachment_different_employee():
    ticket = TicketContext("school-a.sch.uk", "Employee 456")
    draft = OutboundDraft(["school-a.sch.uk"], ["Employee_123_payroll.pdf"])
    result = score_risk(ticket, draft)
    assert result["risk"] == "High"
    assert any("different employee" in r for r in result["reasons"])

def test_internal_document_to_school():
    ticket = TicketContext("school-a.sch.uk", "Employee 123", is_internal_document=True)
    draft = OutboundDraft(["school-a.sch.uk"], ["internal_staff_list.xlsx"])
    result = score_risk(ticket, draft)
    assert result["risk"] == "High"
    assert any("Internal document" in r for r in result["reasons"])

def test_reply_all_external():
    ticket = TicketContext("school-a.sch.uk", "Employee 123")
    draft = OutboundDraft(
        ["school-a.sch.uk", "other-school.sch.uk"],
        [],
        reply_all=True,
        extra_external_recipients=True
    )
    result = score_risk(ticket, draft)
    assert result["risk"] in ("Medium", "High")
    assert any("Reply-all" in r or "does not match" in r for r in result["reasons"])

def test_clean_send():
    ticket = TicketContext("school-a.sch.uk", "Employee 123")
    draft = OutboundDraft(["school-a.sch.uk"], ["Employee_123_payroll.pdf"])
    result = score_risk(ticket, draft)
    assert result["risk"] == "Low"
    assert result["action"] == "Allow"
    assert "No significant issues detected" in result["reasons"][0]
