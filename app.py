import streamlit as st
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def analyze_responses(responses):
    stress_keywords = ['overwhelmed', 'yes', 'stressed', 'bad', 'boring', 'hectic', 'anxious', 'nervous', 'exhausted', 'frustrated']
    stress_percentage = 0

    for response in responses:
        for keyword in stress_keywords:
            if re.search(r'\b' + keyword + r'\b', response.lower(), re.I):
                stress_percentage += 20

    stress_percentage = min(stress_percentage, 100)

    mood = analyze_mood(" ".join(responses))

    return stress_percentage, mood

def analyze_mood(text):
    sentiment_scores = sid.polarity_scores(text)

    if sentiment_scores['compound'] >= 0.05:
        return "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def get_stress_relief_suggestions():
    suggestions = [
        "Practice deep breathing exercises.",
        "Take a short walk or engage in physical activity.",
        "Meditate or try relaxation techniques.",
        "Connect with friends or family for support.",
        "Listen to calming music or nature sounds.",
        "Limit your exposure to stressors and set boundaries.",
        "Consider talking to a therapist or counselor.",
        "Engage in a hobby or activity you enjoy.",
    ]
    return suggestions

st.title("Stress Level and Mood Analyzer Chatbot")
st.subheader("Made By- Paragi Chauhan")
st.write("Please answer the following questions honestly to assess your stress level and analyze your mood.")

questions = [
    "How are you feeling today? Choose one: 'overwhelmed', 'yes', 'stressed', 'bad', 'boring', 'hectic', 'anxious', 'nervous', 'exhausted', 'frustrated'",
    "Are there any specific issues or challenges you're facing?",
    "Have you been sleeping well?",
    "How is your work/school life currently?",
    "Are there any personal concerns or conflicts on your mind?"
]

responses = []

for i, question in enumerate(questions):
    if i > 0:
        # Check if the previous question has been answered
        if not responses[i - 1]:
            st.warning("Please answer the previous question before moving on.")
            break

    answer = st.text_input(question, "")
    responses.append(answer)

if st.button("Analyze"):
    # Check if all questions have been answered
    if None in responses:
        st.warning("Please answer all questions before analyzing.")
    else:
        for answer in responses:
            print(answer)
        stress_percentage, mood = analyze_responses(responses)
        st.write(f"Based on your responses, your estimated stress level is {stress_percentage}%.")
        st.write(f"Based on your responses, your mood appears to be: {mood}.")

        # Check if stress percentage is high and provide relief suggestions
        if stress_percentage > 50:
            st.write("The stress is high. Here are some suggestions to relieve stress:")
            suggestions = get_stress_relief_suggestions()
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
