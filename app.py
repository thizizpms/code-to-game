import streamlit as st
import groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Code to Game", page_icon="🎮", layout="wide")

# ──────────────────────────────────────────
# FULL PAGE CUSTOM UI
# ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #000;
    color: #fff;
    font-family: 'Share Tech Mono', monospace;
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.game-header {
    text-align: center;
    padding: 40px 20px 20px;
    background: linear-gradient(180deg, #0a0a1a 0%, #000 100%);
    border-bottom: 2px solid #00ff88;
    position: relative;
    overflow: hidden;
}
.game-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,136,0.03) 2px,
        rgba(0,255,136,0.03) 4px
    );
    pointer-events: none;
}
.game-title {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(20px, 4vw, 42px);
    color: #00ff88;
    text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88, 0 0 80px #00ff88;
    letter-spacing: 4px;
    animation: pulse 2s ease-in-out infinite;
}
.game-subtitle {
    font-family: 'Orbitron', sans-serif;
    color: #888;
    margin-top: 10px;
    font-size: 13px;
    letter-spacing: 6px;
    text-transform: uppercase;
}
@keyframes pulse {
    0%, 100% { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88; }
    50% { text-shadow: 0 0 30px #00ff88, 0 0 60px #00ff88, 0 0 100px #00ff88; }
}

.main-layout {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 0;
    min-height: calc(100vh - 140px);
}

.sidebar-panel {
    background: #0a0a0a;
    border-right: 1px solid #1a1a1a;
    padding: 24px 16px;
}

.panel-title {
    font-family: 'Orbitron', sans-serif;
    color: #00ff88;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1a1a1a;
}

.algo-btn {
    width: 100%;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: #0f0f0f;
    border: 1px solid #222;
    color: #888;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.algo-btn:hover, .algo-btn.active {
    background: #001a0d;
    border-color: #00ff88;
    color: #00ff88;
    box-shadow: 0 0 10px rgba(0,255,136,0.2);
}

.game-arena {
    background: #050508;
    padding: 24px;
    position: relative;
}

.arena-top {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    align-items: flex-end;
}

.input-group {
    flex: 1;
}
.input-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.stTextInput input, .stNumberInput input {
    background: #0f0f0f !important;
    border: 1px solid #222 !important;
    color: #00ff88 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 4px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 10px rgba(0,255,136,0.2) !important;
}

.start-btn {
    background: #00ff88 !important;
    color: #000 !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 10px !important;
    padding: 12px 24px !important;
    border: none !important;
    cursor: pointer !important;
    letter-spacing: 1px !important;
    transition: all 0.2s !important;
}
.start-btn:hover {
    background: #00cc6a !important;
    box-shadow: 0 0 20px rgba(0,255,136,0.5) !important;
}

/* Visualization canvas */
.viz-container {
    background: #080810;
    border: 1px solid #1a1a1a;
    border-radius: 8px;
    padding: 20px;
    min-height: 300px;
    position: relative;
    overflow: hidden;
}

.bars-container {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 4px;
    height: 250px;
    padding: 10px;
}

.bar {
    flex: 1;
    max-width: 60px;
    border-radius: 4px 4px 0 0;
    position: relative;
    transition: all 0.3s ease;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 6px;
}
.bar-value {
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #000;
    font-weight: bold;
}
.bar-label {
    position: absolute;
    bottom: -20px;
    font-size: 9px;
    color: #555;
    font-family: 'Share Tech Mono', monospace;
}

/* Step info */
.step-info {
    background: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
    min-height: 80px;
}
.step-counter {
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    color: #555;
    letter-spacing: 2px;
    margin-bottom: 8px;
}
.step-text {
    font-family: 'Share Tech Mono', monospace;
    color: #00ff88;
    font-size: 13px;
    line-height: 1.6;
}

/* AI explanation box */
.ai-box {
    background: linear-gradient(135deg, #0a0a1a, #050510);
    border: 1px solid #1a1a3a;
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
}
.ai-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    color: #4466ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.ai-text {
    color: #aac4ff;
    font-size: 13px;
    line-height: 1.7;
    font-family: 'Share Tech Mono', monospace;
}

/* Stats bar */
.stats-row {
    display: flex;
    gap: 16px;
    margin-top: 16px;
}
.stat-box {
    flex: 1;
    background: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 6px;
    padding: 12px;
    text-align: center;
}
.stat-value {
    font-family: 'Press Start 2P', monospace;
    font-size: 16px;
    color: #00ff88;
}
.stat-label {
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    color: #555;
    letter-spacing: 2px;
    margin-top: 4px;
}

/* Controls */
.controls-row {
    display: flex;
    gap: 8px;
    margin-top: 16px;
    justify-content: center;
}

.stButton button {
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    border-radius: 4px !important;
}

/* Sidebar selectbox */
.stSelectbox select {
    background: #0f0f0f !important;
    color: #00ff88 !important;
    border-color: #222 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Speed slider */
.stSlider { padding: 0 !important; }

/* Legend */
.legend {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 12px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #666;
    font-family: 'Share Tech Mono', monospace;
}
.legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 2px;
}

.scanline {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(0,0,0,0.1) 3px,
        rgba(0,0,0,0.1) 4px
    );
    pointer-events: none;
    z-index: 9999;
}
</style>

