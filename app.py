import streamlit as st
import pickle
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ReadMatch — Find Your Next Book",
    page_icon="🔖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — midnight library / premium dark
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6e0d4;
}

.main .block-container {
    padding: 0rem 3.5rem 4rem 3.5rem;
    max-width: 1380px;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.4rem 0 1.2rem 0;
    border-bottom: 1px solid #1e2530;
    margin-bottom: 0;
}
.topbar-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #e6e0d4;
    letter-spacing: 0.01em;
}
.topbar-logo span {
    color: #c9a84c;
}
.topbar-tag {
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5a6070;
    font-weight: 500;
}

/* ── Hero ── */
.hero-wrap {
    padding: 5rem 0 3.5rem 0;
    max-width: 720px;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 1.4rem;
}
.hero-eyebrow::before {
    content: "";
    width: 28px;
    height: 1px;
    background: #c9a84c;
    display: inline-block;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    line-height: 1.08;
    color: #f0ebe0;
    margin: 0 0 1.4rem 0;
    font-weight: 400;
}
.hero-title em {
    font-style: italic;
    color: #c9a84c;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #8b8578;
    line-height: 1.65;
    max-width: 480px;
}

/* ── Stat strip ── */
.stat-strip {
    display: flex;
    gap: 2.5rem;
    padding: 1.6rem 0;
    border-top: 1px solid #1e2530;
    border-bottom: 1px solid #1e2530;
    margin: 2rem 0 2.8rem 0;
}
.stat-item { text-align: left; }
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #c9a84c;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5a6070;
    font-weight: 500;
    margin-top: 0.2rem;
}

/* ── Search panel ── */
.search-panel {
    background: #131920;
    border: 1px solid #1e2a38;
    border-radius: 16px;
    padding: 2rem 2.2rem 2.2rem 2.2rem;
    margin-bottom: 2.5rem;
}
.panel-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5a6070;
    margin-bottom: 0.7rem;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background-color: #0d1117 !important;
    border: 1.5px solid #2a3545 !important;
    border-radius: 10px !important;
    color: #e6e0d4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1rem !important;
    min-height: 52px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
div[data-baseweb="select"] > div:hover {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important;
}
div[data-baseweb="select"] svg { fill: #5a6070 !important; }

div[data-baseweb="popover"] * {
    background-color: #131920 !important;
    color: #e6e0d4 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #1e2a38 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #c9a84c 0%, #a8863a 100%) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(201,168,76,0.25) !important;
    min-height: 52px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(201,168,76,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Selected pill ── */
.selected-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 100px;
    padding: 0.35rem 1rem 0.35rem 0.7rem;
    font-size: 0.82rem;
    color: #c9a84c;
    margin-top: 1rem;
}
.selected-pill .dot {
    width: 7px; height: 7px;
    background: #c9a84c;
    border-radius: 50%;
    flex-shrink: 0;
}
.selected-pill .book-name { font-weight: 600; color: #e6e0d4; }

/* ── Results heading ── */
.results-heading {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin: 2.5rem 0 1.6rem 0;
}
.results-heading h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    font-weight: 400;
    color: #f0ebe0;
    margin: 0;
}
.results-heading .count-tag {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5a6070;
    background: #131920;
    border: 1px solid #1e2530;
    border-radius: 100px;
    padding: 0.22rem 0.7rem;
}

/* ── Book card ── */
.book-card {
    background: #131920;
    border: 1px solid #1e2530;
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
}
.book-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
    border-color: rgba(201,168,76,0.4);
}
.book-card-img-wrap {
    background: #0d1117;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.2rem;
    min-height: 230px;
    position: relative;
}
.book-card-img-wrap img {
    max-height: 200px;
    width: auto;
    max-width: 100%;
    display: block;
    border-radius: 4px;
    box-shadow: 6px 8px 28px rgba(0,0,0,0.55);
}
.rank-badge {
    position: absolute;
    top: 0.75rem;
    left: 0.75rem;
    width: 28px; height: 28px;
    background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.35);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-weight: 700;
    color: #c9a84c;
    font-family: 'Inter', sans-serif;
}
.book-card-body {
    padding: 1rem 1.1rem 1.2rem 1.1rem;
    border-top: 1px solid #1e2530;
}
.book-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 0.95rem;
    color: #e6e0d4;
    line-height: 1.4;
    margin: 0;
    font-weight: 400;
}
.book-card-meta {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a6070;
    font-weight: 500;
    margin-top: 0.5rem;
}

