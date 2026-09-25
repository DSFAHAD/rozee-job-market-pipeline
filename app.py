
import os

import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Job Market Dashboard",
    layout="wide",
    page_icon="📊"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main {
        background: linear-gradient(
            135deg,
            #0D0221 0%,
            #3C096C 100%
        );
    }

    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(122, 92, 250, 0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow:
            0 10px 30px rgba(122, 92, 250, 0.4);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    .block-container {
        animation: fadeIn 0.8s ease-in;
    }

    @keyframes fadeIn {

        from {
            opacity: 0;
            transform: translateY(10px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }

    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        color: #c9c3e0;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# ANIMATED METRIC
# ============================================================

def animated_metric(label, value):

    html_code = """
    <div class="metric-card"
         style="
            background: rgba(255,255,255,0.06);
            border:1px solid rgba(122,92,250,0.3);
            border-radius:16px;
            padding:20px;
            text-align:center;
            font-family:'Segoe UI', sans-serif;
         ">

        <div id="num"
             style="
                font-size:40px;
                font-weight:700;
                background:linear-gradient(
                    90deg,
                    #7209B7,
                    #38BDF8
                );
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
             ">
            0
        </div>

        <div style="
                color:#c9c3e0;
                font-size:14px;
                letter-spacing:1px;
                text-transform:uppercase;
             ">
            LABEL_PLACEHOLDER
        </div>

    </div>

    <script>

        let target = VALUE_PLACEHOLDER;

        let count = 0;

        let el = document.getElementById("num");

        let step = Math.ceil(target / 40) || 1;

        let interval = setInterval(function() {

            count += step;

            if (count >= target) {

                count = target;

                clearInterval(interval);

            }

            el.innerText = count;

        }, 25);

    </script>
    """

    html_code = html_code.replace(
        "LABEL_PLACEHOLDER",
        str(label)
    )

    html_code = html_code.replace(
        "VALUE_PLACEHOLDER",
        str(value)
    )

    components.html(
        html_code,
        height=130
    )


# ============================================================
# DASHBOARD RENDERING
# ============================================================

def render_dashboard(df):

    if df.empty:

        st.info(
            "No postings found for this category yet."
        )

        return


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        animated_metric(
            "Total Postings",
            len(df)
        )


    with col2:

        animated_metric(
            "Unique Companies",
            df["company_name"].nunique()
        )


    with col3:

        animated_metric(
            "Unique Cities",
            df["city"].nunique()
        )


    st.write("")


    # --------------------------------------------------------
    # PLOT SETTINGS
    # --------------------------------------------------------

    plot_bg = "rgba(0,0,0,0)"

    plot_font_color = "#e5e0ff"

    color_scale = [
        "#3C096C",
        "#7209B7",
        "#38BDF8"
    ]


    # ========================================================
    # TOP HIRING COMPANIES
    # ========================================================

    st.subheader(
        "🏢 Top Hiring Companies"
    )


    top_companies = (
        df["company_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )


    top_companies.columns = [
        "company",
        "count"
    ]


    fig1 = px.bar(
        top_companies,
        x="company",
        y="count",
        color="count",
        color_continuous_scale=color_scale
    )


    fig1.update_layout(
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_font_color,
        showlegend=False
    )


    fig1.update_traces(
        marker_line_width=0
    )


    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    # ========================================================
    # TOP SKILLS
    # ========================================================

    st.subheader(
        "🛠️ Top Skills in Demand"
    )


    skills_series = (
        df["raw_skills"]
        .fillna("")
        .astype(str)
        .str.split(", ")
        .explode()
    )


    skills_series = skills_series[
        skills_series.str.strip() != ""
    ]


    if not skills_series.empty:

        top_skills = (
            skills_series
            .value_counts()
            .head(10)
            .reset_index()
        )


        top_skills.columns = [
            "skill",
            "count"
        ]


        fig2 = px.bar(
            top_skills,
            x="count",
            y="skill",
            orientation="h",
            color="count",
            color_continuous_scale=color_scale
        )


        fig2.update_layout(
            plot_bgcolor=plot_bg,
            paper_bgcolor=plot_bg,
            font_color=plot_font_color,
            showlegend=False
        )


        fig2.update_yaxes(
            autorange="reversed"
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )


    else:

        st.info(
            "No skills data available yet."
        )


    # ========================================================
    # POSTINGS BY CITY
    # ========================================================

    st.subheader(
        "📍 Postings by Location"
    )


    top_locations = (
        df["city"]
        .value_counts()
        .head(10)
        .reset_index()
    )


    top_locations.columns = [
        "city",
        "count"
    ]


    location_colors = [
        "#7209B7",
        "#5A189A",
        "#38BDF8",
        "#3C096C",
        "#9D4EDD"
    ]


    fig3 = px.pie(
        top_locations,
        names="city",
        values="count",
        hole=0.5,
        color_discrete_sequence=location_colors
    )


    fig3.update_layout(
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_font_color
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    # ========================================================
    # RAW DATA
    # ========================================================

    st.subheader(
        "📋 Job Market Data"
    )


    st.dataframe(
        df,
        use_container_width=True
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "📊 Pakistan Tech Job Market"
)

st.caption(
    "Job market insights collected from Rozee.pk"
)


# ============================================================
# LOAD DATA FROM CSV
# ============================================================

CSV_PATH = "data/processed/job_market.csv"


if not os.path.exists(CSV_PATH):

    st.error(
        "Dataset not found. "
        "Please make sure "
        "`data/processed/job_market.csv` "
        "exists in the repository."
    )

    st.stop()


try:

    full_df = pd.read_csv(
        CSV_PATH
    )

except Exception as e:

    st.error(
        f"Unable to load dataset: {e}"
    )

    st.stop()


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = [
    "posting_id",
    "job_title",
    "company_name",
    "city",
    "category",
    "salary_min",
    "salary_max",
    "posted_date",
    "raw_skills",
    "source_url"
]


missing_columns = [
    column
    for column in required_columns
    if column not in full_df.columns
]


if missing_columns:

    st.error(
        "Dataset is missing required columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# CHECK DATA
# ============================================================

if full_df.empty:

    st.warning(
        "The dataset is empty."
    )

    st.stop()


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader(
    "📥 Dataset"
)


st.write(
    f"Current dataset contains "
    f"**{len(full_df):,} job postings**."
)


# ============================================================
# DOWNLOAD CSV
# ============================================================

csv_data = full_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Job Market CSV",
    data=csv_data,
    file_name="job_market.csv",
    mime="text/csv"
)


# ============================================================
# CATEGORY TABS
# ============================================================

categories = sorted(
    full_df["category"]
    .dropna()
    .unique()
    .tolist()
)


tab_labels = [
    "All"
] + categories


tabs = st.tabs(
    tab_labels
)


for tab, label in zip(
    tabs,
    tab_labels
):

    with tab:

        if label == "All":

            render_dashboard(
                full_df
            )

        else:

            render_dashboard(
                full_df[
                    full_df["category"] == label
                ]
            )