<div class="scanline"></div>

<div class="game-header">
    <div class="game-title">⚡ CODE TO GAME ⚡</div>
    <div class="game-subtitle">Algorithm Visualizer — Watch Code Come Alive</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────
if "steps"        not in st.session_state: st.session_state.steps = []
if "current_step" not in st.session_state: st.session_state.current_step = 0
if "ai_explain"   not in st.session_state: st.session_state.ai_explain = ""
if "comparisons"  not in st.session_state: st.session_state.comparisons = 0
if "swaps"        not in st.session_state: st.session_state.swaps = 0
if "algo"         not in st.session_state: st.session_state.algo = "Bubble Sort"

# ──────────────────────────────────────────
# ALGORITHM ENGINES
# ──────────────────────────────────────────
def bubble_sort_steps(arr):
    steps = []
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n):
        for j in range(0, n-i-1):
            comparisons += 1
            comparing = [j, j+1]
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1
                steps.append({
                    "array": a.copy(),
                    "comparing": comparing,
                    "swapped": [j, j+1],
                    "sorted": list(range(n-i-1, n)),
                    "msg": f"🔄 Swapped {a[j+1]} and {a[j]} — bigger bubble floats up!",
                    "comparisons": comparisons,
                    "swaps": swaps
                })
            else:
                steps.append({
                    "array": a.copy(),
                    "comparing": comparing,
                    "swapped": [],
                    "sorted": list(range(n-i-1, n)),
                    "msg": f"✅ {a[j]} ≤ {a[j+1]} — already in order, no swap needed",
                    "comparisons": comparisons,
                    "swaps": swaps
                })
    steps.append({
        "array": a.copy(),
        "comparing": [],
        "swapped": [],
        "sorted": list(range(n)),
        "msg": "🎉 SORTED! All bubbles settled in their perfect positions!",
        "comparisons": comparisons,
        "swaps": swaps
    })
    return steps

def selection_sort_steps(arr):
    steps = []
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
            steps.append({
                "array": a.copy(),
                "comparing": [i, j],
                "swapped": [min_idx],
                "sorted": list(range(i)),
                "msg": f"🔍 Searching for minimum in unsorted part... current min: {a[min_idx]}",
                "comparisons": comparisons,
                "swaps": swaps
            })
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
        steps.append({
            "array": a.copy(),
            "comparing": [],
            "swapped": [i],
            "sorted": list(range(i+1)),
            "msg": f"⚡ Placed {a[i]} in its correct position!",
            "comparisons": comparisons,
            "swaps": swaps
        })
    steps.append({
        "array": a.copy(),
        "comparing": [],
        "swapped": [],
        "sorted": list(range(n)),
        "msg": "🎉 SORTED! Every element selected and placed perfectly!",
        "comparisons": comparisons,
        "swaps": swaps
    })
    return steps

def insertion_sort_steps(arr):
    steps = []
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(1, n):
        key = a[i]
        j = i - 1
        steps.append({
            "array": a.copy(),
            "comparing": [i],
            "swapped": [],
            "sorted": list(range(i)),
            "msg": f"🃏 Picking up card {key} to insert in correct position...",
            "comparisons": comparisons,
            "swaps": swaps
        })
        while j >= 0 and a[j] > key:
            comparisons += 1
            a[j+1] = a[j]
            swaps += 1
            steps.append({
                "array": a.copy(),
                "comparing": [j, j+1],
                "swapped": [j+1],
                "sorted": list(range(i)),
                "msg": f"↩️ {a[j]} > {key}, shifting {a[j]} right to make room...",
                "comparisons": comparisons,
                "swaps": swaps
            })
            j -= 1
        a[j+1] = key
        steps.append({
            "array": a.copy(),
            "comparing": [],
            "swapped": [j+1],
            "sorted": list(range(i+1)),
            "msg": f"✅ Inserted {key} into its correct slot!",
            "comparisons": comparisons,
            "swaps": swaps
        })
    steps.append({
        "array": a.copy(),
        "comparing": [],
        "swapped": [],
        "sorted": list(range(n)),
        "msg": "🎉 SORTED! Every card inserted in perfect order!",
        "comparisons": comparisons,
        "swaps": swaps
    })
    return steps

