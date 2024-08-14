import streamlit as st
import pandas as pd
import random

# Set the title of the app
st.title("English-Igala Flashcard Quiz")

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Load the dataset
file_path = 'clean.csv'
data = load_data(file_path)

# Create a list of English-Igala pairs
word_pairs = list(zip(data['English'], data['Igala']))

def generate_options(correct_answer, all_options, num_options=4):
    options = [correct_answer]
    while len(options) < num_options:
        option = random.choice(all_options)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []

total_questions = 5  # Number of questions in the quiz

def start_quiz():
    st.session_state.score = 0
    st.session_state.current_question = 0
    st.session_state.questions = []

    igala_words = data['Igala'].tolist()  # List of all Igala words for generating options

    # Generate questions
    for _ in range(total_questions):
        english_word, correct_translation = random.choice(word_pairs)
        options = generate_options(correct_translation, igala_words)
        st.session_state.questions.append({
            'english_word': english_word,
            'correct_translation': correct_translation,
            'options': options
        })

if st.button("Start Quiz") or len(st.session_state.questions) == total_questions:
    if len(st.session_state.questions) == 0:
        start_quiz()

    if st.session_state.current_question < total_questions:
        question = st.session_state.questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1}: What is the Igala word for '{question['english_word']}'?")

        user_choice = st.radio("Choose an option:", question['options'])

        if st.button("Submit Answer"):
            if user_choice.lower() == question['correct_translation'].lower():
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong. The correct answer is '{question['correct_translation']}'.")
            st.session_state.current_question += 1
            if st.session_state.current_question == total_questions:
                st.balloons()
                st.write(f"Quiz Completed! Your final score: {st.session_state.score}/{total_questions}")
                st.write("Click 'Start Quiz' to play again.")
    else:
        st.write(f"Quiz Completed! Your final score: {st.session_state.score}/{total_questions}")
        st.write("Click 'Start Quiz' to play again.")
else:
    st.write("Click 'Start Quiz' to begin the English-Igala Flashcard Quiz!")
