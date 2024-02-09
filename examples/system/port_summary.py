conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jakekoenig/scrap/websocket, which is NOT a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Look at the active ports and give me a summary (your best guess) of each process."
    },
    {
        "role": "assistant",
        "content": "```python\nimport subprocess\n\ndef get_active_ports():\n    try:\n        result = subprocess.check_output([\"lsof\", \"-i\", \"-P\", \"-n\"], universal_newlines=True)\n        return result\n    except Exception as e:\n        return str(e)\n\nprint(get_active_ports())\nprint(\"CONTINUE\")\n```"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nCOMMAND     PID       USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME\nloginwind   365 jakekoenig    4u  IPv4 0x6766c0ea49259b13      0t0  UDP *:*\nrapportd    601 jakekoenig   10u  IPv4 0x6766c0e57be3faa3      0t0  TCP *:62679 (LISTEN)\nrapportd    601 jakekoenig   11u  IPv4 0x6766c0ea49245713      0t0  UDP *:*\nrapportd    601 jakekoenig   12u  IPv4 0x6766c0ea4924ff13      0t0  UDP *:*\nrapportd    601 jakekoenig   13u  IPv4 0x6766c0ea4925bb13      0t0  UDP *:*\nrapportd    601 jakekoenig   18u  IPv6 0x6766c0ea48efd253      0t0  TCP *:62679 (LISTEN)\nidentitys   625 jakekoenig   16u  IPv4 0x6766c0ea4923f713      0t0  UDP *:*\nidentitys   625 jakekoenig   21u  IPv4 0x6766c0ea4923c313      0t0  UDP *:*\nWiFiAgent   638 jakekoenig    4u  IPv4 0x6766c0ea49fe4f13      0t0  UDP *:*\nGoogle      641 jakekoenig   81u  IPv4 0x6766c0ea4925b713      0t0  UDP *:*\nsharingd    644 jakekoenig    5u  IPv4 0x6766c0ea49259313      0t0  UDP *:*\nsharingd    644 jakekoenig    6u  IPv4 0x6766c0ea4925a713      0t0  UDP *:*\nsharingd    644 jakekoenig    7u  IPv4 0x6766c0ea49258f13      0t0  UDP *:*\nsharingd    644 jakekoenig    8u  IPv4 0x6766c0ea49258b13      0t0  UDP *:*\nsharingd    644 jakekoenig    9u  IPv4 0x6766c0ea49259f13      0t0  UDP *:*\nsharingd    644 jakekoenig   10u  IPv4 0x6766c0ea49fe5713      0t0  UDP *:*\nsharingd    644 jakekoenig   11u  IPv4 0x6766c0ea49fe5f13      0t0  UDP *:*\nControlCe   646 jakekoenig    6u  IPv4 0x6766c0e57be3936b      0t0  TCP *:7000 (LISTEN)\nControlCe   646 jakekoenig    7u  IPv6 0x6766c0ea48eff253      0t0  TCP *:7000 (LISTEN)\nControlCe   646 jakekoenig    8u  IPv4 0x6766c0e57be3aa5b      0t0  TCP *:5000 (LISTEN)\nControlCe   646 jakekoenig    9u  IPv6 0x6766c0ea48effa53      0t0  TCP *:5000 (LISTEN)\nControlCe   646 jakekoenig   16u  IPv4 0x6766c0ea49fe1713      0t0  UDP *:*\nFinder      649 jakekoenig    6u  IPv4 0x6766c0ea49fe1313      0t0  UDP *:*\nchronod     668 jakekoenig   14u  IPv6 0x6766c0ea4925b313      0t0  UDP *:62265\nGoogle      808 jakekoenig   22u  IPv4 0x6766c0e57c00936b      0t0  TCP 192.168.50.139:62684->192.168.50.196:8009 (ESTABLISHED)\nGoogle      808 jakekoenig   23u  IPv4 0x6766c0e57be387f3      0t0  TCP 192.168.50.139:62685->192.168.50.108:8009 (ESTABLISHED)\nGoogle      808 jakekoenig   25u  IPv4 0x6766c0e57ee2936b      0t0  TCP 192.168.50.139:56864->3.163.163.216:443 (ESTABLISHED)\nGoogle      808 jakekoenig   27u  IPv4 0x6766c0e57bff1ee3      0t0  TCP 192.168.50.139:63575->13.224.9.48:443 (ESTABLISHED)\nGoogle      808 jakekoenig   29u  IPv4 0x6766c0e57c5a536b      0t0  TCP 192.168.50.139:54935->140.82.112.25:443 (ESTABLISHED)\nGoogle      808 jakekoenig   30u  IPv4 0x6766c0e57bff4cc3      0t0  TCP 192.168.50.139:62765->18.116.110.156:443 (ESTABLISHED)\nGoogle      808 jakekoenig   32u  IPv4 0x6766c0e57c5a75d3      0t0  TCP 192.168.50.139:63241->74.125.197.188:5228 (ESTABLISHED)\nGoogle      808 jakekoenig   35u  IPv4 0x6766c0e57ee29ee3      0t0  TCP 192.168.50.139:63529->34.104.35.123:80 (CLOSED)\nGoogle      808 jakekoenig   43u  IPv4 0x6766c0e57c5aaf2b      0t0  TCP 192.168.50.139:59895->3.140.2.248:443 (ESTABLISHED)\nGoogle      808 jakekoenig   46u  IPv4 0x6766c0e57bff7aa3      0t0  TCP 192.168.50.139:61583->99.86.37.165:443 (ESTABLISHED)\nGoogle      808 jakekoenig   78u  IPv6 0x6766c0ea4926e313      0t0  UDP *:5353\nGoogle      808 jakekoenig   84u  IPv4 0x6766c0ea4926e713      0t0  UDP *:5353\nGoogle      808 jakekoenig   89u  IPv6 0x6766c0ea4926f313      0t0  UDP *:5353\nGoogle      808 jakekoenig   90u  IPv6 0x6766c0ea4926fb13      0t0  UDP *:5353\nGoogle      808 jakekoenig   91u  IPv6 0x6766c0ea4926c713      0t0  UDP *:5353\nGoogle      808 jakekoenig   92u  IPv6 0x6766c0ea4926cf13      0t0  UDP *:5353\nGoogle      808 jakekoenig   93u  IPv6 0x6766c0ea4926d313      0t0  UDP *:5353\nGoogle      808 jakekoenig   94u  IPv6 0x6766c0ea4926db13      0t0  UDP *:5353\nGoogle      808 jakekoenig   95u  IPv6 0x6766c0ea4926eb13      0t0  UDP *:5353\nControlCe  3827 jakekoenig    4u  IPv4 0x6766c0ea49250b13      0t0  UDP *:*\nSlack\\x20 21118 jakekoenig   23u  IPv4 0x6766c0e57c00aa5b      0t0  TCP 192.168.50.139:62719->34.202.253.140:443 (ESTABLISHED)\nSlack\\x20 21118 jakekoenig   24u  IPv4 0x6766c0e57c5a814b      0t0  TCP 192.168.50.139:50140->44.238.43.4:443 (ESTABLISHED)\nSlack\\x20 21118 jakekoenig   25u  IPv4 0x6766c0e57ee2faa3      0t0  TCP 192.168.50.139:57505->44.235.54.54:443 (ESTABLISHED)\nollama    32111 jakekoenig    4u  IPv4 0x6766c0e57bff6f2b      0t0  TCP 127.0.0.1:11434 (LISTEN)\nDiscord   36550 jakekoenig   21u  IPv4 0x6766c0e57ee2ccc3      0t0  TCP 192.168.50.139:52125->162.159.134.234:443 (ESTABLISHED)\nDiscord   36578 jakekoenig   57u  IPv4 0x6766c0e57ee2d83b      0t0  TCP 127.0.0.1:6463 (LISTEN)\nnode      67428 jakekoenig   17u  IPv4 0x6766c0e57c5a983b      0t0  TCP 192.168.50.139:57682->20.29.134.17:443 (ESTABLISHED)\nPython    75072 jakekoenig   11u  IPv4 0x6766c0e57ee2b5d3      0t0  TCP 192.168.50.139:57622->104.18.7.192:443 (CLOSE_WAIT)\nPython    82002 jakekoenig   11u  IPv4 0x6766c0e57be3ccc3      0t0  TCP 192.168.50.139:63040->104.18.7.192:443 (CLOSE_WAIT)\nPython    82715 jakekoenig    7u  IPv4 0x6766c0e57bff63b3      0t0  TCP 192.168.50.139:57700->104.18.6.192:443 (ESTABLISHED)\n\nCONTINUE\n"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0463800000",
    "timestamp": "2024-02-09_01-28-48",
    "log_version": 0.1,
    "Note": "Had to remind model to print the second response"
}


