from flask import Flask,render_template,jsonify
import sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
app=Flask(__name__)
def conn():
 c=sqlite3.connect(ROOT/"database.db"); c.row_factory=sqlite3.Row; return c
@app.get("/")
def home(): return render_template("index.html")
@app.get("/api/occupations")
def occupations():
 c=conn(); rows=c.execute("""SELECT o.*,
 (SELECT jobs FROM history h WHERE h.cbo=o.cbo AND year=2019) jobs2019,
 (SELECT jobs FROM history h WHERE h.cbo=o.cbo AND year=2024) jobs2024,
 (SELECT salary_real_2024 FROM history h WHERE h.cbo=o.cbo AND year=2024) salary2024
 FROM occupations o ORDER BY name""").fetchall(); c.close()
 out=[]
 for r in rows:
  d=dict(r); d["growth"]=d["jobs2024"]/d["jobs2019"]-1; out.append(d)
 return jsonify(out)
@app.get("/api/occupation/<cbo>")
def occupation(cbo):
 cbo="".join(x for x in cbo if x.isdigit()).zfill(6); c=conn()
 o=c.execute("SELECT * FROM occupations WHERE cbo=?",(cbo,)).fetchone()
 if not o: c.close(); return jsonify({"error":"não encontrada"}),404
 h=[dict(x) for x in c.execute("SELECT * FROM history WHERE cbo=? ORDER BY year",(cbo,))]
 c.close(); d=dict(o); d["history"]=h; d["growth"]=h[-1]["jobs"]/h[0]["jobs"]-1; return jsonify(d)
if __name__=="__main__": app.run(debug=True,host="127.0.0.1",port=5000)
