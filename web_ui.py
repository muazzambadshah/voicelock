import streamlit as st

def main():
    st.title("Voicelock: Secure Voice Messaging & Authentication")
    
    uploaded_file = st.file_uploader("Upload your voice file", type=["wav", "mp3"])
    if uploaded_file is not None:
        st.audio(uploaded_file)
        # Further processing can happen here
        st.write("File uploaded successfully")

if __name__ == "__main__":
    main()
