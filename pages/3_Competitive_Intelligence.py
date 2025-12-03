import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import base64
from PIL import Image
import io

st.set_page_config(page_title="Competitive Intelligence", page_icon="assets/synlab_favicon.png", layout="wide")

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
    
    .competitor-card {
        background: linear-gradient(135deg, #144272, #205295);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .threat-card {
        background: linear-gradient(135deg, #8B0000, #B22222);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .opportunity-card {
        background: linear-gradient(135deg, #006400, #228B22);
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
    <h1>⚔️ Competitive Intelligence</h1>
    <p>Market positioning, competitor analysis, and strategic insights</p>
</div>
""", unsafe_allow_html=True)

# Competitive Landscape Overview
st.subheader("🏆 Competitive Landscape")

col1, col2, col3, col4, col5 = st.columns(5)

# Calculate competitive metrics
labs = ['SYNLAB', 'Clinix', 'Mecure', 'Clina Lancet', 'Afriglobal']
awareness_rates = []
usage_rates = []

for lab in labs:
    heard_col = f'Heard_{lab.replace(" ", "_")}'
    used_col = f'Used_{lab.replace(" ", "_")}'
    
    awareness = (data[heard_col].sum() / len(data)) * 100
    usage = (data[used_col].sum() / len(data)) * 100
    
    awareness_rates.append(awareness)
    usage_rates.append(usage)

for i, lab in enumerate(labs):
    with [col1, col2, col3, col4, col5][i]:
        st.markdown(f"""
        <div class="metric-highlight">
            <h3>{awareness_rates[i]:.1f}%</h3>
            <p>{lab} Awareness</p>
        </div>
        """, unsafe_allow_html=True)

# Market Share Analysis
st.subheader("📊 Market Share Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Awareness Market Share
    awareness_df = pd.DataFrame({'Lab': labs, 'Awareness': awareness_rates})
    fig1 = px.pie(awareness_df, values='Awareness', names='Lab',
                 title="🎯 Brand Awareness Market Share",
                 color_discrete_sequence=['#0A2647', '#144272', '#205295', '#2C74B3', '#F8F9FA'])
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Usage Market Share
    usage_df = pd.DataFrame({'Lab': labs, 'Usage': usage_rates})
    fig2 = px.bar(usage_df, x='Lab', y='Usage',
                 title="📈 Laboratory Usage Rates",
                 color='Usage',
                 color_continuous_scale=['#2C74B3', '#205295', '#144272', '#0A2647'])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     xaxis_title="", yaxis_title="Usage Rate (%)")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Competitive Positioning
st.subheader("🎯 Competitive Positioning")

col1, col2 = st.columns(2)

#Awareness vs Usage line  code with this:

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Create line chart for Awareness vs Usage
    positioning_df = pd.DataFrame({
        'Lab': labs,
        'Awareness': awareness_rates,
        'Usage': usage_rates
    })

    # Sort by Awareness for better line visualization
    positioning_df = positioning_df.sort_values('Awareness')

    fig3 = go.Figure()

    # Add grid lines for better readability
    for y in [10, 20, 30, 40, 50]:
        fig3.add_hline(y=y, line=dict(color="rgba(128, 128, 128, 0.2)", width=1, dash="dash"))
    for x in [20, 30, 40, 50]:
        fig3.add_vline(x=x, line=dict(color="rgba(128, 128, 128, 0.2)", width=1, dash="dash"))

    # Add Usage line (Primary metric from screenshot)
    fig3.add_trace(go.Scatter(
        x=positioning_df['Awareness'],
        y=positioning_df['Usage'],
        mode='lines+markers+text',
        text=positioning_df['Lab'],
        textposition="top center",
        name='Usage Rate (%)',
        line=dict(color='#0A2647', width=3),
        marker=dict(size=12, color='#0A2647', symbol='circle'),
        hovertemplate='<b>%{text}</b><br>Awareness: %{x:.1f}%<br>Usage: %{y:.1f}%<extra></extra>'
    ))

    # Highlight specific competitors as shown in screenshot
    # Add special markers for key competitors
    competitors_to_highlight = {
        'Clinix': {'color': '#8B0000', 'symbol': 'square'},
        'Mecure': {'color': '#205295', 'symbol': 'diamond'},
        'Clina Lancet': {'color': '#2C74B3', 'symbol': 'star'},
        'Afriglobal': {'color': '#32CD32', 'symbol': 'triangle-up'}
    }

    for lab, style in competitors_to_highlight.items():
        if lab in positioning_df['Lab'].values:
            lab_data = positioning_df[positioning_df['Lab'] == lab].iloc[0]
            fig3.add_trace(go.Scatter(
                x=[lab_data['Awareness']],
                y=[lab_data['Usage']],
                mode='markers',
                marker=dict(
                    size=20,
                    color=style['color'],
                    symbol=style['symbol'],
                    line=dict(width=2, color='white')
                ),
                name=lab,
                showlegend=False,
                hovertemplate=f'<b>{lab}</b><br>Awareness: %{{x:.1f}}%<br>Usage: %{{y:.1f}}%<extra></extra>'
            ))

    # Add SYNLAB with special styling
    synlab_data = positioning_df[positioning_df['Lab'] == 'SYNLAB']
    if not synlab_data.empty:
        synlab_data = synlab_data.iloc[0]
        fig3.add_trace(go.Scatter(
            x=[synlab_data['Awareness']],
            y=[synlab_data['Usage']],
            mode='markers',
            marker=dict(
                size=25,
                color='#FFD700',  # Gold color for market leader
                symbol='star',
                line=dict(width=3, color='#FF4500')
            ),
            name='SYNLAB (Market Leader)',
            hovertemplate='<b>SYNLAB (Market Leader)</b><br>Awareness: %{x:.1f}%<br>Usage: %{y:.1f}%<extra></extra>'
        ))

    # Update layout to match screenshot style
    fig3.update_layout(
        title="🎯 Awareness vs Usage Positioning",
        xaxis=dict(
            title="Awareness Rate (%)",
            range=[15, 55],
            tickmode='linear',
            tick0=20,
            dtick=10,
            gridcolor='rgba(128, 128, 128, 0.1)'
        ),
        yaxis=dict(
            title="Usage Rate (%)",
            range=[15, 35],
            tickmode='linear',
            tick0=15,
            dtick=5,
            gridcolor='rgba(128, 128, 128, 0.1)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        hovermode='closest',
        margin=dict(t=50, l=50, r=50, b=50)
    )

    # Add quadrant lines at the median
    median_awareness = positioning_df['Awareness'].median()
    median_usage = positioning_df['Usage'].median()

    fig3.add_shape(
        type="line",
        x0=median_awareness, y0=15,
        x1=median_awareness, y1=35,
        line=dict(color="rgba(0, 0, 0, 0.3)", width=1, dash="dot")
    )

    fig3.add_shape(
        type="line",
        x0=15, y0=median_usage,
        x1=55, y1=median_usage,
        line=dict(color="rgba(0, 0, 0, 0.3)", width=1, dash="dot")
    )

    # Add quadrant labels
    fig3.add_annotation(
        x=25, y=32,
        text="High Awareness, low Usage",
        showarrow=False,
        font=dict(size=10, color="orange")
    )

    fig3.add_annotation(
        x=45, y=18,
        text="High Awareness, High Usage",
        showarrow=False,
        font=dict(size=10, color="green")
    )

    fig3.add_annotation(
        x=25, y=18,
        text="Low Awareness, Low Usage",
        showarrow=False,
        font=dict(size=10, color="red")
    )

    fig3.add_annotation(
        x=45, y=32,
        text="Low Awareness, High Usage",
        showarrow=False,
        font=dict(size=10, color="blue")
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Market Share Trends (simulated)
    segments = ['Youth', 'Professionals', 'Seniors', 'Healthcare']
    synlab_share = [45, 38, 52, 60]
    clinix_share = [35, 42, 30, 25]
    
    fig4 = go.Figure()
    
    fig4.add_trace(go.Scatter(x=segments, y=synlab_share, mode='lines+markers',
                            name='SYNLAB', line=dict(color='#0A2647', width=3)))
    fig4.add_trace(go.Scatter(x=segments, y=clinix_share, mode='lines+markers',
                            name='Clinix', line=dict(color='#8B0000', width=3)))
    
    fig4.update_layout(title="📊 Market Share by Segment",
                      xaxis_title="Customer Segment",
                      yaxis_title="Market Share (%)",
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Competitive Threat Assessment
st.subheader("⚠️ Threat Assessment")

# Calculate threat scores (simplified)
threat_scores = {}
for lab in labs[1:]:  # Exclude SYNLAB
    heard_col = f'Heard_{lab.replace(" ", "_")}'
    used_col = f'Used_{lab.replace(" ", "_")}'
    
    # Threat Score
    awareness = awareness_rates[labs.index(lab)]
    usage = usage_rates[labs.index(lab)]

    # FORMULA: 50% Usage + 50% Awareness
    raw_threat = (0.5 * usage) + (0.5 * awareness)

    # Convert to 0-1 scale
    normalized = raw_threat / 100

    # Scale to 3-10 range
    threat_score = 3 + (normalized * 7)
    threat_score[lab] = threat_score

# Display threat assessment
col1, col2, col3, col4 = st.columns(4)

for i, (lab, score) in enumerate(list(threat_scores.items())[:4]):
    with [col1, col2, col3, col4][i]:
        threat_level = "High" if score > 9 else "Medium" if score > 5 else "Low"
        color = "#B22222" if threat_level == "High" else "#FF8C00" if threat_level == "Medium" else "#32CD32"
        
        st.markdown(f"""
        <div class="threat-card">
            <h4>{lab}</h4>
            <h3>{score:.1f}</h3>
            <p>Threat Score: {threat_level}</p>
        </div>
        """, unsafe_allow_html=True)

# Competitive Health Score
st.subheader("❤️ Competitive Health Score")

# Calculate competitive health metrics - FIXED VERSION
avg_rating = data['SYNLAB_Rating_1_5'].mean()  # Add this line

synlab_health = (
    (awareness_rates[0] / 100) * 0.3 +  # Awareness weight
    (usage_rates[0] / 100) * 0.4 +      # Usage weight  
    (avg_rating / 5) * 0.3              # Quality weight
) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    health_color = "#228B22" if synlab_health >= 70 else "#FF8C00" if synlab_health >= 50 else "#B22222"
    st.markdown(f"""
    <div class="metric-highlight" style="background: linear-gradient(135deg, {health_color}, {health_color}dd);">
        <h3>{synlab_health:.0f}/100</h3>
        <p>SYNLAB Health Score</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Market Leadership Gap
    competitor_scores = []
    for i in range(1, len(labs)):
        # Estimate competitor ratings (using SYNLAB rating as baseline with some variation)
        comp_rating = max(1, min(5, avg_rating + np.random.uniform(-0.5, 0.3)))
        comp_score = (awareness_rates[i] / 100 * 0.3 + usage_rates[i] / 100 * 0.4 + (comp_rating / 5) * 0.3) * 100
        competitor_scores.append(comp_score)
    
    leader_gap = synlab_health - max(competitor_scores) if competitor_scores else 0
    gap_color = "#228B22" if leader_gap > 10 else "#FF8C00" if leader_gap > 0 else "#B22222"
    st.markdown(f"""
    <div class="metric-highlight" style="background: linear-gradient(135deg, {gap_color}, {gap_color}dd);">
        <h3>+{leader_gap:.0f}</h3>
        <p>Leadership Gap</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Market Stability
    stability = 100 - (max(threat_scores.values()) if threat_scores else 0)
    stability_color = "#228B22" if stability >= 80 else "#FF8C00" if stability >= 60 else "#B22222"
    st.markdown(f"""
    <div class="metric-highlight" style="background: linear-gradient(135deg, {stability_color}, {stability_color}dd);">
        <h3>{stability:.0f}%</h3>
        <p>Market Stability</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Growth Potential
    growth_potential = (100 - awareness_rates[0]) * (usage_rates[0] / 100)
    growth_color = "#228B22" if growth_potential >= 20 else "#FF8C00" if growth_potential >= 10 else "#B22222"
    st.markdown(f"""
    <div class="metric-highlight" style="background: linear-gradient(135deg, {growth_color}, {growth_color}dd);">
        <h3>{growth_potential:.0f}%</h3>
        <p>Growth Potential</p>
    </div>
    """, unsafe_allow_html=True)

# Add a health score explanation
st.markdown("""
<div style='background: linear-gradient(135deg, #0A2647, #144272); padding: 15px; border-radius: 10px; color: white; margin: 10px 0;'>
    <h4>📊 Health Score Components</h4>
    <p><strong>Formula:</strong> (Awareness × 30%) + (Usage × 40%) + (Quality × 30%)</p>
    <p><strong>Rating Scale:</strong> 🟢 70-100 (Excellent) | 🟡 50-69 (Good) | 🔴 0-49 (Needs Improvement)</p>
</div>
""", unsafe_allow_html=True)

# SWOT Analysis
st.subheader("🔍 SWOT Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="competitor-card">
        <h4>💪 STRENGTHS</h4>
        <ul>
            <li>Highest brand awareness in market</li>
            <li>Strong perception of quality service</li>
            <li>Loyal customer base among healthcare professionals</li>
            <li>Good geographic coverage</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="threat-card">
        <h4>⚠️ THREATS</h4>
        <ul>
            <li>Clinix gaining traction among professionals</li>
            <li>Price sensitivity in certain segments</li>
            <li>New market entrants with digital focus</li>
            <li>Changing customer preferences</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="opportunity-card">
        <h4>🎯 OPPORTUNITIES</h4>
        <ul>
            <li>Underpenetrated youth market</li>
            <li>Digital service expansion</li>
            <li>Partnerships with healthcare providers</li>
            <li>Service line diversification</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="competitor-card" style="background: linear-gradient(135deg, #8B0000, #B22222);">
        <h4>🔴 WEAKNESSES</h4>
        <ul>
            <li>Lower usage rate compared to awareness</li>
            <li>Perception of being more expensive</li>
            <li>Slower result delivery concerns</li>
            <li>Limited digital presence</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Competitive Recommendations
st.subheader("🚀 Strategic Recommendations")

st.markdown("""
    <div class="competitor-card">
        <h4>🎯 Immediate Actions</h4>
        <ul>
            <li>Target Clinix's professional segment</li>
            <li>Enhance customer support</li>
            <li>Expand to underserved geographic areas</li>
            <li>Develop youth-focused marketing</li>
            <li>Strengthen HMO partnerships</li>
            <li>Introduce loyalty program</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)



# Competitive Intelligence Metrics
st.subheader("📈 Competitive Metrics Dashboard")

metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    # Market Position Index
    synlab_position = (awareness_rates[0] + usage_rates[0]) / 2
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{synlab_position:.1f}</h3>
        <p>Market Position Index</p>
    </div>
    """, unsafe_allow_html=True)

with metrics_col2:
    # Competitive Gap
    largest_competitor_gap = max(awareness_rates[1:])
    gap = awareness_rates[0] - largest_competitor_gap
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>+{gap:.1f}%</h3>
        <p>Awareness Lead vs Top Competitor</p>
    </div>
    """, unsafe_allow_html=True)

with metrics_col3:
    # Threat Level
    max_threat = max(threat_scores.values())
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{max_threat:.1f}</h3>
        <p>Highest Competitor Threat Score</p>
    </div>
    """, unsafe_allow_html=True)

with metrics_col4:
    # Market Share Stability
    share_stability = 85  # Simulated metric
    st.markdown(f"""
    <div class="metric-highlight">
        <h3>{share_stability}%</h3>
        <p>Market Share Stability</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #0A2647; color: white; padding: 15px; border-radius: 10px; text-align: center;'>
    <p>SYNLAB Competitive Intelligence •</p>
</div>
""", unsafe_allow_html=True)
