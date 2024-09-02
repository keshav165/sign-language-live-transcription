import streamlit as st
import numpy as np
import cv2
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load your trained model
model = load_model('C:\\Users\\kesha\\Downloads\\signs.h5')

# Define the signs you want to predict
signs = np.array(["hello", "ok", "iloveyou", "house", "day", "father", "peace", "please", "phone", "no"])

# Initialize Mediapipe models
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Function to perform mediapipe detection
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image.flags.writeable = False  # No write
    results = model.process(image)  # Make detection
    image.flags.writeable = True  # Write
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR
    return image, results

# Function to draw landmarks
def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                              mp_drawing.DrawingSpec(color=(245,117,66), thickness=1, circle_radius=1),
                              mp_drawing.DrawingSpec(color=(245,66,230), thickness=1, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80,110,10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80,256,121), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))

# Extract keypoints from Mediapipe results
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
    return np.concatenate([pose, face, lh, rh])

# Function to visualize prediction probabilities
def prob_viz(res, signs, input_frame, colors):
    output_frame = input_frame.copy()
    for num, (prob, sign) in enumerate(zip(res, signs)):
        if num >= len(colors):
            color = (0, 0, 0)  
        else:
            color = colors[num]
        
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), color, -1)
        cv2.putText(output_frame, sign, (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
    return output_frame

# Streamlit app setup
st.title("Sign Language Recognition")
st.text("Click on 'Start' to begin the video feed.")

# Initialize placeholders
sequence = []
sentence = []
threshold = 0.8

# Use Streamlit's session state to manage the state of the video feed
if 'run' not in st.session_state:
    st.session_state.run = False

# Create buttons for start and stop
start_button = st.button('Start')
stop_button = st.button('Stop')

if start_button:
    st.session_state.run = True

if stop_button:
    st.session_state.run = False

# Video capture and prediction logic
if st.session_state.run:
    cap = cv2.VideoCapture(0)
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            stframe = st.empty()
        
        with col2:
            text_container = st.empty()
        
        while st.session_state.run and cap.isOpened():
            ret, frame = cap.read()
            
            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            
            # Draw landmarks
            draw_styled_landmarks(image, results)
            
            # Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if signs[np.argmax(res)] != sentence[-1]:
                            sentence.append(signs[np.argmax(res)])
                    else:
                        sentence.append(signs[np.argmax(res)])
                
                if len(sentence) > 5:
                    sentence = sentence[-5:]
                
                # Viz probabilities
                image = prob_viz(res, signs, image, [(245,117,16), (117,245,16), (16,117,245)])
            
            # Display results
            stframe.image(image, channels='BGR')
            
            # Update the text container
            with col2:
                text_container.markdown(f"### Predicted Sign: {' '.join(sentence)}")
            
            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()
