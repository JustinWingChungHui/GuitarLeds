#!/usr/bin/env python3
"""
Serves an HTML page listing devices currently connected to the AP,
read from the NetworkManager-managed dnsmasq lease file, followed by
the journal output for wled-button.service.

Usage:
    sudo python3 device_list_server.py [port]

Default port: 80
Page will be available at: http://10.42.0.1:80/
"""

import sys
import time
import html
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

LEASE_FILE = "/var/lib/NetworkManager/dnsmasq-wlan0.leases"
# Older/other setups sometimes use this path instead:
FALLBACK_LEASE_FILE = "/var/lib/misc/dnsmasq.leases"

SERVICE_NAME = "wled-button.service"
# Only show the last N lines of the journal so the page stays small.
# Set to None to show the full output of the current boot.
MAX_LOG_LINES = 200

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 80


def read_leases():
    """
    Each line in a dnsmasq lease file looks like:
    <expiry_epoch> <mac_address> <ip_address> <hostname> <client_id>
    """
    path = LEASE_FILE
    try:
        with open(path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        path = FALLBACK_LEASE_FILE
        try:
            with open(path) as f:
                lines = f.readlines()
        except FileNotFoundError:
            return []

    devices = []
    now = time.time()
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        expiry, mac, ip, hostname = parts[0], parts[1], parts[2], parts[3]
        try:
            expiry = int(expiry)
        except ValueError:
            expiry = 0
        devices.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname if hostname != "*" else "(unknown)",
            "expires_in_min": max(0, round((expiry - now) / 60)),
        })
    # Sort by IP for a stable, readable order
    devices.sort(key=lambda d: tuple(int(x) for x in d["ip"].split(".")))
    return devices


def read_journal():
    """Equivalent of: journalctl -u wled-button.service -b"""
    cmd = ["journalctl", "-u", SERVICE_NAME, "-b", "--no-pager"]
    if MAX_LOG_LINES:
        cmd += ["-n", str(MAX_LOG_LINES)]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10, errors="replace"
        )
        output = result.stdout
        if result.returncode != 0 and result.stderr:
            output += "\n" + result.stderr
        return output.strip() or "(no log output)"
    except FileNotFoundError:
        return "journalctl not found"
    except subprocess.TimeoutExpired:
        return "journalctl timed out"


def render_page(devices, journal):
    rows = ""
    for d in devices:
        rows += f"""
        <tr>
            <td>{html.escape(d['ip'])}</td>
            <td>{html.escape(d['hostname'])}</td>
            <td>{html.escape(d['mac'])}</td>
            <td>{d['expires_in_min']} min</td>
        </tr>"""

    if not devices:
        rows = '<tr><td colspan="4" class="empty">No connected devices found</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="15">
<title>Connected Devices</title>
<style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; background: #111; color: #eee; margin: 2rem; }}
    h1 {{ font-size: 1.3rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.1rem; margin-top: 2rem; margin-bottom: 0.5rem; }}
    p.sub {{ color: #888; margin-top: 0; font-size: 0.85rem; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 700px; }}
    th, td {{ text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid #333; }}
    th {{ color: #aaa; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; }}
    tr:hover {{ background: #1c1c1c; }}
    .empty {{ color: #666; text-align: center; padding: 1.5rem; }}
    pre.log {{ background: #0a0a0a; border: 1px solid #333; padding: 0.75rem; font-size: 0.75rem;
              line-height: 1.4; overflow-x: auto; white-space: pre; max-width: 100%; }}
</style>
</head>
<body>
    <h1>Connected Devices</h1>
    <p class="sub">Auto-refreshes every 15s &middot; {len(devices)} device(s) currently leased</p>
    <table>
        <tr><th>IP Address</th><th>Hostname</th><th>MAC Address</th><th>Lease expires</th></tr>
        {rows}
    </table>

    <h2>{html.escape(SERVICE_NAME)} log</h2>
    <p class="sub">journalctl -u {html.escape(SERVICE_NAME)} -b{f' (last {MAX_LOG_LINES} lines)' if MAX_LOG_LINES else ''}</p>
    <pre class="log">{html.escape(journal)}</pre>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_response(404)
            self.end_headers()
            return
        page = render_page(read_leases(), read_journal()).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def log_message(self, format, *args):
        pass  # keep the console quiet; remove this to see request logs


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Serving device list on http://10.42.0.1:{PORT}/  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass