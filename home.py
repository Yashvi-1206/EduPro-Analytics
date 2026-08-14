import streamlit as st
from components.style import load_css, page_title
from components.cards import kpi_card

st.set_page_config(
    page_title="EduPro Analytics",
    page_icon="🎓",
    layout="wide"
)

load_css()

page_title(
    "EduPro Analytics",
    "🎓"
)

st.subheader("🎓 Predictive Intelligence for Online Learning")

st.write(
    "EduPro Analytics transforms historical course, teacher, user, "
    "and transaction data into actionable business insights and "
    "predictive intelligence."
)
st.divider()

# =====================================================
# PROJECT OBJECTIVES
# =====================================================

st.subheader("🎯 Project Objectives")

col1, col2, col3 = st.columns(3)

with col1:
    kpi_card(
        "Course Demand",
        "Predict Enrollments",
        "🎓",
        "#2563EB"
    )

with col2:
    kpi_card(
        "Revenue Forecast",
        "Predict Course Revenue",
        "💰",
        "#16A34A"
    )

with col3:
    kpi_card(
        "Business Intelligence",
        "Data-Driven Decisions",
        "📊",
        "#7C3AED"
    )

st.divider()

# =====================================================
# WHAT THIS PLATFORM PROVIDES
# =====================================================

st.subheader("🚀 What You Can Explore")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    ### 📊 Descriptive Analytics

    - Revenue trends and performance
    - Course demand and enrollments
    - Teacher performance
    - User behavior
    - Course category analysis
    """)

with col2:

    st.markdown("""
    ### 🤖 Predictive Analytics

    - Enrollment demand prediction
    - Course revenue prediction
    - Category revenue forecasting
    - Feature importance analysis
    - Business recommendations
    """)

st.divider()

# =====================================================
# MACHINE LEARNING
# =====================================================

st.subheader("🧠 Predictive Intelligence")

st.markdown("""
EduPro uses machine learning models to move from **reactive reporting
to proactive planning**.

The predictive system evaluates course characteristics such as:

- Course price
- Course duration
- Course level
- Course rating
- Instructor experience
- Instructor rating
- Course category
- Instructor expertise

These factors are used to estimate future **enrollment demand and
course revenue**.
""")

st.divider()

# =====================================================
# NAVIGATION
# =====================================================

st.subheader("🧭 Explore EduPro")

st.info(
    "Use the sidebar to open the Dashboard, explore course and teacher "
    "performance, analyze revenue and users, review business insights, "
    "or generate AI-powered predictions."
)

st.success(
    "💡 Start with the Dashboard for an overall view, then use "
    "AI Prediction to explore future course demand and revenue."
)