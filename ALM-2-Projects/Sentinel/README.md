# Sentinel — Intrusion Detection & Firewall Simulator

Sentinel is a Flask app for configuring simulated firewall rules, processing synthetic packets, raising IDS alerts, and reviewing a short threat encyclopedia.

## Run locally
```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Features
- SQLite-backed allow/block rules with source IP, destination IP, port, and protocol matching
- Synthetic traffic generator (no real packets sent)
- Rule-based alerts for repeated failed SSH login events and Telnet traffic
- Simple per-source byte-volume anomaly heuristic
- Alert feed and threat encyclopedia
- Health endpoint at `/api/health`

## Limitations
This is a classroom simulator. It does not integrate with a host firewall or inspect real traffic. The anomaly heuristic is intentionally simple and should not be treated as a production IDS. Add authentication, validation, tests, logging, and deployment hardening before any non-classroom use.
