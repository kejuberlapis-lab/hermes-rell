---
name: neurosymbolic-guardrails
description: "Use when enforcing rules. Applies deterministic state hooks."
---

# Neurosymbolic Guardrails

Adapted from AWS AI Agent Guardrails workshop for Hermes Agent. Combines LLM reasoning with deterministic rule engines.

## Architecture

1. **Symbolic Lifecycle Pre-hooks:**
   - Validate input parameters, file paths, and required permissions against explicit schema rules before tool execution.

2. **Symbolic Lifecycle Post-hooks:**
   - Deterministically validate tool responses before returning results to the conversational context.

3. **Hard Constraint Enforcement:**
   - Business rules, safety policies, and access controls are enforced deterministically via code, never left to LLM prompt compliance alone.
