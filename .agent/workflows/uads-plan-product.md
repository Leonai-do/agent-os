---
description: Plan the product mission, roadmap, and tech stack
---

You are helping to plan and document the mission, roadmap and tech stack for the current product. This will include:

- **Gathering Information**: The user's product vision, user personas, problems and key features
- **Mission Document**: Take what you've gathered and create a concise mission document
- **Roadmap**: Create a phased development plan with prioritized features
- **Tech stack**: Establish the technical stack used for all aspects of this product's codebase

## Phase 1: Gather Product Information

Collect comprehensive product information from the user:

```bash
# Check if product folder already exists
if [ -d "agent-os/product" ]; then
    echo "Product documentation already exists. Review existing files or start fresh?"
    # List existing product files
    ls -la agent-os/product/
fi
```

Gather from user the following required information:
- **Product Idea**: Core concept and purpose (required)
- **Key Features**: Minimum 3 features with descriptions
- **Target Users**: At least 1 user segment with use cases
- **Tech stack**: Confirmation or info regarding the product's tech stack choices

If any required information is missing, prompt user:
```
Please provide the following to create your product plan:
1. Main idea for the product
2. List of key features (minimum 3)
3. Target users and use cases (minimum 1)
4. Will this product use your usual tech stack choices or deviate in any way?
```


## Phase 2: Create Mission Document

Create `agent-os/product/mission.md` with comprehensive product definition following this structure for its' content:

#### Mission Structure:
```markdown
# Product Mission

## Pitch
[PRODUCT_NAME] is a [PRODUCT_TYPE] that helps [TARGET_USERS] [SOLVE_PROBLEM]
by providing [KEY_VALUE_PROPOSITION].

## Users

### Primary Customers
- [CUSTOMER_SEGMENT_1]: [DESCRIPTION]
- [CUSTOMER_SEGMENT_2]: [DESCRIPTION]

### User Personas
**[USER_TYPE]** ([AGE_RANGE])
- **Role:** [JOB_TITLE/CONTEXT]
- **Context:** [BUSINESS/PERSONAL_CONTEXT]
- **Pain Points:** [SPECIFIC_PROBLEMS]
- **Goals:** [DESIRED_OUTCOMES]

## The Problem

### [PROBLEM_TITLE]
[PROBLEM_DESCRIPTION]. [QUANTIFIABLE_IMPACT].

**Our Solution:** [SOLUTION_APPROACH]

## Differentiators

### [DIFFERENTIATOR_TITLE]
Unlike [COMPETITOR/ALTERNATIVE], we provide [SPECIFIC_ADVANTAGE].
This results in [MEASURABLE_BENEFIT].

## Key Features

### Core Features
- **[FEATURE_NAME]:** [USER_BENEFIT_DESCRIPTION]

### Collaboration Features
- **[FEATURE_NAME]:** [USER_BENEFIT_DESCRIPTION]

### Advanced Features
- **[FEATURE_NAME]:** [USER_BENEFIT_DESCRIPTION]
```

#### Important Constraints

- **Focus on user benefits** in feature descriptions, not technical details
- **Keep it concise** and easy for users to scan and get the more important concepts quickly


## Phase 3: Create Development Roadmap

Generate `agent-os/product/roadmap.md` with an ordered feature checklist:

Do not include any tasks for initializing a new codebase or bootstrapping a new application. Assume the user is already inside the project's codebase and has a bare-bones application initialized.

#### Creating the Roadmap:

1. **Review the Mission** - Read `agent-os/product/mission.md` to understand the product's goals, target users, and success criteria.

2. **Identify Features** - Based on the mission, determine the list of concrete features needed to achieve the product vision.

3. **Strategic Ordering** - Order features based on:
   - Technical dependencies (foundational features first)
   - Most direct path to achieving the mission
   - Building incrementally from MVP to full product

4. **Create the Roadmap** - Use the structure below as your template. Replace all bracketed placeholders (e.g., `[FEATURE_NAME]`, `[DESCRIPTION]`, `[EFFORT]`) with real content that you create based on the mission.

#### Roadmap Structure:
```markdown
# Product Roadmap

1. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
2. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
3. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
4. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
5. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
6. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
7. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`
8. [ ] [FEATURE_NAME] — [1-2 SENTENCE DESCRIPTION OF COMPLETE, TESTABLE FEATURE] `[EFFORT]`

