import streamlit as st

from  pages.sl_xyi_viewer import XiCViewer

st.set_page_config(page_title="MS Explorer v 0.0.1", layout="wide")

pages = {}

def initialise():
    pages = {
        "XiC Viewer" : XiCViewer()
    }
    return pages


def main():
    st.sidebar.title('Navigation')
    pages = initialise()
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    if selection:
        page = pages[selection]
        page.run()

if __name__=="__main__":
    main()
    
