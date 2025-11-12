# ✅ PDF Merger App - Setup Verification Checklist

## Pre-Setup Verification

- [ ] Python 3.8+ installed: `python --version`
- [ ] pip working: `pip --version`
- [ ] Git installed: `git --version`
- [ ] 500MB free disk space
- [ ] Port 5000 available

## Post-Setup Verification

### After running `setup.bat` or `setup.sh`

- [ ] Virtual environment created (venv folder exists)
- [ ] Dependencies installed without errors
- [ ] `.env` file created
- [ ] `uploads/` directory created
- [ ] `logs/` directory created
- [ ] `temp/` directory created

### Quick Test

```bash
# Activate virtual environment
source venv/bin/activate        # Unix/Linux/macOS
venv\Scripts\activate.bat       # Windows

# Test Python
python --version

# Test Flask
python -c "import flask; print(f'Flask {flask.__version__} OK')"

# Test PyPDF2
python -c "import PyPDF2; print('PyPDF2 OK')"

# Test Flask-CORS
python -c "import flask_cors; print('Flask-CORS OK')"
```

Expected output:
```
Python 3.x.x
Flask 2.3.3 OK
PyPDF2 OK
Flask-CORS OK
```

## Application Verification

### Start Application
```bash
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on/off
```

### Test in Browser
1. Open: http://localhost:5000
2. Should see PDF Merger interface
3. Try uploading sample PDFs

### Test API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health
# Expected: {"status":"healthy"}

# Upload test
curl -X POST http://localhost:5000/api/upload \
  -F "files=@sample.pdf"

# Merge test
curl -X POST http://localhost:5000/api/merge \
  -H "Content-Type: application/json" \
  -d '{"files":["test.pdf"],"output_name":"merged.pdf"}'
```

## Configuration Verification

### Check Environment Variables
```bash
# Unix/Linux/macOS
env | grep -E "FLASK|SECRET|UPLOAD"

# Windows PowerShell
Get-ChildItem env: | Where-Object { $_.Name -match 'FLASK|SECRET|UPLOAD' }
```

Should show:
```
FLASK_ENV=development
SECRET_KEY=dev-key-change-in-production
UPLOAD_FOLDER=uploads
```

### Check Permissions
```bash
# Unix/Linux/macOS
ls -la uploads logs temp
# Should be drwxr-xr-x (755)

# Windows
cacls uploads
```

## Git Verification

### Check Repository
```bash
# Show commits
git log --oneline

# Show status
git status
# Should show: "nothing to commit, working tree clean"

# Show remote (after pushing)
git remote -v
```

## File Structure Verification

### Required Files
```bash
# Check essential files exist
ls -la app.py requirements.txt .env.example .gitignore README.md
```

Should see all files:
- [ ] `app.py` (500+ lines)
- [ ] `requirements.txt` (dependencies)
- [ ] `.env.example` (template)
- [ ] `.gitignore` (git rules)
- [ ] `README.md` (documentation)
- [ ] `LICENSE` (MIT license)
- [ ] `SECURITY.md` (security guide)
- [ ] `DEPLOYMENT.md` (deployment guide)
- [ ] `CONTRIBUTING.md` (contribution guide)
- [ ] `CHANGELOG.md` (version history)
- [ ] `QUICKSTART.md` (quick start)
- [ ] `PROJECT_SUMMARY.md` (this summary)

### Required Directories
```bash
# Check directories exist
ls -d templates static tests uploads logs temp
```

Should see:
- [ ] `templates/` (with index.html)
- [ ] `static/` (with style.css, script.js)
- [ ] `tests/` (with test_app.py)
- [ ] `uploads/` (for temporary files)
- [ ] `logs/` (for log files)
- [ ] `temp/` (for temporary files)

## Functional Verification

### Feature Test Checklist

- [ ] **File Upload**
  - [ ] Can select files via click
  - [ ] Can drag and drop files
  - [ ] Shows file size
  - [ ] Validates PDF type
  - [ ] Rejects non-PDF files

- [ ] **File Management**
  - [ ] Shows selected files list
  - [ ] Can remove individual files
  - [ ] Can clear all files
  - [ ] Shows file count

- [ ] **PDF Merge**
  - [ ] Can set output filename
  - [ ] Shows progress bar
  - [ ] Starts merge process
  - [ ] Downloads merged PDF
  - [ ] Cleans up temp files

- [ ] **UI/UX**
  - [ ] Page loads quickly
  - [ ] Responsive on mobile
  - [ ] Shows error messages
  - [ ] Shows success messages
  - [ ] Progress indication

### API Test Checklist

- [ ] `GET /` - Page loads
- [ ] `GET /api/health` - Returns {"status":"healthy"}
- [ ] `POST /api/upload` - Accepts PDF files
- [ ] `POST /api/merge` - Merges PDFs
- [ ] `POST /api/cleanup` - Cleans files
- [ ] Rate limiting works (100 requests/hour)

## Performance Verification

### Load Testing
```bash
# Test with large files
# Time upload/merge for 10MB+ PDF

