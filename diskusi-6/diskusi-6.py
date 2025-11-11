# diskusi-6.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['year'] = pd.to_datetime(df['date']).dt.year
    return df

DATA_PATH = "/home/mueiya/.cache/kagglehub/datasets/emirhanakku/disaster-and-emergency-response-dataset-20182024/versions/1/global_disaster_response_2018_2024.csv"
df = load_data(DATA_PATH)

st.set_page_config(
    page_title="Disaster Dashboard",
    layout="wide",   # ini penting
    initial_sidebar_state="expanded"
)

# Sidebar Filters
st.sidebar.header("Filter Dataset")
years = sorted(df['year'].unique())
selected_years = st.sidebar.slider("Year Range", min_value=min(years), max_value=max(years),
                                   value=(min(years), max(years)))
countries = df['country'].unique()
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
disaster_types = df['disaster_type'].unique()
selected_disasters = st.sidebar.multiselect("Disaster Types", disaster_types, default=disaster_types)

# Filter DataFrame
filtered_df = df[
    (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1]) &
    (df['country'].isin(selected_countries)) &
    (df['disaster_type'].isin(selected_disasters))
]

# Main Page
st.title("🌍 Disaster & Emergency Response Dashboard")

st.markdown("""
This dashboard is created as a **college assignment** by **[Muhammad Imam Mujaddid Huwaidi] - [050122513]**.  
Data is sourced from [Kaggle - Disaster and Emergency Response Dataset 2018-2024](https://www.kaggle.com/datasets/emirhanakku/disaster-and-emergency-response-dataset-20182024/data).
""")
st.markdown(f"Showing **{filtered_df.shape[0]} records** after filtering.")

# Summary statistics
st.subheader("Summary Statistics")
st.dataframe(filtered_df.describe())

# Plot 1
st.subheader("Disaster Counts by Type")
count_plot = px.bar(
    filtered_df.groupby('disaster_type').size().reset_index(name='count'),
    x='disaster_type', y='count', color='disaster_type'
)
st.plotly_chart(count_plot, use_container_width=True)

# Make 2 column
col1, col2 = st.columns(2)

with col1:
# Plot 2
    st.subheader("Response Efficiency vs Aid Amount")
    scatter_plot = px.scatter(
        filtered_df, x='aid_amount_usd', y='response_efficiency_score',
        color='disaster_type', size='severity_index', hover_data=['country', 'year']
    )
    st.plotly_chart(scatter_plot, use_container_width=True)

    # Plot 3
    st.subheader("Disaster Counts by Country")
    country_counts = filtered_df.groupby('country').size().reset_index(name='count')
    bar_country = px.bar(
        country_counts.sort_values('count', ascending=False),
        x='country', y='count', color='count'
    )
    st.plotly_chart(bar_country, use_container_width=True)

    # Plot 4
    st.subheader("Disaster Trend Over Years")
    trend = filtered_df.groupby(['year', 'disaster_type']).size().reset_index(name='count')
    trend_plot = px.line(
        trend, x='year', y='count', color='disaster_type',
        markers=True
    )
    st.plotly_chart(trend_plot, use_container_width=True)


with col2:
# Plot 5
    st.subheader("Casualties vs Economic Loss")
    bubble_plot = px.scatter(
        filtered_df, x='economic_loss_usd', y='casualties',
        size='severity_index', color='disaster_type',
        hover_data=['country', 'year']
    )
    st.plotly_chart(bubble_plot, use_container_width=True)

    # Plot 6
    st.subheader("Total Economic Loss by Country")
    economic_loss = filtered_df.groupby('country')['economic_loss_usd'].sum().reset_index()
    bar_loss = px.bar(
        economic_loss.sort_values('economic_loss_usd', ascending=False),
        x='country', y='economic_loss_usd', color='economic_loss_usd'
    )
    st.plotly_chart(bar_loss, use_container_width=True)
    # Plot 7 
    st.subheader("Response Time Distribution by Disaster Type")
    box_plot = px.box(
        filtered_df, x='disaster_type', y='response_time_hours',
        color='disaster_type'
    )
    st.plotly_chart(box_plot, use_container_width=True)
