# Security Configuration for PDF Merger App

## File Upload Security

### Validation Rules
- **File Types**: PDF only
- **Max File Size**: 50MB per file
- **Max Files Per Upload**: 100 files
- **Max Total Size**: Limited by `MAX_FILE_SIZE` env variable

### Filename Handling
- Filenames sanitized using `werkzeug.security.secure_filename`
- Unique timestamps added to prevent collisions
- Special characters removed
- Directory traversal attacks prevented

### PDF Validation
- PDF header verification (must start with %PDF)
- Page count validation
- Corruption detection using PyPDF2

## Network Security

### CORS Configuration
- Restricted to localhost by default
- Configurable origins in `app.py`
- Only POST/GET methods allowed

### Rate Limiting
- **Default**: 100 requests per hour per IP
- **Merge Endpoint**: 50 requests per hour per IP
- Uses in-memory store (use Redis for production)

### Headers
- Content-Type validation
- No sensitive headers leaked
- Error messages don't expose internals

## Data Protection

### File Storage
- Files stored in isolated `uploads/` directory
- Outside web root in production
- Temporary files cleaned up after merge
- No files persisted after download

### Logging
- All operations logged with IP address
- Failed validations logged
- Rate limit violations logged
- No sensitive data in logs

### Encryption
- Use HTTPS in production (via reverse proxy)
- Environment variables for secrets (not hardcoded)
- `.env` file ignored by Git

## Authentication & Authorization

### Current Implementation
- No user authentication (stateless service)
- Suitable for internal tools or public merger

### For Production Multi-User
- Implement JWT authentication
- Add user database
- Track file uploads per user
- Add audit logging

### Recommended Additions
```python
from flask_jwt_extended import JWTManager, jwt_required

jwt = JWTManager(app)

@app.route('/api/merge', methods=['POST'])
@jwt_required()
def merge_pdfs():
    # Protected endpoint
    pass
```

## Environment Security

### Required Variables
```
SECRET_KEY - Flask session key (minimum 32 characters)
MAX_FILE_SIZE - Maximum upload size in bytes
UPLOAD_FOLDER - Directory for uploads (isolated)
FLASK_ENV - Set to 'production' for live
```

### Never Commit
- `.env` file
- `*.pem` or `*.key` files
- Database credentials
- API keys
- Secrets

## Deployment Security

### Before Production
1. Change `SECRET_KEY` to random 32+ character string
2. Set `FLASK_ENV=production`
3. Use HTTPS/TLS with valid certificate
4. Set up reverse proxy (Nginx/Apache)
5. Run behind load balancer
6. Enable firewall rules
7. Monitor logs regularly
8. Set up automated backups
9. Use environment-specific `.env` files
10. Enable rate limiting with Redis

### Firewall Rules
```
Allow: 80/tcp (HTTP redirect)
Allow: 443/tcp (HTTPS only)
Deny: Everything else
```

### Reverse Proxy (Nginx) Security
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting
        limit_req zone=api burst=10 nodelay;
    }
}

# HTTP redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Regular Maintenance

### Daily
- Monitor logs for errors
- Check disk space (uploads directory)
- Verify service is running

### Weekly
- Review rate limit hits
- Check for failed validations
- Backup uploaded files

### Monthly
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Review security logs
- Rotate old logs

### Quarterly
- Security audit of code
- Penetration testing
- Update OWASP top 10 checklist

## Compliance

### GDPR (if processing EU user data)
- Add data deletion endpoint
- Implement privacy policy
- Track data processing
- User consent for uploads

### HIPAA (if processing health data)
- Encrypt files at rest
- Audit logging required
- Access controls
- Data retention policies

### SOC 2 (for enterprise)
- Access controls
- Change management
- Incident response
- Availability/uptime SLA

## Incident Response

### If Breach Detected
1. Stop the application
2. Isolate affected systems
3. Preserve logs
4. Notify users
5. Review security logs
6. Fix vulnerabilities
7. Conduct audit
8. Update documentation

### Contact
- Security email: security@yourdomain.com
- Responsible disclosure policy

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Flask Security: https://flask.palletsprojects.com/
- PyPDF2 Docs: https://pypdf2.readthedocs.io/
- CWE Top 25: https://cwe.mitre.org/top25/
