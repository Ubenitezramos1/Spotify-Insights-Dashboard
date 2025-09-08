# ui_wireframe.py
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Spotify Music Insights", page_icon="🎵", layout="wide")

# --------- Minimal CSS (clean spacing + subtle borders) ----------
st.markdown("""
<style>
/* overall spacing */
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
/* cards */
.card {background: #ffffff; border: 1px solid #e9e9e9; border-radius: 12px; padding: 16px;}
.card-soft {background: #f8f8f8; border: 1px solid #ececec; border-radius: 12px; padding: 14px;}
/* section headers */
.hdr {font-weight: 700; font-size: 1.05rem; margin-bottom: 0.35rem;}
.subtle {color: #777;}
.hr {height: 1px; background: #eee; margin: 8px 0 12px 0;}
/* pill buttons (Streamlit buttons are fine; this just tightens layout) */
.btnrow button {margin-right: 8px;}
/* sidebar step styling */
.step {display:flex; align-items:center; gap:.5rem; margin: .25rem 0;}
.step-dot {width: 14px; height: 14px; border-radius: 50%; background: #e0e0e0; display:inline-block;}
.step-dot.done {background: #1DB954;}
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("🎵 Spotify Music Insights Dashboard")
st.caption("Personal analytics from your listening history.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- LAYOUT ----------------------
left, right = st.columns([0.23, 0.77], gap="medium")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("#### Steps")
    # Step indicators (wireframe)
    st.markdown("""
    <div class="step"><span class="step-dot done"></span> 1. Connect Spotify</div>
    <div class="step"><span class="step-dot"></span> 2. Load Data</div>
    <div class="step"><span class="step-dot"></span> 3. View Insights</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-soft" style="margin-top:16px;">', unsafe_allow_html=True)
    st.write("**Privacy**")
    st.caption("Read-only access. No sharing. Revoke anytime.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.caption("GitHub • Docs")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("#### Welcome, Uriel!")
    st.markdown('<div class="card-soft">', unsafe_allow_html=True)
    st.write("**Data Loader**")
    c1, c2, c3 = st.columns([0.35, 0.33, 0.32])
    with c1:
        tr = st.selectbox("Top Tracks Time Range", ["short_term", "medium_term", "long_term"], index=0)
    with c2:
        load_top = st.button("Load Top Tracks", use_container_width=True)
    with c3:
        load_recent = st.button("Load Recent Plays", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- DASHBOARDS (placeholders for now) ----
    st.write("### Dashboards")

    # Top Tracks section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("#### Top Tracks")
    st.info("No tracks yet — load data to get started.")
    # (Later: insert your matplotlib bar chart here)
    st.markdown('</div>', unsafe_allow_html=True)

    # Mood Profile
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.write("#### Mood Profile")
    st.info("Load top tracks to compute danceability, energy, and valence averages.")
    # (Later: show a small table of averages)
    st.markdown('</div>', unsafe_allow_html=True)

    # Recent Activity
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.write("#### Recent Activity")
    st.info("No recent plays captured yet.")
    # (Later: show a dataframe with Song | Artist | Played At)
    st.markdown('</div>', unsafe_allow_html=True)

    # CSV downloads (stub)
    st.caption("Tip: Export CSVs from each section once data is loaded.")

# ------------- Empty/Error/Success microcopy examples -------------
# (Use these messages in your loaders later)
# st.success("Loaded 50 top tracks.")
# st.warning("We didn't find recent activity — listen a bit and reload.")
# st.error("Session expired — please reconnect Spotify.")
