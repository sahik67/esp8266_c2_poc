# ESP8266 C2 PoC - Educational Remote Administration Framework

## ⚠️ Educational Safety Disclaimer

This project is a **controlled Proof-of-Concept (PoC)** designed for educational purposes only. It demonstrates:
- Embedded systems programming with ESP8266/NodeMCU
- Basic C2 (Command and Control) architecture concepts
- Safe system diagnostics and security auditing
- Network communication between embedded devices and PCs

**Use only on authorized test systems within your own network.**

---

## 📋 Project Overview

This system consists of:
1. **ESP8266/NodeMCU** - Hosts a local web server acting as a C2 controller
2. **Python Listener** - Runs on an authorized test PC to parse and execute safe diagnostic commands
3. **Mobile Interface** - Web-based control panel for triggering commands

---

## 🎯 System Capabilities

| Category | Command | Windows | Linux | Description |
|----------|---------|---------|-------|-------------|
| **System Diagnostics** | SYS_INFO | ✅ | ✅ | System hardware and OS information |
| | NET_STAT | ✅ | ✅ | Network adapters and IP configuration |
| | PROCESS_LIST | ✅ | ✅ | Active processes and task list |
| | PORT_SCAN | ✅ | ✅ | Open ports and network connections |
| **Advanced Analysis** | DNS_CACHE | ✅ | ✅ | DNS cache analysis |
| | ROUTE_PRINT | ✅ | ✅ | Routing table diagnostic |
| | ENV_VARS | ✅ | ✅ | Environment variables audit |
| | DISK_CHECK | ✅ | ✅ | Disk health and space check |
| **Performance Tests** | CALC_TEST | ✅ | ✅ | Calculator GUI test |
| | PING_TEST | ✅ | ✅ | Network latency test |
| | CPU_STRESS | ✅ | ✅ | CPU load monitoring |
| | MEM_CHECK | ✅ | ✅ | Memory usage analysis |
| **System Management** | SERVICE_LIST | ✅ | ✅ | Services/systemd status |
| | EVENT_LOG | ✅ | ✅ | Event logs/journal logs |
| | FIREWALL_STATUS | ✅ | ✅ | Firewall status check |
| | STARTUP | ✅ | ✅ | Startup programs/services |
| | HOTFIXES | ✅ | ✅ | Installed hotfixes/updates |
| | NET_DIAG | ✅ | ✅ | Network interface diagnostics |
| | USER_AUDIT | ✅ | ✅ | User accounts audit |
| | SCHED_TASKS | ✅ | ✅ | Scheduled tasks/cron jobs |
| | INSTALLED_PROGS | ✅ | ✅ | Installed programs/packages |
| | BOOT_TIME | ✅ | ✅ | System boot time |
| | NET_CONNECTIONS | ✅ | ✅ | Active network connections |
| **Administrative Tools** | REGEDIT | ✅ | ✅ | Registry Editor/System config |
| | GPEDIT | ✅ | ✅ | Group Policy/Sudoers config |
| | SECPOL | ✅ | ✅ | Security Policy/Firewall rules |
| | COMPMGMT | ✅ | ✅ | Computer Management Console |
| | TASKSCHD | ✅ | ✅ | Task Scheduler/Cron editor |
| | SERVICES | ✅ | ✅ | Services Manager GUI |
| | EVENTVWR | ✅ | ✅ | Event Viewer GUI |
| | DEVMGMT | ✅ | ✅ | Device Manager/PCI devices |
| | DISKMGMT | ✅ | ✅ | Disk Management Console |
| **Performance Monitoring** | PERFMON | ✅ | ✅ | Performance Monitor/htop |
| | RESMON | ✅ | ✅ | Resource Monitor/iotop |
| | MSINFO32 | ✅ | ✅ | System Information/dmidecode |
| | TASKMGR | ✅ | ✅ | Task Manager/top |
| **Security & Encryption** | BITLOCKER | ✅ | ✅ | BitLocker status/LUKS info |
| | CERTMGR | ✅ | ✅ | Certificate Manager |
| | WSCUI | ✅ | ✅ | Windows Security/UFW status |
| | WF_MSC | ✅ | ✅ | Advanced Firewall |
| | LUSRMGR | ✅ | ✅ | Local Users & Groups |
| **Network Administration** | NCPA | ✅ | ✅ | Network Adapter Settings |
| | SHARES | ✅ | ✅ | Shared Folders/NFS shares |
| | SESSIONS | ✅ | ✅ | Active Sessions/Logged users |
| | NET_SHARES | ✅ | ✅ | Network shares audit |
| | RDP_CONFIG | ✅ | ✅ | RDP/SSH configuration |
| **System Maintenance** | SFC | ✅ | ✅ | System File Checker |
| | WUSA | ✅ | ✅ | Update History |
| | DRIVERQUERY | ✅ | ✅ | Driver Query/Kernel modules |
| | POWERCFG | ✅ | ✅ | Power Configuration |
| **Advanced Diagnostics** | PROC_TREE | ✅ | ✅ | Process tree visualization |
| | OPEN_FILES | ✅ | ✅ | Open files and handles |
| | CLEAR_QUEUE | ✅ | ✅ | Clear command queue |

**Total Commands: 53** | **Windows Support: 53** | **Linux Support: 53**

---

## 🛠️ Prerequisites

