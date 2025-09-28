# 📊 BullBearAnalysis

An app that is able to display technical indicators to identify stock trends and calculate portfolio networth using Streamlit.
---


## 📈 Project Overview

This system performs sophisticated technical analysis on historical stock data, implementing algorithms for trend identification, profitability analysis, and interactive visualization. Built with modular, production-ready code following software engineering best practices.

## 🚀 Features

* 📈 Detects and visualizes upward/downward streaks in stock prices
* 🕒 Displays longest streaks with start and end dates
* 📐 Display up to five technical indicators
* 🔎 Filter historical stock data by date ranges.
* 💹 Display buy/sell signals on the chart
* ⚡ Powered by Streamlit for an interactive dashboard to display visualization
* 💾 Data sourced from Yahoo Finance (Yfinance)

---

## 🏗️ Tech Stack

* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **Backend/Data libraries:** Pandas, NumPy, yfinance
* **Version Control:** Git/GitHub

---

## 📂 Project Structure

```
.
├── data/ → Stores datasets and user portfolio data
│ ├── CSV/ → Cached/stored stock data in CSV format
│ └── user_data/ → User-specific data (e.g., portfolio_Test.json)
│
├── pages/ → Streamlit multi-page app scripts
│ └── portfolio_tracker.py
│
├── src/ → Core source code
│ ├── analytics.py → Financial analytics functions
│ ├── config.py → Configuration settings
│ ├── data_loader.py → Data fetching and preprocessing
│ ├── helper.py → Utility/helper functions
│ ├── run_loader.py → Script for bulk loading data
│ ├── technical_indicators.py → Technical analysis functions
│ └── visualization.py → Plotting and charting functions
│
├── tests/ → Unit tests
│ ├── test_analytics.py
│ └── test_data_loader.py
│
├── validation/ → Validation scripts to compare calculations
│ └── validation.py
│
├── app.py → Main Streamlit entry point
├── requirements.txt → Python dependencies
├── README.md → Project documentation
└── .gitignore → Git ignore rules
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/project-name.git
cd project-name
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🧪 Validation & Testing

🛠 WIP ( Work in Progress )

To validate the results:

* The program outputs streak detection results directly in the console.
* Professors can re-run the analysis with sample data provided in `/data`.
* Unit tests (if included) can be run with:

```bash
pytest
```

---

## 📊 Example Output

**Longest Downward Streak and Upward Streak for GME:**

<img width="1913" height="961" alt="image" src="https://github.com/user-attachments/assets/db483fd9-59bd-40ac-89dc-9e40c949b31b" />

---

## 👨‍💻 Authors

* **Your Name** – Developer & Researcher
* **(Optional)** 

---

## 📚 References

* [Streamlit Documentation](https://docs.streamlit.io/)
* [yfinance Library](https://pypi.org/project/yfinance/)

---

## 📜 License

This project is for **academic purposes only**.
