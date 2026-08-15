import streamlit as st
import plotly.express as px
from components.style import load_css, page_title
from components.cards import kpi_card
import pandas as pd
from utils import preprocess_data

st.set_page_config(page_title="User Analysis", layout="wide")

load_css()
page_title("User Analysis", "👤")

df = preprocess_data()

# ==========================
# User Analysis Filters
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

user_filter = st.sidebar.multiselect(
    "👤 User",
    sorted(df["UserName"].dropna().unique()),
    default=sorted(df["UserName"].dropna().unique())
)

gender_filter = st.sidebar.multiselect(
    "⚥ Gender",
    sorted(df["Gender_x"].dropna().unique()),
    default=sorted(df["Gender_x"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "📚 Course Category",
    sorted(df["CourseCategory"].dropna().unique()),
    default=sorted(df["CourseCategory"].dropna().unique())
)

if len(date_range) == 2:

    df = df[
        (df["TransactionDate"] >= pd.Timestamp(date_range[0])) &
        (df["TransactionDate"] <=
 pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))&
        (df["UserName"].isin(user_filter)) &
        (df["Gender_x"].isin(gender_filter)) &
        (df["CourseCategory"].isin(category_filter))
    ]
# ===========================
# KPI Cards
# ===========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Total Users",
        df["UserID"].nunique(),
        "👥",
        "#2563EB"
    )

with c2:
    kpi_card(
        "Average Age",
        round(df["Age_x"].mean(),1),
        "🎂",
        "#16A34A"
    )

with c3:
    kpi_card(
        "Average Spending",
        f"${df.groupby('UserID')['Amount'].sum().mean():,.0f}",
        "💰",
        "#DC2626"
    )

with c4:
    kpi_card(
        "Highest Spending",
        f"${df.groupby('UserID')['Amount'].sum().max():,.0f}",
        "🏆",
        "#7C3AED"
    )

st.divider()

# ===========================
# Gender Distribution
# ===========================

gender = (
    df.groupby("Gender_x")
      .size()
      .reset_index(name="Users")
)

fig1 = px.pie(
    gender,
    names="Gender_x",
    values="Users",
    hole=.5,
    title="Gender Distribution"
)

# ===========================
# Age Distribution
# ===========================

fig2 = px.histogram(
    df,
    x="Age_x",
    nbins=20,
    title="Age Distribution"
)

# ===========================
# Top Spending Users
# ===========================

top_users = (
    df.groupby("UserName")["Amount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig3 = px.bar(
    top_users,
    x="UserName",
    y="Amount",
    color="Amount",
    title="Top 10 Users by Spending"
)

# ===========================
# Spending by Gender
# ===========================

gender_rev = (
    df.groupby("Gender_x")["Amount"]
      .sum()
      .reset_index()
)

fig4 = px.bar(
    gender_rev,
    x="Gender_x",
    y="Amount",
    color="Amount",
    title="Revenue by Gender"
)

# ===========================
# Layout
# ===========================

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

# ===========================
# User Table
# ===========================

st.subheader("User Information")

st.dataframe(
    df[
        [
            "UserName",
            "Age_x",
            "Gender_x",
            "Email"
        ]
    ].drop_duplicates(),
    use_container_width=True
)
st.download_button(
    label="📥 Download User Data (CSV)",
    data=df[
        [
            "UserName",
            "Age_x",
            "Gender_x",
            "Email"
        ]
    ].drop_duplicates().to_csv(index=False),
    file_name="User_Data.csv",
    mime="text/csv"
)