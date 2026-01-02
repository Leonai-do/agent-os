#!/bin/bash
# Convert Agent OS syntax to UADS mustache-like syntax

find .agent-os/workflows -type f -name "*.md" -exec sed -i \
  -e 's/{{workflows\/\([^}]*\)}}/{{ include "workflows\/\1.md" }}/g' \
  -e 's/{{standards\/\([^}]*\)}}/{{ inject "standards\/\1" }}/g' \
  -e 's/{{IF \([^}]*\)}}/{{ if \1 }}/g' \
  -e 's/{{ENDIF \([^}]*\)}}/{{ endif }}/g' \
  -e 's/{{UNLESS \([^}]*\)}}/{{ unless \1 }}/g' \
  -e 's/{{ENDUNLESS \([^}]*\)}}/{{ endunless }}/g' \
  {} \;

echo "✓ Converted Agent OS syntax to UADS mustache syntax"
