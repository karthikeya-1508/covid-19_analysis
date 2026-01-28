import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
sns.set_style("whitegrid")

# ---------- LOAD DATA ----------
df = pd.read_csv("country_wise_latest.csv")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("Filters")

region = st.sidebar.selectbox(
    "WHO Region",
    ["All"] + list(df["WHO Region"].unique())
)

country = st.sidebar.selectbox(
    "Country",
    ["All"] + list(df["Country/Region"].unique())
)

min_cases, max_cases = st.sidebar.slider(
    "Confirmed Cases Range",
    int(df["Confirmed"].min()),
    int(df["Confirmed"].max()),
    (1000, int(df["Confirmed"].max()))
)

sort_by = st.sidebar.selectbox(
    "Sort By",
    ["Confirmed", "Deaths", "Recovered", "Active"]
)

# ---------- APPLY FILTERS ----------
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["WHO Region"] == region]

if country != "All":
    filtered_df = filtered_df[filtered_df["Country/Region"] == country]

filtered_df = filtered_df[
    filtered_df["Confirmed"].between(min_cases, max_cases)
].sort_values(by=sort_by, ascending=False)

# ---------- TITLE ----------
st.title("🌍 COVID-19 Analytics Dashboard")

# ---------- KPIs ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Confirmed", int(filtered_df["Confirmed"].sum()))
c2.metric("Deaths", int(filtered_df["Deaths"].sum()))
c3.metric("Recovered", int(filtered_df["Recovered"].sum()))
c4.metric("Active", int(filtered_df["Active"].sum()))

# ---------- GRAPHS ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Countries by Confirmed Cases")
    top10 = filtered_df.head(10)
    fig, ax = plt.subplots()
    sns.barplot(x="Confirmed", y="Country/Region", data=top10, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Region-wise Confirmed Cases")
    region_cases = filtered_df.groupby("WHO Region")["Confirmed"].sum()
    fig, ax = plt.subplots()
    region_cases.plot(kind="barh", ax=ax)
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Recovery Rate vs Death Rate")
    fig, ax = plt.subplots()
    sns.scatterplot(
        x="Recovered / 100 Cases",
        y="Deaths / 100 Cases",
        hue="WHO Region",
        data=filtered_df,
        ax=ax
    )
    st.pyplot(fig)

with col2:
    st.subheader("Active Cases Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["Active"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)
