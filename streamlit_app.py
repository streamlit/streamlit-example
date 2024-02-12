from enum import Enum

import streamlit as st
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingModel(Enum):
    ALL_MINILM_L12_V2 = "all-MiniLM-L12-v2"


class SimilarityChecker:
    def __init__(self,  embedding_model: str = None, relevance_threshold=0.66, similarity_threshold=0.6) -> None:
        self.model = SentenceTransformer(model_name_or_path=embedding_model)
        self.relevance_threshold = relevance_threshold
        self.similarity_threshold = similarity_threshold

    def get_embedded_sentence(self, text: str):
        return self.model.encode(text, convert_to_tensor=True)

    def relevance_score(self, question_text: str, answer_text: str) -> bool:
        question_embedding = self.get_embedded_sentence(question_text)
        answer_embedding = self.get_embedded_sentence(answer_text)
        score = util.cos_sim(question_embedding, answer_embedding).item()
        return score >= self.relevance_threshold

    def text_similarity(self, text_one: str, text_two: str) -> bool:
        text_one_embedding = self.get_embedded_sentence(text_one)
        text_two_embedding = self.get_embedded_sentence(text_two)
        score = util.cos_sim(text_one_embedding, text_two_embedding).item()
        return score >= self.similarity_threshold

    def relevance_score_row_vectors_sklearn(self, question: str, answer: str) -> bool:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([question, answer])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return cosine_sim[0, 0] >= self.relevance_threshold

    def text_similarity_using_row_vectors(self, text_a: str, text_b: str) -> bool:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return cosine_sim[0, 0] >= self.similarity_threshold

# Streamlit app layout
st.title("Suzy Similarity AI")
option = st.selectbox(
    'Choose your model',
    ( EmbeddingModel.ALL_MINILM_L12_V2.value,))

calculation_type_option = st.selectbox(
    'Choose sklearn calculation or llm embedding model',
    ("sklearn", "llm"))
checker = SimilarityChecker(embedding_model=option)

# Question - Answer Similarity
st.header("Question - Answer Relevance")
question = st.text_input("Question")
answer = st.text_input("Answer")

if st.button("Check Relevance"):
    if calculation_type_option == "llm":
        if question and answer:
            is_relevant = checker.relevance_score(question, answer)
            if is_relevant:
                st.text("The answer is relevant to the question.")
            else:
                st.error("The answer is not relevant to the question.")
        else:
            st.text("Please enter both a question and an answer.")
    else:
        if question and answer:
            is_relevant = checker.relevance_score_row_vectors_sklearn(question, answer)
            if is_relevant:
                st.text("The answer is relevant to the question.")
            else:
                st.error("The answer is not relevant to the question.")
        else:
            st.text("Please enter both a question and an answer.")
# Text Similarity

st.header("Text Similarity")
text_a = st.text_area("Text A")
text_b = st.text_area("Text B")
if st.button("Calculate Similarity Score"):
    if calculation_type_option == "llm":
        if question and answer:
            is_relevant = checker.text_similarity(text_a, text_b)
            if not is_relevant:
                st.text("Texts are not similar")
            else:
                st.error("Texts seems to be duplicated")
        else:
            st.text("Please enter both Text A  and Text B for comparison")
    else:
        if question and answer:
            is_relevant = checker.text_similarity_using_row_vectors(text_a, text_b)
            if not is_relevant:
                st.text("Texts are not similar")
            else:
                st.error("Texts seems to be duplicated")
        else:
            st.text("Please enter both Text A  and Text B for comparison")
