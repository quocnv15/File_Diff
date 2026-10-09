# AI Tools Integration Guide

## 🤖 Claude Code Setup

### Environment Configuration
```bash
# Claude Code is already integrated
# Main context files:
.claude/.agent/readme.md           # Documentation index
.claude/.agent/system/             # System architecture
.claude/.agent/sops/               # Development workflows
.claude/.agent/templates/          # Code templates
```

### VS Code Configuration
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "files.associations": {
    "*.py": "python",
    "*.js": "javascript"
  },
  "editor.formatOnSave": true,
  "editor.tabSize": 4,
  "python.terminal.activateEnvironment": true
}
```

## 🎯 AI-Assisted Development Workflow

### Context Templates
```bash
# Standard project context for Claude
"I'm working on File Comparison system (Vietnamese web app for comparing Excel/PDF/CSV files).
Tech stack: Python FastAPI backend + vanilla JavaScript frontend.
Current goal: [specific task]
Please follow existing patterns in the codebase."
```

## 💡 Development Prompts

### Backend Development
```bash
# API Endpoints
"Create FastAPI endpoint for [functionality] with validation, error handling, and async support"

# File Processors
"Implement [file_type] processor for data extraction, validation, and normalization"

# Comparison Logic
"Design comparison algorithm for [data_type] with configurable sensitivity"
```

### Frontend Development
```bash
# UI Components
"Create responsive component for [functionality] with loading states and accessibility"

# API Integration
"Implement JavaScript module for [endpoint] with error handling and user feedback"

# File Handling
"Create file upload interface with progress tracking and validation"
```

## 🔍 Code Quality & Review

### Automated Review Checklist
```bash
"Review this code for:
✓ Code quality and best practices
✓ Performance optimization
✓ Error handling completeness
✓ Documentation adequacy
✓ Testing coverage
✓ Consistency with project patterns"
```

### Best Practices for AI Assistance
- **Context First**: Always reference existing documentation
- **Specific Prompts**: Provide detailed, context-aware requests
- **Pattern Matching**: Ask to follow existing code patterns
- **Error Handling**: Always request comprehensive error management
- **Performance**: Ask for memory-efficient implementations
- **Testing**: Include testing requirements in prompts

## 📝 Template Prompts

### Backend Template
```bash
"Create FastAPI endpoint with:
- Pydantic request/response models
- Async implementation
- Comprehensive error handling
- Input validation
- Proper HTTP status codes
- API documentation"
```

### Frontend Template
```bash
"Create JavaScript module with:
- Class-based architecture
- Async API integration
- Error handling
- Loading states
- Event handling
- Responsive design"
```

## 🎯 Essential Context

### Always Include This Context
```bash
"Project: File Comparison System (Vietnamese web app)
Tech: Python FastAPI + vanilla JavaScript
Purpose: Compare Excel/PDF/CSV files with diff visualization
Current task: [specific requirement]
Please follow existing code patterns."
```

### Development Rules
1. **Read docs first** - `.agent/readme.md`
2. **Check existing patterns** - Similar implementations
3. **Follow architecture** - Reference `system/project_architecture.md`
4. **Maintain consistency** - Use established conventions

## 📚 Quick Reference
- **Development Workflow**: `sops/file_comparison_dev_workflow.md`
- **Project Architecture**: `system/project_architecture.md`
- **API Reference**: `system/api_endpoints.md`
- **Feature Template**: `templates/file_comparison_feature_template.md`