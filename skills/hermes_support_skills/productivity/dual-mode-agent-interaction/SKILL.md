---
name: dual-mode-agent-interaction
description: Use when balancing instant replies with verified execution.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: productivity
    tags: [interaction-modes, response-latency, tool-discipline, conversational-ai, task-execution, user-experience]
---

# Dual-Mode Agent Interaction & Response Latency Discipline

A class-level operational protocol for AI Agents (both personal assistants and commercial autonomous workers like Tech Worker) to deliver instant, responsive conversational turnarounds on informational turns while maintaining rigorous, verified multi-tool execution on actionable tasks.

## When to Use

- When operating conversational AI agents across Telegram, Discord, Slack, web chats, or interactive terminals.
- When the user's intent is informational, conceptual, exploratory, or asking questions ("hanya bertanya").
- When transitioning from discussion into concrete system modifications, code writing, deployments, or debugging.
- When configuring commercial autonomous agents to balance conversational snappiness with thorough technical rigor.

## Core Principle: Mode Separation

An agent must distinguish between two fundamental interaction modes based on user intent:

```
┌─────────────────────────────────────────────────────────────┐
│                    INBOUND USER MESSAGE                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
               Is it an explicit action/task?
               (ubah, perbaiki, buat, jalankan, fix, deploy)
                               │
                ┌──────────────┴──────────────┐
                │                             │
             [ NO ]                        [ YES ]
                │                             │
    ▼───────────────────────▼     ▼───────────────────────▼
    INFORMATIONAL QUERY MODE      TASK EXECUTION MODE
    • Instant response (<2s)      • Multi-tool execution chain
    • No background writes/tests  • Live file & code mutations
    • No unrequested git backups  • Process restart & health test
    • Concise, direct, natural    • Verified output & brief report
    ▲───────────────────────▲     ▲───────────────────────▲
```

## Procedures

### 1. Informational / Query Mode (Instant Turnaround)
- **Trigger:** User asks a conceptual question, requests analysis, asks for status clarification, or discusses an idea without commanding an immediate change (e.g. *"bagaimana cara kerja X?"*, *"kenapa terjadi Y?"*, *"siapa akun ini?"*, *"bisa ga kalau begini?"*).
- **Behavioral Rules:**
  1. **Zero-Tool / Lightweight-Read:** Do not trigger background writes, heavy code execution, service restarts, or backup pipelines unless the data cannot be known without a single read query.
  2. **Direct Answer First:** Provide the explanation, root cause, or answer immediately in clear, concise language.
  3. **No Unprompted Execution Dumps:** Avoid dumping massive multi-step execution plans or starting background tasks when the user only asked for understanding.

### 2. Task / Execution Mode (Verified Delivery)
- **Trigger:** User gives an explicit imperative command to execute, build, modify, fix, or deploy (e.g. *"hapus X"*, *"perbaiki bug Y"*, *"ganti label ini"*, *"eksekusi sekarang"*).
- **Behavioral Rules:**
  1. **Direct Action:** Execute the necessary tool calls immediately in the same response turn.
  2. **Test-First Verification:** Verify the change against live services or endpoints (`curl`, test execution, or status inspection).
  3. **Operational State Synchronization:** If the change affects persistent configs, databases, or personas, restart relevant systemd services and sync operational backups.
  4. **Concise Completion Report:** Summarize the exact actions taken and verified live results without redundant narrative fluff.

### 3. Application to Commercial Bots (e.g., Tech Worker / Enterprise Bots)
- **Client Engagement:** Customers chatting with a commercial bot on Telegram expect immediate, friendly, and snappy consultation when asking general questions.
- **Task Gating:** When clients send specific code snippets, bug reports, or server connection details, the bot transitions into execution mode: consuming tokens, running tools, and returning verified solutions.

## Pitfalls

- **Unnecessary Tool Chaining on Informational Turns:** Running file search, code execution, service restarts, and git backup scripts during a simple "why is this happening?" query introduces a 20–30 second latency penalty and frustrates user conversational flow.
- **Preemptive Unconfirmed Changes:** Modifying database records or deleting files during an exploratory diagnostic turn before the user has approved the proposed remediation.
- **Narrating Plans Without Execution:** Announcing "I will edit the file and restart the service" on an execution turn without actually making the tool calls in that turn.
- **Failing to Verify Mutated State:** Reporting a fix as completed without running a live check (HTTP status, process poll, or database query) to confirm the service accepted the change.
