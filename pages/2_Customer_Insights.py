import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
from PIL import Image
import io

st.set_page_config(page_title="Customer Insights", page_icon="assets/synlab_favicon.png", layout="wide")

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

# Custom CSS for Navy Blue Theme
st.markdown("""
<style>
    .chart-container {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #0A2647;
        margin: 10px 0;
    }
    
    .metric-highlight {
        background: linear-gradient(135deg, #205295, #2C74B3);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #144272, #205295);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .segment-explanation {
        background: linear-gradient(135deg, #0A2647, #144272);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #2C74B3;
    }
    
    .champion-card {
        background: linear-gradient(135deg, #006400, #228B22);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .at-risk-card {
        background: linear-gradient(135deg, #8B0000, #B22222);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .new-user-card {
        background: linear-gradient(135deg, #205295, #2C74B3);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .prospect-card {
        background: linear-gradient(135deg, #FF8C00, #FFA500);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

display_logo("assets/synlab_logo.jpg", width=200)

@st.cache_data
def load_data():
    return pd.read_csv("data/SYNLAB_Surveydata_AUGMENTED_500.csv")
filtered_data = load_data()

# Page Header
st.markdown("""
<div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 20px; border-radius: 10px; color: white;'>
    <h1>👥 Customer Insights</h1>
    <p>Deep dive into customer demographics, segments, and behaviors</p>
</div>
""", unsafe_allow_html=True)



# Create customer segments
def create_segments(data):
    conditions = [
        (data['Familiarity_Score'] >= 2.5) & (data['SYNLAB_Rating_1_5'] >= 4) & (data['Used_SYNLAB'] == True),
        (data['Familiarity_Score'] >= 2.5) & (data['SYNLAB_Rating_1_5'] < 4) & (data['Used_SYNLAB'] == True),
        (data['Familiarity_Score'] < 2.5) & (data['Used_SYNLAB'] == True),
        (data['Familiarity_Score'] < 2.5) & (data['Used_SYNLAB'] == False) & (data['Heard_SYNLAB'] == True)
    ]
    choices = ['Champions', 'At Risk', 'New Users', 'Prospects']
    return np.select(conditions, choices, default='Others')

filtered_data['Segment'] = create_segments(filtered_data)

# Customer Segments KPI with explanations
st.subheader("🎯 Customer Segments Overview")

col1, col2, col3, col4 = st.columns(4)

segment_percentages = (filtered_data['Segment'].value_counts(normalize=True) * 100).round(1)

with col1:
    if 'Champions' in segment_percentages:
        st.metric("Champions", f"{segment_percentages['Champions']}%")
    else:
        st.metric("Champions", "0%")
    st.markdown(f"""
    <div class="metric-highlight">
        <h3><p>🏆 Champions</p></h3>   
    </div>
    """, unsafe_allow_html=True)

with col2:
    if 'At Risk' in segment_percentages:
        st.metric("At Risk", f"{segment_percentages['At Risk']}%")
    else:
        st.metric("At Risk", "0%")
    st.markdown(f"""
    <div class="metric-highlight">
        <h3><p>⚠️ At Risk</p></h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if 'New Users' in segment_percentages:
        st.metric("New Users", f"{segment_percentages['New Users']}%")
    else:
        st.metric("New Users", "0%")
    st.markdown(f"""
    <div class="metric-highlight">
        <h3><p>🆕 New Users</p></h3>   
    </div>
    """, unsafe_allow_html=True)

with col4:
    if 'Prospects' in segment_percentages:
        st.metric("Prospects", f"{segment_percentages['Prospects']}%")
    else:
        st.metric("Prospects", "0%")
    st.markdown(f"""
    <div class="metric-highlight">
        <h3><p>🎯 Prospects</p></h3>
    </div>
    """, unsafe_allow_html=True)

# Segment Explanations
st.subheader("📖 Customer Segment Definitions")

exp_col1, exp_col2 = st.columns(2)

with exp_col1:
    st.markdown("""
    <div class="champion-card">
        <h4>🏆 Champions</h4>
        <p><strong>Highly familiar + High ratings + Active users</strong></p>
        <p>• Very familiar with SYNLAB</p>
        <p>• Give ratings of 4-5 stars</p>
        <p>• Actively use SYNLAB services</p>
        <p>• Strong brand advocates</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="new-user-card">
        <h4>🆕 New Users</h4>
        <p><strong>Low familiarity + Active users</strong></p>
        <p>• Recently started using SYNLAB</p>
        <p>• Still building familiarity</p>
        <p>• Need onboarding support</p>
        <p>• High potential for loyalty</p>
    </div>
    """, unsafe_allow_html=True)

with exp_col2:
    st.markdown("""
    <div class="at-risk-card">
        <h4>⚠️ At Risk</h4>
        <p><strong>Highly familiar + Low ratings + Active users</strong></p>
        <p>• Know SYNLAB well but dissatisfied</p>
        <p>• Give ratings below 4 stars</p>
        <p>• High risk of churn</p>
        <p>• Need immediate attention</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="prospect-card">
        <h4>🎯 Prospects</h4>
        <p><strong>Low familiarity + Not yet users</strong></p>
        <p>• Aware of SYNLAB but haven't used</p>
        <p>• Need conversion strategies</p>
        <p>• Potential for growth</p>
        <p>• Target for acquisition campaigns</p>
    </div>
    """, unsafe_allow_html=True)

# Customer Segmentation Analysis
st.subheader("📊 Customer Segmentation Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig4 = px.pie(values=segment_percentages.values, names=segment_percentages.index, 
                 title="🎪 Customer Segments Distribution",
                 color_discrete_sequence=['#0A2647', '#144272', '#205295', '#2C74B3', '#F8F9FA'])
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Segment characteristics
    segment_stats = filtered_data.groupby('Segment').agg({
        'SYNLAB_Rating_1_5': 'mean',
        'Likelihood_to_Recommend': 'mean',
        'Total_Labs_Used': 'mean',
        'Familiarity_Score': 'mean'
    }).round(2)
    
   # Style the dataframe
    st.markdown("**📈 Segment Characteristics**")
    
    # Apply color coding to the dataframe
    def color_segment_rows(val):
        if val.name == 'Champions':
            return ['background-color: #228B22; color: white;'] * len(val)
        elif val.name == 'At Risk':
            return ['background-color: #B22222; color: white;'] * len(val)
        elif val.name == 'New Users':
            return ['background-color: #205295; color: white;'] * len(val)
        elif val.name == 'Prospects':
            return ['background-color: #FF8C00; color: white;'] * len(val)
        else:
            return ['background-color: #F8F9FA;'] * len(val)
    
    styled_df = segment_stats.style.apply(color_segment_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Demographic Distribution
st.subheader("📋 Demographic Distribution")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    age_counts = filtered_data['Age_Group'].value_counts()
    fig1 = px.pie(values=age_counts.values, names=age_counts.index, 
                 title="👥 Age Distribution",
                 color_discrete_sequence=['#0A2647', '#144272', '#205295', '#2C74B3'])
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    gender_counts = filtered_data['Gender'].value_counts()
    fig2 = px.bar(x=gender_counts.index, y=gender_counts.values, 
                 title="🚻 Gender Distribution",
                 color_discrete_sequence=['#205295'])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    occupation_counts = filtered_data['Occupation'].value_counts().head(8)
    fig3 = px.bar(x=occupation_counts.values, y=occupation_counts.index, 
                 title="💼 Top Occupations", orientation='h',
                 color_discrete_sequence=['#2C74B3'])
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="Count", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Geographic Distribution (if available)
if 'Latitude' in filtered_data.columns and 'Longitude' in filtered_data.columns:
    st.subheader("🗺️ Geographic Distribution")
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Simple scatter map with theme colors
    fig7 = px.scatter_mapbox(filtered_data, 
                           lat="Latitude", lon="Longitude",
                           color="Segment",
                           color_discrete_sequence=['#0A2647', '#144272', '#205295', '#2C74B3'],
                           size_max=15,
                           zoom=10,
                           title="📍 Customer Distribution by Segment")
    fig7.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="insight-card">
        <h4>🗺️ Location Data</h4>
        <p>Geographic coordinates not available in current dataset</p>
    </div>
    """, unsafe_allow_html=True)

# Key Insights
st.subheader("💡 Customer Insights")

col1, col2 = st.columns(2)

with col1:
    # Top performing segment
    best_segment = segment_stats['SYNLAB_Rating_1_5'].idxmax()
    best_rating = segment_stats['SYNLAB_Rating_1_5'].max()
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🏆 Best Performing Segment</h4>
        <p><strong>{best_segment}</strong> with average rating of <strong>{best_rating}/5</strong></p>
        <p>Focus retention strategies on this group</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gender insights
    gender_rating = filtered_data.groupby('Gender')['SYNLAB_Rating_1_5'].mean()
    highest_gender = gender_rating.idxmax()
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🚻 Gender Performance</h4>
        <p><strong>{highest_gender}</strong> respondents give highest average ratings</p>
        <p>Consider gender-specific messaging</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Age group insights
    age_usage = filtered_data.groupby('Age_Group')['Used_SYNLAB'].mean() * 100
    highest_usage_age = age_usage.idxmax()
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>👥 Age Group Engagement</h4>
        <p><strong>{highest_usage_age}</strong> has highest usage rate at <strong>{age_usage[highest_usage_age]:.1f}%</strong></p>
        <p>Target acquisition in other age groups</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Occupation insights
    occ_awareness = filtered_data.groupby('Occupation')['Heard_SYNLAB'].mean().sort_values(ascending=False).head(1)
    top_occ = occ_awareness.index[0]
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>💼 Occupation Awareness</h4>
        <p><strong>{top_occ}</strong> shows highest brand awareness</p>
        <p>Leverage for referral programs</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #0A2647; color: white; padding: 15px; border-radius: 10px; text-align: center;'>
    <p>SYNLAB Customer Insights • Advanced Segmentation</p>
</div>
""", unsafe_allow_html=True)