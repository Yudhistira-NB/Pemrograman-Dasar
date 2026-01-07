import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Customer Analytics Dashboard")
df = pd.read_csv("Dashboard_Customers/customers.csv")

st.sidebar.header("Filter Data")
departments = st.sidebar.multiselect(
    "Pilih Departments",
    df["Department"].dropna().unique()
)

genders = st.sidebar.multiselect(
    "Pilih Gender",
    df["Gender"].dropna().unique()
)

st.sidebar.header("Filter Rentang Umur")
min_usia, max_usia = int(df["Age"].min()), int(df["Age"].max())
usia_range = st.sidebar.slider(
    "Usia",
    min_value=min_usia,
    max_value=max_usia,
    value=(min_usia, max_usia)
)

df_filtered = df[
    (df["Department"].isin(departments)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].between(usia_range[0], usia_range[1]))
]

st.subheader("Data Tabel")
st.dataframe(df_filtered)

st.subheader("Visualisasi Statistik")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribusi Gender")
    pie_gender = px.pie(
        df_filtered,
        names="Gender",
        color="Gender",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(pie_gender)

with col2:
    st.subheader("Gaji Rata-rata per Department")

    salary_dept = (
        df_filtered
        .groupby("Department")["AnnualSalary"]
        .mean()
        .reset_index()
    )

    bar_salary = px.bar(
        salary_dept,
        x="Department",
        y="AnnualSalary",
        color="Department",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(bar_salary)

    
st.subheader("Rata-rata Gaji Berdasarkan Usia")

salary_age = (
    df_filtered
    .groupby("Age")["AnnualSalary"]
    .mean()
    .reset_index()
    .sort_values("Age")
)

line_age = px.line(
    salary_age,
    x="Age",
    y="AnnualSalary",
    markers=True
)

st.plotly_chart(line_age)


st.subheader("Tambahkan Chart Lainnya Versi Anda Sendiri!")
st.write("Untuk menambahkan chart lihat dan pahami struktur tabel data set file customers.csv")

st.subheader("Frekuensi Berdasarkan Umur")
fig_hist = px.histogram(
    df_filtered, 
    x="Age", 
    nbins=20,
    color_discrete_sequence=['#636EFA']
)
st.plotly_chart(fig_hist)

st.subheader("Hierarki Departemen dan Gender berdasarkan Total Gaji")
fig_tree = px.treemap(
    df_filtered, 
    path=["Department", "Gender"], 
    values="AnnualSalary", # atau bisa menggunakan count
    color="AnnualSalary",
    color_continuous_scale="RdBu",
)
st.plotly_chart(fig_tree)

st.subheader("Distribusi Umur dalam Departemen dan Gender")
fig_sunburst = px.sunburst(
    df_filtered,
    path=["Department", "Gender"],
    color="Age",
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig_sunburst)

st.subheader("Rentang Gaji per Department")
fig_box = px.box(
    df_filtered, 
    x="Department", 
    y="AnnualSalary", 
    color="Department",
    title="Distribusi Gaji (Min, Median, Max)"
)

st.plotly_chart(fig_box)
