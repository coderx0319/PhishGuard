import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import datetime

from main import main

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PhishGuard — Threat Analysis Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GLOBAL CSS — DARK MILITARY CYBER THEME
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;700&display=swap');

/* ---- ROOT VARIABLES ---- */
:root {
    --bg-primary:    #080d12;
    --bg-secondary:  #0d1520;
    --bg-card:       #101c2a;
    --bg-card-hover: #152236;
    --accent:        #00d4ff;
    --accent-dim:    #00a8cc;
    --accent-glow:   rgba(0, 212, 255, 0.15);
    --danger:        #ff3b3b;
    --danger-glow:   rgba(255, 59, 59, 0.2);
    --warning:       #ffb300;
    --warning-glow:  rgba(255, 179, 0, 0.2);
    --success:       #00e676;
    --success-glow:  rgba(0, 230, 118, 0.15);
    --text-primary:  #e8f4f8;
    --text-muted:    #6a8fa8;
    --border:        rgba(0, 212, 255, 0.15);
    --border-strong: rgba(0, 212, 255, 0.35);
    --font-mono:     'Share Tech Mono', monospace;
    --font-main:     'Exo 2', sans-serif;
    --font-heading:  'Rajdhani', sans-serif;
}

/* ---- BASE RESET ---- */
* { box-sizing: border-box; }

.stApp {
    background-color: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse at 10% 0%, rgba(0,212,255,0.04) 0%, transparent 55%),
        radial-gradient(ellipse at 90% 100%, rgba(0,100,180,0.06) 0%, transparent 55%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 39px,
            rgba(0,212,255,0.015) 39px,
            rgba(0,212,255,0.015) 40px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 79px,
            rgba(0,212,255,0.015) 79px,
            rgba(0,212,255,0.015) 80px
        );
    color: var(--text-primary) !important;
    font-family: var(--font-main) !important;
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}

/* ---- TYPOGRAPHY ---- */
h1 {
    font-family: var(--font-heading) !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    text-shadow: 0 0 20px rgba(0,212,255,0.5), 0 0 40px rgba(0,212,255,0.2) !important;
    margin-bottom: 0 !important;
}
h2, h3 {
    font-family: var(--font-heading) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
h4, h5, h6 {
    font-family: var(--font-main) !important;
    color: var(--text-muted) !important;
}
p, li, div { font-family: var(--font-main) !important; }
code, pre { font-family: var(--font-mono) !important; }

/* ---- SIDEBAR LOGO BLOCK ---- */
.sidebar-logo {
    background: linear-gradient(135deg, #0a1929 0%, #0d2035 100%);
    border-bottom: 1px solid var(--border);
    padding: 24px 20px 20px;
    margin-bottom: 8px;
}
.sidebar-logo .logo-mark {
    font-family: var(--font-heading);
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sidebar-logo .logo-sub {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}
.sidebar-version {
    display: inline-block;
    background: var(--accent-glow);
    border: 1px solid var(--border-strong);
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 0.6rem;
    padding: 2px 8px;
    border-radius: 3px;
    letter-spacing: 1px;
    margin-top: 8px;
}

/* ---- SIDEBAR FEATURE LIST ---- */
.feature-list {
    padding: 12px 20px;
}
.feature-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(0,212,255,0.05);
    font-family: var(--font-main);
    font-size: 0.82rem;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}
.feature-item:last-child { border-bottom: none; }
.feature-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
    flex-shrink: 0;
}
.feature-item span { color: var(--text-primary); }

/* ---- SIDEBAR CREDITS ---- */
.sidebar-credits {
    padding: 16px 20px;
    border-top: 1px solid var(--border);
    margin-top: 8px;
}
.credits-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.credits-name {
    font-family: var(--font-heading);
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 1px;
}
.credits-copy {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ---- STATUS BAR ---- */
.status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 16px;
    margin-bottom: 24px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
}
.status-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 8px var(--success);
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.status-time { color: var(--accent); }

/* ---- PAGE HEADER ---- */
.page-header {
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.header-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.header-subtitle {
    font-family: var(--font-main);
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 300;
    margin-top: 4px;
    letter-spacing: 0.5px;
}

/* ---- UPLOAD ZONE ---- */
.upload-container {
    background: var(--bg-card);
    border: 1px dashed var(--border-strong);
    border-radius: 10px;
    padding: 32px 24px;
    text-align: center;
    transition: all 0.3s ease;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.upload-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    animation: scan-line 3s linear infinite;
}
@keyframes scan-line {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
.upload-title {
    font-family: var(--font-heading);
    font-size: 1.1rem;
    color: var(--text-primary);
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.upload-hint {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 1px;
}

/* ---- METRIC CARDS ---- */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 18px 20px !important;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border-strong) !important;
    box-shadow: 0 0 16px var(--accent-glow) !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-heading) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
    text-shadow: 0 0 12px var(--accent-glow);
}

/* ---- SECTION HEADINGS ---- */
.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.section-heading-text {
    font-family: var(--font-heading);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: 2px;
}
.section-tag {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--accent);
    background: var(--accent-glow);
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: 3px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-left: auto;
}

