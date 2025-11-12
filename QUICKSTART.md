# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Windows Users

1. **Run Setup Script**
   ```bash
   setup.bat
   ```
   This automatically:
   - Creates virtual environment
   - Installs dependencies
   - Creates required directories
   - Sets up `.env` file

2. **Activate Virtual Environment**
   ```bash
   venv\Scripts\activate.bat
   ```

3. **Update Environment Settings** (Optional)
   ```bash
   notepad .env
   ```
   Change `SECRET_KEY` if using in production

4. **Start the App**
   ```bash
   python app.py
   ```

5. **Open in Browser**
   ```
   http://localhost:5000
   ```

### macOS/Linux Users

1. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   This automatically:
   - Creates virtual environment
   - Installs dependencies
   - Creates required directories
   - Sets up `.env` file

2. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

3. **Update Environment Settings** (Optional)
   ```bash
   nano .env
   ```
   Change `SECRET_KEY` if using in production

4. **Start the App**
   ```bash
   python app.py
   ```

5. **Open in Browser**
   ```
   http://localhost:5000
   ```

---

## 📝 Project Structure

```
pdf-merger-app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── setup.bat / setup.sh        # Automated setup
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
│
├── templates/
│   └── index.html             # Web interface
│
├── static/
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
│
├── tests/
│   └── test_app.py            # Unit tests
│
├── uploads/                   # Temp file storage (created)
├── logs/                      # Log files (created)
├── temp/                      # Temp files (created)
│
├── README.md                  # Full documentation
├── SECURITY.md               # Security guidelines
├── DEPLOYMENT.md             # Production setup
├── CONTRIBUTING.md           # Contributing guide
├── CHANGELOG.md              # Version history
└── LICENSE                   # MIT License
```

---

## 🔐 Security Features Built-In

✅ **File Validation**
- PDF type verification
- File size limits (50MB/file)
- Corruption detection

✅ **Network Security**
- CORS protection
- Rate limiting (100 req/hr)
- Error handling

✅ **Data Protection**
- Filename sanitization
- Directory traversal prevention
- Temporary file cleanup

✅ **Logging**
- All operations logged
- Security events tracked
- No sensitive data exposed

---

## 🌐 Using the App

### Step 1: Upload Files
- Drag & drop PDFs or click to select
- Maximum 100 files (50MB each)
- Files validate automatically

### Step 2: Review Selection
- See list of selected files
- Remove individual files if needed
- Set output filename

### Step 3: Merge
- Click "Merge PDFs"
- Watch progress bar
- Download merged file automatically

### Step 4: Done
- Files cleaned up automatically
- Ready to merge more

---

## 📚 API Usage

### Upload Files
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "files=@file1.pdf" \
  -F "files=@file2.pdf"
```

### Merge PDFs
```bash
curl -X POST http://localhost:5000/api/merge \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["file1.pdf", "file2.pdf"],
    "output_name": "merged.pdf"
  }'
```

### Check Health
```bash
curl http://localhost:5000/api/health
```

---

## 🔧 Common Tasks

### Run Tests
```bash
pytest tests/
```

### View Logs
```bash
# Real-time tail
tail -f logs/app.log

# Last 50 lines
tail -50 logs/app.log
```

### Clean Uploads
```bash
rm -rf uploads/*
```

### Restart App
```bash
# Stop current process (Ctrl+C)
# Then restart:
python app.py
```

---

## 🚀 Deploy to Production

### Quick Deploy (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Production Checklist
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Setup HTTPS/SSL certificate
- [ ] Configure Nginx reverse proxy
- [ ] Setup process manager (systemd/supervisord)
- [ ] Enable rate limiting with Redis
- [ ] Setup monitoring/logging
- [ ] Configure backups

See `DEPLOYMENT.md` for detailed instructions.

---

## 📞 Need Help?

### Troubleshooting

**Port 5000 Already in Use**
```bash
# Find process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**PDF Merge Fails**
- Check files are valid PDFs
- Verify file size < 50MB
- Review `logs/app.log`

**Setup Issues**
- Ensure Python 3.8+ installed
- Check pip working: `pip --version`
- Run setup script again

### Resources

- 📖 Full README: `README.md`
- 🔒 Security Info: `SECURITY.md`
- 🚀 Deployment: `DEPLOYMENT.md`
- 🤝 Contributing: `CONTRIBUTING.md`
- 📝 Changelog: `CHANGELOG.md`

### GitHub

Push to GitHub:
```bash
git remote add origin https://github.com/username/pdf-merger-app.git
git branch -M main
git push -u origin main
```

---

## 💡 Tips

1. **Development Mode**: `FLASK_ENV=development` enables debug logging
2. **Rate Limiting**: Disable in development with `RATE_LIMIT_ENABLED=false`
3. **Max Files**: Adjust `MAX_FILE_SIZE` in `.env` for larger limits
4. **Logging**: Check `logs/app.log` for detailed operation history
5. **Security**: Always use HTTPS in production

---

## 📄 License

MIT License - Free for commercial and personal use

---

**Last Updated:** November 12, 2024
**Version:** 1.0.0
