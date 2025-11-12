import os
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import PyPDF2
import io
from collections import defaultdict

# Load environment variables
load_dotenv()

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['TEMP_FOLDER'] = os.getenv('TEMP_FOLDER', 'temp')

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Rate limiting storage (in-memory, for production use Redis)
rate_limit_store = defaultdict(list)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Validate file extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_pdf(file_path):
    """Validate that the file is a valid PDF."""
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            # Try to read pages to verify integrity
            _ = len(pdf_reader.pages)
        return True
    except Exception as e:
        logger.error(f"PDF validation failed: {str(e)}")
        return False

def rate_limit(max_requests=100, window_seconds=3600):
    """Rate limiting decorator."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if os.getenv('RATE_LIMIT_ENABLED', 'true').lower() != 'true':
                return f(*args, **kwargs)
            
            client_ip = request.remote_addr
            now = datetime.now()
            cutoff_time = now - timedelta(seconds=window_seconds)
            
            # Clean old requests
            rate_limit_store[client_ip] = [
                req_time for req_time in rate_limit_store[client_ip]
                if req_time > cutoff_time
            ]
            
            # Check rate limit
            if len(rate_limit_store[client_ip]) >= max_requests:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            rate_limit_store[client_ip].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
@rate_limit(max_requests=100, window_seconds=3600)
def upload_files():
    """Handle PDF file uploads."""
    try:
        # Validate request
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400
        
        if len(files) > 100:
            return jsonify({'error': 'Maximum 100 files allowed'}), 400
        
        uploaded_files = []
        total_size = 0
        
        for file in files:
            # Validate filename
            if file.filename == '':
                continue
            
            if not allowed_file(file.filename):
                logger.warning(f"Invalid file type: {file.filename}")
                return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            total_size += file_size
            
            if total_size > app.config['MAX_CONTENT_LENGTH']:
                logger.warning(f"Total file size exceeds limit")
                return jsonify({'error': 'Total file size exceeds limit'}), 413
            
            # Secure filename
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(filepath)
            
            # Validate PDF
            if not validate_pdf(filepath):
                os.remove(filepath)
                logger.error(f"Invalid PDF file: {filename}")
                return jsonify({'error': f'Invalid PDF file: {filename}'}), 400
            
            uploaded_files.append({
                'original_name': filename,
                'stored_name': unique_filename,
                'size': file_size
            })
            logger.info(f"File uploaded: {unique_filename}")
        
        return jsonify({
            'success': True,
            'files': uploaded_files,
            'total_size': total_size
        }), 200
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed. Please try again.'}), 500

@app.route('/api/merge', methods=['POST'])
@rate_limit(max_requests=50, window_seconds=3600)
def merge_pdfs():
    """Merge multiple PDF files."""
    try:
        data = request.get_json()
        
        if not data or 'files' not in data:
            return jsonify({'error': 'No files specified for merge'}), 400
        
        file_list = data.get('files', [])
        output_name = data.get('output_name', 'merged.pdf')
        
        if len(file_list) < 2:
            return jsonify({'error': 'At least 2 files are required to merge'}), 400
        
        if len(file_list) > 100:
            return jsonify({'error': 'Maximum 100 files allowed'}), 400
        
        # Secure output filename
        output_name = secure_filename(output_name)
        if not output_name.endswith('.pdf'):
            output_name += '.pdf'
        
        # Validate all files exist and are valid
        valid_files = []
        for file_name in file_list:
            file_name = secure_filename(file_name)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            
            # Prevent directory traversal
            if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
                logger.warning(f"Directory traversal attempt: {file_name}")
                return jsonify({'error': 'Invalid file path'}), 400
            
            if not os.path.exists(filepath):
                logger.warning(f"File not found: {file_name}")
                return jsonify({'error': f'File not found: {file_name}'}), 404
            
            valid_files.append(filepath)
        
        # Merge PDFs
        pdf_writer = PyPDF2.PdfWriter()
        
        for filepath in valid_files:
            try:
                pdf_reader = PyPDF2.PdfReader(filepath)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            except Exception as e:
                logger.error(f"Error reading PDF {filepath}: {str(e)}")
                return jsonify({'error': f'Error processing PDF: {os.path.basename(filepath)}'}), 400
        
        # Write merged PDF to memory
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        
        logger.info(f"PDFs merged successfully: {len(valid_files)} files")
        
        return send_file(
            output_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=output_name
        )
    
    except Exception as e:
        logger.error(f"Merge error: {str(e)}")
        return jsonify({'error': 'Merge failed. Please try again.'}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Clean up uploaded files (optional endpoint)."""
    try:
        data = request.get_json()
        file_name = data.get('file_name', '')
        
        if not file_name:
            return jsonify({'error': 'No file specified'}), 400
        
        file_name = secure_filename(file_name)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        
        # Prevent directory traversal
        if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
            return jsonify({'error': 'Invalid file path'}), 400
        
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"File cleaned up: {file_name}")
        
        return jsonify({'success': True}), 200
    
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return jsonify({'error': 'Cleanup failed'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors."""
    logger.warning("File too large error")
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # For production, use gunicorn instead
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='127.0.0.1', port=5000)
