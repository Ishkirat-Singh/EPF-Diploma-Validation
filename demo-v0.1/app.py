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

# --- Mock Data Generation ---
# Re-using the robust schema generation from previous step
def generate_mock_data():
    students = []
    majors = ["Généraliste", "Numérique", "Santé", "Aéronautique", "Structure & Matériaux"]
    
    for i in range(1, 41): # Increased sample size for Admin view
        student_id = f"EPF2025-{100+i}"
        latency_days = random.choice([0, 0, 1, 2, 7, 30]) 
        last_updated = datetime.now() - timedelta(days=latency_days)

        c_1a, c_2a, c_3a = 60, 60, 60
        c_4a = random.randint(40, 60)
        c_5a = random.randint(10, 30)
        
        c_s7 = c_4a // 2 + random.randint(-5, 5)
        c_s8 = c_4a - c_s7
        c_s9 = c_5a // 2 + random.randint(-2, 2)
        c_s10 = c_5a - c_s9
        
        # Ensure non-negative
        c_s7, c_s8, c_s9, c_s10 = max(0, c_s7), max(0, c_s8), max(0, c_s9), max(0, c_s10)
        
        # Total Real
        total_credits = c_1a + c_2a + c_3a + c_4a + c_5a

        english_score = random.randint(600, 990)
        internship_choice = random.choices(["Valid", "Ongoing", "Pending"], weights=[0.5, 0.3, 0.2])[0]
        
        comp_status = random.choices(["Acquired", "In Progress", "Incomplete"], weights=[0.6, 0.3, 0.1])[0]

        students.append({
            "Student_ID": student_id,
            "Full_Name": f"Student {i}",
            "Major": random.choice(majors),
            "Total_Credits": total_credits,
            
            # Academic Credits
            "Credits_1A": c_1a, "Credits_2A": c_2a, "Credits_3A": c_3a,
            "Credits_4A": c_4a, "Credits_5A": c_5a,
            
            # Semester Breakdown (for Heatmap)
            "S7": c_s7, "S8": c_s8, "S9": c_s9, "S10": c_s10,
            
            # Language
            "English_Score": english_score,
            "Voltaire_Status": random.choice(["Valid", "Exempt", "Invalid"]),
            
            # Internship
            "Internship_Status": internship_choice,
            "Internship_Start": datetime(2025, 2, 1) if internship_choice != "Pending" else None,
            "Internship_End": datetime(2025, 8, 30) if internship_choice != "Pending" else None,
            
            # Competencies
            "Competencies_Status": comp_status,
            "Last_Updated": last_updated
        })
    return pd.DataFrame(students)

if 'data' not in st.session_state:
    st.session_state.data = generate_mock_data()
df = st.session_state.data

# --- Visualizations ---

def plot_radial_progress(current, target=300):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Total ECTS Progress"},
        delta = {'reference': target},
        gauge = {
            'axis': {'range': [None, target]},
            'bar': {'color': "#004e92"},
            'steps': [{'range': [0, target], 'color': "lightgray"}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': target}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20,r=20,t=30,b=20))
    return fig

def plot_academic_stacked(row):
    years = ['1A', '2A', '3A', '4A', '5A']
    vals = [row[f'Credits_{y}'] for y in years]
    fig = go.Figure(go.Bar(x=years, y=vals, marker_color='#004e92'))
    fig.update_layout(title="Credits per Year", height=300)
    return fig

def plot_english_gauge(score):
    color = "#2ecc71" if score >= 785 else "#e74c3c"
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "TOEIC Score"},
        gauge = {
            'axis': {'range': [None, 990]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 785], 'color': "#fce4ec"},
                {'range': [785, 990], 'color': "#e8f5e9"}],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 785}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20,r=20,t=30,b=20))
    return fig

def plot_internship_timeline_gantt(row):
    if not row['Internship_Start']:
        return None
    df_g = pd.DataFrame([dict(Task="Stage", Start=row['Internship_Start'], Finish=row['Internship_End'])])
    fig = px.timeline(df_g, x_start="Start", x_end="Finish", y="Task", title="Internship Timeline")
    fig.update_yaxes(visible=False)
    fig.update_layout(height=150, margin=dict(l=20,r=20,t=30,b=20))
    return fig

