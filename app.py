import streamlit as st
import pandas as pd
import random

# Set the title of the app
st.title("English-Igala Flashcard Quiz")

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.dropna(subset=['Igala'], inplace=True)  # Drop rows where the Igala word is NaN
    data['Igala'] = data['Igala'].astype(str)  # Convert all Igala words to strings
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
if 'answers' not in st.session_state:
    st.session_state.answers = []

total_questions = 5  # Number of questions in the quiz

def start_quiz():
    st.session_state.score = 0
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.answers = []

    igala_words = data['Igala'].tolist()  # List of all Igala words for generating options

    # Generate questions
    for _ in range(total_questions):
        english_word, correct_translation = random.choice(word_pairs)
        options = generate_options(correct_translation, igala_words)
        st.session_state.questions.append({
            'english_word': english_word,
            'correct_translation': correct_translation,
            'options': options,
            'user_choice': None  # To store the user's choice
        })

# Check if Start Quiz button is clicked
if st.button("Start Quiz"):
    start_quiz()

# Display current question
if st.session_state.questions and st.session_state.current_question < total_questions:
    question = st.session_state.questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1}: What is the Igala word for '{question['english_word']}'?")

    # Display radio buttons for options
    st.session_state.questions[st.session_state.current_question]['user_choice'] = st.radio(
        "Choose an option:",
        question['options'],
        index=question['options'].index(question['user_choice']) if question['user_choice'] else 0
    )

    # Buttons for navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("Previous"):
                st.session_state.current_question -= 1
    with col2:
        if st.session_state.current_question < total_questions - 1:
            if st.button("Next"):
                st.session_state.current_question += 1
    with col3:
        if st.button("Submit Answer"):
            if st.session_state.questions[st.session_state.current_question]['user_choice'] == question['correct_translation']:
                st.session_state.score += 1
            st.session_state.current_question += 1
            if st.session_state.current_question == total_questions:
                st.balloons()
                st.write(f"Quiz Completed! Your final score: {st.session_state.score}/{total_questions}")
                st.write("Click 'Start Quiz' to play again.")

# Summary of answers
if st.session_state.current_question == total_questions:
    st.write("### Quiz Summary")
    for i, q in enumerate(st.session_state.questions):
        st.write(f"**Question {i + 1}:** What is the Igala word for '{q['english_word']}'?")
        st.write(f"- Your answer: {q['user_choice']}")
        st.write(f"- Correct answer: {q['correct_translation']}")
    st.write(f"**Final Score:** {st.session_state.score}/{total_questions}")
    st.write("Click 'Start Quiz' to play again.")
