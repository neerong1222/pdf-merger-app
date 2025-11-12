import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, allowed_file, validate_pdf

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.config['TEMP_FOLDER'] = 'test_temp'
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    import shutil
    if os.path.exists('test_uploads'):
        shutil.rmtree('test_uploads')
    if os.path.exists('test_temp'):
        shutil.rmtree('test_temp')

def test_allowed_file():
    """Test file type validation."""
    assert allowed_file('document.pdf') == True
    assert allowed_file('document.PDF') == True
    assert allowed_file('document.txt') == False
    assert allowed_file('document.exe') == False
    assert allowed_file('nofax') == False

def test_index(client):
    """Test home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'PDF Merger' in response.data

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_upload_no_files(client):
    """Test upload without files."""
    response = client.post('/api/upload')
    assert response.status_code == 400
    assert 'error' in response.json

def test_merge_insufficient_files(client):
    """Test merge with less than 2 files."""
    response = client.post('/api/merge',
        json={'files': ['file1.pdf'], 'output_name': 'output.pdf'}
    )
    assert response.status_code == 400

def test_cleanup_file(client):
    """Test cleanup endpoint."""
    response = client.post('/api/cleanup',
        json={'file_name': 'test.pdf'}
    )
    assert response.status_code == 200
    assert response.json['success'] == True

def test_invalid_content_type(client):
    """Test invalid content type."""
    response = client.post('/api/upload',
        data={'files': 'invalid'},
        content_type='application/json'
    )
    assert response.status_code in [400, 415]
