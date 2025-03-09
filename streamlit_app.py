import streamlit as st
import pickle
from pathlib import Path

# Define paths to the saved models
vectorizer_path = Path("./models/vectorizer.pkl")
model_paths = {
    "Support Vector Machine": Path("./models/LinearSVC.pkl"),
    "Logistic Regression": Path("./models/LogisticRegression.pkl"),
    "Multinomial Naive Bayes": Path("./models/MultinomialNB.pkl")
}

# Load the vectorizer
with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

# Load the models into a dictionary for easy selection
# This will be necessary for dynamically loading the streamlit buttons
models = {}
for model_name, model_path in model_paths.items():
    with open(model_path, "rb") as f:
        models[model_name] = pickle.load(f)

# Streamlit UI design
st.title("Sentiment Analysis Application")
st.write("Enter a review and select the model you want to use for sentiment prediction.")

# Text input for review
user_text = st.text_area("Review Text:", placeholder="Type your review here...")

# Model selection dropdown based on the before model dictionary
model_choice = st.selectbox("Choose a model:", list(models.keys()))

# Predict button; which calls the selected model to predict the sentiment
if st.button("Predict"):
    if user_text:
        # Transform input text using the loaded vectorizer
        user_vector = vectorizer.transform([user_text])
        # Predict sentiment using the chosen model
        prediction = models[model_choice].predict(user_vector)
        sentiment = "Positive" if prediction[0] == 1 else "Negative"
        st.write(f"**Predicted Sentiment:** {sentiment}")
    else:
        st.warning("Please enter some text before predicting.")
