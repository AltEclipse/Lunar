import os
import openai # type: ignore
from googletrans import Translator # type: ignore
from langdetect import detect # type: ignore
import openai # type: ignore
import json

# Environment variables
openai_api_key = os.getenv('openai key here')

# Initialize services
translator = Translator(service_urls=['translate.google.com'])
openai.api_key = openai_api_key

# In-memory storage for session-based memory
memory = {}

# Load memory from file
def load_memory():
    global memory
    try:
        if os.path.exists("memory.json"):
            with open("memory.json", "r") as file:
                memory = json.load(file)
    except Exception as e:
        print(f"Failed to load memory from file: {e}")

# Save memory to file
def save_memory():
    try:
        with open("memory.json", "w") as file:
            json.dump(memory, file)
    except Exception as e:
        print(f"Failed to save memory to file: {e}")

# Function to detect the language of the text
def detect_lang(text):
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection failed: {e}")
        return "unknown"

# Function to translate text to target language
def translate_text(text, target_lang):
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

# Function to generate AI response using OpenAI
def generate_response(prompt, user_id):
    try:
        # Retrieve user's conversation history from memory
        user_history = memory.get(user_id, "")

        # Append the new prompt to the user's history
        user_history += f"\nUser: {prompt}\nBot:"

        # Generate a response using OpenAI's API
        response = openai.Completion.create(
            engine="davinci",
            prompt=user_history,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()

        # Update the user's conversation history in memory
        user_history += bot_response
        memory[user_id] = user_history

        return bot_response
    except Exception as e:
        print(f"Failed to generate AI response: {e}")
        return "Sorry, I couldn't understand what you said."

# Load memory
load_memory()

# Example usage
if __name__ == "__main__":
    user_id = "test_user"

    while True:
        print("\nOptions:")
        print("1. Chat with AI")
        print("2. Translate text")
        print("3. Detect language")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                prompt = input("You: ")
                response = generate_response(prompt, user_id)
                print(f"Bot: {response}")
                save_memory()
            except Exception as e:
                print(f"Error during conversation: {e}")

        elif choice == "2":
            try:
                text_to_translate = input("Enter text to translate: ")
                target_lang = input("Enter target language (e.g., 'en' for English, 'fr' for French): ")
                translated_text = translate_text(text_to_translate, target_lang)
                if translated_text:
                    print(f"Translated text: {translated_text}")
                else:
                    print("Failed to translate text.")
            except Exception as e:
                print(f"Error during translation: {e}")

        elif choice == "3":
            try:
                text = input("Enter text to detect language: ")
                language = detect_lang(text)
                print(f"Detected language: {language}")
            except Exception as e:
                print(f"Error during language detection: {e}")

        elif choice == "4":
            try:
                save_memory()
                print("Memory saved successfully. Exiting...")
                break
            except Exception as e:
                print(f"Error during saving memory: {e}")

        else:
            print("Invalid choice. Please try again.")
