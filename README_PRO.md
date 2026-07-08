# Advanced C2 Framework - Professional Edition v2.0

## ⚠️ Educational Safety Disclaimer

This project is a **controlled Proof-of-Concept (PoC)** designed for educational purposes only. It demonstrates:
- Enterprise-grade security architecture
- Professional embedded systems programming
- Advanced C2 (Command and Control) concepts
- Secure remote administration patterns
- Comprehensive audit logging and monitoring

**Use only on authorized test systems within your own network.**

---

## 🚀 Professional Edition Features

### Security Enhancements
- **API Key Authentication** - HMAC-based secure authentication
- **Rate Limiting** - Configurable request throttling (default: 60 req/min)
- **Input Sanitization** - Whitelist-based command validation
- **Auth Lockout** - Automatic lockout after failed attempts (5 attempts, 5 min lockout)
- **Command Whitelisting** - Only pre-approved commands can execute
- **Constant-Time Comparison** - Timing attack prevention
- **CORS Support** - Cross-origin request handling

### Architecture Improvements
- **Configuration Management** - JSON-based configuration system
- **Modular Design** - Class-based architecture with separation of concerns
- **Thread-Safe Operations** - Lock-based concurrency control
- **Professional Logging** - Structured audit logging with timestamps
- **Statistics Tracking** - Comprehensive metrics and success rates
- **Graceful Shutdown** - Clean termination with final reports
- **Error Handling** - Robust exception handling and recovery

### Monitoring & Observability
- **Real-time Status** - Live system metrics via JSON API
- **Command History** - Detailed execution history (100 entries)
- **Performance Metrics** - Execution time tracking
- **Connection Monitoring** - Heartbeat-based connection detection
- **Resource Monitoring** - Memory and WiFi signal tracking

---

## 📋 System Requirements

### Hardware - Compatible Boards

#### ESP8266 Based Boards (Fully Supported)
1. **NodeMCU v1.0 (ESP-12E)** - ⭐ Recommended
   - ESP8266EX with 4MB Flash
   - Built-in USB-to-Serial (CH340/CP2102)
   - Easy to use, widely available
   - Best for beginners

2. **NodeMCU v3 (ESP-12F/ESP-12S)** - ⭐ Recommended
   - Improved antenna design
   - Better WiFi stability
   - Same pinout as v1.0

3. **Wemos D1 Mini** - ⭐ Recommended
   - Compact form factor
   - ESP8266EX with 4MB Flash
   - Good for small projects
   - Micro USB connector

4. **ESP8266 Generic Boards**
   - ESP-01, ESP-01S (Limited GPIO, not recommended)
   - ESP-07, ESP-08 (Requires external USB adapter)
   - ESP-12E, ESP-12F, ESP-12S (Requires external USB adapter)

#### ESP32 Based Boards (Future Support)
- ESP32 DevKit V1
- ESP32 WROOM
- ESP32-C3 (Not currently supported)

**Board Selection Guide:**
- **Beginners**: NodeMCU v1.0 or Wemos D1 Mini
- **Advanced Users**: ESP-12F/S with custom adapter
- **Production**: NodeMCU v3 for better WiFi stability

### Required Accessories
- USB Data Cable (Micro USB or Mini USB depending on board)
- 5V/2A Power Adapter (optional, for standalone operation)
- Mobile device with web browser (Android/iOS)
- PC with WiFi capability

### Software Requirements

#### Arduino IDE Setup
1. **Arduino IDE 2.0+** (Recommended)
   - Download from: https://www.arduino.cc/en/software
   - Install latest version

2. **ESP8266 Board Package**
   - Open Arduino IDE
   - Go to: File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - Go to: Tools → Board → Boards Manager
   - Search: "esp8266"
   - Install: "esp8266 by ESP8266 Community" (version 3.0.0+)

3. **Required Libraries**
   - ESP8266WiFi (Built-in)
   - ESP8266WebServer (Built-in)
   - ESP8266mDNS (Built-in)
   - ArduinoJson (Install via Library Manager)
   - EEPROM (Built-in)

#### Python Setup
1. **Python 3.8+** (Required)
   - Download from: https://www.python.org/downloads/
   - Install with "Add to PATH" option checked
   - Verify installation: `python --version`

2. **Required Python Packages**
   ```bash
   pip install requests
   ```

3. **Optional Packages** (For advanced features)
   ```bash
   pip install cryptography
   pip install pyyaml
   ```

#### Network Requirements
- 2.4GHz WiFi network (5GHz not supported by ESP8266)
- All devices on same network
- Network firewall allows local communication
- Minimum 2.4GHz WiFi with WPA2 security

---

## 📦 Installation

### Step 1: Install Python Dependencies

```bash
pip install requests
```

### Step 2: Generate Secure API Key

```bash
python pc_listener_pro.py --generate-key
```

Copy the generated key and update both `config.json` and `nodemcu_c2_pro.ino`.

### Step 3: Configure System

Edit `config.json`:

