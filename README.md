# 🚀 Python + SQL + AI Portfolio

This repository features a collection of full-stack Python projects backed by **SQLite databases** and an advanced **Deep Learning** project for medical diagnosis.
Each project includes the **Source Code** (for Developer review) and detailed **Test Cases** or **Analysis** (for QA/Data Science review).

## 📂 Project 1: Smart Parking System
**Core Concept:** Object-Oriented Programming (Inheritance & Polymorphism)
- **Developer Skill:** Implemented a `VIP_Parking` class that overrides parent methods to apply a 50% surcharge.
- **Tester Skill:** Verified "Boundary Value Analysis" by testing the system at full capacity (10/10 slots).
- **Tech Stack:** Python, SQLite, Datetime.

## 📂 Project 2: Employee Leave Management Portal
**Core Concept:** CRUD Operations & Business Logic
- **Developer Skill:** Built a "Month-End Rollover" script using SQL `MIN()` functions to enforce a strict 30-day leave cap.
- **Tester Skill:** Validated database integrity by ensuring negative leave values are rejected.
- **Tech Stack:** Python, SQLite, Exception Handling.

## 📂 Project 3: E-Commerce BOGO Engine
**Core Concept:** Algorithms & Data Structures
- **Developer Skill:** Designed a sorting algorithm to implement a "Buy-One-Get-One-Free" logic that always discounts the cheapest item.
- **Tester Skill:** Performed functional testing on mixed carts (Standard + Promo items) to ensure billing accuracy.
- **Tech Stack:** Python, SQLite, List Manipulation.

## 📂 Project 4: Cervical Cancer Detection System (AI)
**Core Concept:** Computer Vision & Deep Learning
- **Developer Skill:** Trained and benchmarked three architectures (ViT, Custom CNN, EfficientNetB0), achieving **98.68% accuracy** with the Vision Transformer.
- **Tester/Analyst Skill:** Implemented GradCAM for Explainable AI (XAI) to visualize heatmap focus areas on cell images.
- **Tech Stack:** Python, PyTorch, TensorFlow, OpenCV, NumPy.

---

### 🛠️ Combined Tech Stack
- **Languages:** Python 3.x
- **Databases:** SQLite3
- **AI/ML Frameworks:** PyTorch, TensorFlow, Keras, Transformers (HuggingFace)
- **Core Concepts:** OOP, Algorithms, CRUD Operations, CNNs, Vision Transformers (ViT)

---

### 🛠️ How to Run
1. Clone the repo: `git clone [https://github.com/SpandanGowdaBC/Python-SQL-Portfolio]`

**For Projects 1-3 (Python + SQL):**
2. Run any file directly: `python main.py` (or the specific script name)
3. View the Test Cases: Open `QA_Test_Cases.xlsx`

**For Project 4 (AI/Computer Vision):**
2. Navigate to the folder: `cd My_Portfolio/03_Cervical_Cancer_AI`
3. Install dependencies: `pip install -r requirements.txt` (if available)
4. Run the notebook: Open `analysis_notebook.ipynb` in Jupyter Notebook or Google Colab.

---

### 👨‍💻 Author
**[Spandan Gowda B C]** *Aspiring Python Developer, QA Tester & AI Enthusiast*