/* ---- RISK BANNERS ---- */
.risk-banner {
    border-radius: 10px;
    padding: 20px 24px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 16px;
    border: 1px solid;
    font-family: var(--font-heading);
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.risk-banner.high {
    background: var(--danger-glow);
    border-color: var(--danger);
    color: var(--danger);
    box-shadow: 0 0 24px rgba(255,59,59,0.15);
    animation: pulse-risk 2s ease-in-out infinite;
}
.risk-banner.medium {
    background: var(--warning-glow);
    border-color: var(--warning);
    color: var(--warning);
}
.risk-banner.low {
    background: var(--success-glow);
    border-color: var(--success);
    color: var(--success);
}
@keyframes pulse-risk {
    0%, 100% { box-shadow: 0 0 24px rgba(255,59,59,0.15); }
    50% { box-shadow: 0 0 40px rgba(255,59,59,0.35); }
}
.risk-icon { font-size: 1.8rem; }
.risk-label { flex: 1; }
.risk-sublabel {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    opacity: 0.7;
    display: block;
    margin-top: 3px;
    letter-spacing: 2px;
}

/* ---- REASON TAGS ---- */
.reason-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}
.reason-tag {
    background: var(--bg-card);
    border: 1px solid var(--border-strong);
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 5px 12px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}

/* ---- JSON BOXES ---- */
.stJson, [data-testid="stJson"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
}

/* ---- STREAMLIT FILE UPLOADER ---- */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] label {
    font-family: var(--font-mono) !important;
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
[data-testid="stFileDropzone"] {
    background: transparent !important;
    border: 1px dashed var(--border-strong) !important;
    border-radius: 8px !important;
}

/* ---- BUTTONS ---- */
.stButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 6px !important;
    font-family: var(--font-heading) !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 10px 28px !important;
    transition: all 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: var(--accent-glow) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.25) !important;
    transform: translateY(-1px) !important;
}

/* ---- PROGRESS BAR ---- */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent-dim), var(--accent)) !important;
    box-shadow: 0 0 10px var(--accent) !important;
    border-radius: 4px !important;
}
[data-testid="stProgressBar"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    height: 8px !important;
}

/* ---- ALERTS ---- */
.stAlert {
    border-radius: 8px !important;
    font-family: var(--font-main) !important;
}

/* ---- DIVIDER ---- */
hr {
    border-color: var(--border) !important;
    margin: 24px 0 !important;
}

/* ---- DOWNLOAD BUTTON ---- */
.stDownloadButton > button {
    background: var(--accent-glow) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 6px !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,212,255,0.2) !important;
    box-shadow: 0 0 18px rgba(0,212,255,0.3) !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-dim); }

/* ---- FOOTER ---- */
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
header { visibility: hidden !important; }