# Monitor resources
# Memory usage should be < 200MB
# CPU usage should spike only during merge
```

Expected performance:
- Upload 10MB file: < 5 seconds
- Merge 5 x 2MB PDFs: < 3 seconds
- Memory peak: < 200MB

## Security Verification

### Security Checks

- [ ] `.env` file not in Git: `git status | grep .env`
- [ ] No credentials in logs: `cat logs/app.log`
- [ ] File permissions correct: `ls -la uploads`
- [ ] CORS enabled: Check headers
- [ ] Rate limiting active: Try 101+ requests
- [ ] Filename sanitization works: Try `../../../etc/passwd`
- [ ] PDF validation works: Try text file as PDF

### Headers Check
```bash
# Check security headers
curl -i http://localhost:5000/ | grep -E "X-|Content-Type|CORS"
```

## Logging Verification

### Check Logs
```bash
# View application logs
tail -50 logs/app.log

# Should see entries like:
# 2024-11-12 10:00:00 - app - INFO - File uploaded
# 2024-11-12 10:00:05 - app - INFO - PDFs merged
```

## Production Readiness

### Pre-Production Checklist

- [ ] All tests pass: `pytest tests/`
- [ ] No security warnings
- [ ] Documentation complete
- [ ] Git repository clean
- [ ] `.env` updated with production secrets
- [ ] SSL certificate obtained (HTTPS)
- [ ] Nginx configuration ready
- [ ] Process manager configured (systemd/supervisor)
- [ ] Monitoring setup (optional)
- [ ] Backups configured (optional)

## Troubleshooting

### If Setup Fails

1. **Python not found**
   ```bash
   # Install Python 3.8+
   # Download from python.org
   # Restart terminal after install
   ```

2. **pip not working**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Virtual environment fails**
   ```bash
   rm -rf venv
   python -m venv venv
   ```

4. **Dependency install fails**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --upgrade
   ```

5. **Port 5000 in use**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Unix/Linux/macOS
   lsof -i :5000
   kill -9 <PID>
   ```

## Support & Help

- See `QUICKSTART.md` for quick start
- See `README.md` for full documentation
- See `SECURITY.md` for security questions
- See `DEPLOYMENT.md` for deployment issues
- Check logs: `tail -f logs/app.log`

---

## Verification Complete! ✅

If all checkboxes are marked, your PDF Merger App is:
- ✅ Properly installed
- ✅ Fully configured
- ✅ Functionally verified
- ✅ Secure and ready
- ✅ Ready for development or deployment

**Next steps:**
1. Read `QUICKSTART.md` for usage
2. Explore the codebase
3. Run tests: `pytest tests/`
4. Deploy when ready: See `DEPLOYMENT.md`

---

**Verification Date:** [Today's Date]
**Verified By:** [Your Name]
**Status:** ✅ READY FOR USE
