import streamlit as st
import requests


# Function to submit POST request
def submit_request(api_key, audio_url, video_url):
    

    url = "https://api.synclabs.so/lipsync"
    payload = {
        "audioUrl": audio_url,
        "videoUrl": video_url,
        "model": "sync-1.6.0",
        "synergize": True
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

   
    

    if response.status_code == 201:
        response_json = response.json()
        task_id = response_json.get('id')
        st.success(f"Task submitted successfully. Task ID: {task_id}")
        # st.info(f"Execution time: {execution_time:.2f} seconds")
        return task_id
    else:
        st.error(f"Failed to submit request. Status code: {response.status_code}")
        st.text(response.text)
        # st.info(f"Execution time: {execution_time:.2f} seconds")
        return None

# Function to fetch video URL using GET request
def fetch_video_url(api_key, task_id):
    

    url = f"https://api.synclabs.so/lipsync/{task_id}"
    headers = {"x-api-key": api_key}

    response = requests.request("GET", url, headers=headers)

    

    if response.status_code == 200:
        response_json = response.json()
        video_url = response_json.get('url')
        # st.success("Video processing complete.")
        st.text(f"Video URL: {video_url}")
        # st.info(f"Execution time: {execution_time:.2f} seconds")
    else:
        st.error(f"Failed to fetch video URL. Status code: {response.status_code}")
        st.text(response.text)
        # st.info(f"Execution time: {execution_time:.2f} seconds")

# Streamlit app interface
def main():
    st.title("Lipsync Task Management")

    # Input for API key
    api_key = st.text_input("Enter API Key", type="password")

    st.header("Submit Lipsync Task")
    audio_url = st.text_input("Enter Audio URL (MP3)")
    video_url = st.text_input("Enter Video URL (MP4)")

    if st.button("Submit Task"):
        if api_key.strip() == "":
            st.warning("Please enter an API key.")
        elif audio_url.strip() == "" or video_url.strip() == "":
            st.warning("Please enter both audio and video URLs.")
        else:
            st.info(f"Audio URL: {audio_url}")
            st.info(f"Video URL: {video_url}")
            task_id = submit_request(api_key, audio_url, video_url)

    st.header("Check Task Status and Get Video URL")
    st.info("Enter the task ID obtained after submitting the lipsync task.")
    task_id_input = st.text_input("Task ID")

    if st.button("Fetch Video URL"):
        if api_key.strip() == "":
            st.warning("Please enter an API key.")
        elif task_id_input.strip() == "":
            st.warning("Please enter a task ID.")
        else:
            fetch_video_url(api_key, task_id_input)

if __name__ == "__main__":
    main()
