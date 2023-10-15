from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import jwt
import time
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


# You'll need to install PyJWT via pip 'pip install PyJWT' or your project packages file



METABASE_SITE_URL = "https://metabase.anaxee.com"
METABASE_SECRET_KEY = "dd5dba2e33631390fbdc79805c0c9ad6ec3ef7bbb981ab8ae9aa9951c9e7a231"

payload = {
  "resource": {"dashboard": 265},
  "params": {
    
  },
  "exp": round(time.time()) + (60 * 10) # 10 minute expiration
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
