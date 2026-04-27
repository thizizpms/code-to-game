# 🎮 Code to Game — Algorithm Visualizer

> **Watch sorting algorithms come alive as an interactive game!**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red?style=for-the-badge&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 🚀 What is this?

**Code to Game** is an AI-powered algorithm visualizer that turns dry sorting algorithms into an exciting, game-like experience. Instead of reading about how Bubble Sort works, you **watch it happen** — step by step, with colors, stats, and an AI narrator explaining every move.

---

## ✨ Features

- 🫧 **Bubble Sort** — watch bubbles float to the top
- 🎯 **Selection Sort** — watch it hunt for the minimum
- 🃏 **Insertion Sort** — watch cards get inserted one by one
- 🔍 **Binary Search** — watch it eliminate halves like a treasure hunt
- 🤖 **AI Game Narrator** — powered by LLaMA 3.3 70B via Groq API
- 📊 **Live Stats** — comparisons, swaps, progress tracked in real time
- ⚡ **Retro Neon UI** — looks and feels like an actual game
- 🎮 **Step-by-step controls** — go forward, backward, jump to end

---

## 🖥️ Demo

```
Enter numbers → Pick algorithm → Press START → Watch it sort!
```

| Color | Meaning |
|-------|---------|
| 🟡 Yellow | Elements being compared |
| 🔴 Red | Elements being swapped |
| 🟢 Green | Sorted and done! |
| ⬛ Dark | Not yet touched |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core logic & algorithm implementation |
| Streamlit | Web UI framework |
| Groq API | AI narrator (LLaMA 3.3 70B) |
| HTML/CSS | Custom retro game styling |

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/thizizpms/code-to-game.git
cd code-to-game

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 🔑 API Key Setup

1. Get a **free** Groq API key from 👉 [console.groq.com](https://console.groq.com)
2. Paste it in the **API KEY** field in the left sidebar of the app

> The app works without an API key too — AI narration is optional!

---

## 📁 Project Structure

```
code-to-game/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # You are here!
```

---

## 🧠 How it Works

1. You enter numbers and select an algorithm
2. Python runs the algorithm and **saves every single step**
3. Each step stores: current array state, which elements are comparing/swapping/sorted
4. The UI renders each step as colored bars
5. Groq AI generates a fun narrator comment for the algorithm
6. You click NEXT to walk through every step like a game!

---

## 🎯 Algorithms Explained

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|-----------------|
| Bubble Sort | O(n²) | O(1) |
| Selection Sort | O(n²) | O(1) |
| Insertion Sort | O(n²) | O(1) |
| Binary Search | O(log n) | O(1) |

---

## 🙌 Built By

**thizizpms** — Java Developer exploring AI/ML

> *"I built this to make algorithms fun and visual — the way they should have been taught in college!"*

---

⭐ **Star this repo if you found it useful!**