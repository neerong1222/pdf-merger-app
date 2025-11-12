# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-12

### Added
- ✅ Core PDF merging functionality using PyPDF2
- ✅ Drag-and-drop file upload interface
- ✅ Real-time file list management
- ✅ PDF validation and integrity checking
- ✅ File size restrictions (50MB per file, 100 files max)
- ✅ Rate limiting (100 requests/hour per IP)
- ✅ CORS protection with localhost restriction
- ✅ Comprehensive error handling
- ✅ Security logging to file
- ✅ Environment variable configuration
- ✅ Responsive mobile-friendly UI
- ✅ Progress tracking for merge operations
- ✅ Automated file cleanup after merge
- ✅ Health check endpoint
- ✅ API documentation
- ✅ Git integration ready (.gitignore)
- ✅ GitHub Actions CI/CD pipeline
- ✅ Unit tests with pytest
- ✅ Comprehensive README documentation
- ✅ Security guidelines (SECURITY.md)
- ✅ Contributing guidelines (CONTRIBUTING.md)
- ✅ Setup scripts for Windows and Unix
- ✅ MIT License

### Security
- ✅ Filename sanitization to prevent directory traversal
- ✅ PDF file type validation
- ✅ Input validation on all endpoints
- ✅ Rate limiting to prevent abuse
- ✅ CORS restricted to localhost
- ✅ No sensitive data in logs
- ✅ Environment-based configuration
- ✅ .env file excluded from Git

### Documentation
- ✅ Complete README with setup instructions
- ✅ Security documentation
- ✅ API endpoint documentation
- ✅ Deployment instructions (Gunicorn, Docker, Nginx)
- ✅ Troubleshooting guide
- ✅ Contributing guidelines

## [Unreleased]

### Planned Features
- [ ] User authentication (JWT)
- [ ] File encryption at rest
- [ ] Compression option for merged PDFs
- [ ] Batch merge from URLs
- [ ] PDF watermarking
- [ ] Email delivery of merged PDFs
- [ ] Webhook notifications
- [ ] Database storage instead of filesystem
- [ ] Admin dashboard
- [ ] Advanced scheduling
- [ ] PDF splitting/extraction
- [ ] API key management
- [ ] Usage analytics
- [ ] Mobile app

### Improvements
- [ ] Redis-based rate limiting
- [ ] Async task queue (Celery)
- [ ] WebSocket real-time progress
- [ ] Advanced caching
- [ ] GraphQL API option
- [ ] S3/Cloud storage support
- [ ] Database-backed file tracking

### Bug Fixes
- [ ] Issue with corrupted PDF handling
- [ ] Large file timeout issues

## Version History Format

### [1.0.1] - YYYY-MM-DD
#### Added
- New features

#### Changed
- Modified features

#### Deprecated
- Soon-to-be removed features

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security patches

#### Known Issues
- Known problems

---

## How to Use This Changelog

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

Each release is tagged in Git with the version number (e.g., `v1.0.0`).

---

**Last Updated:** November 12, 2024
**Maintainer:** PDF Merger Team
