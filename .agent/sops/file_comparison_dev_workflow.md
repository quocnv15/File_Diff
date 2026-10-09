# File Comparison Development Workflow

## 🚀 Quick Start

### Daily Context Setup (5 minutes)
```bash
# 1. Read project context
cat .agent/readme.md

# 2. Check system status
cd backend && python -c "import uvicorn; print('Backend OK')"
cd ../frontend && echo "Frontend files ready"

# 3. Verify storage structure
ls -la backend/storage/{uploads,processed,exports}
```

### Environment Activation
```bash
# Backend environment
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Frontend (static file serving)
cd ../frontend
# No build process required - direct file serving
```

## 📋 Feature Development Process

### 1. Planning Phase
```bash
# Always start with context reading
cat .agent/readme.md && cat .agent/system/project_architecture.md

# Plan feature implementation
# Define: requirements, architecture, files, API endpoints, UI components
```

**Essential Checklist:**
- [ ] Read project docs for context
- [ ] Define clear requirements
- [ ] Choose: Backend API / Frontend UI / File Processor
- [ ] Plan file structure and dependencies
- [ ] Design API endpoints (if needed)
- [ ] Sketch UI components (if needed)

### 2. Backend Development

**File Structure Setup:**
```bash
# API endpoints
touch backend/api/routes/[feature].py

# File processors
touch backend/processors/[feature]_processor.py

# Comparison logic
touch backend/comparators/[feature]_comparator.py
```

**Implementation Order:**
1. **Models**: Pydantic schemas in `app/models.py`
2. **Processing**: File/data handling logic
3. **API**: FastAPI endpoints with validation
4. **Error Handling**: Comprehensive error management
5. **Tests**: Unit and integration tests

### 3. Frontend Development

**File Structure Setup:**
```bash
# JavaScript modules
touch frontend/scripts/[feature].js

# Styling
touch frontend/styles/[feature].css

# Components (if needed)
touch frontend/components/[feature].html
```

**Implementation Order:**
1. **HTML**: Structure and semantic markup
2. **CSS**: Responsive styling and design
3. **JavaScript**: Functionality and API integration
4. **UX**: Loading states, error handling, accessibility
5. **Testing**: Manual and automated testing

## 🧪 Testing & Quality Assurance

### Backend Testing
```bash
cd backend && source venv/bin/activate

# Test specific functionality
python test_[feature].py

# Full backend test suite
python test_backend.py

# Sample file processing tests
python test_sample_files.py
```

### Frontend Testing
```bash
cd frontend

# Manual testing in browser
# Open index.html and test functionality

# Automated integration tests (if available)
node test_integration.js
```

### Full System Test
```bash
# Complete system validation
python run_project.py --test-only

# Full application run
python run_project.py
```

## ✅ Quality Standards

### Backend Requirements
- [ ] **Type hints** on all functions
- [ ] **Async/await** for I/O operations
- [ ] **Error handling** with proper HTTP status codes
- [ ] **Input validation** using Pydantic models
- [ ] **Memory efficiency** for file processing
- [ ] **Comprehensive tests** covering edge cases

### Frontend Requirements
- [ ] **Modular code** with reusable components
- [ ] **Responsive design** (mobile-first)
- [ ] **Error states** with user-friendly messages
- [ ] **Loading indicators** for async operations
- [ ] **Cross-browser compatibility**
- [ ] **Accessibility** (ARIA labels, keyboard navigation)

## 🏗 Code Patterns

### Backend Patterns
```python
# File Processor Structure
class FileTypeProcessor:
    def __init__(self):
        self.supported_extensions = ['.ext']

    async def process_file(self, file_path: str) -> ProcessedData:
        # File validation and processing
        pass

    def validate_file(self, file_path: str) -> bool:
        # File format validation
        pass

# API Endpoint Structure
@router.post("/endpoint")
async def function_name(
    request: RequestModel,
    background_tasks: BackgroundTasks
) -> ResponseModel:
    # Async processing with proper error handling
    pass
```

### Frontend Patterns
```javascript
// Module Structure
class FeatureModule {
    constructor() {
        this.apiEndpoint = '/api/endpoint';
        this.loading = false;
    }

    async processData(params) {
        // Async API calls with error handling
        try {
            this.setLoading(true);
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                body: JSON.stringify(params)
            });
            return await response.json();
        } catch (error) {
            this.handleError(error);
        } finally {
            this.setLoading(false);
        }
    }
}
```

## 🚀 Quick Commands

### Development Commands
```bash
# Start backend server
cd backend && source venv/bin/activate && python main.py

# Test file processing
python test_sample_processing.py

# Run full system
python run_project.py
```

### File Management
```bash
# Clean storage directories
rm -rf backend/storage/{uploads,processed,exports}/*

# Check file permissions
ls -la backend/storage/

# Create test files
python create_test_samples.py
```

## 📚 Reference Documentation
- **Architecture**: `system/project_architecture.md`
- **API Reference**: `system/api_endpoints.md`
- **File Processing**: `system/file_processing.md`
- **AI Integration**: `sops/ai_tools_integration.md`
- **Feature Template**: `templates/file_comparison_feature_template.md`