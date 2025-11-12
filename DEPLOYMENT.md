# Deployment Guide

## Development Environment

### Quick Start
```bash
./setup.bat                    # Windows
./setup.sh                     # macOS/Linux

source venv/bin/activate      # Activate (Unix)
venv\Scripts\activate.bat     # Activate (Windows)

python app.py                 # Run on localhost:5000
```

## Production Deployment

### Prerequisites
- Linux server (Ubuntu 20.04+ or similar)
- Python 3.8+
- Nginx (reverse proxy)
- Supervisor or systemd (process manager)
- SSL certificate (Let's Encrypt)

### Step-by-Step Setup

#### 1. Server Preparation
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3-pip python3-venv nginx supervisor
```

#### 2. Clone Repository
```bash
cd /var/www
sudo git clone https://github.com/yourusername/pdf-merger-app.git
cd pdf-merger-app
```

#### 3. Setup Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

#### 4. Configure Environment
```bash
cp .env.example .env
sudo nano .env

# Set these values:
FLASK_ENV=production
SECRET_KEY=generate-strong-random-key-here
MAX_FILE_SIZE=52428800
```

Generate SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### 5. Create Directories
```bash
mkdir -p uploads logs temp
sudo chown www-data:www-data uploads logs temp
chmod 750 uploads logs temp
```

#### 6. Setup Gunicorn Service

Create `/etc/systemd/system/pdf-merger.service`:
```ini
[Unit]
Description=PDF Merger App
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/pdf-merger-app
Environment="PATH=/var/www/pdf-merger-app/venv/bin"
EnvironmentFile=/var/www/pdf-merger-app/.env
ExecStart=/var/www/pdf-merger-app/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    --timeout 30 \
    --access-logfile /var/www/pdf-merger-app/logs/access.log \
    --error-logfile /var/www/pdf-merger-app/logs/error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pdf-merger
sudo systemctl start pdf-merger
sudo systemctl status pdf-merger
```

#### 7. Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/pdf-merger`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration (certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Client upload size
    client_max_body_size 50M;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/h;
    limit_req_zone $binary_remote_addr zone=general:10m rate=1000r/h;
    
    location / {
        limit_req zone=general burst=50 nodelay;
        
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /api/ {
        limit_req zone=api burst=10 nodelay;
        
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/pdf-merger /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

Auto-renewal:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

#### 9. Firewall Setup
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### 10. Monitoring & Logs

Check service status:
```bash
sudo systemctl status pdf-merger
sudo journalctl -u pdf-merger -f          # Live logs
tail -f /var/www/pdf-merger-app/logs/app.log
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN mkdir -p uploads logs temp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t pdf-merger:1.0 .

docker run -d \
  -p 5000:5000 \
  -v /host/uploads:/app/uploads \
  -v /host/logs:/app/logs \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  --name pdf-merger \
  pdf-merger:1.0
```

### Database Backup

```bash
#!/bin/bash
BACKUP_DIR="/backups/pdf-merger"
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /var/www/pdf-merger-app/uploads/
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" /var/www/pdf-merger-app/logs/

# Keep only last 30 days
find "$BACKUP_DIR" -type f -mtime +30 -delete
```

Setup cron:
```bash
0 2 * * * /usr/local/bin/backup-pdf-merger.sh
```

### Monitoring

Install Prometheus exporter:
```bash
pip install prometheus-client
```

Add to `app.py`:
```python
from prometheus_client import Counter, Histogram
import time

request_count = Counter('pdf_merger_requests_total', 'Total requests')
request_duration = Histogram('pdf_merger_request_duration_seconds', 'Request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_count.inc()
    duration = time.time() - request.start_time
    request_duration.observe(duration)
    return response
```

### Performance Tuning

```bash
# Increase file descriptor limit
echo "fs.file-max = 2097152" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Tune TCP parameters
echo "net.ipv4.tcp_max_syn_backlog = 5000" | sudo tee -a /etc/sysctl.conf
```

---

**Last Updated:** November 2024
