import streamlit as st
import pandas as pd
import base64
from PIL import Image
import io

st.set_page_config(
    page_title="SYNLAB Analytics Dashboard",
    page_icon="assets/synlab_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Custom CSS with Navy Blue Theme
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --navy-blue: #0A2647;
        --dark-blue: #144272;
        --light-blue: #205295;
        --sky-blue: #2C74B3;
        --cream: #F8F9FA;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3rem;
        color: var(--navy-blue);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: var(--navy-blue);
    }
    
    .css-1d391kg p, .css-1lcbmhc p {
        color: white !important;
    }
    
    /* Filter Section */
    .filter-section {
        background: linear-gradient(135deg, var(--light-blue), var(--sky-blue));
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    
    /* Custom cards */
    .custom-card {
        background: linear-gradient(135deg, var(--light-blue), var(--sky-blue));
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    .custom-card-light {
        background-color: var(--cream);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid var(--light-blue);
        margin: 10px 0;
    }
    
    /* Summary Section */
    .summary-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid var(--navy-blue);
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .summary-header {
        color: var(--navy-blue);
        border-bottom: 2px solid var(--light-blue);
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    /* Footer */
    .footer {
        background-color: var(--navy-blue);
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

display_logo("assets/synlab_logo.jpg", width=200)

# Header with Logo Integration
st.markdown("""
<div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 20px; border-radius: 10px; color: white; text-align: center;'>
    <h1 class="main-header">Analytics Dashboard</h1>
    <p>Comprehensive insights and performance metrics</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for filters
if 'age_filter' not in st.session_state:
    st.session_state.age_filter = []
if 'occupation_filter' not in st.session_state:
    st.session_state.occupation_filter = []
if 'gender_filter' not in st.session_state:
    st.session_state.gender_filter = []
if 'familiarity_filter' not in st.session_state:
    st.session_state.familiarity_filter = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Load data once and store in session state
@st.cache_data
def load_data():
    return pd.read_csv("data/SYNLAB_Surveydata_AUGMENTED_500.csv")

if not st.session_state.data_loaded:
    st.session_state.data = load_data()
    st.session_state.data_loaded = True

# Global filters in sidebar
st.sidebar.markdown("""
<div class="filter-section">
    <h3>🌐 Global Filters</h3>
    <p>Apply across all pages</p>
</div>
""", unsafe_allow_html=True)

# Age filter
st.session_state.age_filter = st.sidebar.multiselect(
    "Age Group",
    options=st.session_state.data['Age_Group'].unique(),
    default=st.session_state.data['Age_Group'].unique(),
    key="global_age_filter"
)

# Occupation filter
st.session_state.occupation_filter = st.sidebar.multiselect(
    "Occupation",
    options=st.session_state.data['Occupation'].unique(),
    default=st.session_state.data['Occupation'].unique(),
    key="global_occupation_filter"
)

# Gender filter
st.session_state.gender_filter = st.sidebar.multiselect(
    "Gender",
    options=st.session_state.data['Gender'].unique(),
    default=st.session_state.data['Gender'].unique(),
    key="global_gender_filter"
)

# Familiarity filter
st.session_state.familiarity_filter = st.sidebar.multiselect(
    "Familiarity Level",
    options=st.session_state.data['Familiarity_with_SYNLAB'].unique(),
    default=st.session_state.data['Familiarity_with_SYNLAB'].unique(),
    key="global_familiarity_filter"
)

# Reset filters button
if st.sidebar.button("🔄 Reset All Filters", type="secondary"):
    st.session_state.age_filter = st.session_state.data['Age_Group'].unique().tolist()
    st.session_state.occupation_filter = st.session_state.data['Occupation'].unique().tolist()
    st.session_state.gender_filter = st.session_state.data['Gender'].unique().tolist()
    st.session_state.familiarity_filter = st.session_state.data['Familiarity_with_SYNLAB'].unique().tolist()
    st.rerun()

# Filter status
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filter Status")
st.sidebar.write(f"**Age Groups:** {len(st.session_state.age_filter)} selected")
st.sidebar.write(f"**Occupations:** {len(st.session_state.occupation_filter)} selected")
st.sidebar.write(f"**Genders:** {len(st.session_state.gender_filter)} selected")
st.sidebar.write(f"**Familiarity Levels:** {len(st.session_state.familiarity_filter)} selected")

# Apply filters to get filtered data
def get_filtered_data():
    filtered_data = st.session_state.data[
        (st.session_state.data['Age_Group'].isin(st.session_state.age_filter)) &
        (st.session_state.data['Occupation'].isin(st.session_state.occupation_filter)) &
        (st.session_state.data['Gender'].isin(st.session_state.gender_filter)) &
        (st.session_state.data['Familiarity_with_SYNLAB'].isin(st.session_state.familiarity_filter))
    ]
    return filtered_data

# Store filtered data in session state
st.session_state.filtered_data = get_filtered_data()

# Main page content

# Themed cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="custom-card">
        <h3>📊 500</h3>
        <p>Survey Responses</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card">
        <h3>🎯 17</h3>
        <p>Analytical Components</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="custom-card">
        <h3>⚔️ 5</h3>
        <p>Competitor Brands</p>
    </div>
    """, unsafe_allow_html=True)

# Content with light cards
st.markdown("""
<div class="custom-card-light">
    <h3>🚀 Welcome to the SYNLAB Comprehensive Analytics Platform</h3>
    <p>Navigate through different sections using the sidebar to explore comprehensive insights about brand performance, customer behavior, and competitive positioning.</p>
    <p><strong>🌐 Global Filters Applied:</strong> All filters in the sidebar work across all pages</p>
</div>
""", unsafe_allow_html=True)

# COMPREHENSIVE TEXT SUMMARY OF ALL PAGES
st.markdown("---")
st.markdown("<h2 class='summary-header'>📋 COMPREHENSIVE DASHBOARD SUMMARY</h2>", unsafe_allow_html=True)

# Executive Summary Section
st.markdown("""
<div class="summary-section">
    <h3>📊 EXECUTIVE OVERVIEW</h3>
    <p><strong>Dataset Overview:</strong> 500 survey responses with comprehensive demographic and brand perception data</p>
    <p><strong>Key Metrics:</strong> Brand awareness, customer satisfaction, service quality ratings, competitive positioning</p>
    <p><strong>Primary Focus:</strong> SYNLAB brand performance across different customer segments and against key competitors</p>
    <p><strong>Data Collection:</strong> August 2024 survey covering various age groups, occupations, and familiarity levels</p>
</div>
""", unsafe_allow_html=True)

# Customer Insights Summary
st.markdown("""
<div class="summary-section">
    <h3>👥 CUSTOMER INSIGHTS</h3>
    <p><strong>Demographic Coverage:</strong> Comprehensive analysis across Age Groups, Occupations, Gender, and Geographic locations</p>
    <p><strong>Segmentation Analysis:</strong> Customer behavior patterns segmented by demographic factors and familiarity levels</p>
    <p><strong>Key Findings:</strong> Variations in brand perception and service expectations across different customer segments</p>
    <p><strong>Behavioral Patterns:</strong> Service usage frequency, preference drivers, and satisfaction drivers by segment</p>
</div>
""", unsafe_allow_html=True)

# Competitive Intelligence Summary
st.markdown("""
<div class="summary-section">
    <h3>⚔️ COMPETITIVE INTELLIGENCE</h3>
    <p><strong>Competitor Set:</strong> Analysis against 5 key competitor brands in the diagnostic services market</p>
    <p><strong>Market Positioning:</strong> SYNLAB's relative position in terms of brand awareness, preference, and perceived quality</p>
    <p><strong>Competitive Advantages:</strong> Identification of SYNLAB's strengths and weaknesses compared to competitors</p>
    <p><strong>Market Share Analysis:</strong> Customer preference distribution and brand switching behavior patterns</p>
</div>
""", unsafe_allow_html=True)

# Strategic Analytics Summary
st.markdown("""
<div class="summary-section">
    <h3>🚀 STRATEGIC ANALYTICS</h3>
    <p><strong>Service Gap Analysis:</strong> Identification of areas where SYNLAB meets or falls short of customer expectations</p>
    <p><strong>Improvement Opportunities:</strong> Prioritized list of service enhancements based on customer feedback</p>
    <p><strong>Strategic Recommendations:</strong> Data-driven insights for marketing, service delivery, and customer experience improvements</p>
    <p><strong>ROI Opportunities:</strong> Areas with highest potential for customer satisfaction and business growth impact</p>
</div>
""", unsafe_allow_html=True)

# Advanced Models Summary
st.markdown("""
<div class="summary-section">
    <h3>🔧 ADVANCED ANALYTICAL MODELS</h3>
    <p><strong>Predictive Analytics:</strong> Customer behavior forecasting and churn prediction models</p>
    <p><strong>Segmentation Models:</strong> Advanced clustering for customer persona development</p>
    <p><strong>Sentiment Analysis:</strong> Text analytics on open-ended responses for qualitative insights</p>
    <p><strong>Machine Learning Insights:</strong> Pattern recognition in customer preferences and service expectations</p>
</div>
""", unsafe_allow_html=True)

# Technical Implementation Summary
st.markdown("""
<div class="summary-section">
    <h3>🛠️ TECHNICAL IMPLEMENTATION</h3>
    <p><strong>Platform:</strong> Streamlit-based interactive dashboard with real-time filtering capabilities</p>
    <p><strong>Data Processing:</strong> Automated data cleaning, transformation, and augmentation pipelines</p>
    <p><strong>Visualization:</strong> Interactive charts, graphs, and metrics with drill-down capabilities</p>
    <p><strong>Global Filters:</strong> Consistent filtering across all analytical components for unified insights</p>
    <p><strong>Responsive Design:</strong> Mobile-friendly interface with optimized user experience</p>
</div>
""", unsafe_allow_html=True)

# Key Performance Indicators
st.markdown("""
<div class="summary-section">
    <h3>📈 KEY PERFORMANCE INDICATORS</h3>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
        <div>
            <h4>Brand Metrics</h4>
            <ul>
                <li>Brand Awareness Score</li>
                <li>Brand Preference Index</li>
                <li>Net Promoter Score (NPS)</li>
                <li>Customer Satisfaction (CSAT)</li>
            </ul>
        </div>
        <div>
            <h4>Service Metrics</h4>
            <ul>
                <li>Service Quality Ratings</li>
                <li>Turnaround Time Satisfaction</li>
                <li>Price Perception Score</li>
                <li>Recommendation Likelihood</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation guide
st.subheader("📖 Navigation Guide")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-card-light">
        <h4>📊 Executive Overview</h4>
        <p>High-level metrics and performance indicators</p>
    </div>
    
    <div class="custom-card-light">
        <h4>👥 Customer Insights</h4>
        <p>Demographic analysis and segmentation</p>
    </div>
    
    <div class="custom-card-light">
        <h4>⚔️ Competitive Intelligence</h4>
        <p>Market positioning and competitor analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card-light">
        <h4>🚀 Strategic Analytics</h4>
        <p>Service gaps and improvement opportunities</p>
    </div>
    
    <div class="custom-card-light">
        <h4>🔧 Advanced Models</h4>
        <p>Predictive analytics and machine learning insights</p>
    </div>
    
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Built by Ibraheem Alawode using Streamlit | For SYNLAB Nigeria Marketing Team</p>
    <p style="font-size: 0.8rem; opacity: 0.8;">
</div>
""", unsafe_allow_html=True)