def binary_search_steps(arr, target):
    steps = []
    a = sorted(arr)
    low, high = 0, len(a) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if a[mid] == target:
            steps.append({
                "array": a,
                "comparing": [mid],
                "swapped": [mid],
                "sorted": list(range(len(a))),
                "msg": f"🎯 FOUND {target} at index {mid}! Target acquired!",
                "comparisons": comparisons,
                "swaps": 0,
                "low": low, "high": high, "mid": mid
            })
            return steps
        elif a[mid] < target:
            steps.append({
                "array": a,
                "comparing": [mid],
                "swapped": [],
                "sorted": list(range(low, mid+1)),
                "msg": f"➡️ {a[mid]} < {target} — target is in RIGHT half, eliminating left!",
                "comparisons": comparisons,
                "swaps": 0,
                "low": low, "high": high, "mid": mid
            })
            low = mid + 1
        else:
            steps.append({
                "array": a,
                "comparing": [mid],
                "swapped": [],
                "sorted": list(range(mid, high+1)),
                "msg": f"⬅️ {a[mid]} > {target} — target is in LEFT half, eliminating right!",
                "comparisons": comparisons,
                "swaps": 0,
                "low": low, "high": high, "mid": mid
            })
            high = mid - 1
    steps.append({
        "array": a,
        "comparing": [],
        "swapped": [],
        "sorted": [],
        "msg": f"❌ {target} NOT FOUND in array!",
        "comparisons": comparisons,
        "swaps": 0
    })
    return steps

ALGOS = {
    "🫧 Bubble Sort"    : "bubble",
    "🎯 Selection Sort" : "selection",
    "🃏 Insertion Sort" : "insertion",
    "🔍 Binary Search"  : "binary",
}

# ──────────────────────────────────────────
# LAYOUT
# ──────────────────────────────────────────
left, right = st.columns([1, 3])

with left:
    st.markdown('<div class="panel-title">SELECT ALGORITHM</div>', unsafe_allow_html=True)
    algo = st.radio("algo", list(ALGOS.keys()), label_visibility="collapsed")
    st.session_state.algo = algo

    st.markdown('<div class="panel-title" style="margin-top:24px;">API KEY</div>', unsafe_allow_html=True)
    api_key = st.text_input("Groq Key", type="password",
                             value=os.getenv("GROQ_API_KEY",""),
                             label_visibility="collapsed",
                             placeholder="gsk_...")

    st.markdown('<div class="panel-title" style="margin-top:24px;">COMPLEXITY</div>', unsafe_allow_html=True)
    complexity_info = {
        "🫧 Bubble Sort"    : "O(n²) time\nO(1) space",
        "🎯 Selection Sort" : "O(n²) time\nO(1) space",
        "🃏 Insertion Sort" : "O(n²) time\nO(1) space",
        "🔍 Binary Search"  : "O(log n) time\nO(1) space",
    }
    st.code(complexity_info.get(algo, ""), language=None)