```json
{
  "server": {
    "host": "192.168.1.15",
    "port": 80,
    "use_mDNS": true,
    "mDNS_hostname": "nodemcu-c2"
  },
  "security": {
    "api_key": "YOUR_GENERATED_SECURE_KEY",
    "enable_auth": true,
    "rate_limit_per_minute": 60,
    "max_queue_size": 20,
    "allowed_clients": [],
    "enable_cors": true
  },
  "logging": {
    "enable_serial": true,
    "log_level": "INFO",
    "max_history": 100
  },
  "monitoring": {
    "heartbeat_interval": 10000,
    "status_update_interval": 30000,
    "connection_timeout": 10000
  },
  "commands": {
    "enable_dangerous_commands": false,
    "require_confirmation": true,
    "auto_clear_on_success": false
  }
}
```

### Step 4: Flash NodeMCU Firmware

1. Open `nodemcu_c2_pro.ino` in Arduino IDE
2. Update WiFi credentials and API key
3. Select Board: NodeMCU 1.0 (ESP-12E Module)
4. Upload firmware to NodeMCU
5. Open Serial Monitor (115200 baud) to verify initialization

### Step 5: Run Professional Listener

```bash
python pc_listener_pro.py --config config.json
```

---

## 🎯 Available Payloads (53 Total)

### System Diagnostics (4)
1. **SYS_INFO** - System hardware and OS architecture diagnostics
2. **NET_STAT** - Network adapters and IP configuration audit
3. **PROCESS_LIST** - Active task and process security list
4. **PORT_SCAN** - Local network port and established connections scan

### Advanced Analysis (4)
5. **DNS_CACHE** - DNS cache auditor (malware analysis)
6. **ROUTE_PRINT** - Routing table diagnostic
7. **ENV_VARS** - Environment variables audit
8. **DISK_CHECK** - Disk geometry and health check

### Performance Tests (4)
9. **CALC_TEST** - Basic GUI application invocation (calculator)
10. **PING_TEST** - Loopback interface stability test
11. **CPU_STRESS** - CPU load monitoring
12. **MEM_CHECK** - Memory usage analysis

### System Management (11)
13. **SERVICE_LIST** - Windows services or systemd units status
14. **EVENT_LOG** - Windows Event Viewer or systemd journal logs
15. **FIREWALL_STATUS** - Windows Firewall or Linux firewall status
16. **STARTUP** - Startup programs and services
17. **HOTFIXES** - Installed hotfixes and updates
18. **NET_DIAG** - Advanced network interface diagnostics
19. **USER_AUDIT** - User accounts and permissions audit
20. **SCHED_TASKS** - Scheduled tasks or cron jobs
21. **INSTALLED_PROGS** - Installed software packages
22. **BOOT_TIME** - System boot time information
23. **NET_CONNECTIONS** - Active network connections with process details

### Administrative Tools (9) ⚠️
24. **REGEDIT** - Registry Editor (Windows) / System config (Linux)
25. **GPEDIT** - Group Policy Editor (Windows) / Sudoers config (Linux)
26. **SECPOL** - Local Security Policy (Windows) / Firewall rules (Linux)
27. **COMPMGMT** - Computer Management Console
28. **TASKSCHD** - Task Scheduler (Windows) / Cron editor (Linux)
29. **SERVICES** - Services Manager GUI
30. **EVENTVWR** - Event Viewer GUI (Windows) / Live journal (Linux)
31. **DEVMGMT** - Device Manager (Windows) / PCI devices (Linux)
32. **DISKMGMT** - Disk Management Console

### Performance Monitoring (4)
33. **PERFMON** - Performance Monitor (Windows) / htop (Linux)
34. **RESMON** - Resource Monitor (Windows) / iotop (Linux)
35. **MSINFO32** - System Information GUI (Windows) / dmidecode (Linux)
36. **TASKMGR** - Task Manager (Windows) / top (Linux)

### Security & Encryption (5) 🔐
37. **BITLOCKER** - BitLocker encryption status (Windows) / LUKS info (Linux)
38. **CERTMGR** - Certificate Manager (Windows) / CA certificates (Linux)
39. **WSCUI** - Windows Security Center (Windows) / UFW status (Linux)
40. **WF_MSC** - Advanced Firewall (Windows) / UFW verbose (Linux)
41. **LUSRMGR** - Local Users and Groups Manager

### Network Administration (5) 🌐
42. **NCPA** - Network Adapter Settings (Windows) / Network devices (Linux)
43. **SHARES** - Shared Folders (Windows) / NFS shares (Linux)
44. **SESSIONS** - Active user sessions (Windows) / Logged in users (Linux)
45. **NET_SHARES** - Network shares audit (SMB/NFS)
46. **RDP_CONFIG** - RDP configuration (Windows) / SSH status (Linux)

### System Maintenance (4) 🔧
47. **SFC** - System File Checker (Windows) / Package integrity (Linux)
48. **WUSA** - Windows Update History (Windows) / Available updates (Linux)
49. **DRIVERQUERY** - Installed drivers (Windows) / Kernel modules (Linux)
50. **POWERCFG** - Power configuration (Windows) / Power status (Linux)