### Hardware
- ESP8266/NodeMCU development board
- USB cable for programming
- Mobile device with web browser

### Software
- Arduino IDE (with ESP8266 board support)
- Python 3.x installed on PC
- Same WiFi network for all devices

---

## 📦 Setup Instructions

### Step 1: Install Python Dependencies

On your PC, open command prompt and run:
```bash
pip install requests
```

### Step 2: Configure NodeMCU Firmware

1. Open `nodemcu_c2.ino` in Arduino IDE
2. Update WiFi credentials:
   ```cpp
   const char* ssid = "Your_Test_WiFi";
   const char* password = "Your_Password";
   ```
3. Select Board: NodeMCU 1.0 (ESP-12E Module)
4. Upload the firmware to your NodeMCU
5. Open Serial Monitor (115200 baud) to get the assigned IP address

### Step 3: Configure Python Listener

1. Open `pc_listener.py`
2. Update the NodeMCU IP address:
   ```python
   NODEMCU_BASE_URL = "http://192.168.1.15"  # Replace with actual IP
   ```

### Step 4: Run the System

1. **Start Python Listener** on your PC:
   ```bash
   python pc_listener.py
   ```
   You should see: `[+] Security Monitor Initialized...`

2. **Access Control Panel** from mobile browser:
   - Navigate to: `http://<NODEMCU_IP>`
   - You'll see the Remote C2 Auditing Dashboard

3. **Trigger Commands** by tapping buttons on the mobile interface

---

## 🎯 Available Payloads

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

### System Management (7)
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

## 🔧 Adding Custom Payloads

To add new payloads to `pc_listener.py`, add a new `elif` block in the `execute_payload()` function:

```python
elif command_type == "YOUR_COMMAND":
    if os.name == 'nt':
        subprocess.Popen(["cmd.exe", "/c", "start cmd.exe /k your_command"])
    else:
        subprocess.Popen(["your_linux_command"])
```

Then add the corresponding button in `nodemcu_c2.ino`:

```cpp
html += "<button class='danger' onclick=\"location.href='/trigger?cmd=YOUR_COMMAND'\">Your Button Text</button>";
```

---

## 📁 Project Structure

```
esp8266_c2_poc/
├── nodemcu_c2.ino      # ESP8266 firmware (Arduino IDE)
├── pc_listener.py      # Python listener script
└── README.md           # This file
```

---

## 🔒 Security Considerations

- This framework operates on **local WiFi only** - no internet exposure
- All commands execute **built-in OS utilities** for diagnostics
- No persistence mechanisms or privilege escalation
- Designed for **authorized testing environments only**
- Monitor all command execution logs for audit purposes

---

## 🐛 Troubleshooting

### Python Listener Issues
- **Connection Timeout**: Ensure NodeMCU and PC are on same WiFi network
- **Module Not Found**: Run `pip install requests`
- **Firewall Blocking**: Allow Python through Windows Firewall

### NodeMCU Issues
- **Not Connecting**: Verify WiFi credentials in `.ino` file
- **IP Not Assigned**: Check Serial Monitor for connection status
- **Web Server Unreachable**: Ensure port 80 is not blocked

---

## 📚 Educational Use Cases

- Learning embedded web server programming
- Understanding C2 architecture concepts
- System diagnostics automation
- Network security auditing fundamentals
- Cross-platform command execution patterns

---

## ⚡ Technical Details

### ESP8266 Web Server Endpoints
- `GET /` - Advanced control panel interface with real-time stats
- `GET /trigger?cmd=COMMAND` - Queue a command
- `GET /check` - Poll for pending commands (Python listener)
- `GET /status` - JSON status endpoint (uptime, queue size, PC connection)
- `GET /history` - Command history in JSON format
- `GET /reset` - Remote system reset

### Advanced Features

#### NodeMCU Enhancements
- **Command Queue System** - Circular buffer supporting up to 10 queued commands
- **Command History** - Stores last 50 executed commands with timestamps
- **Real-time Statistics** - Tracks uptime, success/failure rates, queue size
- **PC Connection Monitoring** - Heartbeat detection with 10-second timeout
- **mDNS Support** - Access via `http://nodemcu-c2.local`
- **Modern UI** - Gradient dark theme with live status updates
- **CORS Enabled** - Cross-origin requests supported for API endpoints

#### Python Listener Enhancements
- **Logging System** - File and console logging with timestamps
- **Command History** - Stores last 100 commands with execution status
- **Statistics Tracking** - Total commands, success/failure rates
- **Threading** - Background status monitoring every 30 seconds
- **Error Handling** - Connection failure detection with exponential backoff
- **Graceful Shutdown** - Ctrl+C handling with final stats output
- **Cross-Platform** - Windows and Linux support with platform-specific commands
- **21 Payloads** - Comprehensive system diagnostics and management

### Command Flow
1. Mobile browser → NodeMCU (trigger command)
2. NodeMCU enqueues command in circular buffer
3. Python listener polls NodeMCU every 1 second
4. NodeMCU dequeues and returns command to Python
5. Python executes corresponding diagnostic payload
6. Statistics and history updated on both sides
7. Real-time status updates via JSON endpoint

---

## 📝 License

Educational use only. Not for production or malicious purposes.

---

## 🤝 Contributing

This is an educational project. Suggestions for additional safe diagnostic payloads are welcome.
