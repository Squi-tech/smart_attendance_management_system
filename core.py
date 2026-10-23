"""Database, attendance maths and face recognition (uses dlib directly, no Flask)."""
import os, io, json, sqlite3
import numpy as np, dlib
from PIL import Image, ImageOps
import face_recognition_models as frm

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data"); PHOTOS = os.path.join(DATA, "photos")
os.makedirs(PHOTOS, exist_ok=True)
TOL = 0.52   # lower = stricter face matching
YEARS = ["1", "2", "3", "4"]; DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
POSES = [("front", "Front view"), ("left", "Left side"), ("right", "Right side"), ("top", "Slightly top"),
         ("bottom", "Slightly bottom"), ("far", "Far view (3-4 m)"), ("near", "Near view (close-up)")]
SCHEMA = """
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
  role TEXT NOT NULL, name TEXT);
CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  roll_no TEXT UNIQUE NOT NULL, name TEXT NOT NULL, dept TEXT, year TEXT, section TEXT, acad TEXT, photo TEXT);
CREATE TABLE IF NOT EXISTS student_photos(id INTEGER PRIMARY KEY, student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
  pose TEXT, filename TEXT, encoding TEXT);
CREATE TABLE IF NOT EXISTS options(id INTEGER PRIMARY KEY, kind TEXT, name TEXT, UNIQUE(kind,name));
CREATE TABLE IF NOT EXISTS subjects(id INTEGER PRIMARY KEY, name TEXT, dept TEXT, year TEXT, UNIQUE(name,dept,year));
CREATE TABLE IF NOT EXISTS timetable(id INTEGER PRIMARY KEY, dept TEXT, year TEXT, section TEXT, acad TEXT,
  day INTEGER, period INTEGER, subject TEXT, UNIQUE(dept,year,section,acad,day,period));
CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY, student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
  subject TEXT, date TEXT, period INTEGER, status TEXT, marked_by INTEGER, UNIQUE(student_id,subject,date,period));
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);
"""
_c = None
def conn():
    global _c
    if _c is None:
        _c = sqlite3.connect(os.path.join(DATA, "attendance.db"), check_same_thread=False)
        _c.row_factory = sqlite3.Row; _c.execute("PRAGMA foreign_keys=ON"); _c.executescript(SCHEMA)
        for k, v in (("safe", 80), ("fine", 75), ("debar", 70)): _c.execute("INSERT OR IGNORE INTO settings VALUES(?,?)", (k, str(v)))
        _c.commit()
    return _c
def q(sql, args=(), one=False):
    rows = conn().execute(sql, args).fetchall(); return (rows[0] if rows else None) if one else rows
def ex(sql, args=()):
    c = conn(); cur = c.execute(sql, args); c.commit(); return cur
def thresholds(): return {r["key"]: int(r["value"]) for r in q("SELECT * FROM settings")}

# ---------- attendance maths ----------
def status_for(pct, t):
    return "Safe" if pct >= t["safe"] else "Risk" if pct >= t["fine"] else "Fine Applicable" if pct >= t["debar"] else "Debar"
def plan(p, total, T):
    """(periods to attend in a row, periods that can be skipped) to stay at or above T percent."""
    if total == 0: return 0, 0
    if p * 100 >= T * total: return 0, max(0, (p * 100) // T - total)
    if T >= 100: return None, 0
    return -(-(T * total - 100 * p) // (100 - T)), 0
def plan_text(x):
    return "not reachable" if x[0] is None else f"attend the next {x[0]} periods" if x[0] else f"can still skip {x[1]} periods"
def summarize(p, total, t):
    pct = round(100 * p / total, 2) if total else 0.0
    return {"present": p, "total": total, "pct": pct, "status": status_for(pct, t) if total else "No data",
            "avoid_fine": plan(p, total, t["fine"]), "avoid_debar": plan(p, total, t["debar"]), "to_safe": plan(p, total, t["safe"])}
def student_report(sid):
    t = thresholds()
    rows = q("SELECT subject,date,period,status FROM attendance WHERE student_id=? ORDER BY date DESC,period DESC", (sid,))
    subj, month, pa = {}, {}, 0
    for r in rows:
        pr = r["status"] == "Present"; pa += pr
        for d, k in ((subj, r["subject"]), (month, r["date"][:7])):
            x = d.setdefault(k, [0, 0]); x[0] += pr; x[1] += 1
    return {"t": t, "overall": summarize(pa, len(rows), t), "history": rows,
            "subjects": {k: summarize(*v, t) for k, v in sorted(subj.items())},
            "months": {k: summarize(*v, t) for k, v in sorted(month.items())}}

# ---------- face recognition ----------
_det = dlib.get_frontal_face_detector()
_sp = dlib.shape_predictor(frm.pose_predictor_five_point_model_location())
_enc = dlib.face_recognition_model_v1(frm.face_recognition_model_location())
def _load(data, max_side=2600):
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB"); im.thumbnail((max_side, max_side))
    return np.ascontiguousarray(np.array(im))
def _describe(img, rect): return np.array(_enc.compute_face_descriptor(img, _sp(img, rect)))
def encode_photo(data):
    img = _load(data, 1600); rects = _det(img, 2)
    if not rects: return None
    big = max(rects, key=lambda r: r.width() * r.height())
    return json.dumps(_describe(img, big).tolist())
def _passes(img):
    yield img
    h, w = img.shape[:2]; th, tw = int(h * .6), int(w * .6)
    for y in (0, h - th):
        for x in (0, w - tw): yield np.ascontiguousarray(img[y:y + th, x:x + tw])
def recognize(photos, known):
    """photos: list of bytes. known: {student_id: [encoding_json,...]}. Returns (present ids, faces seen)."""
    owners, vecs = [], []
    for sid, encs in known.items():
        for e in encs: owners.append(sid); vecs.append(json.loads(e))
    matrix, present, faces = np.array(vecs), set(), 0
    for data in photos:
        for i, view in enumerate(_passes(_load(data))):
            rects = _det(view, 2)
            if i == 0: faces += len(rects)
            if not len(matrix): continue
            for r in rects:
                d = np.linalg.norm(matrix - _describe(view, r), axis=1); b = int(np.argmin(d))
                if d[b] <= TOL: present.add(owners[b])
    return present, faces
