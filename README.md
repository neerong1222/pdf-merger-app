# PDF Merger App

A secure, production-ready web application for merging multiple PDF files with built-in security features and Git integration.

## Features

✅ **Secure PDF Merging**
- Validate PDF integrity before merging
- Sanitize filenames and prevent directory traversal attacks
- File size restrictions (max 50MB per file, 100 files limit)
- CORS protection and rate limiting (100 requests/hour)

✅ **User-Friendly Interface**
- Drag-and-drop file uploads
- Real-time file list with remove option
- Progress tracking during merge
- Responsive mobile design

✅ **Backend Security**
- Environment variable configuration
- Input validation and error handling
- Comprehensive logging
- File type validation (PDF only)
- HTTPS-ready (use reverse proxy in production)

✅ **Git-Ready**
- `.gitignore` for sensitive files
- Environment variable templates
- No credentials in repository

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pdf-merger-app.git
   cd pdf-merger-app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update values:
   ```
   FLASK_ENV=development
   SECRET_KEY=your-production-secret-key-here
   MAX_FILE_SIZE=52428800
   UPLOAD_FOLDER=uploads
   TEMP_FOLDER=temp
   ```

6. **Create Required Directories**
   ```bash
   mkdir -p uploads logs temp
   ```

7. **Run the Application**
   ```bash
   python app.py
   ```
   
   The app will be available at `http://localhost:5000`

## Usage

1. **Open the Application**
   - Navigate to `http://localhost:5000` in your browser

2. **Upload PDF Files**
   - Drag and drop PDFs or click to select
   - Maximum 100 files, 50MB each
   - Files are validated on upload

3. **Merge PDFs**
   - Choose output filename
   - Click "Merge PDFs"
   - Download merged file automatically

4. **Clear Files**
   - Click "Clear" to reset the form

## API Endpoints

### Upload Files
```
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- files: Multiple PDF files
```

### Merge PDFs
```
POST /api/merge
Content-Type: application/json

Body:
{
  "files": ["filename1.pdf", "filename2.pdf"],
  "output_name": "merged.pdf"
}
```

### Cleanup File
```
POST /api/cleanup
Content-Type: application/json

Body:
{
  "file_name": "filename.pdf"
}
```

### Health Check
```
GET /api/health
```

## Security Features

### File Validation
- PDF file type verification
- PDF structure validation
- File size limits
- Filename sanitization

### Rate Limiting
- 100 requests per hour per IP
- Configurable limits
- Prevents abuse

### CORS Protection
- Restricted to localhost by default
- Configure allowed origins in `app.py`

### Error Handling
- Detailed logging without exposing internals
- Graceful error messages
- Exception handling on all endpoints

### Environment Security
- Sensitive data in `.env` (not committed)
- `.env.example` shows required variables
- Production secret key management

## Logging

All operations are logged to `logs/app.log` with:
- Timestamps
- Log level (INFO, WARNING, ERROR)
- Detailed messages
- File operations tracking

View logs:
```bash
tail -f logs/app.log  # Live tail
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-very-secret-key-here
export UPLOAD_FOLDER=/var/pdf-merger/uploads
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t pdf-merger .
docker run -p 5000:5000 pdf-merger
```

## Git Workflow

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit: PDF merger app with security features"
git remote add origin https://github.com/yourusername/pdf-merger-app.git
git branch -M main
git push -u origin main
```

### Regular Commits
```bash
git status
git add .
git commit -m "Descriptive commit message"
git push origin main
```

### Creating Branches
```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
# Create Pull Request on GitHub
```

## Troubleshooting

### Port 5000 Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### File Upload Fails
- Check file is a valid PDF
- Verify file size < 50MB
- Check `uploads` folder exists
- Review logs in `logs/app.log`

### Merge Fails
- Ensure all PDFs are valid
- Check file corruption with `PyPDF2`
- Review error logs
- Try with fewer files

## Project Structure
```
pdf-merger-app/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
├── uploads/              # Temporary upload storage
├── logs/                 # Application logs
└── temp/                 # Temporary files
```

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## Support

For issues, questions, or suggestions:
- Open an Issue on GitHub
- Check existing issues for similar problems
- Provide logs and error messages

## Security Notice

⚠️ **Important for Production**
- Change `SECRET_KEY` in `.env`
- Use HTTPS only
- Implement proper authentication if exposing publicly
- Set up proper backups for uploads
- Monitor logs regularly
- Keep dependencies updated

## Changelog

### v1.0.0 (Initial Release)
- Core PDF merging functionality
- Drag-and-drop interface
- Security features (validation, rate limiting)
- Comprehensive logging
- Git integration ready

---

**Last Updated:** November 2024
**Version:** 1.0.0
