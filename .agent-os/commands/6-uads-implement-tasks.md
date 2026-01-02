---
description: Implement tasks from a spec following a multi-phase process
---

Now that we have a spec and tasks list ready for implementation, we will proceed with implementation of this spec by following this multi-phase process:

- **PHASE 1**: Determine which task group(s) from tasks.md should be implemented
- **PHASE 2**: Implement the given task(s)
- **PHASE 3**: After ALL task groups have been implemented, produce the final verification report

## Phase 1: Determine Tasks to Implement

First, check if the user has already provided instructions about which task group(s) to implement.

**If the user HAS provided instructions:** Proceed to PHASE 2 to implement those specified task group(s).

**If the user has NOT provided instructions:**

Read `agent-os/specs/[this-spec]/tasks.md` to review the available task groups, then output the following message to the user and WAIT for their response:

```
Should we proceed with implementation of all task groups in tasks.md?

If not, then please specify which task(s) to implement.
```

## Phase 2: Implement Tasks

Now that you have the task group(s) to be implemented, proceed with implementation:

{{ include "workflows/implementation/implement-tasks.md" }}

### Display Progress

Display a summary of what was implemented.

**IF all tasks are now marked as done** (with `- [x]`) in tasks.md, display this message:

```
All tasks have been implemented: agent-os/specs/[this-spec]/tasks.md.

NEXT STEP 👉 Run /uads-verify-implementation to verify the implementation.
```

**IF there are still tasks remaining** (marked with `- [ ]`) then display this message:

```
Would you like to proceed with implementation of the remaining tasks in tasks.md?

If not, please specify which task group(s) to implement next.
```

## Phase 3: Final Verification

After all tasks have been implemented, verify the end-to-end implementation:

{{ include "workflows/implementation/verification/verify-tasks.md" }}

{{ include "workflows/implementation/verification/update-roadmap.md" }}

{{ include "workflows/implementation/verification/run-all-tests.md" }}

{{ include "workflows/implementation/verification/create-verification-report.md" }}

## User Standards & Preferences Compliance

IMPORTANT: Ensure that the implementation IS ALIGNED and DOES NOT CONFLICT with the user's standards:

{{ inject "standards/*" }}

## Using External Skills

When specialized capabilities are needed during implementation, invoke skills through the `skillz` MCP server:

- `mcp_skillz_frontend-design` — Create distinctive, production-grade frontend interfaces
- `mcp_skillz_git-sync` — Automate staging, committing, and pushing changes
- `mcp_skillz_url-to-markdown` — Fetch URL and convert content to markdown

**Execution Protocol:**

1. **Primary**: Call the MCP tool directly (e.g., `mcp_skillz_frontend-design`)
2. **Fallback**: If MCP unavailable, skill location: `/home/leonai-do/Host-D-Drive/LeonAI_DO/dev/Agent-Skills/skills-repository`
