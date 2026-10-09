# 📚 Documentation Update System - User Guide

## 🎯 Overview

The Documentation Update System consists of two powerful tools designed to automatically map source code changes and uncommitted files to the `.agent` directory for comprehensive project documentation.

## 🛠️ Available Tools

### 1. `update-doc` (Bash Script)
**Purpose:** Quick documentation updates and git change mapping  
**Best for:** Fast operations, simple documentation tasks

### 2. `doc_mapper.py` (Python Script)  
**Purpose:** Advanced code analysis and component mapping  
**Best for:** Deep code analysis, complexity metrics, dependency tracking

## 🚀 Quick Start

### Initialize Documentation System
```bash
# Initialize .agent directory structure
./update-doc init

# Run full documentation analysis
./update-doc sync --force

# Check documentation status
./update-doc status
```

### Advanced Code Analysis
```bash
# Run comprehensive code analysis
python3 doc_mapper.py analyze

# Show git changes only
python3 doc_mapper.py git

# Show component analysis only  
python3 doc_mapper.py components
```

## 📋 Command Reference

### update-doc Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize .agent structure | `./update-doc init` |
| `scan` | Map source code to docs | `./update-doc scan --dry-run` |
| `git-changes` | Map uncommitted changes | `./update-doc git-changes` |
| `api-docs` | Generate API documentation | `./update-doc api-docs --verbose` |
| `architecture` | Update architecture docs | `./update-doc architecture` |
| `sync` | Full synchronization | `./update-doc sync --force` |
| `clean` | Clean temporary files | `./update-doc clean` |
| `status` | Show documentation status | `./update-doc status` |

### doc_mapper.py Commands

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Full code analysis | `python3 doc_mapper.py analyze` |
| `git` | Git changes analysis | `python3 doc_mapper.py git` |
| `components` | Component analysis only | `python3 doc_mapper.py components` |

## 🗂️ Generated Documentation Structure

```
.agent/
├── readme.md                           # Main documentation index
├── system/                             # System documentation
│   ├── api_documentation.md           # API routes documentation
│   ├── processors.md                  # File processors documentation
│   ├── data_models.md                 # Data models documentation
│   ├── frontend_scripts.md            # Frontend components documentation
│   ├── frontend_styles.md             # CSS styles documentation
│   ├── architecture_current.md        # Current architecture
│   ├── api_analysis.md                # Advanced API analysis (Python)
│   └── openapi_spec.json              # OpenAPI specification
├── reports/                            # Analysis reports
│   ├── uncommitted_changes.md         # Git changes report
│   ├── code_analysis.md               # Code components analysis
│   └── git_changes.md                 # Git changes analysis (Python)
├── mappings/                           # Code-to-documentation mappings
│   ├── file_map.json                  # File mapping structure
│   └── component_mappings.json        # Component mappings (Python)
├── sops/                              # Standard Operating Procedures
├── templates/                         # Documentation templates
├── tasks/                             # Feature documentation
└── logs/                              # Documentation logs
```

## 🔄 Typical Workflow

### 1. Initial Setup
```bash
# Clone or navigate to project
cd /Volumes/Workspace/1-SideProject/File_Diff

# Initialize documentation system
./update-doc init

# Run initial full analysis
./update-doc sync --force
```

### 2. Daily Development Workflow
```bash
# After making code changes
./update-doc git-changes

# Update specific components
./update-doc scan

# Generate updated API docs (if backend changed)
./update-doc api-docs
```

### 3. Comprehensive Analysis (Weekly)
```bash
# Run deep code analysis
python3 doc_mapper.py analyze

# Full documentation sync
./update-doc sync --force

# Check status
./update-doc status
```

### 4. Pre-commit Documentation
```bash
# Document current changes
./update-doc git-changes

# Advanced analysis if needed
python3 doc_mapper.py analyze

# Review generated documentation
ls -la .agent/reports/
```

## 📊 Advanced Features

### Code Complexity Analysis
The Python mapper provides:
- **Cyclomatic Complexity**: Measures code complexity
- **Dependency Tracking**: Identifies function/class dependencies  
- **Documentation Coverage**: Shows which components have docstrings
- **Component Statistics**: Total classes, functions, average complexity

### Git Integration
- **Uncommitted Changes**: Automatic mapping of new/modified/deleted files
- **File Previews**: Content previews for new text files
- **Change Summaries**: Statistics on changes made
- **Timestamp Tracking**: When changes were documented

### API Documentation
- **Route Detection**: Automatic discovery of FastAPI endpoints
- **OpenAPI Integration**: Fetches specs from running backend
- **Interactive Docs**: Links to Swagger/ReDoc interfaces
- **Endpoint Categorization**: Groups routes by functionality

## 🎯 Use Cases

### 1. New Feature Development
```bash
# After implementing a new feature
./update-doc scan
./update-doc git-changes

# Document the new components
python3 doc_mapper.py analyze
```

### 2. Code Review Preparation
```bash
# Generate comprehensive documentation
./update-doc sync --force
python3 doc_mapper.py analyze

# Review component changes
cat .agent/reports/code_analysis.md
```

### 3. Project Handover
```bash
# Complete documentation generation
./update-doc sync --force
python3 doc_mapper.py analyze

# Create documentation package
tar -czf documentation_$(date +%Y%m%d).tar.gz .agent/
```

### 4. Architecture Review
```bash
# Update architecture documentation
./update-doc architecture

# Review component structure
cat .agent/system/architecture_current.md
```

## 🔧 Customization

### Adding New Documentation Types
Edit `update-doc` script to add new mapping functions:
```bash
# Add new mapping function
map_custom_component() {
    # Your custom mapping logic
}
```

### Extending Python Analysis
Modify `doc_mapper.py` to add new analysis features:
```python
def custom_analysis(self, file_path: Path) -> List[CodeComponent]:
    # Your custom analysis logic
    pass
```

## 🚨 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x update-doc doc_mapper.py
   ```

2. **Git Not Found**
   ```bash
   # Install git or skip git-related features
   ./update-doc scan  # instead of git-changes
   ```

3. **Python Not Found**
   ```bash
   # Use python instead of python3
   python doc_mapper.py analyze
   ```

4. **Backend Not Running for API Docs**
   ```bash
   # Start backend first
   cd backend && python main.py
   # Then run API docs generation
   ./update-doc api-docs
   ```

### Debug Mode
```bash
# Enable verbose output
./update-doc sync --verbose

# Dry run mode (no changes made)
./update-doc scan --dry-run
```

## 📈 Best Practices

1. **Run Before Commits**: Always document changes before committing
2. **Regular Sync**: Run full sync weekly to keep docs current
3. **Review Generated Docs**: Check accuracy of automatically generated content
4. **Version Control**: Commit documentation files along with code
5. **Team Communication**: Share documentation status with team members

## 🔗 Integration with Development Workflow

### Pre-commit Hook (Optional)
```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
./update-doc git-changes
python3 doc_mapper.py analyze
git add .agent/
```

### CI/CD Pipeline Integration
```yaml
# Example GitHub Actions step
- name: Update Documentation
  run: |
    ./update-doc sync --force
    python3 doc_mapper.py analyze
    git add .agent/
```

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Run `./update-doc status` for diagnostics
3. Review generated logs in `.agent/logs/`
4. Test with `--dry-run` flag first

**Remember**: This system is designed to enhance, not replace, good documentation practices. Always review and supplement automatically generated documentation with human insights.