---
description: Create a detailed specification document for development
---

Now that we've initiated and planned the details for a new spec, we will now proceed with drafting the specification document.

## Write Specification

{{ include "workflows/specification/write-spec.md" }}

## Completion Message

Display the following message to the user:

```
The spec has been created at agent-os/specs/[this-spec]/spec.md.

Review it closely to ensure everything aligns with your vision and requirements.

Next step: Run /uads-create-tasks to create the implementation tasks list.
```

## User Standards & Preferences Compliance

IMPORTANT: Ensure that the specification document's content is ALIGNED and DOES NOT CONFLICT with the user's standards:

{{ inject "standards/*" }}
