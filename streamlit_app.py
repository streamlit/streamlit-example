# # Only camera module

# # import altair as alt
# # import numpy as np
# # import pandas as pd
# # import streamlit as st
# # from PIL import Image
# # from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
# # from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
# # from clarifai_grpc.grpc.api.status import status_code_pb2

# # # Clarifai API code
# # def predict_food_item(image_bytes, pat, user_id, app_id, model_id, model_version_id):
# #     channel = ClarifaiChannel.get_grpc_channel()
# #     stub = service_pb2_grpc.V2Stub(channel)

# #     metadata = (('authorization', 'Key ' + pat),)

# #     userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

# #     post_model_outputs_response = stub.PostModelOutputs(
# #         service_pb2.PostModelOutputsRequest(
# #             user_app_id=userDataObject,
# #             model_id=model_id,
# #             version_id=model_version_id,
# #             inputs=[
# #                 resources_pb2.Input(
# #                     data=resources_pb2.Data(
# #                         image=resources_pb2.Image(
# #                             base64=image_bytes
# #                         )
# #                     )
# #                 )
# #             ]
# #         ),
# #         metadata=metadata
# #     )

# #     if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
# #         print(post_model_outputs_response.status)
# #         raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

# #     output = post_model_outputs_response.outputs[0]
# #     return output

# # # Streamlit application code
# # st.title("Food Recognition App")

# # # Camera input for image capture
# # st.sidebar.markdown("### Capture Image")
# # captured_image = st.camera_input("Capture Image")

# # # Display the captured image for food recognition
# # if st.sidebar.button("Recognize Food") and captured_image is not None:
# #     # Get Clarifai predictions using the defined function
# #     st.write("Predicted concepts:")
# #     pat = 'ac76a2d4778541baa55aa743c79f00dc'  # Replace with your PAT
# #     user_id = 'clarifai'
# #     app_id = 'main'
# #     model_id = 'food-item-v1-recognition'
# #     model_version_id = 'dfebc169854e429086aceb8368662641'

# #     # Convert the captured image to bytes
# #     image_bytes = captured_image.getvalue()

# #     predicted_output = predict_food_item(
# #         image_bytes, pat, user_id, app_id, model_id, model_version_id
# #     )

# #     for concept in predicted_output.data.concepts:
# #         st.write("%s %.2f" % (concept.name, concept.value))



# # To upload only
# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st
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

# # Sidebar to upload an image
# st.sidebar.markdown("### Upload Image")

# # Upload image from the user's device
# uploaded_file = st.sidebar.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)
#     # Save the uploaded image to a temporary file for later use
#     image.save("uploaded_image.jpg")

# # Display the uploaded image for food recognition
# if st.sidebar.button("Recognize Food"):
#     selected_image_path = "uploaded_image.jpg"
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


# for both
import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from PIL import Image

# Clarifai API code
def predict_food_item(image_bytes, pat, user_id, app_id, model_id, model_version_id):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + pat),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

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

# Sidebar option to choose between camera or upload
option = st.sidebar.radio("Choose an option", ["Capture from Camera", "Upload Image"])

# Function to capture image from camera
def capture_from_camera():
    st.markdown("### Capture Image")
    captured_image = st.camera_input("Capture Image")
    return captured_image

# Function to upload image
def upload_image():
    st.markdown("### Upload Image")
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    return uploaded_file

# Choose capture method based on user option
if option == "Capture from Camera":
    captured_image = capture_from_camera()
elif option == "Upload Image":
    uploaded_file = upload_image()

# Display the selected image for food recognition
if st.button("Recognize Food"):
    if option == "Capture from Camera" and captured_image is not None:
        # Convert the captured image to bytes
        image_bytes = captured_image.getvalue()
    elif option == "Upload Image" and uploaded_file is not None:
        # Read the uploaded image file buffer as bytes
        image_bytes = uploaded_file.read()

    # Get Clarifai predictions using the defined function
    st.write("Predicted concepts:")
    pat = 'ac76a2d4778541baa55aa743c79f00dc'  # Replace with your PAT
    user_id = 'clarifai'
    app_id = 'main'
    model_id = 'food-item-v1-recognition'
    model_version_id = 'dfebc169854e429086aceb8368662641'

    predicted_output = predict_food_item(
        image_bytes, pat, user_id, app_id, model_id, model_version_id
    )

    for concept in predicted_output.data.concepts:
        st.write("%s %.2f" % (concept.name, concept.value))
