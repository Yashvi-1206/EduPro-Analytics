import streamlit as st
import plotly.express as px
from components.style import load_css, page_title
from components.cards import kpi_card
from utils import preprocess_data
import pandas as pd

st.set_page_config(page_title="Revenue Analysis", layout="wide")

load_css()
page_title("Revenue Analysis", "💰")

df = preprocess_data()

# ==========================
# Revenue Analysis Filters
# ==========================

st.sidebar.header("🔎 Filters")

df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])

min_date = df["TransactionDate"].min().date()
max_date = df["TransactionDate"].max().date()

date_range = st.sidebar.date_input(
    "📅 Transaction Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

category_filter = st.sidebar.multiselect(
    "📚 Course Category",
    sorted(df["CourseCategory"].dropna().unique()),
    default=sorted(df["CourseCategory"].dropna().unique())
)

level_filter = st.sidebar.multiselect(
    "🎓 Course Level",
    sorted(df["CourseLevel"].dropna().unique()),
    default=sorted(df["CourseLevel"].dropna().unique())
)

payment_filter = st.sidebar.multiselect(
    "💳 Payment Method",
    sorted(df["PaymentMethod"].dropna().unique()),
    default=sorted(df["PaymentMethod"].dropna().unique())
)

if len(date_range) == 2:

    df = df[
        (df["TransactionDate"] >= pd.Timestamp(date_range[0])) &
        (df["TransactionDate"] <= pd.Timestamp(date_range[1])) &
        (df["CourseCategory"].isin(category_filter)) &
        (df["CourseLevel"].isin(level_filter)) &
        (df["PaymentMethod"].isin(payment_filter))
    ]
# ==========================
# KPI Cards
# ==========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Total Revenue",
        f"${df['Amount'].sum():,.0f}",
        "💰",
        "#2563EB"
    )

with c2:
    kpi_card(
        "Average Revenue",
        f"${df['Amount'].mean():,.0f}",
        "📈",
        "#16A34A"
    )

with c3:
    kpi_card(
        "Highest Transaction",
        f"${df['Amount'].max():,.0f}",
        "🏆",
        "#DC2626"
    )

with c4:
    kpi_card(
        "Enrollments",
        len(df),
        "🎓",
        "#7C3AED"
    )

st.divider()

# ==========================
# Monthly Revenue
# ==========================

monthly = (
    df.groupby("Month")["Amount"]
      .sum()
      .reset_index()
)

fig1 = px.line(
    monthly,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Revenue Trend"
)

# ==========================
# Payment Method
# ==========================

payment = (
    df.groupby("PaymentMethod")["Amount"]
      .sum()
      .reset_index()
)

fig2 = px.pie(
    payment,
    names="PaymentMethod",
    values="Amount",
    hole=0.5,
    title="Revenue by Payment Method"
)

# ==========================
# Category Revenue
# ==========================

category = (
    df.groupby("CourseCategory")["Amount"]
      .sum()
      .reset_index()
)

fig3 = px.bar(
    category,
    x="CourseCategory",
    y="Amount",
    color="Amount",
    title="Revenue by Category"
)
# ==========================
# Category Enrollments
# ==========================

category_enrollment = (
    df.groupby("CourseCategory")["TransactionID"]
    .count()
    .reset_index(name="Enrollments")
)

fig5 = px.bar(
    category_enrollment,
    x="CourseCategory",
    y="Enrollments",
    color="Enrollments",
    title="🎓 Enrollments by Category"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)
# ==========================
# Level Revenue
# ==========================

level = (
    df.groupby("CourseLevel")["Amount"]
      .sum()
      .reset_index()
)

fig4 = px.bar(
    level,
    x="CourseLevel",
    y="Amount",
    color="Amount",
    title="Revenue by Course Level"
)

# ==========================
# Layout
# ==========================

left, right = st.columns(2)

with left:
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.plotly_chart(fig2, use_container_width=True)

left, right = st.columns(2)

with left:
    st.plotly_chart(fig3, use_container_width=True)

with right:
    st.plotly_chart(fig4, use_container_width=True)

# ==========================
# Top Transactions
# ==========================

st.subheader("Top 20 Transactions")

top = df.sort_values(
    "Amount",
    ascending=False
).head(20)

st.dataframe(
    top,
    use_container_width=True
)
st.download_button(
    label="📥 Download Revenue Data",
    data=df.to_csv(index=False),
    file_name="Revenue_Data.csv",
    mime="text/csv"
)