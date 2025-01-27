import speech_recognition as sr
import pyttsx3
import requests
import sqlite3
import asyncio
from nltk.tokenize import word_tokenize
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Initialize GPT-Neo 2.7B model and tokenizer (loaded only once)
model_name = "EleutherAI/gpt-neo-2.7B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Initialize TTS engine globally
engine = pyttsx3.init()

# Initialize database connection
def create_memory_db():
    with sqlite3.connect('assistant_memory.db') as conn:
        c = conn.cursor()

        # Create memory table if not exists
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS memory (
                question TEXT PRIMARY KEY,
                answer TEXT,
                source TEXT
            )
        ''')

        # Create user preferences table if not exists
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS user_preferences (
                name TEXT,
                tone TEXT
            )
        ''')

        conn.commit()

# Save interaction to memory
def save_interaction(question, answer, source="Unknown"):
    with sqlite3.connect('assistant_memory.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO memory (question, answer, source) VALUES (?, ?, ?)", (question, answer, source))
        conn.commit()

# Retrieve answer from memory
def recall_answer(question):
    with sqlite3.connect('assistant_memory.db') as conn:
        c = conn.cursor()
        c.execute("SELECT answer FROM memory WHERE question=?", (question,))
        result = c.fetchone()
        return result[0] if result else None

# Speech-to-Text (with better timeout handling)
def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("brat is listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
            return None

    try:
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        return command.lower()
    except Exception as e:
        print(f"Error in recognition: {e}")
        return None

# Text-to-Speech (with tone adjustments)
def speak(text, tone="neutral"):
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1)

    voices = engine.getProperty('voices')
    if tone == "friendly":
        engine.setProperty('voice', voices[1].id)
    elif tone == "formal":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    engine.say(text)
    engine.runAndWait()

# DuckDuckGo search for unknown queries
def duckduckgo_search(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        results = response.json().get('RelatedTopics', [])
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error with DuckDuckGo search: {e}")
        return []

# Refine queries before searching
def refine_query(query):
    common_phrases = ["tell me about", "information on", "what is", "what are", "how does", "features of", "reviews of", "details of"]
    for phrase in common_phrases:
        if phrase in query:
            query = query.replace(phrase, "information on")
    return query

# Generate response using GPT-Neo asynchronously
async def generate_response_with_gpt_neo(prompt):
    # Use a smaller max_length to speed up generation
    response = generator(prompt, max_length=80, num_return_sequences=1, truncation=True)
    return response[0]['generated_text'] if response else "Sorry, I couldn't generate a response."

# Process the command to determine intent and trigger actions
def process_command(command):
    basic_questions = ["who are you", "what do you know about me", "who is brat", "what is your name", "how are you"]
    
    # Handle basic questions directly
    if command in basic_questions:
        speak("I am brat, your virtual assistant. How can I help you today?", tone="friendly")
        return "basic", None
    
    # Identify search queries
    if "search" in command or "find" in command or "look up" in command:
        return "search", refine_query(command)

    # If no basic action identified, use GPT-Neo
    return "unknown", command

# Main Loop (async)
async def main():
    create_memory_db()  # Ensure the database is ready

    speak("Hey, I'm brat! How can I help you today?", tone="friendly")

    while True:
        command = listen_for_commands()
        if command:
            action_type, action_data = process_command(command)

            if action_type == "search":
                results = duckduckgo_search(action_data)
                if results:
                    speak(f"I found this information on {action_data}:")
                    for result in results[:3]:
                        speak(result.get('Text', ''), tone="friendly")
                else:
                    speak(f"Sorry, I couldn't find anything about {command}.")
            
            elif action_type == "unknown":
                # Using asyncio to handle longer responses from GPT-Neo without blocking
                response = await generate_response_with_gpt_neo(command)
                speak(response, tone="neutral")
            else:
                continue

if __name__ == "__main__":
    asyncio.run(main())  # Run the main function asynchronously
