# Cellular Network Performance Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Network Performance Dashboard",
                   page_icon=None,
                   layout="wide",
                   initial_sidebar_state="expanded")

# Load data
df = pd.read_csv('train.csv')
# Remove Tower ID and User ID columns if they exist
df = df.drop(columns=[col for col in ['Tower ID', 'User ID'] if col in df.columns])

# Sidebar
st.sidebar.header("Network Performance Dashboard")
st.sidebar.write("This dashboard visualizes cellular network performance data.")
st.sidebar.write("")

# Sidebar filters
def get_categorical_columns(df):
    return df.select_dtypes(include=['object']).columns.tolist()

def get_numerical_columns(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()

cat_cols = get_categorical_columns(df)
num_cols = get_numerical_columns(df)

cat_filter = st.sidebar.selectbox("Categorical Filtering", [None] + cat_cols)
num_filter = st.sidebar.selectbox("Numerical Filtering", [None] + num_cols)
row_filter = st.sidebar.selectbox("Row Filtering", [None] + cat_cols)
col_filter = st.sidebar.selectbox("Column Filtering", [None] + cat_cols)
st.sidebar.write("")
st.sidebar.markdown("Made by :satellite: by Eng. Ehab El-Guindy")
# Add LinkedIn and GitHub links
st.sidebar.markdown("**Connect with me:**")
st.sidebar.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/ehab-el-guindy-375a4488)")
st.sidebar.markdown("[🐙 GitHub](https://github.com/ehabelguindy)")

# Main body
st.title("Cellular Network Performance Data Dashboard")
st.write("Explore and analyze cellular network performance metrics.")

# Key metrics
metrics = [
    ("Max Signal Strength (dBm)", df['Signal Strength (dBm)'].max()),
    ("Min Signal Strength (dBm)", df['Signal Strength (dBm)'].min()),
    ("Max SNR", df['SNR'].max()),
    ("Min SNR", df['SNR'].min()),
    ("Max Call Duration (s)", df['Call Duration (s)'].max()),
    ("Min Call Duration (s)", df['Call Duration (s)'].min()),
    ("Max Attenuation", df['Attenuation'].max()),
    ("Min Attenuation", df['Attenuation'].min()),
    ("Max Distance to Tower (km)", df['Distance to Tower (km)'].max()),
    ("Min Distance to Tower (km)", df['Distance to Tower (km)'].min()),
]

cols = st.columns(5)
for i, (label, value) in enumerate(metrics):
    cols[i % 5].metric(label, f"{value:.2f}")

# Scatter plot
st.subheader("Signal Strength vs. SNR")
fig = px.scatter(
    df,
    x='Signal Strength (dBm)',
    y='SNR',
    color=cat_filter if cat_filter else None,
    size=num_filter if num_filter else None,
    facet_col=col_filter if col_filter else None,
    facet_row=row_filter if row_filter else None,
    hover_data=['Call Duration (s)', 'Attenuation', 'Distance to Tower (km)']
)
st.plotly_chart(fig, use_container_width=True)

# Bar chart
st.subheader("Average Call Duration by Environment")
if 'Environment' in df.columns:
    bar_df = df.groupby('Environment')['Call Duration (s)'].mean().reset_index()
    fig2 = px.bar(bar_df, x='Environment', y='Call Duration (s)', color='Environment')
    st.plotly_chart(fig2, use_container_width=True)

# Pie chart
st.subheader("Call Type Distribution")
if 'Call Type' in df.columns:
    pie_df = df['Call Type'].value_counts().reset_index()
    pie_df.columns = ['Call Type', 'Count']
    fig3 = px.pie(pie_df, names='Call Type', values='Count', hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

# Show data
with st.expander("Show Raw Data"):
    st.dataframe(df)

