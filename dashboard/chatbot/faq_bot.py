faq_responses = {
    "what is dropout rate": "Dropout rate measures how many students discontinue before completing the program.",
    "how is prediction done": "The model uses features like attendance, grades, and socioeconomic data to estimate dropout risk.",
    "who developed this project": "This project was developed by Team CodeStorm for the Student Dropout Predictor hackathon."
}

def get_faq_response(user_input):
    user_input = user_input.lower()
    for key in faq_responses:
        if key in user_input:
            return faq_responses[key]
    return None
