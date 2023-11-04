import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import openai
# Note Eleven labs requires ffmpeg as of now, can't be bothered with that right now

def listen():
    # Initialize recognizer
    r = sr.Recognizer()

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print("Talk to me:")
        audio = r.listen(source)

        try:
            # Recognize the speech
            text = r.recognize_google(audio)
            print("Working")
            print(f"You said: {text}")
            return text

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None


# Load your API key from an environment variable or other secure location
openai_api_key = '' 

openai.api_key = openai_api_key

def ask_butler(prompt, temperature=0.7):
    """
    Send a prompt to the OpenAI API and get a response in the style of a polite British Butler.
    
    :param prompt: str - The prompt to send to the API.
    :param temperature: float - Controls the randomness of the output (lower is more deterministic).
    :return: str - The API's text response.
    """

    try:
        # Adding British Butler-like phrases to the prompt to guide the style of the response
        styled_prompt = (
            "As a highly sophisticated and polite British Butler, you address all inquiries with the utmost respect and decorum. "
            "Your responses are articulate, composed, and imbued with a touch of British politeness and wit. "
            f"{prompt}"
        )

        # Call the OpenAI API
        response = openai.Completion.create(
            engine="davinci",  # You can specify other engines as needed.
            prompt=styled_prompt,
            max_tokens=150,
            temperature=temperature,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the text of the response
        response_text = response.choices[0].text.strip()

        return response_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Example usage
prompt = "Could you kindly inform me of the weather today?"
response = ask_butler(prompt)
print(response)
