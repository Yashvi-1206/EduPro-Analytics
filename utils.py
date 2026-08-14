
import streamlit as st
import pandas as pd


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    file = "EduPro Online Platform.xlsx"

    users = pd.read_excel(
        file,
        sheet_name="Users"
    )

    teachers = pd.read_excel(
        file,
        sheet_name="Teachers"
    )

    courses = pd.read_excel(
        file,
        sheet_name="Courses"
    )

    transactions = pd.read_excel(
        file,
        sheet_name="Transactions"
    )

    return users, teachers, courses, transactions


# =====================================================
# PREPROCESS DATA
# =====================================================

def preprocess_data():

    users, teachers, courses, transactions = load_data()

    # Transactions + Courses
    df = transactions.merge(
        courses,
        on="CourseID",
        how="left"
    )

    # Add Teacher information
    df = df.merge(
        teachers,
        on="TeacherID",
        how="left"
    )

    # Add User information
    df = df.merge(
        users,
        on="UserID",
        how="left"
    )

    # Date conversion
    df["TransactionDate"] = pd.to_datetime(
        df["TransactionDate"],
        errors="coerce"
    )

    # Date features
    df["Year"] = df["TransactionDate"].dt.year
    df["Month"] = df["TransactionDate"].dt.month_name()
    df["MonthNumber"] = df["TransactionDate"].dt.month
    df["Day"] = df["TransactionDate"].dt.day
    df["DayName"] = df["TransactionDate"].dt.day_name()

    return df


# =====================================================
# SIDEBAR FILTERS
# =====================================================

def apply_filters(df):

    st.sidebar.header("🔍 Filters")

    category = st.sidebar.multiselect(
        "📚 Course Category",
        sorted(df["CourseCategory"].dropna().unique()),
        default=sorted(df["CourseCategory"].dropna().unique())
    )

    level = st.sidebar.multiselect(
        "🎓 Course Level",
        sorted(df["CourseLevel"].dropna().unique()),
        default=sorted(df["CourseLevel"].dropna().unique())
    )

    payment = st.sidebar.multiselect(
        "💳 Payment Method",
        sorted(df["PaymentMethod"].dropna().unique()),
        default=sorted(df["PaymentMethod"].dropna().unique())
    )

    teacher = st.sidebar.multiselect(
        "👨‍🏫 Teacher",
        sorted(df["TeacherName"].dropna().unique()),
        default=sorted(df["TeacherName"].dropna().unique())
    )

    filtered_df = df[
        df["CourseCategory"].isin(category) &
        df["CourseLevel"].isin(level) &
        df["PaymentMethod"].isin(payment) &
        df["TeacherName"].isin(teacher)
    ]

    return filtered_df