def main():
    summary = """
    - loginwindow: System process for handling the login window, typically not associated with a specific port.
    - rapportd: A daemon process for Apple's Rapport feature, facilitating device-to-device connectivity and experiences.
    - identityservicesd: Manages Apple ID services and communications, often not bound to a specific port.
    - WiFiAgent: Manages WiFi connectivity, not typically visible externally.
    - Google Chrome: Numerous connections suggest active web browsing or open tabs communicating with various services.
    - sharingd: Handles sharing services on macOS, such as AirDrop, Handoff, etc., usually doesn't bind to specific TCP ports for external communications.
    - ControlCenter: Likely associated with macOS's Control Center or similar app-specific control services, listening on ports for local services.
    - Finder: The macOS file management system, occasionally uses network ports for features like AirDrop.
    - chronod: Not a standard macOS service, possibly related to a third-party time synchronization or scheduling application.
    - Slack: Indicates the Slack application is running with active connections to Slack servers.
    - ollama: Possibly a custom or third-party service running locally, listening on localhost.
    - Discord: Indicates Discord app is running, involved in VoIP, message, and digital distribution platform.
    - node: Could indicate a Node.js service or application communicating over the network.
    - Python: Suggests one or more Python scripts or applications are making network connections, possibly web or data-fetching tools.
    """

    print(summary)


if __name__ == "__main__":
    main()
