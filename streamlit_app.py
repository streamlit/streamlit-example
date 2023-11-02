import streamlit as st
import os
import cv2
from PIL import Image
import tempfile
import pandas as pd
import json
from datetime import datetime
from gradio_client import Client
import pyrebase
import json
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import numpy as np
import requests
import base64

firebaseConfig = {
  "apiKey": "AIzaSyBIa20ao3DoT4XTiG-hxlTtAu6l4HIVOSE",
  "authDomain": "visual-product-recogniti-d7cb0.firebaseapp.com",
  "databaseURL": "https://visual-product-recogniti-d7cb0-default-rtdb.firebaseio.com",
  "projectId": "visual-product-recogniti-d7cb0",
  "storageBucket": "visual-product-recogniti-d7cb0.appspot.com",
  "messagingSenderId": "732077642124",
  "appId": "1:732077642124:web:84fc3eeb016d277c4c46a9",
  "measurementId": "G-GK2TPTMQ23"
}

firebase=pyrebase.initialize_app(firebaseConfig)

pyrebase_db=firebase.database()

auth = firebase.auth()

db = firebase.database()


def createPrediction(imagePath):
    current_datetime = datetime.now()
    transactionRecipient= current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    user = f"user{np.random.randint(1, 301)}"
    
    transaction_data = {
        "user" : user,
        "imagePath": imagePath,
        "time": transactionRecipient
    }

    db.child("Prediction").push(transaction_data)

def createFeedback(user, feedback):
    current_datetime = datetime.now()
    transactionRecipient= current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    transaction_data = {
        "user" : user,
        "rating": feedback,
        "time": transactionRecipient
    }

    db.child("Feedback").push(transaction_data)


def createRating(user, rating):
    
    current_datetime = datetime.now()
    transactionRecipient= current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    transaction_data = {
        "user" : user,
        "rating": rating,
        "time": transactionRecipient
    }

    db.child("Rating").push(transaction_data)


def show_average_rating_per_day():
    data = pyrebase_db.child("Rating").get().val()
    data_list = [
        {
            "rating": x["rating"],
            "time": x["time"]
        }
        for i, x in data.items()
    ]



    df = pd.DataFrame(data_list)
    df['time'] = pd.to_datetime(df['time'])  # Convert 'time' to datetime

    # Group data by day and calculate the average rating
    df_grouped = df.groupby(df['time'].dt.date)['rating'].mean().reset_index()

    fig = px.line(
        df_grouped,
        x='time',
        y='rating',
        labels={"rating": "Average Rating", "time": "Date"},
    )

    st.plotly_chart(fig, use_container_width=True)


def show_sentiment():

    data = pyrebase_db.child("Feedback").get().val()
    data_list = [
        {
            "rating": x["rating"],
            "time": x["time"]
        }
        for i, x in data.items()
    ]

    df = pd.DataFrame(data_list)
    
    def analyze_sentiment(feedback):
        analysis = TextBlob(feedback)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    df['Sentiment'] = df['rating'].apply(analyze_sentiment)

    sentiment_counts = df['Sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']

    fig = px.pie(sentiment_counts, values='Count', names='Sentiment', title='Sentiment Distribution of User Feedback')

    st.plotly_chart(fig)


image_folder = 'user_images'
os.makedirs(image_folder, exist_ok=True)

# Create a CSV file for user data (if it doesn't exist)
csv_file = 'user_data.csv'
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=['user', 'image_path', 'upload_time', 'rating'])
    df.to_csv(csv_file, index=False)
# Path to the directory containing similar images
similar_images_dir = ".\gallery"

def read_image(image_file):
    img = cv2.imread(
        image_file, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
    )
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img is None:
        raise ValueError('Failed to read {}'.format(image_file))
    return img


def get_image_paths(prod_ids):
    csv_path = './gallery.csv'  
    data = pd.read_csv(csv_path)
    image_paths = []

    for i, prod_id in enumerate(prod_ids):
        row = data[data['seller_img_id'] == prod_id]
        
        if not row.empty:
            image_path = './' + row.iloc[0]['img_path']
            # print(image_path)
            image_paths.append(image_path)

    return image_paths


powerbi_embed_code =  """<iframe title="Report Section" width="1024" height="664" src="https://app.powerbi.com/view?r=eyJrIjoiMzk5ZmExNGUtZTA4NC00NDgyLTk0YjItNzlhN2ZhY2VlMWQ4IiwidCI6ImFhYzBjNTY0LTZjNWUtNGIwNS04ZGMzLTQwODA4N2Y3N2Y3NiIsImMiOjEwfQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>"""
def add_border_radius(image_url, radius):
    return f"<img src='{image_url}' style='border-radius: {radius}px;' />"


