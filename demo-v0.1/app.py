import streamlit as st
import pandas as pd
import random

# Page Configuration
st.set_page_config(
    page_title="EPF Diploma Validation Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Mock Data Generation ---
def generate_mock_data():
    students = []
    for i in range(1, 21):
        student_id = f"EPF2025-{100+i}"
        name = f"Student {i}"
        program = random.choice(["Généraliste", "Filière Numérique", "Filière Santé"])
        
        # Credits (Goal: 180)
        credits_1a_3a = 60 + 60 + 60 # Assuming full success for earlier years for simplicity
        credits_4a = random.randint(50, 60)
        credits_5a = random.randint(20, 30)
        total_credits = credits_1a_3a + credits_4a + credits_5a
        
        # Validation Criteria
        english_score = random.randint(700, 990)
        english_valid = english_score >= 785
        
        internship_valid = random.choice([True, False])
        
        competencies_valid = random.choice([True, True, False]) # Higher chance of being valid
        
        diploma_eligible = (total_credits >= 300) and english_valid and internship_valid and competencies_valid
        # Note: 300 is total for 5 years (60*5). 180 is usually for the engineering cycle (last 3 years) or similar. 
        # Let's assume 180 for the cycle ingénieur for this demo visualization.
        cycle_credits = credits_4a + credits_5a + 60 # Mocking 3rd year as 60
        
        students.append({
            "Student_ID": student_id,
            "Name": name,
            "Program": program,
            "Total_Credits": total_credits,
            "Cycle_Ing_Credits": cycle_credits,
            "English_Score": english_score,
            "English_Valid": english_valid,
            "Internship_Valid": internship_valid,
            "Competencies_Valid": competencies_valid,
            "Diploma_Eligible": diploma_eligible
        })
    return pd.DataFrame(students)

df = generate_mock_data()

# --- Sidebar ---
st.sidebar.title("🎓 EPF Validation")
page = st.sidebar.radio("Navigation", ["Dashboard Overview", "Student Details", "Data Sources"])

st.sidebar.markdown("---")
st.sidebar.info("MVP Demo v0.1")

# --- Dashboard Overview ---
if page == "Dashboard Overview":
    st.title("📊 Diploma Validation Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        eligible = df[df['Diploma_Eligible']].shape[0]
        st.metric("Diploma Eligible", eligible, delta=f"{eligible/len(df)*100:.1f}%")
    with col3:
        pending_english = df[~df['English_Valid']].shape[0]
        st.metric("Pending English", pending_english, delta_color="inverse")
    with col4:
        pending_internship = df[~df['Internship_Valid']].shape[0]
        st.metric("Pending Internship", pending_internship, delta_color="inverse")
    
    st.markdown("### 📉 Global Progress")
    st.bar_chart(df.set_index("Name")["Cycle_Ing_Credits"])
    
    st.markdown("### 📋 Student List")
    st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'), use_container_width=True)

# --- Student Details ---
elif page == "Student Details":
    st.title("👤 Student Profile")
    
    selected_student_id = st.selectbox("Select Student", df['Student_ID'])
    student = df[df['Student_ID'] == selected_student_id].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(student['Name'])
        st.text(f"ID: {student['Student_ID']}")
        st.text(f"Program: {student['Program']}")
        
        if student['Diploma_Eligible']:
            st.success("✅ DIPLOMA ELIGIBLE")
        else:
            st.warning("⚠️ ACTION REQUIRED")
            
    with col2:
        st.subheader("Validation Criteria")
        
        # Credits Progress
        st.write(f"**Credits (Cycle Ingénieur):** {student['Cycle_Ing_Credits']} / 180")
        st.progress(min(student['Cycle_Ing_Credits'] / 180, 1.0))
        
        # Status Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("English Score", student['English_Score'], delta="Valid" if student['English_Valid'] else "Fail")
        with c2:
            st.metric("Internship", "Valid" if student['Internship_Valid'] else "Pending")
        with c3:
            st.metric("Competencies", "Acquired" if student['Competencies_Valid'] else "In Progress")

    st.markdown("### 📝 Detailed Modules (Mock)")
    # Mock detailed grades for this student
    modules = [
        {"Module": "Data Science", "Credits": 4, "Grade": random.randint(10, 20)},
        {"Module": "Web Development", "Credits": 4, "Grade": random.randint(10, 20)},
        {"Module": "Management", "Credits": 2, "Grade": random.randint(8, 18)},
        {"Module": "English", "Credits": 2, "Grade": random.randint(12, 18)},
        {"Module": "PFE", "Credits": 30, "Grade": "Pending" if not student['Internship_Valid'] else random.randint(14, 20)},
    ]
    st.table(pd.DataFrame(modules))

# --- Data Sources ---
elif page == "Data Sources":
    st.title("🗄️ Data Sources Integration")
    st.markdown("""
    This system integrates data from the following sources:
    
    | Source | Type | Update Frequency | Status |
    | :--- | :--- | :--- | :--- |
    | **Diploma Services** | Excel / Phenix | Continuous | 🟢 Connected |
    | **Language Services** | CSV Export | Monthly | 🟢 Connected |
    | **Internship Services** | API / Excel | Weekly | 🟡 Partial |
    | **International** | Excel | On Demand | 🔴 Pending |
    """)
    
    st.info("Data ingestion pipelines are currently being configured.")
