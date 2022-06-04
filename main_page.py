import streamlit as st

st.set_page_config(page_title="MS Explorer v 0.0.3", layout="wide")

def initialise():
    st.markdown("""
    # Mass Spectrometry Utility Applications 
    Includes 2, 3 and 5 dimensional data visualization and processing

    **Select an MSI application from the sidebar**
    
    ### Streamlit Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)    
""")


def main():
    initialise()

if __name__=="__main__":
    main()
    
