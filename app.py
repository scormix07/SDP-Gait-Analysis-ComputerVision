import streamlit as st
import os

from walk_predictor import predict_walk

TEMP_DIR = './temp'
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to reset the app
def reset_app():
    st.rerun()

# Main function
def main():
    st.title("Gait Anlaysis")
    
    # Initialize session state variables
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'distance' not in st.session_state:
        st.session_state.distance = 17  # Default value for variable1
    if 'stride_ratio' not in st.session_state:
        st.session_state.stride_ratio = 45  # Default value for variable2
    if 'pelvic_thresh' not in st.session_state:
        st.session_state.pelvic_thresh = 20  # Default value for variable2
    if 'use_pelvic' not in st.session_state:
        st.session_state.use_pelvic = False  # Default value for variable2
    
    # Upload video
    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        video_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.session_state.video_path = video_path
    
    # Slider for variable1
    st.sidebar.slider("distance threshold",
                      min_value=10,
                      max_value=30,
                      value=st.session_state.distance,
                      key='distance')
    
    # Slider for variable2
    st.sidebar.slider("Pelvic Threshold",
                      min_value=10,
                      max_value=30,
                      value=st.session_state.pelvic_thresh,
                      key='pelvic_thresh')
    
    st.sidebar.slider("stride ratio",
                      min_value=0,
                      max_value=100,
                      value=st.session_state.stride_ratio,
                      key='stride_ratio')
    
    # Radio button for method selection
    use_pelvic = st.sidebar.radio("Use Pelvic", ("True", "False"),
                      index=1)
    st.session_state.use_pelvic = bool(use_pelvic)
    
    # Classify button
    if st.button("Classify"):
        if st.session_state.video_path is not None:
            prediction_gen = predict_walk(st.session_state.video_path,
                                          st.session_state.distance,
                                          st.session_state.stride_ratio/100,
                                          st.session_state.pelvic_thresh,
                                          use_pelvic=st.session_state.use_pelvic)
            # frame_key = "video_frame"
            video_placeholder = st.empty()
            opImg_placeholder = st.empty()
            for item, item2 in prediction_gen:
                if isinstance(item, str):
                    opImg_placeholder.empty()
                    video_placeholder.success(item)
                else:
                    video_placeholder.image(item, caption='Tracking video')
                    opImg_placeholder.image(item2, caption='OpenImg video', clamp=True)
                    
        else:
            st.error("Please upload a video first.")
    
    # Reset button
    if st.button("Reset"):
        reset_app()

# Run the app
if __name__ == "__main__":
    main()