/* ── No-image placeholder ── */
.no-img {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #1a2235, #131920);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    border-radius: 4px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #3a4050;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1a1f28;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    books = pickle.load(open('books.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return books, similarity

books, similarity = load_data()

# ─────────────────────────────────────────────
# RECOMMEND FUNCTION
# ─────────────────────────────────────────────
def recommend(book_name):
    if book_name not in books['title'].values:
        return [], []

    book_index = books[books['title'] == book_name].index[0]
    distances = similarity[book_index]

    books_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_books, recommended_images = [], []
    for i in books_list:
        recommended_books.append(books.iloc[i[0]].title)
        recommended_images.append(books.iloc[i[0]].thumbnail)

    return recommended_books, recommended_images

# ─────────────────────────────────────────────
# UI LAYOUT
# ─────────────────────────────────────────────

# ── Top Bar ──
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">read<span>match</span></div>
    <div class="topbar-tag">Content-Based Recommendation Engine</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──
total_books = len(books)
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-eyebrow">AI-Powered Discovery</div>
    <h1 class="hero-title">Your next great read<br>is <em>one search away.</em></h1>
    <p class="hero-sub">
        ReadMatch uses content-based filtering to surface books that share
        the DNA of what you already love — authors, genre, themes, and more.
    </p>
</div>

<div class="stat-strip">
    <div class="stat-item">
        <div class="stat-num">{total_books:,}</div>
        <div class="stat-lbl">Books Indexed</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">5</div>
        <div class="stat-lbl">Picks Per Query</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">ML</div>
        <div class="stat-lbl">Powered</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Search Panel ──
st.markdown('<div class="search-panel">', unsafe_allow_html=True)
st.markdown('<p class="panel-label">🔖 Search by book title</p>', unsafe_allow_html=True)

col_select, col_btn = st.columns([5, 1.2], gap="medium")

with col_select:
    selected_book = st.selectbox(
        label="",
        options=books['title'].values,
        label_visibility="collapsed"
    )

with col_btn:
    st.markdown('<div style="padding-top:0.1rem">', unsafe_allow_html=True)
    recommend_clicked = st.button("Find Matches →")
    st.markdown('</div>', unsafe_allow_html=True)

if selected_book:
    st.markdown(f"""
    <div class="selected-pill">
        <span class="dot"></span>
        <span>Selected: <span class="book-name">{selected_book}</span></span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Results ──
if recommend_clicked:
    with st.spinner("Scanning the library…"):
        names, images = recommend(selected_book)

    if names:
        st.markdown("""
        <div class="results-heading">
            <h2>Recommended Reads</h2>
            <span class="count-tag">5 Matches Found</span>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(5, gap="medium")

        for i, col in enumerate(cols):
            with col:
                img_html = (
                    f'<img src="{images[i]}" alt="{names[i]}" />'
                    if images[i] and str(images[i]).startswith("http")
                    else '<div class="no-img">📚</div>'
                )
                st.markdown(f"""
                <div class="book-card">
                    <div class="book-card-img-wrap">
                        <div class="rank-badge">#{i+1}</div>
                        {img_html}
                    </div>
                    <div class="book-card-body">
                        <p class="book-card-title">{names[i]}</p>
                        <div class="book-card-meta">Match #{i+1}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Book not found in the index. Try another title.")

# ── Footer ──
st.markdown("""
<div class="footer">
    ReadMatch &nbsp;·&nbsp; Content-Based Book Recommendation Engine &nbsp;·&nbsp; Built with Streamlit & Scikit-learn
</div>
""", unsafe_allow_html=True)