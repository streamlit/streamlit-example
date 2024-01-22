import streamlit as st
import tensorflow as tf

"""
# Movie Rating prediction!
based on your comments about the movie

"""
model = tf.saved_model.load('./models')

