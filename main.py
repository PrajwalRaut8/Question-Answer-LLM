import os
import streamlit as st
import google.generativeai as palm

# Set up the API key and configure the Google Generative AI
API_KEY = 'API_KEY'
os.environ['GEMINI_API_KEY'] = API_KEY
palm.configure(api_key=os.environ['GEMINI_API_KEY'])

# Streamlit app title
st.title("Question-Answer with AI")

# Dropdown for selecting a topic
topic = st.selectbox("Select a topic:", ["Geography", "Health", "Sports"], index=0)


# Function to generate a question using Google Generative AI
def generate_question(topic):
    prompt = f"Generate a question related to {topic}."
    try:
        response = palm.generate_text(prompt=prompt)
        if response and hasattr(response, 'result'):
            question = response.result.strip()
        else:
            question = "Failed to generate a question."
    except Exception as e:
        question = "Failed to generate a question due to an error."
    return question


# Button to generate a question
if st.button("Generate Question"):
    if topic:
        generated_question = generate_question(topic)
        if generated_question != "Failed to generate a question.":
            st.session_state.question = generated_question
        else:
            st.warning("Failed to generate a question.")
    else:
        st.warning("Please select a topic to generate a question.")

# Display the generated question if it exists in session state
if "question" in st.session_state:
    st.write("Generated Question:", st.session_state.question)

# Input box for user's answer
user_answer = st.text_input("Your Answer:")


# Function to validate the user's answer using Google Generative AI
def validate_answer(question, user_answer):
    validation_prompt = (
        f"Question: {question}\n"
        f"User's Answer: {user_answer}\n"
        f"Is the user's answer correct? Respond with 'Yes' or 'No'."
    )
    try:
        response = palm.generate_text(prompt=validation_prompt)
        if response and hasattr(response, 'result'):
            response_text = response.result.strip()
            if "yes" in response_text.lower():
                return "Correct Answer!", None
            else:
                return "Incorrect Answer.", None
        else:
            return "Failed to validate the answer.", None
    except Exception as e:
        return "Failed to validate the answer due to an error.", None


# Function to get the correct answer if user's answer is wrong
def get_correct_answer(question):
    correct_answer_prompt = f"Provide the correct answer to the following question:\nQuestion: {question}"
    try:
        response = palm.generate_text(prompt=correct_answer_prompt)
        if response and hasattr(response, 'result'):
            correct_answer = response.result.strip()
            return correct_answer
        else:
            return "Unable to retrieve the correct answer."
    except Exception as e:
        return "Unable to retrieve the correct answer due to an error."


# Button to validate the user's answer
if st.button("Submit Answer"):
    if "question" in st.session_state and user_answer.strip():
        validation_result, _ = validate_answer(st.session_state.question, user_answer)
        st.write(validation_result)
        if "Incorrect" in validation_result:
            correct_answer = get_correct_answer(st.session_state.question)
            st.write("The correct answer is:", correct_answer)
    else:
        st.warning("Please generate a question and provide your answer.")