> Notes
> - Order items by technical dependencies and product architecture
> - Each item should represent an end-to-end (frontend + backend) functional and testable feature
```

Effort scale:
- `XS`: 1 day
- `S`: 2-3 days
- `M`: 1 week
- `L`: 2 weeks
- `XL`: 3+ weeks

#### Important Constraints

- **Make roadmap actionable** - include effort estimates and dependencies
- **Priorities guided by mission** - When deciding on order, aim for the most direct path to achieving the mission as documented in mission.md
- **Ensure phases are achievable** - start with MVP, build incrementally


## Phase 4: Document Tech Stack

Create `agent-os/product/tech-stack.md` with a list of all tech stack choices that cover all aspects of this product's codebase.

### Creating the Tech Stack document

#### Step 1: Note User's Input Regarding Tech Stack

IF the user has provided specific information in the current conversation in regards to tech stack choices, these notes ALWAYS take precidence.  These must be reflected in your final `tech-stack.md` document that you will create.

#### Step 2: Gather User's Default Tech Stack Information

Reconcile and fill in the remaining gaps in the tech stack list by finding, reading and analyzing information regarding the tech stack.  Find this information in the following sources, in this order:

1. If user has provided their default tech stack under "User Standards & Preferences Compliance", READ and analyze this document.
2. If the current project has any of these files, read them to find information regarding tech stack choices for this codebase:
  - `claude.md`
  - `agents.md`

#### Step 3: Create the Tech Stack Document

Create `agent-os/product/tech-stack.md` and populate it with the final list of all technical stack choices, reconciled between the information the user has provided to you and the information found in provided sources.


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


### Standard: standards/global/coding-style.md

## Coding style best practices

- **Consistent Naming Conventions**: Establish and follow naming conventions for variables, functions, classes, and files across the codebase
- **Automated Formatting**: Maintain consistent code style (indenting, line breaks, etc.)
- **Meaningful Names**: Choose descriptive names that reveal intent; avoid abbreviations and single-letter variables except in narrow contexts
- **Small, Focused Functions**: Keep functions small and focused on a single task for better readability and testability
- **Consistent Indentation**: Use consistent indentation (spaces or tabs) and configure your editor/linter to enforce it
- **Remove Dead Code**: Delete unused code, commented-out blocks, and imports rather than leaving them as clutter
- **Backward compatibility only when required:** Unless specifically instructed otherwise, assume you do not need to write additional code logic to handle backward compatibility.
- **DRY Principle**: Avoid duplication by extracting common logic into reusable functions or modules


### Standard: standards/global/commenting.md

## Code commenting best practices

- **Self-Documenting Code**: Write code that explains itself through clear structure and naming
- **Minimal, helpful comments**: Add concise, minimal comments to explain large sections of code logic.
- **Don't comment changes or fixes**: Do not leave code comments that speak to recent or temporary changes or fixes. Comments should be evergreen informational texts that are relevant far into the future.


### Standard: standards/global/conventions.md

## General development conventions

- **Consistent Project Structure**: Organize files and directories in a predictable, logical structure that team members can navigate easily
- **Clear Documentation**: Maintain up-to-date README files with setup instructions, architecture overview, and contribution guidelines
- **Version Control Best Practices**: Use clear commit messages, feature branches, and meaningful pull/merge requests with descriptions
- **Environment Configuration**: Use environment variables for configuration; never commit secrets or API keys to version control
- **Dependency Management**: Keep dependencies up-to-date and minimal; document why major dependencies are used
- **Code Review Process**: Establish a consistent code review process with clear expectations for reviewers and authors
- **Testing Requirements**: Define what level of testing is required before merging (unit tests, integration tests, etc.)
- **Feature Flags**: Use feature flags for incomplete features rather than long-lived feature branches
- **Changelog Maintenance**: Keep a changelog or release notes to track significant changes and improvements


### Standard: standards/global/error-handling.md

## Error handling best practices

- **User-Friendly Messages**: Provide clear, actionable error messages to users without exposing technical details or security information
- **Fail Fast and Explicitly**: Validate input and check preconditions early; fail with clear error messages rather than allowing invalid state
- **Specific Exception Types**: Use specific exception/error types rather than generic ones to enable targeted handling
- **Centralized Error Handling**: Handle errors at appropriate boundaries (controllers, API layers) rather than scattering try-catch blocks everywhere
- **Graceful Degradation**: Design systems to degrade gracefully when non-critical services fail rather than breaking entirely
- **Retry Strategies**: Implement exponential backoff for transient failures in external service calls
- **Clean Up Resources**: Always clean up resources (file handles, connections) in finally blocks or equivalent mechanisms


### Standard: standards/global/tech-stack.md

---

## 📖 Extended Instructions

**IMPORTANT**: This workflow has additional instructions due to length constraints.

**You MUST read the extended instructions now** before proceeding:

Use the `view_file` tool to load the remaining instructions:

```python
view_file(
    AbsolutePath="/home/leonai-do/agent-os/.agent/extended/uads-plan-product.txt"
)
```

The extended file contains critical continuation of this workflow:

- Tech stack
- Framework & Runtime
- Frontend
- Database & Storage
- Testing & Quality
