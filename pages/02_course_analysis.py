import streamlit as st
import plotly.express as px
from utils import preprocess_data, apply_filters
import pandas as pd


st.set_page_config(page_title="Course Analysis", layout="wide")

df = preprocess_data()

# ==========================
# Course Analysis Filters
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

course_filter = st.sidebar.multiselect(
    "📖 Course",
    sorted(df["CourseName"].dropna().unique()),
    default=sorted(df["CourseName"].dropna().unique())
)

if len(date_range) == 2:

    df = df[
        (df["TransactionDate"] >= pd.Timestamp(date_range[0])) &
        (df["TransactionDate"] <= pd.Timestamp(date_range[1])) &
        (df["CourseCategory"].isin(category_filter)) &
        (df["CourseLevel"].isin(level_filter)) &
        (df["CourseName"].isin(course_filter))
    ]

st.title("📚 Course Analysis")

# -------------------------
# Course Category
# -------------------------

category = (
    df.groupby("CourseCategory")
    .agg(
        Revenue=("Amount", "sum"),
        Enrollments=("TransactionID", "count"),
        Courses=("CourseID", "nunique")
    )
    .reset_index()
)

fig = px.bar(
    category,
    x="CourseCategory",
    y="Revenue",
    color="Revenue",
    title="Revenue by Course Category"
)

st.plotly_chart(fig, use_container_width=True)

fig_enrollment = px.bar(
    category,
    x="CourseCategory",
    y="Enrollments",
    color="Enrollments",
    title="🎓 Enrollments by Course Category"
)

st.plotly_chart(
    fig_enrollment,
    use_container_width=True
)

# -------------------------
# Course Level
# -------------------------

level = (
    df.groupby("CourseLevel")["Amount"]
      .sum()
      .reset_index()
)

fig2 = px.pie(
    level,
    names="CourseLevel",
    values="Amount",
    title="Revenue by Course Level"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Course Price Distribution
# -------------------------

fig3 = px.histogram(
    df,
    x="CoursePrice",
    nbins=20,
    title="Course Price Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# Course Duration
# -------------------------

fig4 = px.box(
    df,
    x="CourseLevel",
    y="CourseDuration",
    color="CourseLevel",
    title="Course Duration by Level"
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# Course Rating
# -------------------------

fig5 = px.scatter(
    df,
    x="CoursePrice",
    y="CourseRating",
    color="CourseCategory",
    title="Course Price vs Rating"
)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------
# Top Courses
# -------------------------

top = (
    df.groupby("CourseName")["Amount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig6 = px.bar(
    top,
    x="CourseName",
    y="Amount",
    color="Amount",
    title="Top 10 Revenue Courses"
)

st.plotly_chart(fig6, use_container_width=True)

top_enrollment = (
    df.groupby("CourseName")["TransactionID"]
    .count()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Enrollments")
)

fig7 = px.bar(
    top_enrollment,
    x="CourseName",
    y="Enrollments",
    color="Enrollments",
    title="🎓 Top 10 Courses by Enrollments"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.subheader("Course Dataset")

st.dataframe(df[
    [
        "CourseName",
        "CourseCategory",
        "CourseLevel",
        "CoursePrice",
        "CourseDuration",
        "CourseRating"
    ]
].drop_duplicates(), use_container_width=True)