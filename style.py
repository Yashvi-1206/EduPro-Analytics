import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* Keep Streamlit's default theme/background */

    /* Page headings */
    h1, h2, h3 {
        font-weight: 700;
    }

    /* KPI hover effect only */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        transition: 0.3s;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    </style>
    """, unsafe_allow_html=True)


def page_title(title, icon):

    st.markdown(
        f"""
        <h1 style="
            text-align:center;
            font-weight:700;
        ">
            {icon} {title}
        </h1>
        """,
        unsafe_allow_html=True
    )