/* ---- TABS ---- */
[data-testid="stTabs"] button {
    font-family: var(--font-heading) !important;
    font-size: 0.8rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

/* ---- SUCCESS / ERROR TEXT ---- */
.stSuccess { background: var(--success-glow) !important; border-color: var(--success) !important; }
.stError   { background: var(--danger-glow)  !important; border-color: var(--danger)  !important; }
.stWarning { background: var(--warning-glow) !important; border-color: var(--warning) !important; }
.stInfo    { background: var(--accent-glow)  !important; border-color: var(--accent)  !important; }

</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-mark">🛡️ PhishGuard</div>
        <div class="logo-sub">Threat Analysis Platform</div>
        <div class="sidebar-version">v2.0.0 — STABLE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-list">
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#6a8fa8;
                    text-transform:uppercase; letter-spacing:2px; margin-bottom:10px;">
            CAPABILITIES
        </div>
        <div class="feature-item"><div class="feature-dot"></div><span>IOC Extraction</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>VirusTotal Integration</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>AbuseIPDB Lookup</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>WHOIS Intelligence</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>SPF / DMARC Validation</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>HTML Phishing Analysis</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>URL Expansion Engine</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>Risk Scoring Engine</span></div>
        <div class="feature-item"><div class="feature-dot"></div><span>Attachment Scanning</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="padding: 0 20px; margin-bottom: 12px;">
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#6a8fa8;
                    text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;">
            HOW TO USE
        </div>
        <div style="font-family:'Exo 2',sans-serif; font-size:0.78rem; color:#a0bdd0; line-height:1.7;">
            1. Upload a <code style="color:#00d4ff;">.eml</code> file<br>
            2. Click <strong style="color:#e8f4f8;">Run Analysis</strong><br>
            3. Review threat report<br>
            4. Export JSON report
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-credits">
        <div class="credits-label">Built By</div>
        <div class="credits-name">Shantanu Vedante</div>
        <div class="credits-copy">© 2026 — All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# STATUS BAR (FIXED datetime)
# =========================
now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d  %H:%M:%S UTC")
st.markdown(f"""
<div class="status-bar">
    <div class="status-indicator">
        <div class="status-dot"></div>
        <span>SYSTEM ONLINE</span>
    </div>
    <span>PhishGuard Threat Intelligence Platform</span>
    <span class="status-time">{now}</span>
</div>
""", unsafe_allow_html=True)

# =========================
# PAGE HEADER
# =========================
st.markdown('<div class="header-eyebrow">// PHISHING EMAIL ANALYSIS DASHBOARD</div>', unsafe_allow_html=True)
st.title("🛡️ PhishGuard")
st.markdown('<div class="header-subtitle">Analyze suspicious emails with multi-source threat intelligence & OSINT enrichment</div>', unsafe_allow_html=True)
st.markdown("---")


# =========================
# UPLOAD SECTION
# =========================
st.markdown("""
<div class="section-heading">
    <span class="section-heading-text">📤 Email Submission</span>
    <span class="section-tag">Step 01</span>
</div>
""", unsafe_allow_html=True)

col_up, col_info = st.columns([2, 1])

with col_up:
    uploaded_file = st.file_uploader(
        "UPLOAD EMAIL FILE (.eml)",
        type=["eml"],
        help="Upload a raw .eml email file for analysis"
    )

with col_info:
    st.markdown("""
    <div style="background: #0d1520; border: 1px solid rgba(0,212,255,0.15);
                border-radius: 10px; padding: 18px; height: 100%;">
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem;
                    color:#6a8fa8; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px;">
            SUPPORTED FORMATS
        </div>
        <div style="font-family:'Exo 2',sans-serif; font-size:0.82rem; color:#a0bdd0; line-height:1.9;">
            ✦ &nbsp;<code style="color:#00d4ff;">.eml</code> — Raw email files<br>
            ✦ &nbsp;Exported from Outlook, Gmail,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Thunderbird, Apple Mail<br>
            ✦ &nbsp;Max file size: <span style="color:#e8f4f8;">25 MB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# ANALYSIS FLOW (FIXED)
# =========================
if uploaded_file:
    os.makedirs("samples", exist_ok=True)
    file_path = os.path.join("samples", "uploaded.eml")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✅  **{uploaded_file.name}** uploaded successfully — ready for analysis")

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, col_hint = st.columns([1, 3])
    with col_btn:
        run = st.button("🔍  Run Analysis")

    if run:

        st.markdown("---")
        st.markdown("""
        <div class="section-heading">
            <span class="section-heading-text">⚙️ Analysis Engine</span>
            <span class="section-tag">Processing</span>
        </div>
        """, unsafe_allow_html=True)

        # ✅ phases defined correctly
        phases = [
            ("🔎", "Parsing Email Headers"),
            ("🧬", "Extracting IOCs"),
            ("🌐", "Querying VirusTotal"),
            ("🛰️", "AbuseIPDB Lookup"),
            ("📡", "WHOIS Intelligence"),
            ("🔐", "SPF / DMARC Validation"),
            ("🕵️", "HTML Phishing Analysis"),
            ("📊", "Scoring Risk Level"),
        ]

        # UI slots
        phase_cols = st.columns(len(phases))
        phase_slots = []

        for i, (icon, label) in enumerate(phases):
            with phase_cols[i]:
                slot = st.empty()
                slot.markdown(f"""
                <div style="text-align:center; padding:8px 4px;
                            background:#0d1520; border:1px solid rgba(0,212,255,0.1);
                            border-radius:8px; font-size:0.75rem; color:#6a8fa8;
                            font-family:'Exo 2',sans-serif;">
                    <div style="font-size:1.2rem; margin-bottom:4px;">{icon}</div>
                    {label}
                </div>
                """, unsafe_allow_html=True)
                phase_slots.append(slot)

        st.markdown("<br>", unsafe_allow_html=True)

        progress = st.progress(0)
        current_progress = 0

        # ✅ FIXED LOOP (correct indentation + logic)
        for i, (icon, label) in enumerate(phases):

            phase_slots[i].markdown(f"""
            <div style="text-align:center; padding:8px 4px;
                        background:rgba(0,212,255,0.08); border:1px solid rgba(0,212,255,0.4);
                        border-radius:8px; font-size:0.75rem; color:#00d4ff;
                        font-family:'Exo 2',sans-serif;
                        box-shadow: 0 0 10px rgba(0,212,255,0.15);">
                <div style="font-size:1.2rem; margin-bottom:4px;">{icon}</div>
                <strong>{label}</strong>
            </div>
            """, unsafe_allow_html=True)

            target = int((i + 1) * (100 / len(phases)))

            while current_progress < target:
                current_progress += 1
                progress.progress(current_progress)   # ✅ fixed call
                time.sleep(0.005)

        # ✅ MAIN EXECUTION CORRECT POSITION
        main()

        st.success("✔ Analysis complete — report generated")
        # ============================
        # LOAD & DISPLAY REPORT
        # ============================
        if os.path.exists("report.json"):
            with open("report.json") as f:
                data = json.load(f)

            st.markdown("---")

            # ---- METRICS ROW ----
            st.markdown("""
            <div class="section-heading">
                <span class="section-heading-text">📊 Executive Summary</span>
                <span class="section-tag">Report</span>
            </div>
            """, unsafe_allow_html=True)

            urls_count    = len(data.get("iocs", {}).get("urls", []))
            ip_count      = len(data.get("iocs", {}).get("ips", []))
            attach_count  = len(data.get("attachments", []))
            risk          = data.get("risk_score", "UNKNOWN")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🔗 URLs Detected",    urls_count)
            c2.metric("🌐 IPs Identified",   ip_count)
            c3.metric("📎 Attachments",      attach_count)
            c4.metric("🚨 Risk Level",       risk)

            # ---- RISK BANNER ----
            risk_class = risk.lower() if risk in ("HIGH", "MEDIUM", "LOW") else "low"
            risk_icons = {"high": "☠️", "medium": "⚠️", "low": "✅"}
            risk_descs = {
                "high":   "THREAT CONFIRMED — Immediate action required",
                "medium": "SUSPICIOUS INDICATORS — Review recommended",
                "low":    "LOW THREAT LEVEL — No immediate action needed",
            }
            st.markdown(f"""
            <div class="risk-banner {risk_class}">
                <span class="risk-icon">{risk_icons.get(risk_class, '❓')}</span>
                <span class="risk-label">
                    {risk} RISK
                    <span class="risk-sublabel">{risk_descs.get(risk_class, '')}</span>
                </span>
            </div>
            """, unsafe_allow_html=True)

            # ---- RISK REASONS ----
            reasons = data.get("risk_reasons", [])
            if reasons:
                st.markdown("""
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
                            color:#6a8fa8; text-transform:uppercase; letter-spacing:2px;
                            margin-bottom:8px;">
                    Risk Indicators
                </div>
                """, unsafe_allow_html=True)
                tags_html = "".join([f'<span class="reason-tag">⚑ {r}</span>' for r in reasons])
                st.markdown(f'<div class="reason-tags">{tags_html}</div>', unsafe_allow_html=True)

            st.markdown("---")

            # ---- TABS FOR DETAILED REPORT ----
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "  IOC & URLs  ",
                "  Threat Intel  ",
                "  Auth & WHOIS  ",
                "  HTML Analysis  ",
                "  Attachments  ",
            ])

            # ---- TAB 1: IOCs & URLs ----
            with tab1:
                st.markdown("""
                <div class="section-heading">
                    <span class="section-heading-text">Indicators of Compromise</span>
                </div>
                """, unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("""
                    <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem;
                                color:#6a8fa8; text-transform:uppercase; letter-spacing:2px;
                                margin-bottom:8px;">Extracted IOCs</div>
                    """, unsafe_allow_html=True)
                    st.json(data.get("iocs", {}))
                with col_b:
                    st.markdown("""
                    <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem;
                                color:#6a8fa8; text-transform:uppercase; letter-spacing:2px;
                                margin-bottom:8px;">Expanded URLs</div>
                    """, unsafe_allow_html=True)
                    st.json(data.get("expanded_urls", []))

            # ---- TAB 2: THREAT INTEL / VT CHART ----
            with tab2:
                st.markdown("""
                <div class="section-heading">
                    <span class="section-heading-text">VirusTotal Detection Summary</span>
                </div>
                """, unsafe_allow_html=True)

                vt_data    = data.get("threat_intel", {}).get("virustotal", [])
                stats_list = [item.get("stats", {}) for item in vt_data if item.get("stats")]

                if stats_list:
                    combined = {"malicious": 0, "suspicious": 0, "harmless": 0, "undetected": 0}
                    for stat in stats_list:
                        for key in combined:
                            combined[key] += stat.get(key, 0)

                    labels = list(combined.keys())
                    values = list(combined.values())
                    colors = ["#ff3b3b", "#ffb300", "#00e676", "#6a8fa8"]

                    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
                    fig.patch.set_facecolor("#080d12")

                    # Bar chart
                    ax1 = axes[0]
                    ax1.set_facecolor("#0d1520")
                    bars = ax1.bar(labels, values, color=colors, width=0.55, zorder=3)
                    for bar, val in zip(bars, values):
                        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                                 str(val), ha='center', va='bottom',
                                 color='#e8f4f8', fontsize=9, fontfamily='monospace')
                    ax1.set_title("Detection Breakdown", color="#00d4ff", fontsize=10, pad=10,
                                  fontfamily='monospace', fontweight='bold')
                    ax1.tick_params(colors="#6a8fa8", labelsize=8)
                    ax1.set_ylabel("Count", color="#6a8fa8", fontsize=8)
                    for spine in ax1.spines.values():
                        spine.set_color((0, 212/255, 1, 0.15))
                    ax1.yaxis.set_label_coords(-0.1, 0.5)
                    ax1.grid(axis='y', color=(0, 212/255, 1, 0.08), linestyle='--', zorder=0)
                    ax1.set_axisbelow(True)

                    # Pie chart
                    ax2 = axes[1]
                    ax2.set_facecolor("#0d1520")
                    wedge_props = dict(width=0.55, edgecolor='#080d12', linewidth=2)
                    ax2.pie(values, labels=None, colors=colors,
                            autopct='%1.0f%%', pctdistance=0.75,
                            wedgeprops=wedge_props, startangle=90,
                            textprops={'color': '#e8f4f8', 'fontsize': 8, 'fontfamily': 'monospace'})
                    legend_patches = [mpatches.Patch(color=c, label=l.capitalize()) for c, l in zip(colors, labels)]
                    ax2.legend(handles=legend_patches, loc='lower center',
                               bbox_to_anchor=(0.5, -0.1), ncol=2,
                               frameon=False, labelcolor='#a0bdd0',
                               prop={'family': 'monospace', 'size': 7})
                    ax2.set_title("Detection Distribution", color="#00d4ff", fontsize=10, pad=10,
                                  fontfamily='monospace', fontweight='bold')

                    plt.tight_layout(pad=2.5)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("No VirusTotal data available in this report.")

                st.markdown("""
                <div class="section-heading" style="margin-top:24px;">
                    <span class="section-heading-text">Raw Threat Intelligence</span>
                </div>
                """, unsafe_allow_html=True)
                st.json(data.get("threat_intel", {}))

            # ---- TAB 3: AUTH & WHOIS ----
            with tab3:
                col_w, col_a = st.columns(2)
                with col_w:
                    st.markdown("""
                    <div class="section-heading">
                        <span class="section-heading-text">🌍 WHOIS Intelligence</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.json(data.get("whois", []))
                with col_a:
                    st.markdown("""
                    <div class="section-heading">
                        <span class="section-heading-text">📧 SPF / DMARC Auth</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.json(data.get("email_auth", []))

            # ---- TAB 4: HTML ANALYSIS ----
            with tab4:
                st.markdown("""
                <div class="section-heading">
                    <span class="section-heading-text">HTML Phishing Signals</span>
                </div>
                """, unsafe_allow_html=True)
                st.json(data.get("html_analysis", []))

            # ---- TAB 5: ATTACHMENTS ----
            with tab5:
                st.markdown("""
                <div class="section-heading">
                    <span class="section-heading-text">Attachment Analysis</span>
                </div>
                """, unsafe_allow_html=True)
                st.json(data.get("attachments", []))

            # ---- DOWNLOAD ----
            st.markdown("---")
            st.markdown("""
            <div class="section-heading">
                <span class="section-heading-text">⬇️ Export Report</span>
                <span class="section-tag">JSON</span>
            </div>
            """, unsafe_allow_html=True)

            col_dl, col_dl2 = st.columns([1, 3])
            with col_dl:
                st.download_button(
                    label="⬇️  Download JSON Report",
                    data=json.dumps(data, indent=4),
                    file_name=f"phishguard_report_{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d  %H:%M:%S UTC')}.json",
                    mime="application/json"
                )
            with col_dl2:
                st.markdown("""
                <div style="padding-top:12px; font-family:'Share Tech Mono',monospace;
                            font-size:0.68rem; color:#6a8fa8;">
                    Full structured report with all IOCs, threat intel, risk scoring & metadata
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ Report file not generated. Please check the backend (`main.py`) for errors.")

# =========================
# EMPTY STATE (no file)
# =========================
else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; opacity:0.5;">
        <div style="font-size:3.5rem; margin-bottom:16px;">📭</div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem;
                    color:#6a8fa8; text-transform:uppercase; letter-spacing:2px;">
            No email loaded
        </div>
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.7rem;
                    color:#4a6a80; margin-top:8px;">
            Upload a .eml file above to begin threat analysis
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
            padding: 4px 0 12px;
            font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#4a6a80;">
    <span>🛡️ PhishGuard — Phishing Threat Intelligence Platform</span>
    <span>Built by <span style="color:#00d4ff;">Shantanu Vedante</span> &nbsp;·&nbsp; © 2026</span>
</div>
""", unsafe_allow_html=True)