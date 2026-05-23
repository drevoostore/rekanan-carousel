# Logging System - Rekanan Directory Server v2.1

## Overview

Complete logging system implemented for tracking:
- User access to all pages
- API calls with IP addresses
- HTML generation events
- Errors and warnings

---

## Log Files

All logs stored in `/home/dev/shopify/logs/`:

| File | Purpose | Format |
|------|---------|--------|
| `server.log` | Main application log | Timestamped, all levels |
| `access.log` | User access tracking | Timestamped events |
| `error.log` | Error tracking | Timestamped errors |

---

## What Gets Logged

### 1. Server Events
```
2026-05-07 09:55:26 | INFO | 🚀 Starting Rekanan Directory Server v2.0
2026-05-07 09:55:26 | INFO | SERVER_START | Rekanan Directory Server v2.0
```

### 2. Page Access
```
2026-05-07 10:15:33 | ACCESS | GET-CODE.HTML (Customer UI) | IP: 192.168.22.100 | UA: Mozilla/5.0...
2026-05-07 10:16:45 | ACCESS | LOGS.HTML (Admin Logs Page) | IP: 192.168.22.100 | UA: Mozilla/5.0...
```

### 3. API Calls
```
2026-05-07 10:17:22 | API | POST UPDATE (Generate HTML) | IP: 192.168.22.100
2026-05-07 10:17:23 | API | GET PREVIEW (Get generated HTML) | IP: 192.168.22.100
```

### 4. HTML Generation
```
2026-05-07 10:17:22 | INFO | Fetching CSV from: https://docs.google.com/...
2026-05-07 10:17:23 | INFO | CSV fetched successfully (2048 bytes)
2026-05-07 10:17:23 | INFO | Parsed 13 rekanans from CSV
2026-05-07 10:17:23 | INFO | Generating HTML from rekanan data...
2026-05-07 10:17:23 | INFO | HTML generated (45678 bytes, 12 cities)
2026-05-07 10:17:23 | INFO | ✅ Generated successfully! 13 rekanans, 12 cities | IP: 192.168.22.100
2026-05-07 10:17:23 | SUCCESS | UPDATE | 13 rekanans | 12 cities | IP: 192.168.22.100
```

### 5. Errors
```
2026-05-07 10:20:15 | ERROR | Update failed: Failed to fetch CSV: Connection timeout | IP: 192.168.22.100
```

---

## Admin Dashboard

Access: `http://server-ip:5005/logs.html`

Features:
- **Real-time statistics** (page views, API calls, successes, errors)
- **Access logs viewer** (last 50 entries)
- **Error logs viewer** (last 20 entries)
- **Auto-refresh** (toggle every 10 seconds)
- **Color-coded log types** (ACCESS, API, SUCCESS, ERROR)

### Screenshot Description

The dashboard shows:
1. **Stats cards** at top (4 gradient cards)
2. **Auto-refresh toggle** with manual refresh button
3. **Access logs** table with timestamp, type, message
4. **Error logs** table (red highlighted)

---

## API Endpoints for Logs

### Get Recent Logs (JSON)
```bash
curl http://server-ip:5005/api/logs
```

Response:
```json
{
  "success": true,
  "access_logs": [
    "2026-05-07 10:15:33 | ACCESS | GET-CODE.HTML | IP: 192.168.22.100",
    "2026-05-07 10:17:22 | API | POST UPDATE | IP: 192.168.22.100",
    "2026-05-07 10:17:23 | SUCCESS | UPDATE | 13 rekanans | IP: 192.168.22.100"
  ],
  "error_logs": [
    "2026-05-07 10:20:15 | ERROR | Update failed: Connection timeout"
  ],
  "log_files": {
    "server": "/home/dev/shopify/logs/server.log",
    "access": "/home/dev/shopify/logs/access.log",
    "error": "/home/dev/shopify/logs/error.log"
  }
}
```

---

## Log Analysis Examples

### Count user visits today
```bash
grep "GET-CODE.HTML" /home/dev/shopify/logs/access.log | wc -l
```

### Count HTML generations today
```bash
grep "SUCCESS | UPDATE" /home/dev/shopify/logs/access.log | wc -l
```

### Find all errors
```bash
cat /home/dev/shopify/logs/error.log
```

### See who accessed logs page
```bash
grep "LOGS.HTML" /home/dev/shopify/logs/access.log
```

### Track by IP address
```bash
grep "IP: 192.168.22.100" /home/dev/shopify/logs/access.log
```

---

## Monitoring Recommendations

### Daily Checks
1. Check error log: `tail -20 logs/error.log`
2. Count daily users: `grep $(date +%Y-%m-%d) logs/access.log | wc -l`
3. Check for failed updates: `grep "ERROR" logs/error.log | tail -10`

### Weekly Reports
```bash
# Generate weekly summary
echo "=== Weekly Report ===" 
echo "Total page views: $(grep ACCESS logs/access.log | wc -l)"
echo "Total API calls: $(grep API logs/access.log | wc -l)"
echo "Successful updates: $(grep SUCCESS logs/access.log | wc -l)"
echo "Errors: $(grep ERROR logs/error.log | wc -l)"
```

---

## Security Notes

- **IP addresses** are logged for all requests
- **User agents** are logged for page access
- **CSV URLs** are logged (first 50 chars only)
- **No sensitive data** in logs (passwords, tokens, etc.)
- **Log files** should be protected (chmod 640)

---

## Log Rotation

For production, setup log rotation:

```bash
# /etc/logrotate.d/rekanan-directory
/home/dev/shopify/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 640 dev dev
}
```

---

## Files Modified

| File | Changes |
|------|---------|
| `scripts/server.py` | Added comprehensive logging system |
| `src/logs.html` | New admin dashboard for viewing logs |
| `logs/` | New directory with 3 log files |

---

## Testing

### Test logging works:
```bash
# Start server
cd /home/dev/shopify
source shopifyvenv/bin/activate
python3 scripts/server.py

# In another terminal, access pages
curl http://localhost:5005/get-code.html
curl http://localhost:5005/logs.html
curl -X POST http://localhost:5005/api/update -H "Content-Type: application/json" -d '{}'

# Check logs
tail -20 logs/access.log
tail -20 logs/server.log
```

---

## Production Deployment

### Start with logging:
```bash
cd /home/dev/shopify
source shopifyvenv/bin/activate
nohup python3 scripts/server.py > logs/server.log 2>&1 &
```

### Monitor in real-time:
```bash
tail -f logs/access.log logs/error.log
```

### Check server health:
```bash
curl http://server-ip:5005/health
```

---

**Version:** 2.1  
**Created:** May 7, 2026  
**Status:** ✅ Production Ready
