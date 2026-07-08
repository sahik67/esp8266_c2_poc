#!/usr/bin/env python3
"""
Advanced C2 Listener - Professional Remote Administration Framework
Educational Proof-of-Concept for Authorized Security Testing
Version: 2.0 Professional
"""

import time
import requests
import subprocess
import os
import json
import logging
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import platform
import signal
import sys
import argparse

# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

class Config:
    """Centralized configuration management"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "server": {
                "host": "192.168.1.15",
                "port": 80,
                "use_mDNS": True,
                "mDNS_hostname": "nodemcu-c2"
            },
            "security": {
                "api_key": "CHANGE_THIS_TO_SECURE_RANDOM_KEY",
                "enable_auth": True,
                "rate_limit_per_minute": 60,
                "max_queue_size": 20,
                "allowed_clients": [],
                "enable_cors": True
            },
            "logging": {
                "enable_serial": True,
                "log_level": "INFO",
                "max_history": 100
            },
            "monitoring": {
                "heartbeat_interval": 10000,
                "status_update_interval": 30000,
                "connection_timeout": 10000
            },
            "commands": {
                "enable_dangerous_commands": False,
                "require_confirmation": True,
                "auto_clear_on_success": False
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def get(self, *keys, default=None):
        """Get nested configuration value"""
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value

# ============================================================================
# SECURITY & AUTHENTICATION
# ============================================================================

class SecurityManager:
    """Handles authentication, encryption, and security operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.get("security", "api_key")
        self.enable_auth = config.get("security", "enable_auth")
        self.rate_limit = config.get("security", "rate_limit_per_minute")
        self.request_timestamps = []
        self.session_token = secrets.token_hex(32)
        
    def verify_api_key(self, provided_key: str) -> bool:
        """Verify API key using constant-time comparison"""
        if not self.enable_auth:
            return True
        return hmac.compare_digest(self.api_key, provided_key)
    
    def check_rate_limit(self) -> bool:
        """Check if request is within rate limit"""
        now = datetime.now()
        self.request_timestamps = [
            ts for ts in self.request_timestamps 
            if now - ts < timedelta(minutes=1)
        ]
        
        if len(self.request_timestamps) >= self.rate_limit:
            return False
        
        self.request_timestamps.append(now)
        return True
    
    def generate_signature(self, data: str) -> str:
        """Generate HMAC signature for data"""
        return hmac.new(
            self.api_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def sanitize_command(self, command: str) -> str:
        """Sanitize command input to prevent injection"""
        allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
        return ''.join(c for c in command if c in allowed_chars)

# ============================================================================
# AUDIT & LOGGING
# ============================================================================

class AuditLogger:
    """Professional audit logging system"""
    
    def __init__(self, config: Config):
        self.config = config
        self.log_file = "c2_audit.log"
        self.logger = self._setup_logger()
        self.audit_lock = Lock()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logging"""
        logger = logging.getLogger("C2_AUDIT")
        logger.setLevel(getattr(logging, self.config.get("logging", "log_level", default="INFO")))
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_command(self, command: str, status: str, details: str = ""):
        """Log command execution"""
        with self.audit_lock:
            self.logger.info(f"CMD: {command} | STATUS: {status} | {details}")
    
    def log_security_event(self, event_type: str, details: str):
        """Log security-related events"""
        with self.audit_lock:
            self.logger.warning(f"SECURITY: {event_type} | {details}")
    
    def log_error(self, error: str, context: str = ""):
        """Log errors"""
        with self.audit_lock:
            self.logger.error(f"ERROR: {error} | {context}")

# ============================================================================
# STATISTICS & MONITORING
# ============================================================================

@dataclass
class SystemStats:
    """System statistics tracking"""
    total_commands: int = 0
    successful_commands: int = 0
    failed_commands: int = 0
    blocked_commands: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_command: Optional[str] = None
    last_command_time: Optional[datetime] = None
    uptime: float = 0.0
    
    def get_success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_commands == 0:
            return 0.0
        return (self.successful_commands / self.total_commands) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "total_commands": self.total_commands,
            "successful_commands": self.successful_commands,
            "failed_commands": self.failed_commands,
            "blocked_commands": self.blocked_commands,
            "success_rate": self.get_success_rate(),
            "start_time": self.start_time.isoformat(),
            "last_command": self.last_command,
            "last_command_time": self.last_command_time.isoformat() if self.last_command_time else None,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }

class CommandHistory:
    """Thread-safe command history management"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.history: List[Dict] = []
        self.lock = Lock()
    
    def add(self, command: str, status: str, execution_time: float = 0.0):
        """Add command to history"""
        with self.lock:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "status": status,
                "execution_time": execution_time
            }
            self.history.append(entry)
            
            if len(self.history) > self.max_size:
                self.history.pop(0)
    
    def get_recent(self, count: int = 10) -> List[Dict]:
        """Get recent commands"""
        with self.lock:
            return self.history[-count:]
    
    def clear(self):
        """Clear history"""
        with self.lock:
            self.history.clear()

