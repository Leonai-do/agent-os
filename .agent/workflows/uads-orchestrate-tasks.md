---
description: Orchestrate implementation of a spec through structured task execution
---

Now that we have a spec and tasks list ready for implementation, we will proceed with orchestrating implementation of each task group using this process.

## Phase 1: Get tasks.md for this spec

**IF you already know which spec we're working on** and that spec folder has a `tasks.md` file, use that and skip to Phase 2.

**IF you don't know which spec** or it doesn't have a `tasks.md`, output the following request:

```
Please point me to a spec's tasks.md that you want to orchestrate implementation for.

If you don't have one yet, then run any of these commands first:
/uads-shape-spec
/uads-write-spec
/uads-create-tasks
```

## Phase 2: Create orchestration.yml

In this spec's folder, create: `agent-os/specs/[this-spec]/orchestration.yml`

Populate it with the names of each task group found in this spec's `tasks.md` using this EXACT structure:

```yaml
task_groups:
  - name: [task-group-name]
  - name: [task-group-name]
  - name: [task-group-name]
  # Repeat for each task group found in tasks.md
```

## Phase 3: Assign standards to each task group

Ask the user to specify which standards should guide the implementation of each task group:

```
Please specify the standard(s) that should be used to guide the implementation of each task group:

1. [task-group-name]
2. [task-group-name]
3. [task-group-name]
[repeat for each task-group]

For each task group number, you can specify any combination of:

"all" to include all standards
"global/*" to include all files inside standards/global
"frontend/css.md" to include specific standard
"none" to include no standards
```

Using the user's responses, update `orchestration.yml`:

```yaml
task_groups:
  - name: [task-group-name]
    standards:
      - [user's 1st response for this task group]
      - [user's 2nd response for this task group]
  - name: [task-group-name]
    standards:
      - [user's response]
  # Repeat for each task group
```

Example final `orchestration.yml`:

```yaml
task_groups:
  - name: authentication-system
    standards:
      - all
  - name: user-dashboard
    standards:
      - global/*
      - frontend/components.md
      - frontend/css.md
  - name: api-endpoints
    standards:
      - backend/*
      - global/error-handling.md
```

## Phase 4: Generate Implementation Prompts

Generate an ordered series of prompt texts for each task group in `agent-os/specs/[this-spec]/implementation/prompts/`.

**LOOP through EACH task group** and create a markdown file with prompt text:

### Step 1: Create the prompt markdown file

Use this naming convention:  
`agent-os/specs/[this-spec]/implementation/prompts/[task-group-number]-[task-group-title].md`

Example: If the 3rd task group is "Comment System" → create `3-comment-system.md`

### Step 2: Populate the prompt file

Use this template (replace bracketed content):

```markdown
We're continuing our implementation of [spec-title] by implementing task group number [task-group-number]:

## Implement this task and its sub-tasks:

[paste entire task group including parent task, all sub-tasks, and sub-bullet points]

## Understand the context

Read @agent-os/specs/[this-spec]/spec.md to understand the context for this spec and where the current task fits into it.

Also read these for further context:

- @agent-os/specs/[this-spec]/planning/requirements.md
- @agent-os/specs/[this-spec]/planning/visuals

## Perform the implementation

Implement all tasks assigned to you and ONLY those task(s) that have been assigned to you.

## Implementation process:

1. Analyze the provided spec.md, requirements.md, and visuals (if any)
2. Analyze patterns in the codebase according to its built-in workflow
3. Implement the assigned task group according to requirements and standards
4. Update `agent-os/specs/[this-spec]/tasks.md` to update the tasks you've implemented to mark that as done by updating their checkbox to checked state: `- [x]`

## Guide your implementation using:
- **The existing patterns** that you've found and analyzed in the codebase.
- **Specific notes provided in requirements.md, spec.md AND/OR tasks.md**
- **Visuals provided (if any)** which would be located in `agent-os/specs/[this-spec]/planning/visuals/`
- **User Standards & Preferences** which are defined below.

## Self-verify and test your work by:
- Running ONLY the tests you've written (if any) and ensuring those tests pass.
- IF your task involves user-facing UI, and IF you have access to browser testing tools, open a browser and use the feature you've implemented as if you are a user to ensure a user can use the feature in the intended way.
  - Take screenshots of the views and UI elements you've tested and store those in `agent-os/specs/[this-spec]/verification/screenshots/`.  Do not store screenshots anywhere else in the codebase other than this location.
  - Analyze the screenshot(s) you've taken to check them against your current requirements.


## User Standards & Preferences Compliance

IMPORTANT: Ensure that your implementation work is ALIGNED and DOES NOT CONFLICT with the user's standards:

[Insert standards from orchestration.yml for this task group]
```

### Step 3: Output the created prompts

Output to user:

```
Ready to begin implementation of [spec-title]!

Use the following list of prompts to direct the implementation of each task group:

[list prompt files in order]

Input those prompts into this chat one-by-one or queue them to run in order.

Progress will be tracked in agent-os/specs/[this-spec]/tasks.md
```

## Using External Skills

When specialized capabilities are needed, invoke skills through the `skillz` MCP server:

- `mcp_skillz_frontend-design` — UI design tasks
- `mcp_skillz_git-sync` — Git operations

**Execution Protocol:**

1. **Primary**: Call the MCP tool directly
2. **Fallback**: Skill location: `/home/leonai-do/Host-D-Drive/LeonAI_DO/dev/Agent-Skills/skills-repository`
