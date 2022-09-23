import sys
import streamlit as st

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
    sys.exit(st._main())