# ============================================================================
# COMMAND EXECUTION ENGINE
# ============================================================================

class CommandExecutor:
    """Advanced command execution with safety checks"""
    
    def __init__(self, config: Config, security: SecurityManager, audit: AuditLogger):
        self.config = config
        self.security = security
        self.audit = audit
        self.os_type = os.name
        self.platform_system = platform.system()
        self.enable_dangerous = config.get("commands", "enable_dangerous_commands", default=False)
        
        # Command whitelist
        self.whitelisted_commands = self._build_whitelist()
    
    def _build_whitelist(self) -> set:
        """Build command whitelist"""
        base_commands = {
            "SYS_INFO", "NET_STAT", "PROCESS_LIST", "PORT_SCAN", "CALC_TEST",
            "DNS_CACHE", "ROUTE_PRINT", "ENV_VARS", "DISK_CHECK", "PING_TEST",
            "CPU_STRESS", "MEM_CHECK", "SERVICE_LIST", "EVENT_LOG", "FIREWALL_STATUS",
            "NET_DIAG", "USER_AUDIT", "SCHED_TASKS", "INSTALLED_PROGS", "BOOT_TIME",
            "NET_CONNECTIONS", "STARTUP", "HOTFIXES", "REGEDIT", "GPEDIT", "SECPOL",
            "COMPMGMT", "TASKSCHD", "SERVICES", "EVENTVWR", "PERFMON", "RESMON",
            "DEVMGMT", "DISKMGMT", "SHARES", "SESSIONS", "NCPA", "WF_MSC",
            "LUSRMGR", "POWERCFG", "MSINFO32", "DRIVERQUERY", "SFC", "WUSA",
            "BITLOCKER", "CERTMGR", "WSCUI", "RDP_CONFIG", "PROC_TREE", "OPEN_FILES",
            "NET_SHARES", "TASKMGR", "CLEAR_QUEUE"
        }
        
        if self.enable_dangerous:
            dangerous_commands = {
                # Add dangerous commands if enabled
            }
            base_commands.update(dangerous_commands)
        
        return base_commands
    
    def validate_command(self, command: str) -> Tuple[bool, str]:
        """Validate command against whitelist and security rules"""
        sanitized = self.security.sanitize_command(command)
        
        if sanitized != command:
            return False, "Command contains invalid characters"
        
        if command not in self.whitelisted_commands:
            return False, "Command not in whitelist"
        
        return True, "Valid"
    
    def execute_command(self, command: str, window_title: str = "Command Output") -> bool:
        """Execute system command safely"""
        try:
            if self.os_type == 'nt':
                subprocess.Popen(
                    ["cmd.exe", "/c", f"start cmd.exe /k title {window_title} && {command}"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                subprocess.Popen(
                    ["gnome-terminal", "--title", window_title, "--", "bash", "-c", 
                     f"{command}; read -p 'Press Enter to close...'"]
                )
            return True
        except Exception as e:
            self.audit.log_error(str(e), f"Command: {command}")
            return False
    
    def execute_gui(self, command: List[str]) -> bool:
        """Execute GUI application"""
        try:
            subprocess.Popen(command)
            return True
        except Exception as e:
            self.audit.log_error(str(e), f"GUI: {command}")
            return False

# ============================================================================
# PAYLOAD EXECUTION ENGINE
# ============================================================================

class PayloadExecutor:
    """Advanced payload execution with comprehensive command mapping"""
    
    def __init__(self, executor: CommandExecutor, audit: AuditLogger, stats: SystemStats, history: CommandHistory):
        self.executor = executor
        self.audit = audit
        self.stats = stats
        self.history = history
        self.command_map = self._build_command_map()
    
    def _build_command_map(self) -> Dict:
        """Build comprehensive command mapping"""
        return {
            # System Diagnostics
            "SYS_INFO": {"nt": ("systeminfo", "System Information"), "posix": ("uname -a", "System Information")},
            "NET_STAT": {"nt": ("ipconfig /all", "Network Configuration"), "posix": ("ifconfig", "Network Configuration")},
            "PROCESS_LIST": {"nt": ("tasklist /v", "Process List"), "posix": ("ps aux", "Process List")},
            "PORT_SCAN": {"nt": ("netstat -ano", "Port Scanner"), "posix": ("netstat -tulpn", "Port Scanner")},
            # Advanced Analysis
            "DNS_CACHE": {"nt": ("ipconfig /displaydns", "DNS Cache"), "posix": ("cat /etc/resolv.conf", "DNS Configuration")},
            "ROUTE_PRINT": {"nt": ("route print", "Routing Table"), "posix": ("route -n", "Routing Table")},
            "ENV_VARS": {"nt": ("set", "Environment Variables"), "posix": ("printenv", "Environment Variables")},
            "DISK_CHECK": {"nt": ("wmic logicaldisk get caption,description,freespace,size,volumename", "Disk Information"), "posix": ("df -h", "Disk Information")},
            # Performance Tests
            "CALC_TEST": {"nt": ("GUI", ["calc.exe"]), "posix": ("GUI", ["gnome-calculator"])},
            "PING_TEST": {"nt": ("ping -n 4 127.0.0.1", "Network Latency Test"), "posix": ("ping -c 4 127.0.0.1", "Network Latency Test")},
            "CPU_STRESS": {"nt": ("wmic cpu get loadpercentage /value", "CPU Load"), "posix": ("top -bn1 | head -20", "CPU Load")},
            "MEM_CHECK": {"nt": ("wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value", "Memory Information"), "posix": ("free -h", "Memory Information")},
            # System Management
            "SERVICE_LIST": {"nt": ("sc query state= all", "Services Status"), "posix": ("systemctl list-units --type=service", "Services Status")},
            "EVENT_LOG": {"nt": ("wevtutil qe System /c:10 /rd:true /f:text", "Event Logs"), "posix": ("journalctl -n 20 --no-pager", "System Logs")},
            "FIREWALL_STATUS": {"nt": ("netsh advfirewall show allprofiles", "Firewall Status"), "posix": ("sudo ufw status", "Firewall Status")},
            "STARTUP": {"nt": ("wmic startup get command,caption", "Startup Programs"), "posix": ("systemctl list-unit-files --type=service", "Startup Services")},
            "HOTFIXES": {"nt": ("wmic qfe get hotfixid,installedon", "Hotfixes"), "posix": ("dpkg --get-selections | grep -v deinstall", "Installed Packages")},
            "NET_DIAG": {"nt": ("netsh interface ipv4 show interfaces", "Network Interfaces"), "posix": ("ip link show", "Network Interfaces")},
            "USER_AUDIT": {"nt": ("net user", "User Accounts"), "posix": ("whoami && id", "User Information")},
            "SCHED_TASKS": {"nt": ("schtasks /query /fo LIST", "Scheduled Tasks"), "posix": ("crontab -l", "Cron Jobs")},
            "INSTALLED_PROGS": {"nt": ("wmic product get name,version,vendor", "Installed Programs"), "posix": ("dpkg -l", "Installed Packages")},
            "BOOT_TIME": {"nt": ("wmic os get lastbootuptime", "Boot Time"), "posix": ("uptime -s", "Boot Time")},
            "NET_CONNECTIONS": {"nt": ("netstat -b", "Network Connections with Processes"), "posix": ("ss -tulpn", "Network Connections")},
            # Administrative Tools
            "REGEDIT": {"nt": ("GUI", ["regedit.exe"]), "posix": ("nano /etc/passwd", "System Configuration")},
            "GPEDIT": {"nt": ("GUI", ["gpedit.msc"]), "posix": ("sudo visudo", "Sudoers Configuration")},
            "SECPOL": {"nt": ("GUI", ["secpol.msc"]), "posix": ("sudo iptables -L -v", "Firewall Rules")},
            "COMPMGMT": {"nt": ("GUI", ["compmgmt.msc"]), "posix": ("sudo systemctl status", "System Status")},
            "TASKSCHD": {"nt": ("GUI", ["taskschd.msc"]), "posix": ("crontab -e", "Cron Editor")},
            "SERVICES": {"nt": ("GUI", ["services.msc"]), "posix": ("sudo systemctl list-units --type=service --state=running", "Running Services")},
            "EVENTVWR": {"nt": ("GUI", ["eventvwr.msc"]), "posix": ("sudo journalctl -f", "Live Journal Logs")},
            "PERFMON": {"nt": ("GUI", ["perfmon.exe"]), "posix": ("htop", "System Monitor")},
            "TASKMGR": {"nt": ("GUI", ["taskmgr.exe"]), "posix": ("top", "Task Manager")},
            "RESMON": {"nt": ("GUI", ["resmon.exe"]), "posix": ("iotop", "I/O Monitor")},
            "DEVMGMT": {"nt": ("GUI", ["devmgmt.msc"]), "posix": ("lspci -v", "PCI Devices")},
            "DISKMGMT": {"nt": ("GUI", ["diskmgmt.msc"]), "posix": ("sudo fdisk -l", "Disk Partitions")},
            "SHARES": {"nt": ("net share", "Shared Folders"), "posix": ("sudo exportfs -v", "NFS Shares")},
            "SESSIONS": {"nt": ("query session", "Active Sessions"), "posix": ("who", "Logged In Users")},
            "NCPA": {"nt": ("GUI", ["ncpa.cpl"]), "posix": ("nmcli device show", "Network Devices")},
            "WF_MSC": {"nt": ("GUI", ["wf.msc"]), "posix": ("sudo ufw show verbose", "Firewall Details")},
            "LUSRMGR": {"nt": ("GUI", ["lusrmgr.msc"]), "posix": ("sudo cat /etc/group", "User Groups")},
            "POWERCFG": {"nt": ("powercfg /list", "Power Plans"), "posix": ("upower -i /org/freedesktop/UPower", "Power Status")},
            "MSINFO32": {"nt": ("GUI", ["msinfo32.exe"]), "posix": ("sudo dmidecode", "Hardware Info")},
            "DRIVERQUERY": {"nt": ("driverquery", "Installed Drivers"), "posix": ("lsmod", "Kernel Modules")},
            "SFC": {"nt": ("sfc /scannow", "System File Checker"), "posix": ("sudo debsums -c", "Package Integrity")},
            "WUSA": {"nt": ("wmic qfe list", "Update History"), "posix": ("apt list --upgradable", "Available Updates")},
            "BITLOCKER": {"nt": ("manage-bde -status", "BitLocker Status"), "posix": ("sudo cryptsetup luksDump", "LUKS Info")},
            "CERTMGR": {"nt": ("GUI", ["certmgr.msc"]), "posix": ("sudo update-ca-certificates --fresh", "Certificates")},
            "WSCUI": {"nt": ("GUI", ["windowsdefender://"]), "posix": ("sudo ufw status verbose", "Security Status")},
            "RDP_CONFIG": {"nt": ("reg query \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\"", "RDP Settings"), "posix": ("systemctl status sshd", "SSH Status")},
            "NET_SHARES": {"nt": ("powershell \"Get-SmbShare | Select-Object Name,Path,Description\"", "SMB Shares"), "posix": ("showmount -e localhost", "NFS Exports")},
            "PROC_TREE": {"nt": ("wmic process get name,parentprocessid,processid", "Process Tree"), "posix": ("pstree -p", "Process Tree")},
            "OPEN_FILES": {"nt": ("openfiles /query /v", "Open Files"), "posix": ("sudo lsof", "Open Files")}
        }
    
    def execute(self, command_type: str) -> bool:
        """Execute payload with validation and logging"""
        start_time = time.time()
        
        # Validate command
        is_valid, reason = self.executor.validate_command(command_type)
        if not is_valid:
            self.audit.log_security_event("COMMAND_BLOCKED", f"{command_type} - {reason}")
            self.stats.blocked_commands += 1
            return False
        
        # Get command mapping
        if command_type not in self.command_map:
            self.audit.log_error("Unknown command", command_type)
            return False
        
        cmd_map = self.command_map[command_type]
        os_type = "nt" if self.executor.os_type == 'nt' else "posix"
        
        if os_type not in cmd_map:
            self.audit.log_error("Platform not supported", f"{command_type} on {os_type}")
            return False
        
        cmd_data = cmd_map[os_type]
        success = False
        
        try:
            if cmd_data[0] == "GUI":
                success = self.executor.execute_gui(cmd_data[1])
            else:
                success = self.executor.execute_command(cmd_data[0], cmd_data[1])
        except Exception as e:
            self.audit.log_error(str(e), f"Command: {command_type}")
        
        execution_time = time.time() - start_time
        
        # Update statistics
        self.stats.total_commands += 1
        if success:
            self.stats.successful_commands += 1
        else:
            self.stats.failed_commands += 1
        self.stats.last_command = command_type
        self.stats.last_command_time = datetime.now()
        
        # Add to history
        self.history.add(command_type, "SUCCESS" if success else "FAILED", execution_time)
        
        # Log execution
        self.audit.log_command(command_type, "SUCCESS" if success else "FAILED", f"Time: {execution_time:.3f}s")
        
        return success

# ============================================================================
# C2 CLIENT - MAIN CONTROLLER
# ============================================================================

class C2Client:
    """Main C2 client controller"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = Config(config_file)
        self.security = SecurityManager(self.config)
        self.audit = AuditLogger(self.config)
        self.stats = SystemStats()
        self.history = CommandHistory(self.config.get("logging", "max_history", default=100))
        self.executor = CommandExecutor(self.config, self.security, self.audit)
        self.payload_executor = PayloadExecutor(self.executor, self.audit, self.stats, self.history)
        
        self.base_url = f"http://{self.config.get('server', 'host')}"
        self.running = False
        
    def get_node_status(self) -> Optional[Dict]:
        """Get NodeMCU status"""
        try:
            headers = {}
            if self.security.enable_auth:
                headers["X-API-Key"] = self.security.api_key
            
            response = requests.get(f"{self.base_url}/status", headers=headers, timeout=3)
            return response.json()
        except Exception as e:
            self.audit.log_error(str(e), "Status check failed")
            return None
    
    def check_for_commands(self) -> Optional[str]:
        """Check for pending commands from NodeMCU"""
        try:
            if not self.security.check_rate_limit():
                self.audit.log_security_event("RATE_LIMIT_EXCEEDED", "Too many requests")
                return None
            
            headers = {}
            if self.security.enable_auth:
                headers["X-API-Key"] = self.security.api_key
            
            response = requests.get(f"{self.base_url}/check", headers=headers, timeout=3)
            server_response = response.text.strip()
            
            if server_response not in ["WAITING", "NONE"]:
                return server_response
            return None
            
        except Exception as e:
            self.audit.log_error(str(e), "Command check failed")
            return None
    
    def status_monitor(self):
        """Background status monitoring thread"""
        interval = self.config.get("monitoring", "status_update_interval", default=30000) / 1000
        
        while self.running:
            time.sleep(interval)
            status = self.get_node_status()
            if status:
                self.audit.logger.info(
                    f"NodeMCU Status - Uptime: {status.get('uptime', 0)/1000:.0f}s, "
                    f"Queue: {status.get('queueSize', 0)}, "
                    f"PC Connected: {status.get('pcConnected', False)}, "
                    f"Free Heap: {status.get('freeHeap', 0)} bytes"
                )
    
    def run(self):
        """Main execution loop"""
        self.running = True
        self.audit.logger.info("=" * 60)
        self.audit.logger.info("ADVANCED C2 LISTENER - PROFESSIONAL EDITION")
        self.audit.logger.info("=" * 60)
        self.audit.logger.info(f"Target: {self.base_url}")
        self.audit.logger.info(f"Platform: {platform.system()} {platform.release()}")
        self.audit.logger.info(f"Authentication: {'ENABLED' if self.security.enable_auth else 'DISABLED'}")
        self.audit.logger.info(f"Rate Limit: {self.security.rate_limit} requests/minute")
        self.audit.logger.info("=" * 60)
        
        # Start status monitor thread
        monitor_thread = Thread(target=self.status_monitor, daemon=True)
        monitor_thread.start()
        
        consecutive_failures = 0
        max_failures = 10
        
        try:
            while self.running:
                command = self.check_for_commands()
                
                if command:
                    self.audit.logger.info(f"[+] Command received: {command}")
                    success = self.payload_executor.execute(command)
                    consecutive_failures = 0
                else:
                    consecutive_failures = 0 if consecutive_failures == 0 else consecutive_failures - 1
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.audit.logger.info("[!] Shutdown signal received")
        except Exception as e:
            self.audit.logger.error(f"[!] Fatal error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        self.audit.logger.info("=" * 60)
        self.audit.logger.info("FINAL STATISTICS")
        self.audit.logger.info("=" * 60)
        self.audit.logger.info(json.dumps(self.stats.to_dict(), indent=2))
        self.audit.logger.info("=" * 60)
        self.audit.logger.info("RECENT COMMAND HISTORY")
        self.audit.logger.info("=" * 60)
        for entry in self.history.get_recent(10):
            self.audit.logger.info(json.dumps(entry, indent=2))
        self.audit.logger.info("=" * 60)
        self.audit.logger.info("C2 Listener Shutdown Complete")

# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Advanced C2 Listener")
    parser.add_argument("--config", default="config.json", help="Configuration file path")
    parser.add_argument("--generate-key", action="store_true", help="Generate new API key")
    
    args = parser.parse_args()
    
    if args.generate_key:
        print(f"Generated API Key: {secrets.token_hex(32)}")
        return
    
    client = C2Client(args.config)
    client.run()

if __name__ == "__main__":
    main()
