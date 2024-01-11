import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

import streamlit as st
import pandas as pd
import numpy as np

st.title('Explain my test results please!')
st.header('Instructions')
st.markdown('Take a picture of your lab test results, upload it, and we will explain it to you!')


def load_image():
    uploaded_file = st.file_uploader(label='Upload your test results image below:')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption='', width=600)
        return image_data
        
image = load_image()
if  image is not None:
    image = np.asarray(Image.open(BytesIO(image)).convert('RGB'))
if st.button('Process Image'):
    result = ocr_model.ocr(image)
    texts = [res[1][0] for res in result[0] if len(res[1][0]) > 1]
    result = llm(prompt_template_extract.format(text=",".join(texts)))
    print("result: ", result)
    result = literal_eval(result)
    result['drug'] = " ".join(result['drug'].split(" ")[:2])
    
st.caption('Disclaimer: Not medical advice, not liable, blah')
