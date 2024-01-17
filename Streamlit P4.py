import streamlit as st

st.markdown("# Alan Jones")
st.markdown("## Writer and Developer")
st.markdown("""
    I write articles about Data Science, Python and related topics. 
    The articles are mostly written on the Medium platform.
    
    You can find my articles [here](https://alan-jones.medium.com)
    and if you would like to know when I publish new ones, you can 
    sign up for an email alert on my Medium 
    [page](https://alan-jones.medium.com/subscribe).
    Below are a few articles you might find interesting...
""")

with st.container():
    image_col, text_col = st.columns((1,2))
    with image_col:
        st.image("https://cdn-images-1.medium.com/max/906/1*dVSDol9pouoO9IX_E_-35Q.png")

    with text_col:
        st.subheader("A Multi-page Interactive Dashboard with Streamlit and Plotly")
        st.write("""Beautiful interactive multipage dashboards are made easy with Streamlit
            """)
        st.markdown("[Read more...](https://towardsdatascience.com/a-multi-page-interactive-dashboard-with-streamlit-and-plotly-c3182443871a)")

with st.container():
    image_col, text_col = st.columns((1,2))
    with image_col:
        st.image("https://cdn-images-1.medium.com/max/906/1*hjhCIWGgLzOznTFwDyeIeA.png")

    with text_col:
        st.subheader("Rational UI Design with Streamlit")
        st.write("""
            From one point of view Streamlit is a retrograde step in web development because 
            it lets you mix up the logic of your app with the way it is presented. But from 
            another it is very much simplifying web design.""")
        st.markdown("[Read more...](https://towardsdatascience.com/rational-ui-design-with-streamlit-61619f7a6ea4)")
