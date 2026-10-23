# Smart Attendance (Streamlit)

```
smart_attendance_streamlit/
├── streamlit_app.py     # the app (pages for admin, faculty, student)
├── core.py              # database, attendance maths, face recognition
├── ui.py                # premium styling and components
├── requirements.txt
├── .streamlit/config.toml   # theme
├── data/.gitkeep        # database and photos are created here
└── .gitignore
```
Run locally: `pip install -r requirements.txt` then `streamlit run streamlit_app.py`.
Deploy: push to GitHub (these files at the repo root), open share.streamlit.io, New app, main file `streamlit_app.py`, Advanced settings, Python 3.11.
Streamlit Cloud wipes its disk on restart, so data there is temporary.


Version 3.1 (shown in the sidebar). If the sidebar does not say 3.0, you are running an old copy.
