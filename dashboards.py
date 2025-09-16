import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from etl import df_top_tracks, df_recent_activity

def _download_button(df: pd.DataFrame, label: str, filename: str):
    if df is not None and not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(label=label, data=csv, file_name=filename, mime="text/csv")

def top_tracks_viz():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("#### Top Tracks")
    df = df_top_tracks()
    if df.empty:
        st.info("No tracks yet — load data to get started.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    topn = st.slider("How many tracks?", 5, 50, 10)
    top_df = df.head(topn).copy()

    # Bar chart (matplotlib, single figure)
    plt.figure()
    plt.barh(top_df["track_name"][::-1], top_df["popularity"][::-1])
    plt.xlabel("Popularity")
    plt.title(f"Top {topn} Tracks by Popularity")
    st.pyplot(plt.gcf())

    st.dataframe(top_df)
    _download_button(top_df, "Download Top Tracks CSV", "top_tracks.csv")
    st.markdown('</div>', unsafe_allow_html=True)

def mood_profile_viz():
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.write("#### Mood Profile")
    df = df_top_tracks()
    if df.empty:
        st.info("Load top tracks to compute danceability, energy, and valence averages.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    metrics = df[["danceability", "energy", "valence"]].dropna().mean().to_frame("Average").T
    st.table(metrics.round(2))
    _download_button(metrics, "Download Mood Averages CSV", "mood_profile.csv")
    st.markdown('</div>', unsafe_allow_html=True)

def recent_activity_viz():
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.write("#### Recent Activity")
    df = df_recent_activity()
    if df.empty:
        st.info("No recent plays captured yet.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.dataframe(df.head(200))  # show a chunk
    _download_button(df, "Download Recent Plays CSV", "recent_plays.csv")
    st.markdown('</div>', unsafe_allow_html=True)

def listening_heatmap_viz():
    """Hour x Weekday listening intensity from the 'plays' table."""
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.write("#### Listening Heatmap (Hour × Weekday)")

    df = df_recent_activity()
    if df.empty:
        st.info("Load recent plays to see your listening heatmap.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Parse timestamps and build hour/weekday features
    df = df.copy()
    df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce", utc=True).dt.tz_convert(None)
    df["hour"] = df["played_at"].dt.hour
    df["weekday"] = df["played_at"].dt.weekday  # 0=Mon ... 6=Sun

    pivot = df.pivot_table(index="weekday", columns="hour", values="track_name", aggfunc="count").fillna(0)

    # One chart per figure; let matplotlib pick default colormap
    plt.figure()
    plt.imshow(pivot.values, aspect="auto")
    plt.title("Plays by Weekday (rows) and Hour (cols)")
    plt.xlabel("Hour of Day (0–23)")
    plt.ylabel("Weekday (0=Mon … 6=Sun)")
    plt.colorbar(label="Play Count")
    st.pyplot(plt.gcf())

    # Provide downloadable raw matrix
    pivot_reset = pivot.reset_index()
    _download_button(pivot_reset, "Download Heatmap Matrix CSV", "listening_heatmap_matrix.csv")

    st.markdown('</div>', unsafe_allow_html=True)
