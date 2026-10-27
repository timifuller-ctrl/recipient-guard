# Recipient Guard

Open-source AI agent to reduce accidental data breaches from misdirected emails and documents in support ticket workflows (especially Zoho).

Built from real-world incident patterns (wrong school domain, attachment for different employee, internal documents sent externally, reply-all to unexpected external addresses).

## Status
Early prototype. Core risk-scoring logic is working.

## Quick start
```bash
python examples/sample_cases.py
```

## Detection rules (v0.1)
1. Wrong school / organisation domain
2. Attachment referencing a different employee
3. Internal document sent to external school domain
4. Reply-all introducing unexpected external recipients
5. General pause-and-check gate on medium/high risk

## Roadmap
- Better matching and more test cases
- Simple web UI
- Zoho API integration
- Optional local LLM layer
- Audit logging

MIT License
