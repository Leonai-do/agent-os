#!/usr/bin/env python3
"""
UADS Compiler - Compiles UADS commands to Antigravity workflows
Supports mustache-like syntax: {{ include "..." }}, {{ inject "..." }}
Automatically splits files exceeding 12,000 character limit
"""

import os
import re
import sys
import yaml
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Antigravity workflow character limit
CHARACTER_LIMIT = 12000

class UADSCompiler:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.uads_dir = self.project_root / ".agent-os"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load UADS configuration"""
        config_path = self.uads_dir / "config.yml"
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def compile_all(self):
        """Compile all commands to Antigravity format"""
        commands_dir = self.uads_dir / "commands"
        if not commands_dir.exists():
            print(f"❌ Commands directory not found: {commands_dir}")
            return
        
        # Get target output directory
        target = self.config.get('target', {})
        output_dir = self.project_root / target.get('output_dir', '.agent/workflows')
        
        # Clean output directories if configured
        if self.config.get('compile', {}).get('clean', True):
            for d in [output_dir, self.project_root / ".agent" / "extended"]:
                if d.exists():
                    import shutil
                    shutil.rmtree(d)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Compile each command
        compiled_count = 0
        for command_file in sorted(commands_dir.glob("*-uads-*.md")):
            output_file = output_dir / command_file.name
            if self.compile_command(command_file, output_file):
                compiled_count += 1
        
        print(f"\n✅ Compiled {compiled_count} commands to {output_dir}")
        return compiled_count
    
    def compile_command(self, source: Path, target: Path) -> bool:
        """Compile a single command file, splitting if necessary"""
        try:
            print(f"📝 Compiling {source.name}...", end=" ")
            
            with open(source, 'r') as f:
                content = f.read()
            
            # Process the content
            compiled = self._process_content(content)
            
            # Check if splitting is needed
            if len(compiled) > CHARACTER_LIMIT:
                self._split_and_write(compiled, target, source.stem)
                print(f"✓ (split: {len(compiled):,} chars)")
            else:
                # Write as single file
                with open(target, 'w') as f:
                    f.write(compiled)
                print(f"✓ ({len(compiled):,} chars)")
            
            return True
            
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def _split_and_write(self, content: str, target: Path, command_name: str):
        """Split large file into main + extended files"""
        # Extract frontmatter
        frontmatter_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            body = content[len(frontmatter):]
        else:
            frontmatter = ""
            body = content
        
        # Find a good split point (try to split at section boundary)
        # Aim for ~11,000 chars to leave headroom
        split_target = 11000 - len(frontmatter)
        split_point = self._find_split_point(body, split_target)
        
        # Split content
        main_body = body[:split_point]
        extended_body = body[split_point:]
        
        # Create extended folder (separate from workflows to avoid being treated as commands)
        extended_dir = self.project_root / ".agent" / "extended"
        extended_dir.mkdir(parents=True, exist_ok=True)
        
        # Write extended content with .txt extension to avoid being treated as markdown command
        extended_file = extended_dir / f"{command_name}.txt"
        with open(extended_file, 'w') as f:
            f.write(extended_body.strip())
        
        # Create main file with read instruction
        main_content = frontmatter + main_body.rstrip() + "\n\n"
        main_content += "---\n\n"
        main_content += "## 📖 Extended Instructions\n\n"
        main_content += f"**IMPORTANT**: This workflow has additional instructions due to length constraints.\n\n"
        main_content += f"**You MUST read the extended instructions now** before proceeding:\n\n"
        main_content += f"Use the `view_file` tool to load the remaining instructions:\n\n"
        main_content += f"```python\n"
        main_content += f"view_file(\n"
        main_content += f"    AbsolutePath=\"{extended_file.absolute()}\"\n"
        main_content += f")\n"
        main_content += f"```\n\n"
        main_content += f"The extended file contains critical continuation of this workflow:\n"
        main_content += self._generate_extended_preview(extended_body)
        
        # Write main file
        with open(target, 'w') as f:
            f.write(main_content)
    
    def _find_split_point(self, text: str, target: int) -> int:
        """Find a good split point near target position (at section boundary)"""
        # Look for markdown headers near the target
        window = 500  # Search window
        search_start = max(0, target - window)
        search_end = min(len(text), target + window)
        search_text = text[search_start:search_end]
        
        # Find all headers in the window
        headers = list(re.finditer(r'\n## ', search_text))
        
        if headers:
            # Use the header closest to target
            best_header = min(headers, key=lambda m: abs(m.start() - (target - search_start)))
            return search_start + best_header.start() + 1  # +1 to keep the newline
        
        # No header found, split at paragraph
        paragraphs = list(re.finditer(r'\n\n', search_text))
        if paragraphs:
            best_para = min(paragraphs, key=lambda m: abs(m.start() - (target - search_start)))
            return search_start + best_para.start() + 2  # +2 to skip double newline
        
        # Fallback: split at target
        return target
    
    def _generate_extended_preview(self, extended_text: str) -> str:
        """Generate a preview of what's in the extended file"""
        # Find first few headers
        headers = re.findall(r'^##+ (.+)$', extended_text, re.MULTILINE)[:5]
        if headers:
            preview = "\n".join(f"- {h}" for h in headers)
            return f"\n{preview}\n"
        return "\n- Additional workflow steps and instructions\n"
    
    def _process_content(self, content: str) -> str:
        """Process mustache-like template syntax"""
        # Process includes first (since they may contain injects)
        content = self._process_includes(content)
        
        # Process injects (standards)
        content = self._process_injects(content)
        
        # Process conditionals (if any remain)
        content = self._process_conditionals(content)
        
        return content
    
    def _process_includes(self, content: str) -> str:
        """Process {{ include "path.md" }} directives"""
        pattern = r'\{\{\s*include\s+"([^"]+)"\s*\}\}'
        
        def replace_include(match):
            include_path = match.group(1)
            file_path = self.uads_dir / include_path
            
            if not file_path.exists():
                return f"\n⚠️ Warning: Include file not found: {include_path}\n"
            
            try:
                with open(file_path, 'r') as f:
                    included_content = f.read()
                
                # Recursively process included content
                return self._process_content(included_content)
            except Exception as e:
                return f"\n⚠️ Error including {include_path}: {e}\n"
        
        return re.sub(pattern, replace_include, content)
    
    def _process_injects(self, content: str) -> str:
        """Process {{ inject "pattern" }} directives for standards"""
        pattern = r'\{\{\s*inject\s+"([^"]+)"\s*\}\}'
        
        def replace_inject(match):
            inject_pattern = match.group(1)
            standards_dir = self.uads_dir / "standards"
            
            # Convert pattern to glob pattern
            if inject_pattern.endswith('/*'):
                glob_pattern = inject_pattern
            elif inject_pattern == 'standards/*':
                glob_pattern = '**/*'
            else:
                glob_pattern = inject_pattern
            
            # Find matching files
            matches = []
            search_path = standards_dir / glob_pattern.replace('standards/', '')
            
            if '*' in glob_pattern:
                # Wildcard pattern
                for file_path in standards_dir.rglob('*.md'):
                    rel_path = file_path.relative_to(self.uads_dir)
                    if self._matches_pattern(str(rel_path), inject_pattern):
                        matches.append(file_path)
            else:
                # Specific file
                file_path = self.uads_dir / inject_pattern
                if file_path.exists():
                    matches.append(file_path)
            
            if not matches:
                return f"\n⚠️ No standards found matching: {inject_pattern}\n"
            
            # Read and concatenate all matched files
            injected_content = []
            for file_path in sorted(matches):
                try:
                    with open(file_path, 'r') as f:
                        rel_path = file_path.relative_to(self.uads_dir)
                        injected_content.append(f"\n### Standard: {rel_path}\n")
                        injected_content.append(f.read())
                except Exception as e:
                    injected_content.append(f"\n⚠️ Error reading {file_path}: {e}\n")
            
            return '\n'.join(injected_content)
        
        return re.sub(pattern, replace_inject, content)
    
    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Check if a path matches a glob pattern"""
        # Simple pattern matching
        if pattern == 'standards/*':
            return path.startswith('standards/')
        
        if pattern.endswith('/*'):
            base = pattern[:-2]
            return path.startswith(base + '/')
        
        return path == pattern
    
    def _process_conditionals(self, content: str) -> str:
        """Process {{ if flag }} and {{ unless flag }} conditionals (basic support)"""
        # For now, just remove conditional blocks since we don't use them in UADS
        # This is a placeholder for future conditional logic if needed
        
        # Remove {{ if ... }} blocks (keep content for now)
        content = re.sub(r'\{\{\s*if\s+\w+\s*\}\}', '', content)
        content = re.sub(r'\{\{\s*endif\s*\}\}', '', content)
        
        # Remove {{ unless ... }} blocks (remove content)
        content = re.sub(r'\{\{\s*unless\s+\w+\s*\}\}.*?\{\{\s*endunless\s*\}\}', '', content, flags=re.DOTALL)
        
        return content


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("UADS Compiler - Universal Agent Directory Standard")
        print("\nUsage:")
        print("  uads compile [--project-root PATH]  Compile all commands")
        print("  uads help                           Show this help")
        return
    
    command = sys.argv[1]
    
    if command == "help":
        print("UADS Compiler v1.0.0")
        print("\nCommands:")
        print("  compile    Compile UADS commands to Antigravity workflows")
        print("  help       Show this help message")
        return
    
    if command == "compile":
        # Get project root
        project_root = os.getcwd()
        if '--project-root' in sys.argv:
            idx = sys.argv.index('--project-root')
            if idx + 1 < len(sys.argv):
                project_root = sys.argv[idx + 1]
        
        print(f"🚀 UADS Compiler")
        print(f"📁 Project: {project_root}\n")
        
        try:
            compiler = UADSCompiler(project_root)
            compiler.compile_all()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        print("Run 'uads help' for usage information")


if __name__ == "__main__":
    main()
