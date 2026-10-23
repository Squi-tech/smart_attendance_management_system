"""Premium look-and-feel: CSS and small HTML components for the Streamlit app."""
import html, json
import streamlit as st
import inspect
import streamlit.components.v1 as components
from core import plan_text

COLORS = {"Safe": "#16a34a", "Risk": "#d97706", "Fine Applicable": "#ea580c", "Debar": "#dc2626", "No data": "#94a3b8"}
E = html.escape
def md(s): st.markdown(s, unsafe_allow_html=True)

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp,.stApp p,.stApp label,.stApp input,.stApp textarea,.stApp button,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp li,.stApp td,.stApp th{font-family:'Inter',system-ui,sans-serif}
[data-testid=stIconMaterial],[class*="material-symbols"],[class*="material-icons"]{font-family:'Material Symbols Rounded','Material Icons'!important}
input[type=password]::-ms-reveal,input[type=password]::-ms-clear{display:none}
.stElementContainer:has(iframe[height="0"]){height:0;margin:0;overflow:hidden;position:absolute}
.stApp{background:radial-gradient(1100px 480px at 8% -8%,#e0e7ff 0%,transparent 60%),radial-gradient(800px 400px at 100% 0,#fce7f3 0%,transparent 55%),#f6f7fb}
#MainMenu,footer{visibility:hidden}header[data-testid=stHeader]{background:transparent}
.block-container{padding-top:2rem;max-width:1180px}
h1,h2,h3{letter-spacing:-.02em;color:#0f172a}
[data-testid=stSidebar]{background:linear-gradient(180deg,#0b1020 0%,#1e1b4b 100%)}
[data-testid=stSidebar] *{color:#e5e7eb}
[data-testid=stSidebar] [role=radiogroup]{gap:.25rem}
[data-testid=stSidebar] [role=radiogroup] label{padding:.6rem .85rem;border-radius:12px;transition:.15s;width:100%}
[data-testid=stSidebar] [role=radiogroup] label:hover{background:rgba(255,255,255,.08)}
[data-testid=stSidebar] [role=radiogroup] label:has(input:checked){background:linear-gradient(135deg,#4f46e5,#7c3aed)}
[data-testid=stSidebar] [role=radiogroup] label>div:first-child{display:none}
[data-testid=stSidebar] .stButton>button{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);color:#fff;width:100%}
.stButton>button,.stFormSubmitButton>button{border-radius:12px;font-weight:600;padding:.55rem 1.2rem;border:1px solid #e2e8f0;transition:.15s}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(30,27,75,.12)}
button[kind=primary],button[data-testid=stBaseButton-primary],button[data-testid=stBaseButton-primaryFormSubmit],button[data-testid=stBaseButton-secondaryFormSubmit]{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;border:0;box-shadow:0 8px 20px rgba(79,70,229,.32)}
button[kind=primary] p,button[data-testid=stBaseButton-primaryFormSubmit] p,button[data-testid=stBaseButton-secondaryFormSubmit] p{color:#fff}
[data-baseweb=input],[data-baseweb=select]>div,[data-baseweb=textarea]{border-radius:12px!important}
[data-testid=stForm]{background:#fff;border:1px solid #e8eaf3;border-radius:20px;padding:1.4rem;box-shadow:0 12px 32px rgba(30,27,75,.07)}
[data-testid=stExpander]{background:#fff;border:1px solid #e8eaf3;border-radius:16px}
[data-testid=stDataFrame]{border-radius:14px;overflow:hidden;border:1px solid #e8eaf3}
[data-testid=stImage] img{border-radius:14px}
.stTabs [data-baseweb=tab-list]{gap:.35rem;background:#fff;padding:.35rem;border-radius:16px;border:1px solid #e8eaf3}
.stTabs [data-baseweb=tab]{border-radius:12px;padding:.5rem 1.1rem;height:auto}
.stTabs [aria-selected=true]{background:linear-gradient(135deg,#4f46e5,#7c3aed)}
.stTabs [aria-selected=true] p{color:#fff}.stTabs [data-baseweb=tab-highlight],.stTabs [data-baseweb=tab-border]{display:none}
.hero{background:linear-gradient(135deg,#312e81 0%,#6d28d9 55%,#db2777 100%);color:#fff;border-radius:26px;padding:2.4rem 2.2rem;margin-bottom:1.6rem;box-shadow:0 24px 48px rgba(79,70,229,.28);position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;right:-60px;top:-60px;width:240px;height:240px;border-radius:50%;background:rgba(255,255,255,.12)}
.hero h1{color:#fff;font-size:2.3rem;font-weight:800;margin:0 0 .4rem}.hero p{color:#e0e7ff;margin:0;font-size:1.05rem}
.hero .pills{margin-top:1rem;display:flex;gap:.5rem;flex-wrap:wrap}.hero .pills span{background:rgba(255,255,255,.16);border-radius:99px;padding:.25rem .8rem;font-size:.82rem}
.sec{margin:.2rem 0 1rem}.sec h2{margin:0;font-size:1.7rem;font-weight:800}.sec p{margin:.15rem 0 0;color:#64748b}
.card,.tile,.stat,.scard{background:#fff;border:1px solid #e8eaf3;border-radius:20px;box-shadow:0 8px 24px rgba(30,27,75,.05)}
.tile{padding:1.2rem 1.3rem;margin-bottom:.5rem;transition:.18s}.tile:hover{transform:translateY(-3px);box-shadow:0 16px 36px rgba(79,70,229,.16);border-color:#c7d2fe}
.tile .ic{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;font-size:1.4rem;background:linear-gradient(135deg,#e0e7ff,#fae8ff);margin-bottom:.7rem}
.tile b{font-size:1.15rem}.tile p{margin:.1rem 0 0;color:#64748b;font-size:.9rem}
.stat{padding:1.1rem 1.2rem;height:100%}.stat small{color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:.05em;font-size:.72rem}
.stat div{font-size:1.7rem;font-weight:800;margin-top:.3rem;line-height:1.2}
.chip{display:inline-block;padding:.2rem .75rem;border-radius:99px;font-size:.8rem;font-weight:700}
.ringbox{display:flex;justify-content:center;padding:1rem}.rg{width:132px;height:132px;border-radius:50%;display:grid;place-items:center}
.ri{width:100px;height:100px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}.ri b{font-size:1.5rem}.ri span{font-size:.7rem;color:#64748b}
.scard{padding:1rem 1.2rem;margin-bottom:.8rem}.scard .top{display:flex;justify-content:space-between;align-items:center;gap:.5rem}
.bar{height:9px;background:#eef0f7;border-radius:99px;margin:.7rem 0;overflow:hidden}.bar i{display:block;height:100%;border-radius:99px}
.scard p{margin:.15rem 0;font-size:.88rem;color:#475569}
.callout{border-radius:14px;padding:.9rem 1.1rem;margin:.8rem 0;border-left:5px solid;font-size:.95rem}
.brand{font-size:1.25rem;font-weight:800;margin-bottom:.2rem}.who{background:rgba(255,255,255,.08);border-radius:14px;padding:.7rem .9rem;margin:.6rem 0 1rem}
.who small{color:#a5b4fc!important;text-transform:uppercase;letter-spacing:.06em}
</style>"""

def wide(fn):
    """Full-width kwarg that works on old and new Streamlit versions."""
    return {"width": "stretch"} if "width" in inspect.signature(fn).parameters else {"use_container_width": True}
def inject(): md(CSS)
def hero(title, sub, pills=()):
    md(f'<div class="hero"><h1>{E(title)}</h1><p>{E(sub)}</p><div class="pills">{"".join(f"<span>{E(p)}</span>" for p in pills)}</div></div>')
def section(title, sub=""): md(f'<div class="sec"><h2>{E(title)}</h2>{f"<p>{E(sub)}</p>" if sub else ""}</div>')
def tile(title, sub, icon): md(f'<div class="tile"><div class="ic">{icon}</div><b>{E(title)}</b><p>{E(sub)}</p></div>')
def stat(label, value_html): md(f'<div class="stat"><small>{E(label)}</small><div>{value_html}</div></div>')
def chip(status):
    c = COLORS.get(status, "#64748b"); return f'<span class="chip" style="background:{c}22;color:{c}">{E(status)}</span>'
def ring(pct, status):
    c = COLORS.get(status, "#94a3b8")
    md(f'<div class="card ringbox"><div class="rg" style="background:conic-gradient({c} {min(pct,100)*3.6}deg,#e8eaf3 0)"><div class="ri"><b>{pct}%</b><span>Overall</span></div></div></div>')
def callout(text, tone="info"):
    c, bg = {"info": ("#4f46e5", "#eef2ff"), "warn": ("#d97706", "#fffbeb"), "ok": ("#16a34a", "#f0fdf4")}[tone]
    md(f'<div class="callout" style="border-color:{c};background:{bg}">{text}</div>')
def subject_card(name, x, t):
    c = COLORS.get(x["status"], "#94a3b8")
    md(f'<div class="scard"><div class="top"><b>{E(name)}</b>{chip(x["status"])}</div>'
       f'<div class="bar"><i style="width:{min(x["pct"],100)}%;background:{c}"></i></div>'
       f'<p><b>{x["pct"]}%</b> · {x["present"]} of {x["total"]} periods attended</p>'
       f'<p>To avoid a fine ({t["fine"]}%): {E(plan_text(x["avoid_fine"]))}</p>'
       f'<p>To avoid debarment ({t["debar"]}%): {E(plan_text(x["avoid_debar"]))}</p>'
       f'<p>To be safe ({t["safe"]}%): {E(plan_text(x["to_safe"]))}</p></div>')
def brand(name, role):
    st.sidebar.markdown(f'<div class="brand">🎓 Smart Attendance</div><div class="who"><small>{E(role)}</small><br><b>{E(name)}</b></div>', unsafe_allow_html=True)

ENTER_JS = r"""
(function(){
 if(window.__enterNav) return; window.__enterNav=true;
 var SEL='input[type=text],input[type=password],input[type=number],input:not([type])';
 function ok(el){return el.matches(SEL)&&!el.closest('[data-baseweb=select],[data-testid=stDateInput],[data-testid=stFileUploader]')&&!el.disabled&&!el.readOnly&&el.offsetParent!==null;}
 function action(t){var el=t.parentElement;while(el){
   var bs=[].slice.call(el.querySelectorAll('button')).filter(function(b){return !b.disabled&&b.offsetParent!==null&&(t.compareDocumentPosition(b)&4);});
   if(bs.length){var p=bs.filter(function(b){return /primary/i.test((b.getAttribute('kind')||'')+(b.getAttribute('data-testid')||''));})[0];return {scope:el,btn:p||bs[0]};}
   el=el.parentElement;} return null;}
 document.addEventListener('keydown',function(e){
  if(e.key!=='Enter'||e.shiftKey||e.isComposing) return;
  var t=e.target; if(!t||!t.matches||!ok(t)) return;
  var form=t.closest('[data-testid=stForm]'), act=form?null:action(t);
  var scope=form||(act&&act.scope); if(!scope) return;
  var list=[].slice.call(scope.querySelectorAll(SEL)).filter(ok), i=list.indexOf(t);
  if(i<0) return;
  if(i<list.length-1){e.preventDefault();e.stopPropagation();list[i+1].focus();if(list[i+1].select)list[i+1].select();return;}
  if(form) return;
  e.preventDefault();e.stopPropagation();t.blur();
  if(act&&act.btn) setTimeout(function(){act.btn.click();},250);
 },true);
})();
"""
def enter_nav():
    """Enter moves to the next text box; Enter in the last box submits the form / presses the action button.
    The script is loaded every way Streamlit allows (each is guarded, so it only runs once)."""
    try: st.html("<script>" + ENTER_JS + "</script>", unsafe_allow_javascript=True)
    except Exception: pass
    try:
        components.html("<script>try{var s=window.parent.document.createElement('script');s.textContent=" + json.dumps(ENTER_JS) +
                        ";window.parent.document.head.appendChild(s);}catch(e){}</script>", height=0)
    except Exception: pass
