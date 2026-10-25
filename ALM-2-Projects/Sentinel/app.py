from flask import Flask, render_template, request, jsonify
import sqlite3, json, statistics, time, os
app=Flask(__name__)
DB="sentinel.db"

def connect():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    c.executescript("""
    CREATE TABLE IF NOT EXISTS rules(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, src_ip TEXT, dst_ip TEXT, port INTEGER, protocol TEXT, description TEXT);
    CREATE TABLE IF NOT EXISTS alerts(id INTEGER PRIMARY KEY AUTOINCREMENT, created REAL, severity TEXT, message TEXT, src_ip TEXT, details TEXT);
    CREATE TABLE IF NOT EXISTS traffic(id INTEGER PRIMARY KEY AUTOINCREMENT, created REAL, src_ip TEXT, dst_ip TEXT, port INTEGER, protocol TEXT, event TEXT, bytes INTEGER);
    """)
    return c
def add_alert(c,severity,message,src,details=""):
    c.execute("INSERT INTO alerts(created,severity,message,src_ip,details) VALUES(?,?,?,?,?)",(time.time(),severity,message,src,details))
def rowdicts(rows): return [dict(r) for r in rows]
@app.get("/")
def index():
    with connect() as c:
        rules=rowdicts(c.execute("SELECT * FROM rules ORDER BY id DESC").fetchall())
        alerts=rowdicts(c.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 30").fetchall())
    return render_template("index.html",rules=rules,alerts=alerts)
@app.get("/api/rules")
def get_rules():
    with connect() as c: return jsonify(rowdicts(c.execute("SELECT * FROM rules ORDER BY id DESC").fetchall()))
@app.post("/api/rules")
def add_rule():
    d=request.json or {}; action=d.get("action","block").lower()
    if action not in ("allow","block"): return jsonify(error="Action must be allow or block."),400
    try: port=int(d["port"]) if d.get("port") else None
    except ValueError: return jsonify(error="Port must be an integer."),400
    if port is not None and not 1<=port<=65535: return jsonify(error="Port must be 1–65535."),400
    with connect() as c:
        cur=c.execute("INSERT INTO rules(action,src_ip,dst_ip,port,protocol,description) VALUES(?,?,?,?,?,?)",
            (action,d.get("src_ip") or None,d.get("dst_ip") or None,port,(d.get("protocol") or "ANY").upper(),d.get("description","")))
        return jsonify(id=cur.lastrowid,message="Rule saved.")
@app.delete("/api/rules/<int:rid>")
def delete_rule(rid):
    with connect() as c: c.execute("DELETE FROM rules WHERE id=?",(rid,))
    return jsonify(message="Rule deleted.")
@app.post("/api/traffic")
def traffic():
    d=request.json or {}
    src=d.get("src_ip","192.168.1.10"); dst=d.get("dst_ip","192.168.1.20")
    try: port=int(d.get("port",80)); size=int(d.get("bytes",500))
    except (TypeError,ValueError): return jsonify(error="Port and bytes must be integers."),400
    protocol=d.get("protocol","TCP").upper(); event=d.get("event","normal").lower()
    if not 1<=port<=65535 or not 0<=size<=100000000: return jsonify(error="Port or byte count out of range."),400
    with connect() as c:
        rules=c.execute("SELECT * FROM rules ORDER BY id").fetchall()
        verdict="allow"; matched=None
        for r in rules:
            if r["src_ip"] and r["src_ip"]!=src: continue
            if r["dst_ip"] and r["dst_ip"]!=dst: continue
            if r["port"] and r["port"]!=port: continue
            if r["protocol"] not in ("ANY",protocol): continue
            verdict=r["action"]; matched=dict(r); break
        c.execute("INSERT INTO traffic(created,src_ip,dst_ip,port,protocol,event,bytes) VALUES(?,?,?,?,?,?,?)",
                  (time.time(),src,dst,port,protocol,event,size))
        if verdict=="block": add_alert(c,"high",f"Firewall BLOCK: simulated packet matched rule #{matched['id']}.",src,json.dumps(matched))
        if event in ("failed_ssh","ssh_failed"):
            count=c.execute("SELECT COUNT(*) FROM traffic WHERE src_ip=? AND event IN ('failed_ssh','ssh_failed') AND created>?",(src,time.time()-60)).fetchone()[0]
            if count>=5: add_alert(c,"high",f"Rule-based IDS: {count} failed SSH logins from {src} in about one minute.",src)
        if port==23: add_alert(c,"medium",f"Rule-based IDS: suspicious Telnet traffic from {src}.",src)
        # Simple anomaly detector: compare the newest event's bytes with recent history for this source.
        prior=[x[0] for x in c.execute("SELECT bytes FROM traffic WHERE src_ip=? AND id < (SELECT MAX(id) FROM traffic) ORDER BY id DESC LIMIT 30",(src,)).fetchall()]
        if len(prior)>=5:
            mean=statistics.mean(prior); sd=statistics.pstdev(prior)
            if sd>0 and size>mean+3*sd: add_alert(c,"medium",f"Anomaly IDS: {size} bytes is more than 3 standard deviations above recent source history.",src,f"mean={mean:.1f}; sd={sd:.1f}")
        return jsonify(verdict=verdict,matched_rule=matched,packet={"src_ip":src,"dst_ip":dst,"port":port,"protocol":protocol,"bytes":size,"event":event},
                       message="Packet was simulated; no real network traffic was sent.")
@app.get("/api/alerts")
def get_alerts():
    with connect() as c: return jsonify(rowdicts(c.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 50").fetchall()))
@app.post("/api/alerts/clear")
def clear_alerts():
    with connect() as c: c.execute("DELETE FROM alerts")
    return jsonify(message="Alerts cleared.")
@app.get("/api/health")
def health(): return jsonify(status="ok",mode="simulation-only")
if __name__=="__main__": app.run(debug=True)