with right:
    # Input row
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown("**ENTER NUMBERS** *(comma separated)*")
        nums_input = st.text_input("nums", value="64, 34, 25, 12, 22, 11, 90",
                                    label_visibility="collapsed")
    with c2:
        if ALGOS[algo] == "binary":
            st.markdown("**TARGET**")
            target = st.number_input("target", value=25, label_visibility="collapsed")
        else:
            target = None
            st.markdown(" ")
            st.markdown(" ")
    with c3:
        st.markdown(" ")
        start = st.button("▶ START", type="primary", use_container_width=True)

    if start:
        try:
            arr = [int(x.strip()) for x in nums_input.split(",") if x.strip()]
            if len(arr) < 2:
                st.error("Enter at least 2 numbers!")
            elif len(arr) > 20:
                st.error("Max 20 numbers for best visualization!")
            else:
                algo_key = ALGOS[algo]
                if algo_key == "bubble":
                    st.session_state.steps = bubble_sort_steps(arr)
                elif algo_key == "selection":
                    st.session_state.steps = selection_sort_steps(arr)
                elif algo_key == "insertion":
                    st.session_state.steps = insertion_sort_steps(arr)
                elif algo_key == "binary":
                    st.session_state.steps = binary_search_steps(arr, int(target))
                st.session_state.current_step = 0

                # AI explanation
                if api_key:
                    try:
                        client = groq.Groq(api_key=api_key)
                        resp = client.chat.completions.create(
                            messages=[{"role":"user","content":
                                f"Explain {algo} algorithm in 2-3 fun, engaging sentences like you're a game narrator. "
                                f"Use gaming metaphors. Input array: {arr}. Be exciting and use emojis!"}],
                            model="llama-3.3-70b-versatile",
                            max_tokens=150,
                        )
                        st.session_state.ai_explain = resp.choices[0].message.content
                    except:
                        st.session_state.ai_explain = f"🎮 Watch how {algo} conquers the array step by step!"
                else:
                    st.session_state.ai_explain = f"🎮 Watch how {algo} conquers the array step by step! Add Groq API key for AI commentary."
        except:
            st.error("Invalid input! Enter numbers separated by commas.")

    # ── VISUALIZATION ──────────────────────────
    if st.session_state.steps:
        step = st.session_state.steps[st.session_state.current_step]
        arr  = step["array"]
        mx   = max(arr) if arr else 1

        # Build bars HTML
        bars_html = '<div class="bars-container">'
        for i, val in enumerate(arr):
            h = max(20, int((val / mx) * 220))
            if i in step.get("swapped", []):
                color = "#ff4466"
                glow  = "box-shadow: 0 0 15px #ff4466, 0 0 30px #ff4466;"
            elif i in step.get("comparing", []):
                color = "#ffcc00"
                glow  = "box-shadow: 0 0 15px #ffcc00;"
            elif i in step.get("sorted", []):
                color = "#00ff88"
                glow  = "box-shadow: 0 0 10px #00ff88;"
            else:
                color = "#334"
                glow  = ""
            bars_html += f'''
            <div class="bar" style="height:{h}px; background:{color}; {glow}">
                <span class="bar-value">{val}</span>
                <span class="bar-label">[{i}]</span>
            </div>'''
        bars_html += '</div>'

        # Legend
        legend_html = '''
        <div class="legend">
            <div class="legend-item"><div class="legend-dot" style="background:#ffcc00"></div> Comparing</div>
            <div class="legend-item"><div class="legend-dot" style="background:#ff4466"></div> Swapping</div>
            <div class="legend-item"><div class="legend-dot" style="background:#00ff88"></div> Sorted</div>
            <div class="legend-item"><div class="legend-dot" style="background:#334"></div> Unsorted</div>
        </div>'''

        st.markdown(f'''
        <div class="viz-container">
            {bars_html}
            {legend_html}
        </div>
        ''', unsafe_allow_html=True)

        # Step info
        total = len(st.session_state.steps)
        curr  = st.session_state.current_step
        st.markdown(f'''
        <div class="step-info">
            <div class="step-counter">STEP {curr+1} OF {total}</div>
            <div class="step-text">{step["msg"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        # Stats
        st.markdown(f'''
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-value">{step.get("comparisons",0)}</div>
                <div class="stat-label">COMPARISONS</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{step.get("swaps",0)}</div>
                <div class="stat-label">SWAPS</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{curr+1}/{total}</div>
                <div class="stat-label">PROGRESS</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{int((curr+1)/total*100)}%</div>
                <div class="stat-label">COMPLETE</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # AI explanation
        if st.session_state.ai_explain:
            st.markdown(f'''
            <div class="ai-box">
                <div class="ai-label">🤖 AI GAME NARRATOR</div>
                <div class="ai-text">{st.session_state.ai_explain}</div>
            </div>
            ''', unsafe_allow_html=True)

        # Controls
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            if st.button("⏮ FIRST"):
                st.session_state.current_step = 0
                st.rerun()
        with b2:
            if st.button("◀ PREV") and curr > 0:
                st.session_state.current_step -= 1
                st.rerun()
        with b3:
            st.markdown(f"<div style='text-align:center;padding:8px;font-family:Orbitron;font-size:10px;color:#555'>{curr+1}/{total}</div>", unsafe_allow_html=True)
        with b4:
            if st.button("NEXT ▶") and curr < total-1:
                st.session_state.current_step += 1
                st.rerun()
        with b5:
            if st.button("LAST ⏭"):
                st.session_state.current_step = total - 1
                st.rerun()

        # Progress bar
        progress = (curr + 1) / total
        st.progress(progress)

    else:
        # Empty state
        st.markdown('''
        <div class="viz-container" style="display:flex;align-items:center;justify-content:center;flex-direction:column;gap:16px;">
            <div style="font-family:Press Start 2P,monospace;font-size:32px;color:#1a1a2e;">▶</div>
            <div style="font-family:Orbitron,sans-serif;font-size:12px;color:#333;letter-spacing:4px;">SELECT ALGORITHM → ENTER NUMBERS → PRESS START</div>
        </div>
        ''', unsafe_allow_html=True)
