import speech_recognition as sr
from textblob import TextBlob

def transcribe_audio(audio_file):
    """Convert speech to text from an audio file."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Error connecting to speech recognition service."

def analyze_tone(text, mode):
    """Analyze the tone of the text based on the selected mode."""
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity  # -1 to 1 scale
    feedback = ""
    
    if mode == "formal":
        if sentiment_score < -0.3:
            feedback = "Your tone sounds too negative for a formal setting. Try neutral or positive wording."
        elif sentiment_score > 0.3:
            feedback = "Your tone is positive and engaging, suitable for formal communication."
        else:
            feedback = "Your tone is neutral. Ensure clarity and professionalism."
    
    elif mode == "casual":
        if sentiment_score < -0.2:
            feedback = "You sound too serious for a casual conversation. Relax your tone."
        elif sentiment_score > 0.5:
            feedback = "Your tone is friendly and engaging. Well done!"
        else:
            feedback = "Your tone is balanced but could be more expressive."
    
    elif mode == "sales":
        if sentiment_score < 0:
            feedback = "Sales communication should be positive and persuasive. Try to sound more confident."
        elif sentiment_score > 0.4:
            feedback = "Great! Your tone is enthusiastic and persuasive."
        else:
            feedback = "You sound neutral. Try to add more excitement to engage customers."
    
    return feedback

def main():
    audio_path = "whine.wav"  # Replace with actual audio file path
    transcript = transcribe_audio(audio_path)
    if transcript:
        print("Transcript:", transcript)
        mode = "formal"  # Change mode as needed
        feedback = analyze_tone(transcript, mode)
        print("Feedback:", feedback)

if __name__ == "__main__":
    main()
