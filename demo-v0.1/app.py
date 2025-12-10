import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="EPF Validation Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Mock Data Generation (IT Schema View) ---
def generate_mock_data():
    students = []
    majors = ["Généraliste", "Numérique", "Santé", "Aéronautique", "Structure & Matériaux"]
    
    for i in range(1, 26):
        student_id = f"EPF2025-{100+i}"
        
        # Latency Simulation (Last fetch time)
        latency_days = random.choice([0, 1, 2, 7, 30]) 
        last_updated = datetime.now() - timedelta(days=latency_days)

        # Credits Breakdown
        c_1a = 60
        c_2a = 60
        c_3a = 60
        c_4a = random.randint(50, 60)
        c_5a = random.randint(10, 30)
        
        # Semester details (Mocking 4A/5A semesters)
        c_s7 = c_4a // 2 + random.randint(0, 5)
        c_s8 = c_4a - c_s7
        c_s9 = c_5a // 2 + random.randint(0, 2)
        c_s10 = c_5a - c_s9
        
        english_score = random.randint(700, 990)
        internship_choice = random.choice(["Valid", "Ongoing", "Pending"])
        
        # Competencies mock
        comp_status = random.choice(["Acquired", "In Progress", "Incomplete"])

        students.append({
            "Student_ID": student_id,
            "Full_Name": f"Student {i}",
            "Major": random.choice(majors),
            "Year_Level": "5A",
            
            # Academic Credits
            "Credits_1A": c_1a,
            "Credits_2A": c_2a,
            "Credits_3A": c_3a,
            "Credits_4A": c_4a,
            "Credits_5A": c_5a,
            "Credits_S7": c_s7,
            "Credits_S8": c_s8,
            "Credits_S9": c_s9,
            "Credits_S10": c_s10,
            
            # Language
            "English_Score": english_score,
            "Voltaire_Status": random.choice(["Valid", "Exempt", "Invalid"]),
            
            # Internship
            "Internship_Status": internship_choice,
            "Internship_Start": datetime(2025, 2, 1) if internship_choice != "Pending" else None,
            "Internship_End": datetime(2025, 8, 30) if internship_choice != "Pending" else None,
            
            # Competencies
            "Competencies_Status": comp_status,
            
            # System Info
            "Last_Updated": last_updated
        })
    return pd.DataFrame(students)

df = generate_mock_data()

# --- Visualizations ---

def plot_credits_stacked(student_row):
    """Stacked Bar Chart for Years"""
    years = ['1A', '2A', '3A', '4A', '5A']
    credits = [student_row[f'Credits_{y}'] for y in years]
    
    fig = go.Figure(data=[
        go.Bar(name='Credits', x=years, y=credits, marker_color='#004e92')
    ])
    fig.update_layout(title="Academic Progress (Yearly)", yaxis_title="Credits", yaxis_range=[0, 70])
    return fig

def plot_english_gauge(score):
    """Gauge Chart for TOEIC"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "TOEIC Score (Min 785)"},
        delta = {'reference': 785},
        gauge = {
            'axis': {'range': [None, 990]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 785], 'color': "lightgray"},
                {'range': [785, 990], 'color': "#2ecc71"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 785}}))
    fig.update_layout(height=300)
    return fig

def plot_internship_gantt(student_row):
    """Gantt Schema for Internship"""
    if not student_row['Internship_Start']:
        return None
        
    df_gantt = pd.DataFrame([
        dict(Task="Internship", Start=student_row['Internship_Start'], Finish=student_row['Internship_End'], Resource="Stage")
    ])
    
    fig = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Resource", title="Internship Timeline")
    fig.update_yaxes(visible=False)
    fig.update_layout(height=200)
    return fig

def plot_competencies_radar(student_row):
    """Radar Chart for Competencies"""
    categories = ['Technical', 'Management', 'Communication', 'Innovation', 'Ethics']
    # Mock scores for visualization
    r = [random.randint(3, 5) for _ in range(5)]
    
    fig = go.Figure(data=go.Scatterpolar(
      r=r,
      theta=categories,
      fill='toself',
      name=student_row['Full_Name']
    ))
    fig.update_layout(
      polar=dict(
        radialaxis=dict(visible=True, range=[0, 5])
      ),
      showlegend=False,
      title="Competency Profile"
    )
    return fig

# --- Layout ---

st.sidebar.title("🎓 EPF Validation")
page = st.sidebar.radio("Navigation", ["Dashboard", "Individual Review", "System Hygiene"])

if page == "Dashboard":
    st.title("📊 Global Validation Status")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df))
    col2.metric("Graduation Ready", len(df[df['English_Score']>=785]), delta="Est.")
    
    # Latency Warning
    stale_data = len(df[df['Last_Updated'] < datetime.now() - timedelta(days=7)])
    col3.metric("Records > 7 Days Old", stale_data, delta_color="inverse")
    
    st.dataframe(df, use_container_width=True)

elif page == "Individual Review":
    st.title("👤 Student Validation Profile")
    
    selected_id = st.selectbox("Search Student ID", df['Student_ID'])
    student = df[df['Student_ID'] == selected_id].iloc[0]
    
    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader(f"{student['Full_Name']} ({student['Major']})")
    with c2:
        # Latency Indicator
        days_ago = (datetime.now() - student['Last_Updated']).days
        color = "green" if days_ago < 7 else "orange"
        st.caption(f"Last Updated: {days_ago} days ago 🕒", help="Data source latency check")
        
    st.divider()
    
    # Row 1: Academics & Language
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("### 1. Academic Progress")
        st.plotly_chart(plot_credits_stacked(student), use_container_width=True)
        
    with col_b:
        st.write("### 2. Language Proficiency")
        st.plotly_chart(plot_english_gauge(student['English_Score']), use_container_width=True)
        st.info(f"Voltaire Status: {student['Voltaire_Status']}")

    st.divider()
    
    # Row 2: Internship & Competencies
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.write("### 3. Professional Experience")
        gantt = plot_internship_gantt(student)
        if gantt:
            st.plotly_chart(gantt, use_container_width=True)
        else:
            st.warning("No validated internship found.")
        st.caption("Status: " + student['Internship_Status'])
            
    with col_d:
        st.write("### 4. Competency Matrix")
        st.plotly_chart(plot_competencies_radar(student), use_container_width=True)

elif page == "System Hygiene":
    st.title("🛠️ IT & Data Health")
    st.info("This view monitors the connection with Phenix, CSM, and Language Databases.")
    
    st.table(pd.DataFrame({
        "Source": ["Phenix (ERP)", "Internship DB", "Language Svc"],
        "Status": ["🟢 Connected", "🟢 Connected", "🟡 Latency > 5d"],
        "Last Sync": [datetime.now(), datetime.now(), datetime.now() - timedelta(days=6)]
    }))
