CONF_FILE = "config.yml"

class LANG:
    TITLE = "SSH Tunnel Manager"
    START = "Start"
    STOP = "Stop"
    ADD = "Add"
    CLOSE = "Close"
    KILL_SSH = "Kill All SSH Processes"
    ALREADY_RUNNING = "SSH Tunnel Manager is already running"
    OOPS = "Oops!"
    CONF_NOT_FOUND = F"{CONF_FILE} not found in application directory"

class KEYS:
    REMOTE_ADDRESS = "remote_address"
    LOCAL_PORT = "local_port"
    PROXY_HOST = "proxy_host"
    BROWSER_OPEN = "browser_open"
    
class ICONS:
    TUNNEL = ":icons/tunnel.png"
    START = ":icons/start.png"
    STOP = ":icons/stop.png"
    KILL_SSH = ":icons/kill.png"

class CMDS:    
    SSH = "ssh"
    SSH_KILL_NIX = "killall ssh"
    SSH_KILL_WIN = "taskkill /im ssh.exe /t /f"
