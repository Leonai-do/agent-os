---
description: Create a detailed and strategic tasks list for development of a spec
---

I want you to create a tasks breakdown from a given spec and requirements for a new feature.

## Phase 1: Get Spec and Requirements

The FIRST STEP is to make sure you have ONE OR BOTH of these files to inform your tasks breakdown:

- `agent-os/specs/[this-spec]/spec.md`
- `agent-os/specs/[this-spec]/planning/requirements.md`

**IF you don't have ONE OR BOTH of those files**, then ask user to provide direction on where to you can find them by outputting the following request then wait for user's response:

```
I'll need a spec.md or requirements.md (or both) in order to build a tasks list.

Please direct me to where I can find those. If you haven't created them yet, you can run /2-uads-shape-spec or /3-uads-write-spec.
```

Once you've confirmed you have the spec and/or requirements, proceed to Phase 2.

## Phase 2: Create Tasks List

{{ include "workflows/implementation/create-tasks-list.md" }}

## User Standards & Preferences Compliance

IMPORTANT: Ensure that the tasks list you create IS ALIGNED and DOES NOT CONFLICT with the user's standards:

{{ inject "standards/*" }}
