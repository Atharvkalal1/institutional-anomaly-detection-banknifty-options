# -*- coding: utf-8 -*-
"""Dashboard CSS, kept out of app.py.

Pure presentation layer: colors, spacing, glassmorphism, typography and
micro-animations for the Bank Nifty surveillance dashboard. No Python
logic, data flow, or Streamlit widget behaviour lives here — this module
only injects CSS via st.markdown(unsafe_allow_html=True).
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
    --bg:#070B14;
    --card:rgba(15,20,35,.75);
    --card-border:rgba(255,255,255,0.08);
    --blue:#00CFFF;
    --cyan:#3ABEFF;
    --purple:#8B5CF6;
    --green:#22C55E;
    --red:#EF4444;
    --text:#F3F6FB;
    --text-dim:#8791A8;
}

/* ---------------------------------------------------------------- */
/* Base app shell                                                    */
/* ---------------------------------------------------------------- */
html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* animated backdrop: soft grid + radial glow, fixed behind everything */
.stApp::before{
    content:"";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(0,207,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,207,255,0.05) 1px, transparent 1px);
    background-size: 46px 46px;
    mask-image: radial-gradient(ellipse 75% 55% at 50% 0%, #000 20%, transparent 75%);
    animation: gridDrift 40s linear infinite;
}
.stApp::after{
    content:"";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(680px circle at 12% 8%, rgba(0,207,255,0.10), transparent 55%),
        radial-gradient(640px circle at 92% 4%, rgba(139,92,246,0.10), transparent 55%),
        radial-gradient(900px circle at 50% 100%, rgba(0,207,255,0.04), transparent 60%);
}
@keyframes gridDrift{
    0%{ background-position: 0 0, 0 0; }
    100%{ background-position: 46px 46px, 46px 46px; }
}
.block-container{ position: relative; z-index: 1; padding-top: 1.6rem; max-width: 1400px; }

::-webkit-scrollbar{ width:10px; height:10px; }
::-webkit-scrollbar-track{ background: transparent; }
::-webkit-scrollbar-thumb{ background: rgba(0,207,255,0.25); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover{ background: rgba(0,207,255,0.45); }

/* ---------------------------------------------------------------- */
/* Header                                                             */
/* ---------------------------------------------------------------- */
.surv-header{ display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:14px; margin-bottom:6px; }
.surv-title{ font-size: 2.15rem; font-weight: 800; letter-spacing:-0.01em; line-height:1.15; margin:0; }
.surv-title .grad{ background: linear-gradient(120deg, var(--blue), var(--cyan)); -webkit-background-clip:text; background-clip:text; color:transparent; }
.surv-title .plain{ color: var(--text); }
.surv-subtitle{ font-family:'JetBrains Mono', monospace; font-size: 0.78rem; letter-spacing:0.03em; color: var(--text-dim); margin-top: 6px; }
.session-badge{
    display:inline-flex; align-items:center; gap:8px;
    background: var(--card); border:1px solid var(--card-border); border-radius: 999px;
    padding: 7px 16px; font-family:'JetBrains Mono', monospace; font-size:0.72rem; color: var(--text-dim);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 0 0 1px rgba(0,207,255,0.05) inset;
}
.session-badge .pulse-dot{
    width:7px; height:7px; border-radius:50%; background: var(--green);
    box-shadow: 0 0 8px 2px rgba(34,197,94,0.6);
    animation: pulseDot 1.8s ease-in-out infinite;
}
@keyframes pulseDot{ 0%,100%{ opacity:1; transform:scale(1);} 50%{ opacity:.5; transform:scale(0.8);} }

/* ---------------------------------------------------------------- */
/* Glass card shell — applied to Streamlit's own bordered containers  */
/* ---------------------------------------------------------------- */
div[data-testid="stVerticalBlockBorderWrapper"]{
    background: var(--card) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px -12px rgba(0,0,0,0.55), 0 0 0 1px rgba(0,207,255,0.03) inset;
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    animation: fadeInUp .5s ease both;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{
    border-color: rgba(0,207,255,0.28) !important;
    box-shadow: 0 12px 40px -12px rgba(0,0,0,0.6), 0 0 24px -6px rgba(0,207,255,0.15);
    transform: translateY(-2px);
}
@keyframes fadeInUp{ from{ opacity:0; transform:translateY(10px);} to{ opacity:1; transform:translateY(0);} }

/* chart card gets a touch more glow + padding */
.chart-card div[data-testid="stVerticalBlockBorderWrapper"]{
    border-color: rgba(0,207,255,0.14) !important;
}
.chart-card div[data-testid="stVerticalBlockBorderWrapper"]:hover{
    box-shadow: 0 16px 48px -16px rgba(0,0,0,0.65), 0 0 32px -8px rgba(0,207,255,0.2);
}

/* ---------------------------------------------------------------- */
/* Metrics                                                            */
/* ---------------------------------------------------------------- */
[data-testid="stMetricValue"]{
    color: var(--text) !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    letter-spacing: -0.01em;
}
[data-testid="stMetricLabel"]{
    color: var(--text-dim) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}
.card-heading{
    font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--cyan); margin-bottom: 10px; display:flex; align-items:center; gap:8px;
}
.card-heading::before{ content:''; width:6px; height:6px; border-radius:50%; background: var(--cyan); box-shadow: 0 0 8px 2px rgba(58,190,255,0.6); }

/* status pill */
.status-pill{
    display:inline-flex; align-items:center; gap:6px; padding: 4px 12px; border-radius: 999px;
    font-family:'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 600; letter-spacing:0.04em;
    text-transform: uppercase; margin: 2px 0 8px 0; white-space: nowrap;
}
.status-pill.low{ color: var(--green); background: rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.35); box-shadow: 0 0 14px -4px rgba(34,197,94,0.5); }
.status-pill.medium{ color: #FBBF24; background: rgba(251,191,36,0.12); border:1px solid rgba(251,191,36,0.35); box-shadow: 0 0 14px -4px rgba(251,191,36,0.5); }
.status-pill.high{ color: var(--red); background: rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.35); box-shadow: 0 0 14px -4px rgba(239,68,68,0.5); }
.status-pill .dot{ width:6px; height:6px; border-radius:50%; background: currentColor; animation: pulseDot 1.8s ease-in-out infinite; }

.risk-score-big{ font-size: 2.6rem; font-weight: 800; letter-spacing:-0.02em; line-height:1; color: var(--text); }
.risk-score-big .of100{ font-size: 1.1rem; color: var(--text-dim); font-weight: 500; }

.risk-message{
    font-family:'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing:0.02em;
    line-height: 1.5; margin: 8px 0 4px 0; padding: 8px 10px;
    border-radius: 8px; white-space: normal; word-break: break-word;
}
.risk-message.low{ color: var(--green); background: rgba(34,197,94,0.08); border-left: 2px solid var(--green); }
.risk-message.medium{ color: #FBBF24; background: rgba(251,191,36,0.08); border-left: 2px solid #FBBF24; }
.risk-message.high{ color: var(--red); background: rgba(239,68,68,0.08); border-left: 2px solid var(--red); }

.component-row{ display:flex; flex-wrap:wrap; gap: 8px; margin-top: 10px; }
.component-chip{
    font-family:'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--text-dim);
    background: rgba(255,255,255,0.03); border:1px solid var(--card-border); border-radius: 8px; padding: 4px 9px;
}

/* ---------------------------------------------------------------- */
/* Buttons                                                            */
/* ---------------------------------------------------------------- */
.stButton > button, .stDownloadButton > button, .stLinkButton > a{
    background: rgba(0,207,255,0.06) !important;
    border: 1px solid rgba(0,207,255,0.28) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    backdrop-filter: blur(10px);
    transition: transform .2s ease, box-shadow .2s ease, background .2s ease, border-color .2s ease;
    position: relative;
    overflow: hidden;
}
.stButton > button:hover, .stDownloadButton > button:hover{
    background: rgba(0,207,255,0.14) !important;
    border-color: rgba(0,207,255,0.55) !important;
    box-shadow: 0 6px 24px -6px rgba(0,207,255,0.45);
    transform: translateY(-2px);
}
.stButton > button:active{ transform: translateY(0); }

/* ---------------------------------------------------------------- */
/* News panel                                                        */
/* ---------------------------------------------------------------- */
.news-scroll{ max-height: 420px; overflow-y: auto; padding-right: 4px; }
.news-item{
    border: 1px solid var(--card-border);
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 10px;
    font-size: 0.82rem;
    line-height: 1.45;
    transition: transform .2s ease, border-color .2s ease, background .2s ease;
}
.news-item:hover{
    border-color: rgba(0,207,255,0.3);
    background: rgba(0,207,255,0.04);
    transform: translateX(3px);
}
.news-item .headline a{ color: var(--text); text-decoration:none; font-weight: 600; }
.news-item .headline a:hover{ color: var(--cyan); }
.news-item .meta{ color: var(--text-dim); font-size: 0.72rem; margin-top: 6px; font-family:'JetBrains Mono', monospace; }
.sent-badge{
    display:inline-block; font-family:'JetBrains Mono', monospace; font-size: 0.66rem; font-weight:700;
    padding: 2px 8px; border-radius: 999px; margin-right: 8px; letter-spacing:0.03em;
}
.sent-badge.pos{ color: var(--green); background: rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.3); }
.sent-badge.neg{ color: var(--red); background: rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); }
.sent-badge.neu{ color: var(--text-dim); background: rgba(255,255,255,0.05); border:1px solid var(--card-border); }

/* ---------------------------------------------------------------- */
/* Chat input                                                        */
/* ---------------------------------------------------------------- */
[data-testid="stChatInput"]{
    background: var(--card) !important;
    border: 1px solid rgba(0,207,255,0.25) !important;
    border-radius: 999px !important;
    backdrop-filter: blur(14px);
    transition: border-color .25s ease, box-shadow .25s ease;
}
[data-testid="stChatInput"]:focus-within{
    border-color: rgba(0,207,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,207,255,0.12), 0 0 24px -6px rgba(0,207,255,0.4);
}
[data-testid="stChatInput"] textarea{ color: var(--text) !important; }
[data-testid="stChatMessage"]{
    background: var(--card) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(12px);
}

/* ---------------------------------------------------------------- */
/* Sidebar / misc                                                    */
/* ---------------------------------------------------------------- */
div[data-testid="stSidebar"]{ background-color: #070B14; border-right: 1px solid var(--card-border); }
[data-testid="stExpander"]{
    background: var(--card) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(12px);
}
hr{ border-color: var(--card-border) !important; }
.stCaption, [data-testid="stCaptionContainer"]{ color: var(--text-dim) !important; }

/* Plotly chart container polish */
.js-plotly-plot{ border-radius: 12px; overflow: hidden; }
</style>
"""


def load_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
