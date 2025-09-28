import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import base64
from PIL import Image
import io

# Page config
st.set_page_config(page_title="Executive Overview", page_icon="assets/synlab_favicon.png", layout="wide")

# Function to load and encode images
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

# Function to display logo with proper sizing
def display_logo(image_path, width=200):
    try:
        logo_base64 = get_image_base64(image_path)
        if logo_base64:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <img src="data:image/png;base64,{logo_base64}" width="{width}" alt="SYNLAB Logo">
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not load logo: {e}")

# Custom CSS for this page
st.markdown("""
<style>
    /* Navy Blue Theme for Charts */
    .chart-container {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #0A2647;
        margin: 10px 0;
    }
    
    /* Metric highlight */
    .metric-highlight {
        background: linear-gradient(135deg, #205295, #2C74B3);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

display_logo("assets/synlab_logo.jpg", width=200)


@st.cache_data
def load_data():
    return pd.read_csv("data/SYNLAB_Surveydata_AUGMENTED_500.csv")
data = load_data()


# Sidebar with themed styling
st.sidebar.markdown("""
<div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px;'>
    <h3>🎛️ Global Filters</h3>
</div>
""", unsafe_allow_html=True)

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

# Apply filters
filtered_data = data[
    (data['Age_Group'].isin(age_filter)) & 
    (data['Occupation'].isin(occupation_filter))
]

# Main content
st.markdown("""
<div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 20px; border-radius: 10px; color: white;'>
    <h1>🏠 Executive Overview</h1>
    <p>High-level performance metrics and key insights at a glance</p>
</div>
""", unsafe_allow_html=True)

# KPI Row 1 - Brand Health
st.subheader("📊 Brand Health Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

# Custom metric styling
def styled_metric(label, value, delta=None):
    return f"""
    <div class="metric-highlight">
        <h3>{value}</h3>
        <p>{label}</p>
    </div>
    """

with col1:
    total = len(filtered_data)
    st.markdown(styled_metric("Total Respondents", str(total)), unsafe_allow_html=True)

with col2:
    awareness = (filtered_data['Heard_SYNLAB'].sum() / total) * 100
    st.markdown(styled_metric("Brand Awareness", f"{awareness:.1f}%"), unsafe_allow_html=True)

with col3:
    avg_rating = filtered_data['SYNLAB_Rating_1_5'].mean()
    st.markdown(styled_metric("Avg Rating", f"{avg_rating:.1f}/5"), unsafe_allow_html=True)

with col4:
    promoters = (filtered_data['Likelihood_to_Recommend'] >= 3).sum()
    nps = ((promoters / total) * 100) - ((filtered_data['Likelihood_to_Recommend'] <= 2).sum() / total * 100)
    st.markdown(styled_metric("Net Promoter Score", f"{nps:.0f}"), unsafe_allow_html=True)

with col5:
    usage = (filtered_data['Used_SYNLAB'].sum() / total) * 100
    st.markdown(styled_metric("Usage Rate", f"{usage:.1f}%"), unsafe_allow_html=True)

# Charts with Navy Blue theme
st.markdown("---")
st.subheader("📈 Performance Charts")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Brand Awareness Comparison with theme colors
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
                 title="🚀 Brand Awareness Comparison",
                 color='Awareness',
                 color_continuous_scale=['#2C74B3', '#205295', '#144272', '#0A2647'])
    
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#0A2647")
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Rating Distribution with theme colors
    fig2 = px.histogram(filtered_data, x='SYNLAB_Rating_1_5',
                      title="⭐ SYNLAB Rating Distribution",
                      nbins=5,
                      color_discrete_sequence=['#0A2647'])
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#0A2647")
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# More charts with theme
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Familiarity vs Rating
    familiarity_rating = filtered_data.groupby('Familiarity_with_SYNLAB')['SYNLAB_Rating_1_5'].mean().reset_index()
    fig3 = px.bar(familiarity_rating, x='Familiarity_with_SYNLAB', y='SYNLAB_Rating_1_5',
                 title="📊 Average Rating by Familiarity Level",
                 color='SYNLAB_Rating_1_5',
                 color_continuous_scale=['#2C74B3', '#205295', '#144272', '#0A2647'])
    
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#0A2647")
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Recommendation Distribution
    rec_counts = filtered_data['Likelihood_to_Recommend'].value_counts().sort_index()
    fig4 = px.pie(values=rec_counts.values, names=rec_counts.index,
                 title="💫 Recommendation Likelihood",
                 color_discrete_sequence=['#0A2647', '#144272', '#205295', '#2C74B3', '#F8F9FA'])
    
    fig4.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#0A2647")
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Quick Insights Cards
st.subheader("🚀 Performance Snapshot")

col1, col2, col3 = st.columns(3)

with col1:
    # Response Rate Quality
    completion_rate = (filtered_data.notna().sum().mean() / len(filtered_data.columns)) * 100
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{completion_rate:.1f}%</h3>
        <p>Data Completion Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Sentiment Score
    positive_sentiment = (filtered_data['SYNLAB_Rating_1_5'] >= 4).sum() / len(filtered_data) * 100
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{positive_sentiment:.1f}%</h3>
        <p>Positive Sentiment</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Market Coverage
    unique_areas = filtered_data['Area'].nunique() if 'Area' in filtered_data.columns else 15
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{unique_areas}</h3>
        <p>Areas Covered</p>
    </div>
    """, unsafe_allow_html=True)
# Insights with themed cards
st.markdown("---")
st.subheader("💡 Quick Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #205295, #2C74B3); padding: 20px; border-radius: 10px; color: white;'>
        <h4>🚀 Top Strength</h4>
        <p>{filtered_data['Belief_Quality_Service'].sum()} respondents believe in quality service</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #144272, #205295); padding: 20px; border-radius: 10px; color: white; margin-top: 10px;'>
        <h4>🎯 Loyal Customers</h4>
        <p>{filtered_data['Familiarity_Score'].mean():.1f}/3 average familiarity score</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #2C74B3, #205295); padding: 20px; border-radius: 10px; color: white;'>
        <h4>🔧 Improvement Area</h4>
        <p>{filtered_data['Improve_Result_Speed'].sum()} respondents want faster results</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 20px; border-radius: 10px; color: white; margin-top: 10px;'>
        <h4>⚔️ Competition Alert</h4>
        <p>{filtered_data['Heard_Clinix'].sum()} respondents aware of Clinix</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #0A2647; color: white; padding: 15px; border-radius: 10px; text-align: center;'>
    <p>SYNLAB Executive Overview</p>
</div>
""", unsafe_allow_html=True)