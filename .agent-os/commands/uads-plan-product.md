---
description: Plan the product mission, roadmap, and tech stack
---

You are helping to plan and document the mission, roadmap and tech stack for the current product. This will include:

- **Gathering Information**: The user's product vision, user personas, problems and key features
- **Mission Document**: Take what you've gathered and create a concise mission document
- **Roadmap**: Create a phased development plan with prioritized features
- **Tech stack**: Establish the technical stack used for all aspects of this product's codebase

## Phase 1: Gather Product Information

{{ include "workflows/planning/gather-product-info.md" }}

## Phase 2: Create Mission Document

{{ include "workflows/planning/create-product-mission.md" }}

## Phase 3: Create Development Roadmap

{{ include "workflows/planning/create-product-roadmap.md" }}

## Phase 4: Document Tech Stack

{{ include "workflows/planning/create-product-tech-stack.md" }}

## Final Validation

Verify all files created successfully:

```bash
# Validate all product files exist
for file in mission.md roadmap.md; do
    if [ ! -f "agent-os/product/$file" ]; then
        echo "Error: Missing $file"
    else
        echo "✓ Created agent-os/product/$file"
    fi
done

echo "Product planning complete! Review your product documentation in agent-os/product/"
```

## User Standards & Preferences Compliance

IMPORTANT: When planning the product's tech stack, mission statement and roadmap, use the user's standards and preferences for context and baseline assumptions:

{{ inject "standards/global/*" }}
