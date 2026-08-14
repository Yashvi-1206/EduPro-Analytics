import streamlit as st


def kpi_card(title, value, icon, color):

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:25px;
            border-radius:20px;
            color:#FFFFFF !important;
            box-shadow:0px 8px 20px rgba(0,0,0,0.15);
            margin-bottom:15px;
        ">

        <h4 style="
            margin:0;
            color:#FFFFFF !important;
            font-weight:600;
        ">
            {icon} {title}
        </h4>

        <h1 style="
            margin-top:10px;
            font-size:38px;
            color:#FFFFFF !important;
            font-weight:700;
        ">
            {value}
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )