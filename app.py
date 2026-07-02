import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Employee Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>

.main{
    padding-top:10px;
}

div[data-testid="metric-container"]{
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:10px;
    padding:10px;
    box-shadow:0 1px 3px rgba(0,0,0,0.08);
}

h1{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

st.title("📊 Employee Insights Dashboard")
st.write("Analyze employee data using Python, Pandas and Streamlit.")

# ---------------- Read CSV ----------------
df = pd.read_csv("employee_dataset.csv")

# ---------------- Create Sidebar Filters ----------------
st.sidebar.header("🔍 Filter Employees")
st.sidebar.markdown("---")
st.sidebar.write("### Dashboard Filters")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

city = st.sidebar.selectbox(
    "City",
    ["All"] + sorted(df["City"].unique().tolist())
)

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

search = st.sidebar.text_input("🔎 Search Employee")

# ---------------- Create filtered_df ----------------
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]

if city != "All":
    filtered_df = filtered_df[filtered_df["City"] == city]

if gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender]

if search:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search, case=False)
    ]

# ---------------- Calculate KPIs ----------------
st.markdown("---")
st.subheader("📊 Dashboard Overview")

total_employees = len(filtered_df)

if total_employees > 0:
    average_salary = filtered_df["Salary"].mean()
    highest_salary = filtered_df["Salary"].max()
    average_rating = filtered_df["Performance_Rating"].mean()
else:
    average_salary = 0
    highest_salary = 0
    average_rating = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Employees", total_employees)
col2.metric("💰 Average Salary", f"${average_salary:,.0f}")
col3.metric("🏆 Highest Salary", f"${highest_salary:,.0f}")
col4.metric("⭐ Average Rating", f"{average_rating:.1f}")

# ==========================
# VISUALIZATIONS (2-column grid)
# ==========================

st.markdown("---")
st.subheader("📈 Visualizations")

# ---- Row 1: Department | Gender ----
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("#### 📊 Employees by Department")
    fig, ax = plt.subplots(figsize=(5, 3))
    department_counts = filtered_df["Department"].value_counts()
    department_counts.plot(kind="bar", ax=ax, edgecolor="black")
    ax.set_title("Employees by Department", fontsize=11, fontweight="bold")
    ax.set_xlabel("Department", fontsize=9)
    ax.set_ylabel("Employees", fontsize=9)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

with row1_col2:
    st.markdown("#### 🥧 Gender Distribution")
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    filtered_df["Gender"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 9},
        ax=ax
    )
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("<br>", unsafe_allow_html=True)

# ---- Row 2: Salary | City ----
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("#### 💰 Salary Distribution")
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(filtered_df["Salary"], bins=10, edgecolor="black")
    ax.set_title("Salary Distribution", fontsize=11, fontweight="bold")
    ax.set_xlabel("Salary", fontsize=9)
    ax.set_ylabel("Employees", fontsize=9)
    ax.tick_params(axis='both', labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

with row2_col2:
    st.markdown("#### 🌍 Employees by City")
    fig, ax = plt.subplots(figsize=(5, 3))
    city_counts = filtered_df["City"].value_counts()
    city_counts.plot(kind="bar", ax=ax, edgecolor="black")
    ax.set_title("Employees by City", fontsize=11, fontweight="bold")
    ax.set_xlabel("City", fontsize=9)
    ax.set_ylabel("Employees", fontsize=9)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("<br>", unsafe_allow_html=True)

# ---- Row 3: Performance Rating | Business Insights ----
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown("#### ⭐ Performance Rating")
    fig, ax = plt.subplots(figsize=(5, 3))
    filtered_df["Performance_Rating"].value_counts().sort_index().plot(
        kind="bar", ax=ax, edgecolor="black"
    )
    ax.set_title("Performance Rating", fontsize=11, fontweight="bold")
    ax.set_xlabel("Rating", fontsize=9)
    ax.set_ylabel("Employees", fontsize=9)
    ax.tick_params(axis='both', labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

with row3_col2:
    st.markdown("#### 💡 Business Insights")
    if not filtered_df.empty:
        highest_department = (
            filtered_df.groupby("Department")["Salary"].mean().idxmax()
        )
        dept_avg_salary = (
            filtered_df.groupby("Department")["Salary"].mean().max()
        )
        largest_city = filtered_df["City"].value_counts().idxmax()
        best_rating = filtered_df["Performance_Rating"].mean()

        st.success(f"🏆 Highest Paying Department: {highest_department}")
        st.info(f"💰 Average Salary in that Department: ${dept_avg_salary:,.0f}")
        st.success(f"🌍 City with Maximum Employees: {largest_city}")
        st.info(f"⭐ Average Performance Rating: {best_rating:.2f}")
    else:
        st.warning("No employee data available for the selected filters.")

# ---------------- Employee Dataset (Expander) ----------------
st.markdown("---")
with st.expander("📋 View Employee Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Filtered Data",
        csv,
        "employee_data.csv",
        "text/csv"
    )

# ---------------- Project Information ----------------
st.markdown("---")

st.markdown(
    """
    ### 👨‍💻 Project Information

    **Employee Insights Dashboard**

    Developed using **Python, Pandas, Matplotlib and Streamlit**

    Built as part of my Data Analysis learning journey.
    """
)

st.markdown("---")
st.caption("Developed using Python • Pandas • Streamlit • Matplotlib")