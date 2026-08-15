import streamlit as st
import plotly.express as px
from components.style import load_css,page_title
from components.cards import kpi_card
from utils import preprocess_data
import pandas as pd

st.set_page_config(
    page_title="EduPro Dashboard",
    layout="wide"
)
load_css()

page_title(
    "EduPro Analytics Dashboard",
    "🎓"
)

df = preprocess_data()
# ==========================
# Dashboard Filters
# ==========================

st.sidebar.header("🔎 Filters")
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

# Date filter
df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])

min_date = df["TransactionDate"].min().date()
max_date = df["TransactionDate"].max().date()

date_range = st.sidebar.date_input(
    "📅 Transaction Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Course Category
category_filter = st.sidebar.multiselect(
    "📚 Course Category",
    options=sorted(df["CourseCategory"].dropna().unique()),
    default=sorted(df["CourseCategory"].dropna().unique())
)

# Course Level
level_filter = st.sidebar.multiselect(
    "🎓 Course Level",
    options=sorted(df["CourseLevel"].dropna().unique()),
    default=sorted(df["CourseLevel"].dropna().unique())
)

# Payment Method
payment_filter = st.sidebar.multiselect(
    "💳 Payment Method",
    options=sorted(df["PaymentMethod"].dropna().unique()),
    default=sorted(df["PaymentMethod"].dropna().unique())
)

# Teacher
teacher_filter = st.sidebar.multiselect(
    "👨‍🏫 Teacher",
    options=sorted(df["TeacherName"].dropna().unique()),
    default=sorted(df["TeacherName"].dropna().unique())
)

# ==========================
# Apply Filters
# ==========================

if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    df = df[
        (df["TransactionDate"] >= start_date) &
        (df["TransactionDate"] <= end_date) &
        (df["CourseCategory"].isin(category_filter)) &
        (df["CourseLevel"].isin(level_filter)) &
        (df["PaymentMethod"].isin(payment_filter)) &
        (df["TeacherName"].isin(teacher_filter))
    ]


col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    kpi_card(
        "Revenue",
        f"${df['Amount'].sum():,.0f}",
        "💰",
        "#2563EB"
    )

with col2:
    kpi_card(
        "Enrollments",
        len(df),
        "📈",
        "#059669"
    )

with col3:
    kpi_card(
        "Courses",
        df["CourseID"].nunique(),
        "📚",
        "#DC2626"
    )

with col4:
    kpi_card(
        "Teachers",
        df["TeacherID"].nunique(),
        "👨‍🏫",
        "#7C3AED"
    )
with col5:
    kpi_card(
        "Enrollments",
        len(df),
        "🎓",
        "#F59E0B"
    )    

# -----------------------
# Revenue Trend
# -----------------------

daily_revenue = (
    df.groupby("TransactionDate")["Amount"]
    .sum()
    .reset_index()
    .sort_values("TransactionDate")
)

fig = px.line(
    daily_revenue,
    x="TransactionDate",
    y="Amount",
    markers=True,
    title="📈 Revenue Trend Over Time"
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

fig.update_layout(
    xaxis_title="Transaction Date",
    yaxis_title="Revenue",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=450
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
# -----------------------
# Revenue by Course Category
# -----------------------
# -----------------------
# Monthly Revenue & Transactions
# -----------------------

monthly_summary = (
    df.assign(
        Month=df["TransactionDate"].dt.to_period("M").astype(str)
    )
    .groupby("Month")
    .agg(
        Revenue=("Amount", "sum"),
        Transactions=("Amount", "count")
    )
    .reset_index()
)

fig_monthly = px.bar(
    monthly_summary,
    x="Month",
    y="Revenue",
    title="📊 Monthly Revenue",
    text_auto=".2s"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=400
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

category = (
    df.groupby("CourseCategory")["Amount"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    category,
    values="Amount",
    names="CourseCategory",
    title="Revenue by Course Category"
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)



# -----------------------
# Top 10 Courses
# -----------------------

top = (
    df.groupby("CourseName")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top,
    x="CourseName",
    y="Amount",
    color="Amount",
    title="Top 10 Revenue Courses"
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)


# -----------------------
# Course Level
# -----------------------

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
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
# =====================================================
# First Row
# =====================================================

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# Second Row
# =====================================================

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# -----------------------
# Rating Distribution
# -----------------------

fig5 = px.histogram(
    df,
    x="CourseRating",
    nbins=10,
    title="Course Rating Distribution"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
# -----------------------
# Transactions Table
# -----------------------

st.subheader("Latest Transactions")

st.dataframe(
    df.tail(20),
    use_container_width=True
)