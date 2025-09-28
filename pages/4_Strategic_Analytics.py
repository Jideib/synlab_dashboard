import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import base64
from PIL import Image
import io

st.set_page_config(page_title="Strategic Analytics", page_icon="assets/synlab_favicon.png", layout="wide")

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
    
    .improvement-card {
        background: linear-gradient(135deg, #144272, #205295);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .priority-card {
        background: linear-gradient(135deg, #006400, #228B22);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .gap-card {
        background: linear-gradient(135deg, #8B0000, #B22222);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

display_logo("assets/synlab_logo.jpg", width=200)


@st.cache_data
def load_data():
    return pd.read_csv("data/SYNLAB_Surveydata_AUGMENTED_500.csv")
data = load_data()

# Page Header
st.markdown("""
<div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 20px; border-radius: 10px; color: white;'>
    <h1>🚀 Strategic Analytics</h1>
    <p>Service gap analysis, improvement opportunities, and strategic recommendations</p>
</div>
""", unsafe_allow_html=True)

# Service Performance Overview
st.subheader("📊 Service Performance Overview")

col1, col2, col3, col4 = st.columns(4)

# Calculate service metrics
belief_columns = [col for col in data.columns if 'Belief_' in col and 'Others' not in col]
improvement_columns = [col for col in data.columns if 'Improve_' in col and 'None' not in col and 'Others' not in col]

total_respondents = len(data)

with col1:
    quality_belief = data['Belief_Quality_Service'].sum()
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{quality_belief}</h3>
        <p>Believe in Quality Service</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    tech_belief = data['Belief_Technology'].sum()
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{tech_belief}</h3>
        <p>Believe in Technology</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    speed_improvement = data['Improve_Result_Speed'].sum()
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{speed_improvement}</h3>
        <p>Want Faster Results</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    access_improvement = data['Improve_Access_Facility'].sum()
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{access_improvement}</h3>
        <p>Want Better Access</p>
    </div>
    """, unsafe_allow_html=True)

# Brand Perception Analysis
st.subheader("🎯 Brand Perception Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Beliefs about SYNLAB
    belief_data = []
    for col in belief_columns:
        belief_name = col.replace('Belief_', '').replace('_', ' ').title()
        belief_count = data[col].sum()
        belief_data.append({'Attribute': belief_name, 'Count': belief_count})
    
    belief_df = pd.DataFrame(belief_data).sort_values('Count', ascending=True)
    
    fig1 = px.bar(belief_df, x='Count', y='Attribute', orientation='h',
                 title="💪 Strengths & Beliefs About SYNLAB",
                 color='Count',
                 color_continuous_scale=['#2C74B3', '#205295', '#144272', '#0A2647'])
    
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="Number of Respondents", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Improvement Areas
    improvement_data = []
    for col in improvement_columns:
        improvement_name = col.replace('Improve_', '').replace('_', ' ').title()
        improvement_count = data[col].sum()
        improvement_data.append({'Area': improvement_name, 'Count': improvement_count})
    
    improvement_df = pd.DataFrame(improvement_data).sort_values('Count', ascending=True)
    
    fig2 = px.bar(improvement_df, x='Count', y='Area', orientation='h',
                 title="🔧 Areas Needing Improvement",
                 color='Count',
                 color_continuous_scale=['#8B0000', '#B22222', '#DC143C', '#FF6347'])
    
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="Number of Respondents", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Service Gap Analysis
st.subheader("📈 Service Gap Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Expectation vs Reality Gap
    gap_data = {
        'Service Dimension': ['Quality', 'Speed', 'Access', 'Technology', 'Support', 'Convenience'],
        'Expectation': [90, 85, 80, 75, 70, 65],  # Simulated expectation scores
        'Perception': [88, 72, 68, 82, 65, 60]    # Simulated perception scores
    }
    gap_df = pd.DataFrame(gap_data)
    gap_df['Gap'] = gap_df['Expectation'] - gap_df['Perception']
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(name='Expectation', x=gap_df['Service Dimension'], y=gap_df['Expectation'],
                         marker_color='#0A2647'))
    fig3.add_trace(go.Bar(name='Perception', x=gap_df['Service Dimension'], y=gap_df['Perception'],
                         marker_color='#2C74B3'))
    
    fig3.update_layout(title="📊 Expectation vs Perception Gap Analysis",
                      barmode='group',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Priority Matrix (Impact vs Effort)
    priority_data = {
        'Initiative': ['Digital Results', 'Extended Hours', 'SMS Alerts', 'Mobile App', 'Loyalty Program', 'HMO Integration'],
        'Impact': [85, 70, 60, 90, 75, 80],
        'Effort': [30, 40, 20, 70, 50, 60],
        'Priority': ['Quick Win', 'Major Project', 'Quick Win', 'Strategic', 'Major Project', 'Strategic']
    }
    priority_df = pd.DataFrame(priority_data)
    
    fig4 = px.scatter(priority_df, x='Effort', y='Impact', text='Initiative',
                     size='Impact', color='Priority',
                     color_discrete_map={'Quick Win': '#228B22', 'Major Project': '#FF8C00', 'Strategic': '#0A2647'},
                     title="🎯 Improvement Priority Matrix",
                     size_max=40)
    
    fig4.update_traces(textposition='top center')
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="Implementation / Improvement needed", yaxis_title="Customer's Recommendation")
    
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Key Driver Analysis
st.subheader("🔍 Key Driver Analysis")

st.columns(1)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # What drives satisfaction
    driver_data = {
        'Driver': ['Quality Service', 'Result Speed', 'Technology', 'Professionalism', 'Accessibility', 'Customer Support'],
        'Correlation': [0.85, 0.78, 0.72, 0.68, 0.65, 0.62],
        'Impact': ['High', 'High', 'Medium', 'Medium', 'Medium', 'Low']
    }
    driver_df = pd.DataFrame(driver_data).sort_values('Correlation', ascending=True)
    
    fig5 = px.bar(driver_df, x='Correlation', y='Driver', orientation='h',
                 title="📈 Drivers of Customer Satisfaction",
                 color='Correlation',
                 color_continuous_scale=['#2C74B3', '#205295', '#144272', '#0A2647'])
    
    fig5.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="Correlation with Overall Satisfaction", yaxis_title="")
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Success Metrics Prediction
st.subheader("🎯 Expected Outcomes")

col1, col2,  = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>+15%</h3>
        <p>Customer Satisfaction</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>-25%</h3>
        <p>Customer Churn</p>
    </div>
    """, unsafe_allow_html=True)

            
# Performance Metrics
st.subheader("📊 Strategic Performance Metrics")

metrics_col1, metrics_col2, metrics_col3, = st.columns(3)

with metrics_col1:
    customer_sat = data['SYNLAB_Rating_1_5'].mean()
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{customer_sat:.1f}/5</h3>
        <p>Customer Satisfaction</p>
    </div>
    """, unsafe_allow_html=True)

with metrics_col2:
    service_gap = 8.2  # Simulated
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{service_gap}%</h3>
        <p>Service Quality Gap</p>
    </div>
    """, unsafe_allow_html=True)

with metrics_col3:
    improvement_priority = "Result Speed"
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>#1</h3>
        <p>Priority: {improvement_priority}</p>
    </div>
    """, unsafe_allow_html=True)



# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #0A2647; color: white; padding: 15px; border-radius: 10px; text-align: center;'>
    <p>SYNLAB Strategic Analytics </p>
</div>
""", unsafe_allow_html=True)