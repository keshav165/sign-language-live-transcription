
1. Introduction

Welcome to the Sign Language Recognition Application! This tool is designed to recognize specific sign language gestures in real-time using a camera feed. The application is built with a machine learning model and deployed using Streamlit. The user interface is simple and intuitive, featuring a video panel for real-time capture and two control buttons: “Start” and “Stop”.

2. System Requirements

Before you begin, ensure your system meets the following requirements:

	•	Operating System: Windows, macOS, or Linux
	•	Python Version: 3.7 or higher
	•	Streamlit Version: 1.2.0 or higher
	•	Webcam: Built-in or external webcam
	•	Internet Connection: Required for the initial setup and updates

3. Installation and Setup

Follow these steps to install and set up the application:

	1.	Clone the Repository:
If you haven’t already, clone the repository containing the project code.

git clone https://github.com/keshav165/sign-language-live-transcription
cd your-repository


	2.	Create a Virtual Environment:
It’s recommended to create a virtual environment to manage dependencies.

python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate


	3.	Install Dependencies:
Install the required Python packages by running:

pip install -r requirements.txt


	4.	Run the Application:
Start the Streamlit application with the following command:

streamlit run app.py

This will open the application in your default web browser.

4. Using the Application

Starting the Video Feed

	1.	Launch the Application:
Once the application is running, you will see a simple interface with a video panel and two buttons.
	2.	Start Button:
	•	Click the “Start” button to activate the webcam and begin the real-time video feed.
	•	The video feed will appear in the video panel, and the model will start processing the gestures.

Stopping the Video Feed

	1.	Stop Button:
	•	To stop the video feed, click the “Stop” button.
	•	This will deactivate the webcam and pause the gesture recognition process.

Viewing Predictions

	•	As you perform signs in front of the camera, the model will analyze them and display the corresponding text predictions next to the video panel.
	•	Ensure you perform the signs clearly and within the camera’s view for accurate predictions.

5. Troubleshooting

Here are some common issues and their solutions:

	•	No Video Feed:
	•	Ensure your webcam is properly connected and not being used by another application.
	•	Try refreshing the page or restarting the application.
	•	Incorrect Predictions:
	•	Ensure you are performing the gestures clearly and within the camera’s frame.
	•	The model may require more training data if it consistently fails to recognize certain signs.
	•	Application Not Starting:
	•	Verify that all dependencies are installed correctly.
	•	Check for any error messages in the terminal and resolve them as indicated.

6. FAQs

	•	Can I add more signs to the model?
	•	Yes, you can retrain the model with additional signs and update the application.
	•	Is the application compatible with mobile devices?
	•	Currently, the application is optimized for desktop use. Mobile compatibility may require additional adjustments.
	•	How can I update the application?
	•	Pull the latest changes from the repository and rerun the application.
