"""
Integration tests for API endpoints
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient

# Try to import FastAPI app
try:
    from app.main import app
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    app = None


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI app not available")
class TestFileUploadAPI:
    """Test file upload API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user"""
        return {
            "id": "user_123",
            "username": "testuser",
            "email": "test@example.com"
        }
    
    @pytest.fixture
    def sample_excel_file(self):
        """Create sample Excel file for testing"""
        content = b"mock excel content for testing"
        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        temp_file.write(content)
        temp_file.close()
        
        yield temp_file.name
        
        # Cleanup
        try:
            os.unlink(temp_file.name)
        except OSError:
            pass
    
    @patch('api.routes.files.get_current_user')
    @patch('api.routes.files.validate_file_size')
    @patch('api.routes.files.save_uploaded_file')
    @patch('api.routes.files.generate_file_id')
    @patch('api.routes.files.calculate_file_hash')
    def test_file_upload_success(
        self, 
        mock_hash, 
        mock_file_id, 
        mock_save, 
        mock_validate_size,
        mock_user_auth,
        client, 
        sample_excel_file, 
        mock_user
    ):
        """Test successful file upload"""
        # Mock dependencies
        mock_user_auth.return_value = mock_user
        mock_validate_size.return_value = None
        mock_file_id.return_value = "test_file_123"
        mock_hash.return_value = "d41d8cd98f00b204e9800998ecf8427e"
        mock_save.return_value = "/uploads/test_file_123.xlsx"
        
        with open(sample_excel_file, 'rb') as test_file:
            response = client.post(
                "/api/files/upload",
                files={"file": ("test.xlsx", test_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                headers={"Authorization": "Bearer mock_token"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        file_data = data["data"]
        assert file_data["file_id"] == "test_file_123"
        assert file_data["original_name"] == "test.xlsx"
        assert file_data["processing_status"] == "uploaded"
    
    @patch('api.routes.files.get_current_user')
    def test_file_upload_no_file(self, mock_user_auth, client, mock_user):
        """Test file upload with no file provided"""
        mock_user_auth.return_value = mock_user
        
        response = client.post(
            "/api/files/upload",
            files={},
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "No filename provided" in data["error"]["message"]
    
    @patch('api.routes.files.get_current_user')
    def test_file_upload_unsupported_type(self, mock_user_auth, client, mock_user):
        """Test file upload with unsupported file type"""
        mock_user_auth.return_value = mock_user
        
        response = client.post(
            "/api/files/upload",
            files={"file": ("test.txt", "content", "text/plain")},
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Unsupported file type" in data["error"]["message"]
    
    def test_get_supported_formats(self, client):
        """Test getting supported file formats"""
        response = client.get("/api/files/supported-formats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "input_formats" in data["data"]
        assert "output_formats" in data["data"]
        
        # Check for expected formats
        input_formats = {fmt["format"] for fmt in data["data"]["input_formats"]}
        assert "pdf" in input_formats
        assert "excel" in input_formats
        assert "csv" in input_formats
    
    @patch('api.routes.files.get_current_user')
    def test_validate_file_success(self, mock_user_auth, client, mock_user):
        """Test file validation with valid file"""
        mock_user_auth.return_value = mock_user
        
        response = client.post(
            "/api/files/validate-file",
            json={
                "file_name": "test.xlsx",
                "file_size": 1024000,
                "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            },
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["validation_details"]["file_type_supported"] is True
    
    @patch('api.routes.files.get_current_user')
    def test_process_file_success(self, mock_user_auth, client, mock_user):
        """Test successful file processing"""
        mock_user_auth.return_value = mock_user
        
        response = client.post(
            "/api/files/test_file_123/process",
            json={
                "extract_tables": True,
                "extract_images": False,
                "ocr_enabled": False
            },
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        file_data = data["data"]
        assert file_data["file_id"] == "test_file_123"
        assert file_data["processing_status"] == "completed"


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI app not available")
class TestComparisonAPI:
    """Test comparison API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user"""
        return {
            "id": "user_123",
            "username": "testuser",
            "email": "test@example.com"
        }
    
    @pytest.fixture
    def sample_comparison_request(self):
        """Sample comparison request data"""
        return {
            "file1_id": "file_123",
            "file2_id": "file_456",
            "comparison_options": {
                "tolerance_settings": {
                    "quantity": 0.1,
                    "unit_price": 0.01,
                    "amount": 0.01
                },
                "key_columns": ["description"],
                "ignore_columns": [],
                "case_sensitive": False
            }
        }
    
    @pytest.fixture
    def mock_file_data(self):
        """Mock file data for comparison"""
        return {
            "file_id": "file_123",
            "structured_data": [
                {
                    "type": "table",
                    "headers": ["description", "quantity", "unit_price", "amount"],
                    "rows": [
                        ["Product A", "10", "100.00", "1000.00"],
                        ["Product B", "5", "50.00", "250.00"]
                    ]
                }
            ],
            "metadata": {
                "processing_time": 2.5,
                "tables_extracted": 1
            }
        }
    
    @patch('api.routes.comparison.get_current_user')
    @patch('api.routes.comparison.DataComparator')
    @patch('api.routes.comparison._get_file_data')
    def test_compare_files_success(
        self, 
        mock_get_file, 
        mock_comparator_class, 
        mock_user_auth,
        client, 
        sample_comparison_request, 
        mock_file_data, 
        mock_user
    ):
        """Test successful file comparison"""
        # Setup mocks
        mock_user_auth.return_value = mock_user
        mock_get_file.side_effect = [mock_file_data, mock_file_data]
        
        # Mock comparator
        mock_comparator = Mock()
        mock_comparator.compare = AsyncMock(return_value={
            "comparison_id": "comp_123",
            "summary": {
                "total_rows_compared": 2,
                "matching_rows": 2,
                "different_rows": 0,
                "missing_rows": 0,
                "accuracy_rate": 100.0,
                "total_differences": 0,
                "comparison_time": 0.5
            },
            "differences": []
        })
        mock_comparator_class.return_value = mock_comparator
        
        response = client.post(
            "/api/comparison/compare",
            json=sample_comparison_request,
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        comparison_data = data["data"]
        assert comparison_data["comparison_id"] == "comp_123"
        assert comparison_data["summary"]["total_rows_compared"] == 2
        assert comparison_data["summary"]["accuracy_rate"] == 100.0
    
    @patch('api.routes.comparison.get_current_user')
    def test_compare_files_missing_ids(self, mock_user_auth, client, mock_user):
        """Test comparison with missing file IDs"""
        mock_user_auth.return_value = mock_user
        
        response = client.post(
            "/api/comparison/compare",
            json={"file1_id": "", "file2_id": "file_456"},
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Both file1_id and file2_id are required" in data["error"]["message"]
    
    @patch('api.routes.comparison.get_current_user')
    def test_compare_files_same_file(self, mock_user_auth, client, mock_user):
        """Test comparison with same file IDs"""
        mock_user_auth.return_value = mock_user
        
        response = client.post(
            "/api/comparison/compare",
            json={"file1_id": "file_123", "file2_id": "file_123"},
            headers={"Authorization": "Bearer mock_token"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Files must be different" in data["error"]["message"]
    
    def test_get_comparison_types(self, client):
        """Test getting available comparison types"""
        response = client.get("/api/comparison/comparison-types")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        
        # Check for expected comparison types
        type_names = [comp_type["type"] for comp_type in data["data"]]
        assert "products" in type_names
        assert "invoices" in type_names
        assert "contracts" in type_names
        assert "custom" in type_names
        
        # Check structure of comparison types
        for comp_type in data["data"]:
            assert "type" in comp_type
            assert "name" in comp_type
            assert "description" in comp_type
            assert "default_tolerances" in comp_type
            assert "recommended_fields" in comp_type


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI app not available")
class TestHealthAPI:
    """Test health check API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        with patch('psutil.cpu_percent', return_value=45.0), \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk:
            
            # Mock memory
            mock_memory.return_value.percent = 60.0
            
            # Mock disk
            mock_disk.return_value.percent = 70.0
            
            response = client.get("/api/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "system_info" in data
            assert "dependencies" in data
            assert "uptime" in data
            assert "version" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs_url" in data
        assert "health_url" in data