def render_predict():
    st.title("Predict Section")
    
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


    if uploaded_image is not None:

        temp_dir = tempfile.TemporaryDirectory()
        
        temp_image_path = os.path.join(temp_dir.name, "uploaded_image.jpg")
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_image.read())

        with open(temp_image_path, 'rb') as image_file:
            # Read the image data
            image_data = image_file.read()

        base64_encoded = base64.b64encode(image_data).decode('utf-8')

        # Print or use the base64_encoded string as needed
        # print(base64_encoded)

        response = requests.post("https://awacke1-image-to-text-salesforce-blip-image-capt-f549b46.hf.space/run/predict", json={
            "data": [
                f"data:image/png;base64,{base64_encoded}",
            ]
        }).json()

        data = response["data"][0]

        target_size = (224, 280)  # Size to resize the images

        search_image = read_image(temp_image_path)

        resized_search_image = Image.fromarray(search_image).resize(target_size)
                    
        st.image(resized_search_image, caption="Input Image", use_column_width=False)

        st.markdown(f"<h3>{data}</h3>", unsafe_allow_html=True)


        client = Client("https://thenujan-vpr-deploy.hf.space/")
        result = client.predict(
                        temp_image_path,	
                        api_name="/predict"
        )

        with open(result, 'r') as json_file:
            data = json.load(json_file)

        similar_image_ids = data['similar_image_ids'][0]

        similar_image_paths = get_image_paths(similar_image_ids)

        st.write(f"Found {len(similar_image_ids)} similar images.")

        images_per_page = 20
        num_pages = (len(similar_image_ids) + images_per_page - 1) // images_per_page

        page_num = st.slider("Select Page", min_value=1, max_value=num_pages)

        start_idx = (page_num - 1) * images_per_page
        end_idx = min(start_idx + images_per_page, len(similar_image_ids))

        images_per_row = 4

        for i in range(start_idx, end_idx, images_per_row):
            row_images = similar_image_paths[i:i + images_per_row]
            row = st.columns(images_per_row)
            
            for j, similar_image_path in enumerate(row_images):
                if os.path.exists(similar_image_path):
                    similar_image = read_image(similar_image_path)
                    resized_image = Image.fromarray(similar_image).resize(target_size)
                    row[j].image(resized_image, caption=similar_image_path, use_column_width=True)
                else:
                    st.write(f"Image not found: {similar_image_path}")

        createPrediction(temp_image_path)


def render_dashboard():
    st.title("Dashboard Section")
    
    view_option = st.radio("Select a view:", ("Show Dashboard", "Show Model Performance", "Show User Sentiment Analysis"))

    if view_option == "Show Dashboard":
        st.subheader("Power BI Dashboard")
        dashboard_container = st.empty()
        dashboard_container.markdown(powerbi_embed_code, unsafe_allow_html=True)
    elif view_option == "Show Model Performance":
        st.subheader("Model Performance")
        show_average_rating_per_day()

    elif view_option == "Show User Sentiment Analysis":
        st.subheader("User Sentiment Analysis")
        show_sentiment()

    

def render_feedback():
    st.title("Feedback Section")
    st.write("Provide your feedback and rating here:")
    st.write("Rate the feedback:")
    user = f"user{np.random.randint(1, 301)}"
    rating = st.radio("Select your rating (1-5 stars)", [1, 2, 3, 4, 5])
    if st.button("Submit Rating"):
        createRating(user, rating)
        st.write(f"You rated the feedback as {rating} star(s).")

    user_feedback = st.text_area("Enter your feedback here:")
    if st.button("Submit Feedback"):
        createFeedback(user, user_feedback)
        st.write("Feedback submitted successfully!")


def main():

    # Add CSS styles for the navigation buttons
    st.markdown(
        """
        <style>
        .navigation-button {
            padding: 10px 20px;
            background-color: #333;
            color: white;
            border: none;
            cursor: pointer;
        }
        .navigation-button:hover {
            background-color: #555;
        }
        .selected-button {
            background-color: #000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create a sidebar navigation bar
    st.sidebar.markdown("<h1 style='color:black;'>Navigation</h1>", unsafe_allow_html=True)

    # Define the navigation options
    navigation_options = ["Predict", "Dashboard", "Feedback"]

    # Create buttons for navigation
    selected_option = st.sidebar.radio("Go to", navigation_options, index=0, key="navigation")

    # Display the selected option in the sidebar
    st.sidebar.write(f"Selected: {selected_option}")

    # Render different sections based on the selected option
    if selected_option == "Predict":
        # Call the render_predict() function
        render_predict()
    elif selected_option == "Dashboard":
        # Call the render_dashboard() function
        render_dashboard()
    elif selected_option == "Feedback":
        # Call the render_feedback() function
        render_feedback()

st.set_page_config(layout="wide")
# st.markdown('<style>body{background-color: Blue;}</style>',unsafe_allow_html=True)


if __name__ == "__main__":
    main()
