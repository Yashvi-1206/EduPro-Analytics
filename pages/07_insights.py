import streamlit as st
from utils import preprocess_data
from components.style import load_css, page_title

st.set_page_config(page_title="Business Insights", layout="wide")

load_css()
page_title("Business Insights", "📈")

df = preprocess_data()

st.subheader("📊 Key Business Insights")

# Highest Revenue Category
best_category = (
    df.groupby("CourseCategory")["Amount"]
    .sum()
    .idxmax()
)

best_category_revenue = (
    df.groupby("CourseCategory")["Amount"]
    .sum()
    .max()
)

st.success(
    f"🏆 Highest Revenue Category: **{best_category}** (${best_category_revenue:,.2f})"
)

# Best Teacher
best_teacher = (
    df.groupby("TeacherName")["Amount"]
    .sum()
    .idxmax()
)

best_teacher_revenue = (
    df.groupby("TeacherName")["Amount"]
    .sum()
    .max()
)

st.info(
    f"👨‍🏫 Top Performing Teacher: **{best_teacher}** (${best_teacher_revenue:,.2f})"
)

# Best Course
best_course = (
    df.groupby("CourseName")["Amount"]
    .sum()
    .idxmax()
)

st.success(
    f"📚 Best Selling Course: **{best_course}**"
)
# Best Course by Enrollment

best_enrollment_course = (
    df.groupby("CourseName")["TransactionID"]
    .count()
    .idxmax()
)

best_enrollment_count = (
    df.groupby("CourseName")["TransactionID"]
    .count()
    .max()
)

st.success(
    f"🎓 Highest Demand Course: **{best_enrollment_course}** "
    f"({best_enrollment_count} enrollments)"
)
# Highest Demand Category

best_demand_category = (
    df.groupby("CourseCategory")["TransactionID"]
    .count()
    .idxmax()
)

best_demand_count = (
    df.groupby("CourseCategory")["TransactionID"]
    .count()
    .max()
)

st.info(
    f"📚 Highest Demand Category: **{best_demand_category}** "
    f"({best_demand_count} enrollments)"
)

# Best Payment Method
best_payment = (
    df.groupby("PaymentMethod")["Amount"]
    .sum()
    .idxmax()
)

st.info(
    f"💳 Most Used Payment Method: **{best_payment}**"
)

# Average Ratings
st.metric(
    "⭐ Average Course Rating",
    round(df["CourseRating"].mean(), 2)
)

st.metric(
    "👨‍🏫 Average Teacher Rating",
    round(df["TeacherRating"].mean(), 2)
)

st.divider()

st.subheader("📋 Business Recommendations")

recommendations = [
    "Prioritize high-demand course categories when planning new course launches.",
    "Use predicted enrollment to identify courses with strong future demand.",
    "Use predicted revenue to support course pricing decisions.",
    "Promote high-rated instructors and courses with strong enrollment performance.",
    "Review low-enrollment courses and consider improving content, pricing, or marketing.",
    "Focus resources on categories showing both strong enrollment and revenue.",
    "Monitor course price sensitivity before changing pricing."
]
for rec in recommendations:
    st.write("✅", rec)