### Advanced Diagnostics (3) 🔍
51. **PROC_TREE** - Process tree visualization
52. **OPEN_FILES** - Open files and handles
53. **CLEAR_QUEUE** - Clear command queue (NodeMCU)

---

## 🔒 Security Architecture

### Authentication Flow
1. Client sends request with `X-API-Key` header
2. Server verifies key using constant-time comparison
3. Failed attempts are tracked and trigger lockout
4. Rate limiting prevents brute force attacks

### Command Validation
1. Command is sanitized (alphanumeric, underscore, hyphen only)
2. Command is checked against whitelist
3. Invalid commands are blocked and logged
4. Blocked commands increment security metrics

### Rate Limiting
- Sliding window algorithm (1-minute window)
- Configurable limit (default: 60 requests/minute)
- HTTP 429 response when limit exceeded
- Per-client tracking possible via IP

### Audit Logging
- All commands logged with timestamps
- Security events logged separately
- Execution time tracked for performance analysis
- Logs written to file and console

---

## 📊 API Endpoints

### Public Endpoints
- `GET /` - Professional control dashboard
- `GET /status` - System status (JSON)

### Authenticated Endpoints
- `GET /trigger?cmd=COMMAND` - Queue command (requires API key)
- `GET /check` - Poll for commands (requires API key)
- `GET /history` - Command history (requires API key)
- `GET /reset` - System reset (requires API key)

### Status Response Format
```json
{
  "uptime": 1234567,
  "totalCommands": 150,
  "successfulCommands": 145,
  "failedCommands": 3,
  "blockedCommands": 2,
  "queueSize": 5,
  "pcConnected": true,
  "pcStatus": "CONNECTED",
  "lastCommand": "SYS_INFO",
  "freeHeap": 45678,
  "wifiRSSI": -65,
  "authEnabled": true,
  "isLocked": false
}
```

---

## 🔧 Configuration Options

### Security Settings
- `api_key`: Secure random key for authentication
- `enable_auth`: Enable/disable authentication
- `rate_limit_per_minute`: Maximum requests per minute
- `max_queue_size`: Maximum commands in queue
- `allowed_clients`: Optional whitelist of client IPs

### Logging Settings
- `log_level`: DEBUG, INFO, WARNING, ERROR
- `max_history`: Maximum command history entries
- `enable_serial`: Enable serial output on NodeMCU

### Monitoring Settings
- `heartbeat_interval`: PC heartbeat check interval (ms)
- `status_update_interval`: Status update interval (ms)
- `connection_timeout`: Connection timeout (ms)

### Command Settings
- `enable_dangerous_commands`: Enable potentially dangerous commands
- `require_confirmation`: Require confirmation before execution
- `auto_clear_on_success`: Auto-clear queue on successful execution

---

## 📁 Project Structure

```
esp8266_c2_poc/
├── config.json              # Configuration file
├── nodemcu_c2.ino           # Original firmware
├── nodemcu_c2_pro.ino       # Professional firmware
├── pc_listener.py            # Original listener
├── pc_listener_pro.py        # Professional listener
├── README.md                # Original documentation
└── README_PRO.md            # Professional documentation
```

---

## 🐛 Troubleshooting

### Authentication Issues
- **401 Unauthorized**: Check API key matches in both config and firmware
- **429 Rate Limit**: Reduce request frequency or increase rate limit
- **System Locked**: Wait 5 minutes for lockout to expire

### Connection Issues
- **PC Disconnected**: Check Python listener is running
- **WiFi Issues**: Verify NodeMCU is connected to network
- **mDNS Not Working**: Use IP address instead of hostname

### Command Issues
- **Command Blocked**: Check command is in whitelist
- **Queue Full**: Increase max_queue_size or clear queue
- **Execution Failed**: Check Python listener logs for details

---

## 📚 Educational Use Cases

- Learning enterprise security architecture
- Understanding C2 security patterns
- Implementing rate limiting and authentication
- Professional audit logging practices
- Thread-safe programming patterns
- Configuration management systems
- API security best practices

---

## ⚡ Performance Characteristics

- **Command Queue**: 20 commands max
- **History Storage**: 100 entries
- **Rate Limit**: 60 requests/minute (configurable)
- **Auth Lockout**: 5 attempts, 5-minute lockout
- **Heartbeat Timeout**: 10 seconds
- **Memory Usage**: ~45KB free heap typical
- **Response Time**: <100ms for API calls

---

## 📝 License

Educational use only. Not for production or malicious purposes.

---

## 🤝 Contributing

This is an educational project. Suggestions for additional security features and safe diagnostic payloads are welcome.

---

## 🔐 Security Best Practices

1. **Always change default API keys**
2. **Use strong WiFi passwords**
3. **Keep firmware updated**
4. **Monitor audit logs regularly**
5. **Use on isolated test networks only**
6. **Never expose to internet**
7. **Review command whitelist carefully**
8. **Enable authentication in production**
9. **Regular security audits recommended**
10. **Document all configuration changes**

---

## 📞 Support

For issues or questions related to this educational project, please refer to the documentation and ensure you are following all safety guidelines.
