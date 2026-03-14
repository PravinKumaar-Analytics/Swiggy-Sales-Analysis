# 🛵   Swiggy Sales Analysis 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end sales analytics project on Swiggy food order data, featuring an interactive **Streamlit dashboard** and a full **Exploratory Data Analysis (EDA)** script. The project uncovers revenue trends, cuisine breakdowns, city/state performance, and quarterly summaries from real order data.

---

## 📸 Dashboard Preview

### KPIs & Sales Trends
![Dashboard KPI & Charts](https://github.com/PravinKumaar-Analytics/Swiggy-Sales-Analysis/blob/96fe028477a40ca07d9c4b03ffbf1687e527c0cf/3-Streamlit-Dashboard-Screenshots/2-Dashboard_KPI_Charts_1.jpeg)

### Cuisine & City Breakdown + State-wise Revenue
![Dashboard Charts 2](https://github.com/PravinKumaar-Analytics/Swiggy-Sales-Analysis/blob/96fe028477a40ca07d9c4b03ffbf1687e527c0cf/3-Streamlit-Dashboard-Screenshots/3-Dashboard_Charts_2.jpeg)

### Quarterly Performance Summary
![Dashboard Charts 3](https://github.com/PravinKumaar-Analytics/Swiggy-Sales-Analysis/blob/96fe028477a40ca07d9c4b03ffbf1687e527c0cf/3-Streamlit-Dashboard-Screenshots/3-Dashboard_Charts_2.jpeg)

---

## 📊 Key Metrics (from Dataset)

| KPI | Value |
|-----|-------|
| 💰 Total Revenue | ₹53.01 Million |
| ⭐ Average Rating | 4.3 / 5 |
| 🛒 Average Order Value | ₹269 |
| 🗳️ Total Rating Count | 55,91,574 |
| 📦 Total Orders | 1,97,430 |

---

## 📁 Project Structure

```
swiggy-sales-analysis/
│
├── swiggy_data.xlsx              # Source dataset (orders, ratings, cities, states)
├── Swiggy-EDA-Analysis.py        # Standalone EDA script (Matplotlib + Plotly)
├── Streamlit_Dashboard.py        # Interactive Streamlit dashboard app
│
├── Dashboard_KPI_Charts_1.jpeg   # Screenshot: KPIs & Sales Trends
├── Dashboard_Charts_2.jpeg       # Screenshot: Cuisine & State Revenue
├── Dashboard_Charts_3.jpeg       # Screenshot: Quarterly Performance
│
└── README.md
```

---

## 📋 Dataset Columns

| Column | Description |
|--------|-------------|
| `Order Date` | Date the order was placed |
| `Dish Name` | Name of the food item ordered |
| `Price (INR)` | Order value in Indian Rupees |
| `Rating` | Customer rating (out of 5) |
| `Rating Count` | Number of votes/ratings |
| `City` | City where the order was placed |
| `State` | State of the order |

---

## 🔍 Analysis Performed

### 📈 Sales Trends
- **Monthly Revenue Trend** — Line chart tracking revenue across months
- **Daily Revenue Pattern** — Bar chart comparing Mon–Sun revenue, highlighting weekday vs. weekend patterns

### 🍽️ Cuisine & Food Breakdown
- **Veg vs. Non-Veg Revenue** — Donut chart classifying dishes using keyword matching
  - Non-Veg keywords: `chicken`, `egg`, `fish`, `mutton`, `prawn`, `biryani`, `kabab`, etc.
- **Cuisine Categories Highlighted:** Biryani, South Indian, North Indian, Desserts, Pizza, Salads

### 🏙️ City & State Performance
- **Top 5 Cities by Revenue:**

  | Rank | City | Revenue |
  |------|------|---------|
  | 1 | Bengaluru | ₹54,56,798 |
  | 2 | Lucknow | ₹31,17,360 |
  | 3 | Hyderabad | ₹30,21,712 |
  | 4 | Mumbai | ₹30,15,573 |
  | 5 | New Delhi | ₹28,29,181 |

- **State-wise Revenue** — Horizontal bar chart across all Indian states; Karnataka leads, followed by Uttar Pradesh and Telangana

### 📅 Quarterly Performance Summary

| Quarter | Revenue | Avg Rating | Orders |
|---------|---------|------------|--------|
| 2025 Q1 | ₹1,96,67,822 | 4.34 ⭐ | 73,096 |
| 2025 Q2 | ₹1,99,02,257 | 4.34 ⭐ | 74,163 |
| 2025 Q3 | ₹1,34,42,427 | 4.34 ⭐ | 50,171 |

---

## 🖥️ Streamlit Dashboard Features

- 📂 **File Upload** — Drag & drop your own `swiggy_data.xlsx` to analyze
- 🔎 **Dynamic Filters** — Filter data interactively by State and City
- 📊 **Interactive Charts** — All visualizations built with Plotly (hover, zoom, pan)
- 🎨 **Swiggy-themed UI** — Dark navy background with orange accent colors matching Swiggy's branding

---

## 🛠️ Technologies Used

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading, cleaning, grouping |
| `numpy` | Numerical operations & keyword-based classification |
| `matplotlib` | Static charts (EDA script) |
| `seaborn` | Statistical visualizations |
| `plotly` | Interactive charts in dashboard |
| `streamlit` | Web-based interactive dashboard |
| `openpyxl` | Reading `.xlsx` Excel files |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/swiggy-sales-analysis.git
cd swiggy-sales-analysis

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn plotly streamlit openpyxl

# 3. Run the standalone EDA script
python Swiggy-EDA-Analysis.py

# 4. Launch the interactive Streamlit Dashboard
streamlit run Streamlit_Dashboard.py
```

Once launched, open your browser at `http://localhost:8501` and upload `swiggy_data.xlsx` to explore the full dashboard.

---

## 💡 Key Insights

- 🏆 **Karnataka (Bengaluru)** is the top revenue-generating state and city by a significant margin
- 📅 **Q2 2025** was the best-performing quarter with ₹1.99 Cr in revenue and 74,163 orders
- 🌿 **Veg items** account for the majority (~69%) of revenue; Non-Veg contributes ~31%
- 📉 Revenue in **Q3 2025** dipped compared to Q1 and Q2, suggesting seasonality or partial data
- ⭐ Average customer rating remains consistently at **4.34** across all quarters — indicating strong satisfaction

---
