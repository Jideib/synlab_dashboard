import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="SYNLAB Analytics Dashboard",
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("SYNLAB_Surveydata_AUGMENTED_500.csv")

data = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filters")

age_filter = st.sidebar.multiselect(
    "Age Group",
    options=data['Age_Group'].unique(),
    default=data['Age_Group'].unique()
)

occupation_filter = st.sidebar.multiselect(
    "Occupation", 
    options=data['Occupation'].unique(),
    default=data['Occupation'].unique()
)

familiarity_filter = st.sidebar.multiselect(
    "Familiarity Level",
    options=data['Familiarity_with_SYNLAB'].unique(), 
    default=data['Familiarity_with_SYNLAB'].unique()
)

# Apply filters
filtered_data = data[
    (data['Age_Group'].isin(age_filter)) &
    (data['Occupation'].isin(occupation_filter)) &
    (data['Familiarity_with_SYNLAB'].isin(familiarity_filter))
]

# Main dashboard
st.title("🏥 SYNLAB Analytics Dashboard")
st.markdown("---")

# KPI Metrics
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Respondents", 
        len(filtered_data),
        delta=f"{len(filtered_data) - len(data)}" if len(filtered_data) != len(data) else None
    )

with col2:
    avg_rating = filtered_data['SYNLAB_Rating_1_5'].mean()
    st.metric("Average Rating", f"{avg_rating:.1f}/5")

with col3:
    awareness = (filtered_data['Heard_SYNLAB'].sum() / len(filtered_data)) * 100
    st.metric("Brand Awareness", f"{awareness:.1f}%")

with col4:
    recommendation = ((filtered_data['Recommendation_Score'] >= 4).sum() / len(filtered_data)) * 100
    st.metric("Recommendation Rate", f"{recommendation:.1f}%")

with col5:
    usage = (filtered_data['Used_SYNLAB'].sum() / len(filtered_data)) * 100
    st.metric("Usage Rate", f"{usage:.1f}%")

# Charts Row 1
st.markdown("---")
st.subheader("📈 Brand Performance")

col1, col2 = st.columns(2)

with col1:
    # Brand Awareness Comparison
    awareness_data = {
        'Lab': ['SYNLAB', 'Clinix', 'Mecure', 'Clina Lancet', 'Afriglobal'],
        'Awareness': [
            filtered_data['Heard_SYNLAB'].sum(),
            filtered_data['Heard_Clinix'].sum(),
            filtered_data['Heard_Mecure'].sum(),
            filtered_data['Heard_Clina_Lancet'].sum(), 
            filtered_data['Heard_Afriglobal'].sum()
        ]
    }
    awareness_df = pd.DataFrame(awareness_data)
    fig1 = px.bar(awareness_df, x='Lab', y='Awareness', 
                 title="Brand Awareness Comparison",
                 color='Awareness')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Rating Distribution
    fig2 = px.histogram(filtered_data, x='SYNLAB_Rating_1_5',
                      title="SYNLAB Rating Distribution",
                      nbins=5,
                      color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    # Familiarity vs Rating
    familiarity_rating = filtered_data.groupby('Familiarity_with_SYNLAB')['SYNLAB_Rating_1_5'].mean().reset_index()
    fig3 = px.bar(familiarity_rating, x='Familiarity_with_SYNLAB', y='SYNLAB_Rating_1_5',
                 title="Average Rating by Familiarity Level",
                 color='SYNLAB_Rating_1_5')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Demographic Distribution
    demo_col = st.selectbox("Select Demographic", ['Age_Group', 'Gender', 'Occupation'])
    demo_counts = filtered_data[demo_col].value_counts().reset_index()
    demo_counts.columns = [demo_col, 'Count']
    fig4 = px.pie(demo_counts, names=demo_col, values='Count',
                 title=f"Distribution by {demo_col}")
    st.plotly_chart(fig4, use_container_width=True)

# Competitive Analysis
st.markdown("---")
st.subheader("⚔️ Competitive Analysis")

# Usage comparison
usage_data = {
    'Lab': ['SYNLAB', 'Clinix', 'Mecure', 'Clina Lancet', 'Afriglobal'],
    'Usage_Rate': [
        (filtered_data['Used_SYNLAB'].sum() / len(filtered_data)) * 100,
        (filtered_data['Used_Clinix'].sum() / len(filtered_data)) * 100,
        (filtered_data['Used_Mecure'].sum() / len(filtered_data)) * 100,
        (filtered_data['Used_Clina_Lancet'].sum() / len(filtered_data)) * 100,
        (filtered_data['Used_Afriglobal'].sum() / len(filtered_data)) * 100
    ]
}
usage_df = pd.DataFrame(usage_data)

fig5 = px.bar(usage_df, x='Lab', y='Usage_Rate',
             title="Laboratory Usage Rates",
             color='Usage_Rate')
st.plotly_chart(fig5, use_container_width=True)

# Raw Data Preview
if st.checkbox("Show Raw Data"):
    st.subheader("📋 Raw Data Preview")
    st.dataframe(filtered_data)

# Footer
st.markdown("---")
st.markdown("SYNLAB Analytics Dashboard • Built with Streamlit")