def plot_radar_competencies(row_name, scores=[4,3,5,4,2]):
    cats = ['Technical', 'Management', 'Comms', 'Innovation', 'Ethics']
    fig = go.Figure(go.Scatterpolar(r=scores, theta=cats, fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Competency Profile", height=300)
    return fig

# --- ADMIN Aggregate Charts ---

def plot_admin_english_hist(df):
    fig = px.histogram(df, x="English_Score", nbins=20, title="Cohort English Scores", color_discrete_sequence=['#004e92'])
    fig.add_vline(x=785, line_width=3, line_dash="dash", line_color="red", annotation_text="Threshold")
    return fig

def plot_admin_internship_pie(df):
    fig = px.pie(df, names="Internship_Status", title="Internship Validation Status", hole=0.4)
    return fig

def plot_admin_credits_box(df):
    fig = px.box(df, y="Total_Credits", title="Cohort Credits Distribution")
    return fig

# --- MAIN APP LOGIC ---

st.sidebar.title("🔧 Dev Mode")
role = st.sidebar.radio("Select Role View:", ["Student", "Admin"])

# ----------------- STUDENT VIEW -----------------
if role == "Student":
    # Login Simulation
    st.sidebar.markdown("---")
    st.sidebar.header("👤 Login Simulation")
    selected_id = st.sidebar.selectbox("Select Student:", df['Student_ID'])
    student = df[df['Student_ID'] == selected_id].iloc[0]
    
    st.title(f"🎓 Student Portal: {student['Full_Name']}")
    st.caption(f"Major: {student['Major']} | ID: {student['Student_ID']}")
    
    # KPIs Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Status", "On Track" if student['Total_Credits'] > 280 else "Action Needed")
    
    # Traffic Light Logic for PFE
    pfe_light = "🟢 GO" if student['Internship_Status'] == "Valid" else "🔴 NO GO"
    if student['Internship_Status'] == "Ongoing": pfe_light = "🟡 PENDING"
    k2.metric("PFE Authorization", pfe_light)

    # Simple Badge for Voltaire
    volt_emoji = "✅" if student['Voltaire_Status'] == "Valid" else "❌"
    k3.metric("Voltaire", f"{volt_emoji} {student['Voltaire_Status']}")
    
    # Latency Helper
    days_ago = (datetime.now() - student['Last_Updated']).days
    k4.metric("Data Freshness", f"{days_ago} days ago", delta_color="inverse", delta=days_ago)

    st.divider()

    # --- TABS FOR DETAILED VISUALIZATIONS ---
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Academics", "🇬🇧 Languages", "💼 Internships", "🧠 Competencies"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(plot_radial_progress(student['Total_Credits']), use_container_width=True)
        with c2:
            st.plotly_chart(plot_academic_stacked(student), use_container_width=True)
        
        st.subheader("Semester Breakdown (Heatmap Style)")
        # Creating a mini heatmap dataframe just for this student
        sem_df = pd.DataFrame([
            {"Semester": "S7", "Credits": student['S7']},
            {"Semester": "S8", "Credits": student['S8']},
            {"Semester": "S9", "Credits": student['S9']},
            {"Semester": "S10", "Credits": student['S10']}
        ]).set_index("Semester").T
        
        st.dataframe(sem_df.style.background_gradient(cmap="RdYlGn", vmin=0, vmax=30), use_container_width=True)

    with tab2:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.plotly_chart(plot_english_gauge(student['English_Score']), use_container_width=True)
        with c2:
            st.info("The gauge indicates your TOEIC score relative to the 785 graduation threshold.")
            if student['English_Score'] < 785:
                st.error("⚠️ Remedial English modules required.")
            else:
                st.success("✅ Language requirement met.")

    with tab3:
        st.subheader("Professional Experience Validation")
        timeline = plot_internship_timeline_gantt(student)
        if timeline:
            st.plotly_chart(timeline, use_container_width=True)
        else:
            st.warning("No Internship Data Registered.")
        
        st.metric("Validation Status", student['Internship_Status'])

    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            # Random mock scores for the spider chart
            mock_scores = [random.randint(2,5) for _ in range(5)]
            st.plotly_chart(plot_radar_competencies(student['Full_Name'], mock_scores), use_container_width=True)
        with c2:
            st.write("### Competency Status")
            st.info(f"Global Status: {student['Competencies_Status']}")
            st.write("Check with your pedagogical supervisor for specific missing UEs.")

# ----------------- ADMIN VIEW -----------------
elif role == "Admin":
    st.title("📊 Administration Control Tower")
    st.info("Aggregate view of the entire student cohort.")
    
    # Global KPIs
    adm1, adm2, adm3 = st.columns(3)
    adm1.metric("Total Students", len(df))
    eligible_count = len(df[(df['Total_Credits'] >= 300) & (df['English_Score'] >= 785)])
    adm2.metric("Graduation Eligible", eligible_count, delta=f"{eligible_count/len(df)*100:.1f}%")
    adm3.metric("Pending Internships", len(df[df['Internship_Status'] != "Valid"]))
    
    st.divider()
    
    # Aggregate Visualizations
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Cohort English Proficiency")
        st.plotly_chart(plot_admin_english_hist(df), use_container_width=True)
        
    with col_b:
        st.subheader("2. Internship Status Distribution")
        st.plotly_chart(plot_admin_internship_pie(df), use_container_width=True)
        
    st.subheader("3. Academic Progress Distribution")
    st.plotly_chart(plot_admin_credits_box(df), use_container_width=True)
    
    st.subheader("4. Detailed Student List")
    st.dataframe(df.style.highlight_min(subset=["Total_Credits"], color="#ffcdd2"), use_container_width=True)
