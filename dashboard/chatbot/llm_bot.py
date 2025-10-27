# dashboard/chatbot/llm_bot.py

from transformers import pipeline
import pandas as pd

# --- Load Dataset ---
try:
    df = pd.read_csv("D:/Programming/Hackathon/data/cleaned_data.csv")
except FileNotFoundError:
    df = pd.DataFrame()

# --- Initialize GPT-2 Generator ---
generator = pipeline(
    "text-generation",
    model="gpt2"
)

# --- Chatbot Function ---
def get_ai_response(user_input):
    user_input_lower = user_input.lower()

    # --- Check dataset first ---
    if not df.empty:
        # High risk / dropout count
        if any(word in user_input_lower for word in ["high risk", "students at risk", "dropout count"]):
            if 'dropout' in df.columns:
                high_risk_count = df[df['dropout'] == 1].shape[0]
                return f"There are {high_risk_count} students predicted as high risk for dropout."  # <-- RETURN HERE

        # Dropout by department
        if any(word in user_input_lower for word in ["dropout by department", "department"]):
            if 'department' in df.columns and 'dropout' in df.columns:
                dep_counts = df[df['dropout'] == 1]['department'].value_counts().to_dict()
                return f"Dropout distribution by department: {dep_counts}"  # <-- RETURN HERE

        # Average CGPA
        if any(word in user_input_lower for word in ["average cgpa", "cgpa"]):
            if 'cgpa' in df.columns:
                avg_cgpa = df['cgpa'].mean()
                return f"The average CGPA of students is {avg_cgpa:.2f}."  # <-- RETURN HERE

    # --- Fallback to GPT-2 only if dataset not used ---
    try:
        output = generator(
            user_input,
            max_new_tokens=100,
            do_sample=True,
            truncation=True
        )
        generated_text = output[0]['generated_text'].replace(user_input, '').strip()
        return generated_text
    except Exception as e:
        return f"[AI BOT ERROR]: {e}"
