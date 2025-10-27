# dashboard/app.py
import streamlit as st
import pandas as pd
from chatbot.llm_bot import get_ai_response  # Import your chatbot function

# --- App Config ---
st.set_page_config(
    page_title="Student Dropout Predictor Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Sidebar Navigation ---
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Dashboard", "👩‍🎓 Students List", "📊 Student Detail View", "⚙️ Simulation Panel", "🤖 Chatbot"]
)

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("D:/Programming/Hackathon/data/cleaned_data.csv")
        return df
    except FileNotFoundError:
        st.warning("⚠️ Cleaned data file not found. Please add 'cleaned_data.csv' in data/ folder.")
        return pd.DataFrame()

df = load_data()

# --- Pages ---
if page == "🏠 Dashboard":
    st.title("🎓 Student Dropout Predictor – Dashboard")
    st.write("Welcome to the Student Dropout Early Warning System.")
    st.markdown("""
    This dashboard provides insights into student performance, attendance, and predicted dropout risks.
    """)
    
    if not df.empty:
        st.subheader("📈 Dataset Overview")
        st.dataframe(df.head())
    else:
        st.info("Data will appear here once 'cleaned_data.csv' is available.")

elif page == "👩‍🎓 Students List":
    st.title("👩‍🎓 Students List")
    st.write("View all students and their risk status here.")
    
    if not df.empty:
        search = st.text_input("Search by Name or ID:")
        filtered_df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)] if search else df
        st.dataframe(filtered_df)
    else:
        st.info("Student list will load once dataset is available.")

elif page == "📊 Student Detail View":
    st.title("📊 Student Detail View")
    st.write("View individual student details and dropout prediction.")
    
    student_id = st.text_input("Enter Student ID:")
    if st.button("Get Details") and student_id:
        if not df.empty:
            student = df[df['student_id'].astype(str) == student_id]
            if not student.empty:
                st.dataframe(student)
                st.info("Predicted dropout risk will appear here once model is connected.")
            else:
                st.error("Student ID not found.")
        else:
            st.warning("Dataset not loaded.")

elif page == "⚙️ Simulation Panel":
    st.title("⚙️ Simulation Panel")
    st.write("Experiment with changes (like CGPA or Attendance) to see how dropout risk changes.")
    
    cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
    attendance = st.slider("Attendance (%)", 0, 100, 80)
    study_hours = st.slider("Study Hours/Week", 0, 50, 20)
    
    if st.button("Predict Risk"):
        st.info("Predicted dropout risk will appear here once model is connected.")

elif page == "🤖 Chatbot":
    st.title("🤖 Student Dropout Chatbot")
    st.write("Ask questions about the students and dropout predictions.")
    
    user_input = st.text_input("Type your question here:")
    if st.button("Ask") and user_input:
        response = get_ai_response(user_input)
        st.markdown(f"**AI Bot:** {response}")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Student Dropout Predictor")
