#!/usr/bin/env python3
"""
🧠 Advanced Documentation Mapper
Advanced code analysis and documentation mapping system

Author: Claude Code Assistant
Version: 1.0.0
"""

import os
import ast
import re
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class CodeComponent:
    """Represents a code component extracted from source files"""
    name: str
    type: str  # function, class, method, etc.
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    complexity: int = 0
    dependencies: List[str] = None
    metadata: Dict[str, Any] = None

class DocumentationMapper:
    """Advanced documentation mapping and analysis system"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.agent_dir = self.project_root / ".agent"
        self.components: List[CodeComponent] = []
        self.mappings = defaultdict(list)
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamps"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] 📚 {message}")
    
    def scan_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        for pattern in ["**/*.py"]:
            python_files.extend(self.project_root.glob(pattern))
        
        # Exclude common non-source directories
        exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}
        python_files = [
            f for f in python_files 
            if not any(exclude_dir in str(f) for exclude_dir in exclude_dirs)
        ]
        
        self.log(f"Found {len(python_files)} Python files")
        return python_files
    
    def scan_javascript_files(self) -> List[Path]:
        """Find all JavaScript files in the project"""
        js_files = []
        for pattern in ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx"]:
            js_files.extend(self.project_root.glob(pattern))
        
        exclude_dirs = {".git", "node_modules", "dist", "build"}
        js_files = [
            f for f in js_files 
            if not any(exclude_dir in str(f) for exclude_dir in exclude_dirs)
        ]
        
        self.log(f"Found {len(js_files)} JavaScript/TypeScript files")
        return js_files
    
    def analyze_python_file(self, file_path: Path) -> List[CodeComponent]:
        """Analyze a Python file and extract components"""
        components = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Extract classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    component = CodeComponent(
                        name=node.name,
                        type="class",
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node),
                        complexity=self.calculate_complexity(node),
                        dependencies=self.extract_dependencies(node)
                    )
                    components.append(component)
                
                elif isinstance(node, ast.FunctionDef):
                    component = CodeComponent(
                        name=node.name,
                        type="function",
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node),
                        complexity=self.calculate_complexity(node),
                        dependencies=self.extract_dependencies(node)
                    )
                    components.append(component)
                    
        except Exception as e:
            self.log(f"Error analyzing {file_path}: {e}", "ERROR")
        
        return components
    
    def analyze_javascript_file(self, file_path: Path) -> List[CodeComponent]:
        """Analyze a JavaScript file and extract components"""
        components = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract functions using regex
            function_patterns = [
                r'function\s+(\w+)\s*\(',
                r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'(\w+)\s*:\s*function\s*\(',
                r'async\s+function\s+(\w+)\s*\(',
                r'export\s+(?:default\s+)?function\s+(\w+)\s*\(',
                r'class\s+(\w+)',
                r'const\s+(\w+)\s*=\s*class\s*\{'
            ]
            
            for pattern in function_patterns:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    component_type = "class" if "class" in pattern else "function"
                    
                    component = CodeComponent(
                        name=match.group(1),
                        type=component_type,
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=line_num,
                        docstring=self.extract_js_docstring(content, match.start()),
                        complexity=self.estimate_js_complexity(content, match)
                    )
                    components.append(component)
                    
        except Exception as e:
            self.log(f"Error analyzing {file_path}: {e}", "ERROR")
        
        return components
    
    def calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for a node"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.With):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def extract_dependencies(self, node: ast.AST) -> List[str]:
        """Extract dependencies from a node"""
        dependencies = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dependencies.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    dependencies.append(child.func.attr)
        
        return list(set(dependencies))
    
    def extract_js_docstring(self, content: str, position: int) -> Optional[str]:
        """Extract JavaScript docstring near a function"""
        # Look for JSDoc comments before the function
        before_content = content[:position]
        lines = before_content.split('\n')
        
        # Check last few lines for JSDoc
        for line in reversed(lines[-5:]):
            if '/**' in line:
                # Extract JSDoc content
                docstart = before_content.rfind('/**')
                docend = before_content.find('*/', docstart)
                if docend != -1:
                    return before_content[docstart:docend+2].strip()
        
        return None
    
    def estimate_js_complexity(self, content: str, match) -> int:
        """Estimate JavaScript function complexity"""
        # Get the function content
        start = match.start()
        # Find the next opening brace
        brace_start = content.find('{', start)
        if brace_start == -1:
            return 1
        
        # Count braces to find function end
        brace_count = 0
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    function_content = content[brace_start:i+1]
                    break
        else:
            return 1
        
        # Count complexity keywords
        complexity_keywords = ['if', 'else', 'for', 'while', 'try', 'catch', '&&', '||']
        complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            complexity += function_content.count(keyword)
        
        return complexity
    
    def get_git_changes(self) -> Dict[str, List[str]]:
        """Get uncommitted git changes"""
        changes = {
            'added': [],
            'modified': [],
            'deleted': []
        }
        
        try:
            # Get git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    status = line[:2]
                    file_path = line[3:]
                    
                    if status == '??':
                        changes['added'].append(file_path)
                    elif status[0] in ['M', 'A']:
                        changes['modified'].append(file_path)
                    elif status[0] == 'D':
                        changes['deleted'].append(file_path)
                        
        except subprocess.SubprocessError as e:
            self.log(f"Error getting git changes: {e}", "ERROR")
        
        return changes
    
    def generate_component_documentation(self) -> str:
        """Generate documentation for all components"""
        doc_lines = [
            "# 🧠 Code Components Analysis",
            "",
            f"*Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## 📊 Summary",
            "",
            f"- **Total Components**: {len(self.components)}",
            f"- **Classes**: {len([c for c in self.components if c.type == 'class'])}",
            f"- **Functions**: {len([c for c in self.components if c.type == 'function'])}",
            f"- **Average Complexity**: {sum(c.complexity for c in self.components) / len(self.components):.1f}" if self.components else "- **Average Complexity**: 0",
            "",
            "---",
            ""
        ]
        
        # Group by type
        by_type = defaultdict(list)
        for component in self.components:
            by_type[component.type].append(component)
        
        for comp_type, components in by_type.items():
            doc_lines.extend([
                f"## {comp_type.title()}s",
                ""
            ])
            
            # Sort by file then line number
            components.sort(key=lambda c: (c.file_path, c.line_number))
            
            for component in components:
                doc_lines.extend([
                    f"### {component.name}",
                    f"**File:** `{component.file_path}:{component.line_number}`",
                    f"**Complexity:** {component.complexity}"
                ])
                
                if component.docstring:
                    # Clean up docstring
                    docstring = component.docstring.strip()
                    if len(docstring) > 200:
                        docstring = docstring[:200] + "..."
                    doc_lines.extend([
                        "**Documentation:**",
                        f"```",
                        docstring,
                        f"```"
                    ])
                
                if component.dependencies:
                    doc_lines.extend([
                        f"**Dependencies:** {', '.join(component.dependencies[:5])}"
                    ])
                    if len(component.dependencies) > 5:
                        doc_lines.append(f"*...and {len(component.dependencies) - 5} more*")
                
                doc_lines.extend(["", "---", ""])
        
        return '\n'.join(doc_lines)
    
    def generate_api_documentation(self) -> str:
        """Generate API documentation from backend code"""
        api_docs = [
            "# 🚪 Backend API Documentation",
            "",
            f"*Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## API Routes",
            ""
        ]
        
        # Look for FastAPI route definitions
        backend_files = list(self.project_root.glob("backend/**/*.py"))
        
        for file_path in backend_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find route decorators
                route_pattern = r'@(router|app)\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]'
                
                routes = re.findall(route_pattern, content)
                if routes:
                    api_docs.extend([
                        f"### {file_path.name}",
                        f"**Path:** `{file_path.relative_to(self.project_root)}`",
                        ""
                    ])
                    
                    for prefix, method, path in routes:
                        api_docs.extend([
                            f"#### {method.upper()} {path}",
                            ""
                        ])
                    
                    api_docs.extend(["", "---", ""])
                    
            except Exception as e:
                self.log(f"Error processing {file_path}: {e}", "ERROR")
        
        return '\n'.join(api_docs)
    
    def save_mappings(self):
        """Save mappings to JSON file"""
        mappings_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_components': len(self.components),
            'components': [
                {
                    'name': c.name,
                    'type': c.type,
                    'file_path': c.file_path,
                    'line_number': c.line_number,
                    'complexity': c.complexity,
                    'dependencies': c.dependencies,
                    'has_docstring': bool(c.docstring)
                }
                for c in self.components
            ]
        }
        
        self.agent_dir.mkdir(exist_ok=True)
        mappings_file = self.agent_dir / 'mappings' / 'component_mappings.json'
        
        with open(mappings_file, 'w', encoding='utf-8') as f:
            json.dump(mappings_data, f, indent=2)
        
        self.log(f"Component mappings saved to {mappings_file}")
    
    def run_full_analysis(self):
        """Run complete code analysis and documentation generation"""
        self.log("Starting comprehensive code analysis...")
        
        # Analyze Python files
        python_files = self.scan_python_files()
        for py_file in python_files:
            components = self.analyze_python_file(py_file)
            self.components.extend(components)
        
        # Analyze JavaScript files
        js_files = self.scan_javascript_files()
        for js_file in js_files:
            components = self.analyze_javascript_file(js_file)
            self.components.extend(components)
        
        self.log(f"Analyzed {len(python_files)} Python and {len(js_files)} JavaScript files")
        self.log(f"Found {len(self.components)} total components")
        
        # Generate documentation files
        self.agent_dir.mkdir(exist_ok=True)
        (self.agent_dir / 'reports').mkdir(exist_ok=True)
        (self.agent_dir / 'system').mkdir(exist_ok=True)
        (self.agent_dir / 'mappings').mkdir(exist_ok=True)
        
        # Save component documentation
        component_doc = self.generate_component_documentation()
        with open(self.agent_dir / 'reports' / 'code_analysis.md', 'w', encoding='utf-8') as f:
            f.write(component_doc)
        
        # Save API documentation
        api_doc = self.generate_api_documentation()
        with open(self.agent_dir / 'system' / 'api_analysis.md', 'w', encoding='utf-8') as f:
            f.write(api_doc)
        
        # Save git changes documentation
        changes = self.get_git_changes()
        if any(changes.values()):
            git_doc = self.generate_git_changes_doc(changes)
            with open(self.agent_dir / 'reports' / 'git_changes.md', 'w', encoding='utf-8') as f:
                f.write(git_doc)
        
        # Save mappings
        self.save_mappings()
        
        self.log("Analysis completed successfully!")
        
    def generate_git_changes_doc(self, changes: Dict[str, List[str]]) -> str:
        """Generate documentation for git changes"""
        doc_lines = [
            "# 📝 Git Changes Analysis",
            "",
            f"*Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## 📊 Summary",
            "",
            f"- **Added files:** {len(changes['added'])}",
            f"- **Modified files:** {len(changes['modified'])}",
            f"- **Deleted files:** {len(changes['deleted'])}",
            "",
            "---",
            ""
        ]
        
        if changes['added']:
            doc_lines.extend([
                "## 🆕 Added Files",
                ""
            ])
            for file_path in changes['added']:
                doc_lines.append(f"- `{file_path}`")
            doc_lines.extend(["", ""])
        
        if changes['modified']:
            doc_lines.extend([
                "## ✏️ Modified Files",
                ""
            ])
            for file_path in changes['modified']:
                doc_lines.append(f"- `{file_path}`")
            doc_lines.extend(["", ""])
        
        if changes['deleted']:
            doc_lines.extend([
                "## 🗑️ Deleted Files",
                ""
            ])
            for file_path in changes['deleted']:
                doc_lines.append(f"- `{file_path}`")
            doc_lines.extend(["", ""])
        
        return '\n'.join(doc_lines)

def main():
    """Main entry point"""
    import sys
    
    mapper = DocumentationMapper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            mapper.run_full_analysis()
        elif command == "git":
            changes = mapper.get_git_changes()
            git_doc = mapper.generate_git_changes_doc(changes)
            print(git_doc)
        elif command == "components":
            python_files = mapper.scan_python_files()
            js_files = mapper.scan_javascript_files()
            
            for py_file in python_files:
                components = mapper.analyze_python_file(py_file)
                mapper.components.extend(components)
            
            for js_file in js_files:
                components = mapper.analyze_javascript_file(js_file)
                mapper.components.extend(components)
            
            doc = mapper.generate_component_documentation()
            print(doc)
        else:
            print("Usage: python doc_mapper.py [analyze|git|components]")
    else:
        mapper.run_full_analysis()

if __name__ == "__main__":
    main()