# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st
# import cv2
# from PIL import Image
# from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
# from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
# from clarifai_grpc.grpc.api.status import status_code_pb2

# # Clarifai API code
# def predict_food_item(image_path, pat, user_id, app_id, model_id, model_version_id):
#     channel = ClarifaiChannel.get_grpc_channel()
#     stub = service_pb2_grpc.V2Stub(channel)

#     metadata = (('authorization', 'Key ' + pat),)

#     userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

#     with open(image_path, "rb") as image_file:
#         image_bytes = image_file.read()

#     post_model_outputs_response = stub.PostModelOutputs(
#         service_pb2.PostModelOutputsRequest(
#             user_app_id=userDataObject,
#             model_id=model_id,
#             version_id=model_version_id,
#             inputs=[
#                 resources_pb2.Input(
#                     data=resources_pb2.Data(
#                         image=resources_pb2.Image(
#                             base64=image_bytes
#                         )
#                     )
#                 )
#             ]
#         ),
#         metadata=metadata
#     )

#     if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
#         print(post_model_outputs_response.status)
#         raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

#     output = post_model_outputs_response.outputs[0]
#     return output

# # Streamlit application code
# st.title("Food Recognition App")

# # Sidebar to capture image from the camera or upload an image
# option = st.sidebar.selectbox("Choose an option", ["Capture from Camera", "Upload Image"])

# if option == "Capture from Camera":
#     st.sidebar.markdown("### Capture Image")
    
#     # Capture image from the camera
#     cap = cv2.VideoCapture(0)
#     if st.sidebar.button("Capture"):
#         _, frame = cap.read()
#         image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         st.sidebar.image(image, caption="Captured Image", use_column_width=True)
#         # Save the captured image to a temporary file for later use
#         image.save("captured_image.jpg")

# elif option == "Upload Image":
#     st.sidebar.markdown("### Upload Image")
    
#     # Upload image from the user's device
#     uploaded_file = st.sidebar.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)
#         # Save the uploaded image to a temporary file for later use
#         image.save("uploaded_image.jpg")

# # Display the selected image for food recognition
# if st.sidebar.button("Recognize Food"):
#     selected_image_path = "captured_image.jpg" if option == "Capture from Camera" else "uploaded_image.jpg"
#     st.image(selected_image_path, caption="Selected Image for Recognition", use_column_width=True)
    
#     # Get Clarifai predictions using the defined function
#     st.write("Predicted concepts:")
#     pat = 'ac76a2d4778541baa55aa743c79f00dc'  # Replace with your PAT
#     user_id = 'clarifai'
#     app_id = 'main'
#     model_id = 'food-item-v1-recognition'
#     model_version_id = 'dfebc169854e429086aceb8368662641'

#     predicted_output = predict_food_item(
#         selected_image_path, pat, user_id, app_id, model_id, model_version_id
#     )

#     for concept in predicted_output.data.concepts:
#         st.write("%s %.2f" % (concept.name, concept.value))

# # Close the camera if it was opened
# if option == "Capture from Camera":
#     cap.release()

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Clarifai API code
def predict_food_item(image_path, pat, user_id, app_id, model_id, model_version_id):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + pat),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=model_id,
            version_id=model_version_id,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    output = post_model_outputs_response.outputs[0]
    return output

# Streamlit application code
st.title("Food Recognition App")

# Sidebar to upload an image
st.sidebar.markdown("### Upload Image")

# Upload image from the user's device
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)
    # Save the uploaded image to a temporary file for later use
    image.save("uploaded_image.jpg")

# Display the uploaded image for food recognition
if st.sidebar.button("Recognize Food"):
    selected_image_path = "uploaded_image.jpg"
    st.image(selected_image_path, caption="Selected Image for Recognition", use_column_width=True)
    
    # Get Clarifai predictions using the defined function
    st.write("Predicted concepts:")
    pat = 'ac76a2d4778541baa55aa743c79f00dc'  # Replace with your PAT
    user_id = 'clarifai'
    app_id = 'main'
    model_id = 'food-item-v1-recognition'
    model_version_id = 'dfebc169854e429086aceb8368662641'

    predicted_output = predict_food_item(
        selected_image_path, pat, user_id, app_id, model_id, model_version_id
    )

    for concept in predicted_output.data.concepts:
        st.write("%s %.2f" % (concept.name, concept.value))
