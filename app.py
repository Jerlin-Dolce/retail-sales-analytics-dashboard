from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Retail Sales Analytics", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    [data-testid="stMetric"] {background: white; padding: 16px; border-radius: 12px; border: 1px solid #e8edf5;}
    h1 {color: #172554;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Retail Sales Analytics Dashboard")
st.caption("An interactive data analytics portfolio project | Sales, profit, products and customer insights")

@st.cache_data
def load_data():
    path = Path(__file__).parent / "sales_data.csv"
    return pd.read_csv(path, parse_dates=["Order_Date"])

df = load_data()

with st.sidebar:
    st.header("🔎 Dashboard filters")
    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    customer_types = st.multiselect("Customer type", sorted(df["Customer_Type"].unique()), default=sorted(df["Customer_Type"].unique()))

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[(filtered["Order_Date"].dt.date >= date_range[0]) & (filtered["Order_Date"].dt.date <= date_range[1])]
filtered = filtered[filtered["Region"].isin(regions) & filtered["Category"].isin(categories) & filtered["Customer_Type"].isin(customer_types)]

if filtered.empty:
    st.warning("No data matches these filters. Try selecting a wider date range or more filter options.")
    st.stop()

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()
avg_order = total_sales / orders if orders else 0
margin = (total_profit / total_sales * 100) if total_sales else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Sales", f"${total_sales:,.0f}")
m2.metric("Total Profit", f"${total_profit:,.0f}")
m3.metric("Orders", f"{orders:,}")
m4.metric("Profit Margin", f"{margin:.1f}%")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("📈 Monthly sales trend")
    monthly = filtered.set_index("Order_Date").resample("MS").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    fig = px.line(monthly, x="Order_Date", y=["Sales", "Profit"], markers=True,
                  labels={"Order_Date":"Month", "value":"Amount ($)", "variable":"Metric"},
                  color_discrete_sequence=["#2563eb", "#16a34a"])
    fig.update_layout(legend_title_text="", hovermode="x unified", margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("🧩 Sales by category")
    category_sales = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.pie(category_sales, names="Category", values="Sales", hole=.48,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(margin=dict(l=10,r=10,t=20,b=10), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("🌍 Regional performance")
    region_data = filtered.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
    fig = px.bar(region_data, x="Region", y="Sales", color="Profit", color_continuous_scale="Blues",
                 labels={"Sales":"Sales ($)", "Profit":"Profit ($)"}, text_auto=".2s")
    fig.update_layout(margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("🏆 Top 10 products by sales")
    top_products = filtered.groupby("Product", as_index=False)["Sales"].sum().nlargest(10, "Sales").sort_values("Sales")
    fig = px.bar(top_products, x="Sales", y="Product", orientation="h", text_auto=".2s",
                 labels={"Sales":"Sales ($)", "Product":""}, color="Sales", color_continuous_scale="Teal")
    fig.update_layout(showlegend=False, coloraxis_showscale=False, margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("💡 Quick insights")
best_region = region_data.sort_values("Sales", ascending=False).iloc[0]
best_category = category_sales.iloc[0]
best_product = filtered.groupby("Product")["Sales"].sum().idxmax()
c1, c2, c3 = st.columns(3)
c1.info(f"**Leading region:** {best_region['Region']} generated ${best_region['Sales']:,.0f} in sales.")
c2.info(f"**Top category:** {best_category['Category']} contributed ${best_category['Sales']:,.0f} in sales.")
c3.info(f"**Best-selling product:** {best_product}.")

st.divider()
st.subheader("📋 Order details")
search = st.text_input("Search by order ID or product")
table = filtered.copy()
if search:
    mask = table["Order_ID"].str.contains(search, case=False, na=False) | table["Product"].str.contains(search, case=False, na=False)
    table = table[mask]
st.dataframe(table.sort_values("Order_Date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("⬇️ Download filtered data as CSV", data=table.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_sales_data.csv", mime="text/csv")

st.caption("Dataset: synthetic sample retail transactions created for this portfolio project. Values are illustrative, not real company data.")
