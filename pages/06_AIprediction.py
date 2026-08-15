import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="AI Prediction",
    layout="wide"
)

st.title("🤖 EduPro Predictive Intelligence")

st.write(
    "Predict expected course enrollments and revenue "
    "using the trained machine learning models."
)

# =====================================================
# LOAD MODELS
# =====================================================

try:
    enrollment_model = joblib.load(
        "enrollment_model.pkl"
    )

    revenue_model = joblib.load(
        "course_revenue_model.pkl"
    )


except Exception as e:

    st.error(
        "Models not found. Please run train_model.py first."
    )

    st.stop()


# =====================================================
# USER INPUTS
# =====================================================

st.subheader("📚 Course Information")

col1, col2 = st.columns(2)

with col1:

    course_category = st.selectbox(
        "Course Category",
        [
            "Programming",
            "Business",
            "Design",
            "Data Science",
            "Marketing"
        ]
    )

    course_type = st.selectbox(
        "Course Type",
        [
            "Online",
            "Offline"
        ]
    )

    course_level = st.selectbox(
        "Course Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    expertise = st.text_input(
        "Instructor Expertise",
        "Programming"
    )


with col2:

    price = st.number_input(
        "Course Price",
        min_value=0.0,
        value=100.0
    )

    duration = st.number_input(
        "Course Duration",
        min_value=1.0,
        value=20.0
    )

    course_rating = st.slider(
        "Course Rating",
        1.0,
        5.0,
        4.0
    )

    experience = st.number_input(
        "Instructor Experience",
        min_value=0.0,
        value=5.0
    )

    teacher_rating = st.slider(
        "Instructor Rating",
        1.0,
        5.0,
        4.0
    )


# =====================================================
# FEATURE ENGINEERING
# =====================================================

if st.button("🔮 Predict"):

    # Price Band

    if price <= 50:
        price_band = "Low"
    elif price <= 150:
        price_band = "Medium"
    else:
        price_band = "High"


    # Duration Bucket

    if duration <= 20:
        duration_bucket = "Short"
    elif duration <= 50:
        duration_bucket = "Medium"
    else:
        duration_bucket = "Long"


    # Rating Tier

    if course_rating <= 3:
        rating_tier = "Low"
    elif course_rating <= 4:
        rating_tier = "Good"
    else:
        rating_tier = "Excellent"


    # Experience Bucket

    if experience <= 2:
        experience_bucket = "Beginner"
    elif experience <= 5:
        experience_bucket = "Intermediate"
    elif experience <= 10:
        experience_bucket = "Experienced"
    else:
        experience_bucket = "Expert"


    # =================================================
    # CREATE INPUT DATA
    # =================================================

    input_data = pd.DataFrame({

        "CourseCategory": [course_category],

        "CourseType": [course_type],

        "CourseLevel": [course_level],

        "CoursePrice": [price],

        "CourseDuration": [duration],

        "CourseRating": [course_rating],

        "YearsOfExperience": [experience],

        "TeacherRating": [teacher_rating],

        "Expertise": [expertise],

        "PriceBand": [price_band],

        "DurationBucket": [duration_bucket],

        "RatingTier": [rating_tier],

        "ExperienceBucket": [experience_bucket]
    })


    # =================================================
    # PREDICTIONS
    # =================================================

    enrollment_prediction = enrollment_model.predict(
        input_data
    )[0]

    revenue_prediction = revenue_model.predict(
        input_data
    )[0]


    # =================================================
    # DISPLAY RESULTS
    # =================================================

    st.subheader("📊 Prediction Results")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Expected Enrollments",
            f"{max(0, enrollment_prediction):,.0f}"
        )


    with col2:

        st.metric(
            "Expected Course Revenue",
            f"${max(0, revenue_prediction):,.2f}"
        )


    st.success(
        "Prediction completed successfully."
    )
    
    # =====================================================
# FEATURE IMPORTANCE EXPLORER
# =====================================================

st.divider()

st.subheader("🔍 Feature Importance Explorer")

st.write(
    "Understand which course and instructor factors "
    "have the greatest influence on predictions."
)

importance_type = st.selectbox(
    "Select Prediction Target",
    [
        "Enrollment Demand",
        "Course Revenue"
    ]
)

if importance_type == "Enrollment Demand":

    importance_file = "enrollment_feature_importance.pkl"

else:

    importance_file = "revenue_feature_importance.pkl"


try:

    importance_df = joblib.load(
        importance_file
    )

    top_features = (
        importance_df
        .head(15)
        .sort_values(
            "Importance",
            ascending=True
        )
    )

    fig_importance = px.bar(
        top_features,
        x="Importance",
        y="Feature",
        orientation="h",
        title=f"Top Features Influencing {importance_type}"
    )

    st.plotly_chart(
        fig_importance,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        "Feature importance data not found. "
        "Please run train_model.py again."
    )