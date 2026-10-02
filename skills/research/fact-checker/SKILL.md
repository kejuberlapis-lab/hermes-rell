---
name: fact-checker
description: "Use when checking facts. Verifies live web sources."
---

# Real-Time Fact-Checker

Adapted from open-source hallucination detectors for Hermes Agent.

## Procedure

1. **Extraction of Factual Claims:**
   - Break statements into discrete testable atomic claims (dates, metrics, API versions, release details).

2. **Live Ground-Truth Verification:**
   - Use `web_search` and `web_extract` to fetch primary sources directly from official documentation, release notes, or repositories.

3. **Triangulation:**
   - Require independent verification for disputed or non-trivial claims.
   - Flag any claim that cannot be backed by a live URL or document as `[unverified]`.
