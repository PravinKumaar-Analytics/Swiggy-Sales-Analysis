# IMPORT LIBRARIES #

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# IMPORT DATA #

df =pd.read_excel("C:/Users/pravi/Downloads/swiggy_data.xlsx")
print(df.head())
print(df.tail())

# METADATA #

print("No of Rows:",df.shape[0])
print("No of Columns:",df.shape[1])
df.info()

# DATATYPES #

df.dtypes
print(df.describe())

# KPI's #

total_sales=df["Price (INR)"].sum()
print("Total Sales (INR):",round(total_sales,2)) # round is used to reduce decimal

average_rating=df["Rating"].mean()
print("Average Rating:",round(average_rating,1))

average_order_value=df["Price (INR)"].mean()
print("Average Order Value (INR):",round(average_order_value,2))

rating_count=df["Rating Count"].sum()
print("Rating Count:",round(rating_count,2))

total_orders=len(df)
print("Total Orders:",round(total_orders,2))

# CHARTS #

# MONTHLY SALES #

df["Order Date"]=pd.to_datetime(df["Order Date"])

df["YearMonth"] =df["Order Date"].dt.to_period("M").astype(str)

monthly_revenue=df.groupby("YearMonth") ["Price (INR)"].sum().reset_index()

plt.figure()

plt.plot(monthly_revenue["YearMonth"], monthly_revenue["Price (INR)"])

plt.xticks(rotation=45)

plt.xlabel("Month")

plt.ylabel("Revenue (INR)")

plt.title("Monthly Revenue Trend")

plt.tight_layout()

plt.show()

# DAILY SALES TREND #

df["DayName"] = pd.to_datetime(df["Order Date"]).dt.day_name()

daily_revenue = (
            df.groupby("DayName") ["Price (INR)"]
            .sum()
            .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
)
plt.figure(figsize=(10,5))

plt.bar(daily_revenue.index, daily_revenue.values)

plt.title("Daily Revenue Trend (Man-Sun)")

plt.xlabel("Day")

plt.ylabel("Revenue (INR)")

plt.xticks(rotation=30)

plt.show()

# TOTAL SALES BY FOOD TYPE #

non_veg_keywords = [

       "chicken", "egg", "fish", "mutton",

       "prawn", "biryani", "kabab", "kebab",

       "non-veg", "non veg"
]
df["Food Category"]= np.where(

df["Dish Name"] .str.lower().str.contains("|".join(non_veg_keywords), na=False),

"Non-Veg",

"Veg"
)

food_revenue=(
    df.groupby("Food Category")["Price (INR)"]
    .sum()
    .reset_index()
)

fig = px.pie(

   food_revenue,

   values="Price (INR)",

   names ="Food Category",

   hole= 0.5,

   title="Revenue Contribution: Veg vs Non-Veg",

)

fig.update_traces(

textinfo="percent+label",

pull=[0.05, 0]

)

fig.update_layout(

height=500,

margin=dict(t=60, b=40, l=40, r=40)
)

fig.show()

# TOTAL SALES BY STATE #

fig = px.bar(

df.groupby("State", as_index=False) ["Price (INR)"].sum()

.sort_values("Price (INR)", ascending=False),

x="Price (INR)",

y="State",

orientation="h",

title="Revenue by State (INR)"
)
fig.update_layout (height=600, yaxis=dict(autorange="reversed"))

fig.show()

# QUARTERLY PERFORMANCE SUMMARY #

df ["Order_Date"] = pd.to_datetime(df["Order Date"])

df [ "Quarter"]= df ["Order_Date"].dt.to_period("Q").astype(str)

quarterly_summary = (

       df.groupby("Quarter", as_index=False)

       .agg(

            Total_Sales=("Price (INR)", "sum"),

            Avg_Rating=("Rating", "mean"),

            Total_Orders=("Order_Date", "count")
       )
       .sort_values("Quarter")

)
quarterly_summary["Total Sales"]= quarterly_summary["Total_Sales"].round(0)
quarterly_summary = (
    df.groupby("Quarter")
    .agg(
        Revenue=("Price (INR)", "sum"),
        Avg_Rating=("Rating", "mean")
    )
    .reset_index()
)

quarterly_summary["Avg_Rating"] = quarterly_summary["Avg_Rating"].round(2)


print(quarterly_summary)


# TOP 5 CITIES BY SALES #

top_5_cities = (

df.groupby("City") ["Price (INR)"]

      .sum()
      .nlargest(5)
      .sort_values()
      .reset_index()

)

fig = px.bar(

top_5_cities,

x="Price (INR)",

y="City",

orientation="h",

title="Top 5 Cities by Sales (INR)",

color_discrete_sequence=["red"]
)
fig.show()
