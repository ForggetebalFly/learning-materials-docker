import json, os
from pathlib import Path
from threading import Lock
from flask import Flask, request, jsonify, render_template, redirect
app = Flask(__name__)
DATA = Path(os.environ.get('DATA_FILE', '/app/data/resources.json'))
lock = Lock()
def load():
    return json.loads(DATA.read_text(encoding='utf-8'))
def save(rows):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    temp = DATA.with_suffix('.tmp')
    temp.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    temp.replace(DATA)
@app.get('/')
def index():
    return render_template('index.html', rows=load())
@app.get('/api/resources')
def listing(): return jsonify(load())
@app.post('/api/resources')
def create():
    data = request.get_json(silent=True) or request.form
    title = str(data.get('title','')).strip()
    if not title: return jsonify(error='Title is required'),400
    with lock:
        rows=load()
        item={'id':max((r['id'] for r in rows),default=0)+1,'title':title,'category':str(data.get('category','Docker')).strip()[:60]}
        rows.append(item); save(rows)
    if request.is_json: return jsonify(item),201
    return redirect('/')
@app.delete('/api/resources/<int:item_id>')
def remove(item_id):
    with lock:
        rows=load(); remaining=[r for r in rows if r['id']!=item_id]
        if len(rows)==len(remaining): return jsonify(error='Not found'),404
        save(remaining)
    return '',204
@app.get('/health')
def health(): return jsonify(status='ok', resources=len(load()))
