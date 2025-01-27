# brat - Virtual Assistant

brat is a locally hosted virtual assistant designed to help with various tasks, including answering queries, retrieving information, and interacting in a conversational manner. It combines speech recognition, text-to-speech, memory storage, and AI-generated responses for a seamless user experience.

## Features

1. **Speech-to-Text**: Uses `speech_recognition` to process voice commands.
2. **Text-to-Speech**: Provides responses with `pyttsx3` using different tones.
3. **Memory Management**: Stores and recalls interactions in an SQLite database.
4. **AI-Powered Responses**: Generates contextual responses using GPT-Neo 2.7B from the Transformers library.
5. **Web Search**: Performs DuckDuckGo searches for unanswered queries.
6. **Customizable Interaction**: Adjusts responses based on user preferences and tone settings.

## Prerequisites

- Python 3.8 or higher
- A working microphone

### Required Libraries
Install the dependencies using:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `speech_recognition`
- `pyttsx3`
- `requests`
- `sqlite3` (built-in with Python)
- `nltk`
- `transformers`
- `torch`
- `asyncio`

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download GPT-Neo 2.7B model**:
   The model is loaded via the Transformers library. Ensure you have enough disk space and memory to use the model efficiently.

4. **Initialize the Database**:
   The database is automatically initialized when you run the assistant for the first time. It creates tables for storing memory and user preferences.

## Usage

1. **Run the Assistant**:
   ```bash
   python <script_name>.py
   ```

2. Speak your command when prompted:
   brat listens and processes your voice input to perform tasks such as answering questions, searching the web, or generating AI-powered responses.

3. **Examples of Commands**:
   - "What is the capital of France?"
   - "Search for the history of black holes."
   - "Tell me about yourself."

## Project Structure

- `assistant_memory.db`: SQLite database for storing memory and user preferences.
- `<script_name>.py`: Main script containing the assistant's logic.
- `requirements.txt`: List of dependencies for the project.

## Customization

1. **Adjust Speech Tone**:
   Modify the `tone` parameter in the `speak()` function to change how brat interacts (e.g., `friendly`, `neutral`, `formal`).

2. **Refine Queries**:
   The `refine_query()` function can be updated to add or modify common phrases for refining user queries.

## Troubleshooting

- **Speech Recognition Errors**: Ensure your microphone is functioning correctly and the environment is free of excessive noise.
- **Memory Storage Issues**: Check the SQLite database file for integrity and ensure write permissions.
- **Performance Issues**: Running GPT-Neo 2.7B requires significant hardware resources. Consider using a smaller model if performance is a concern.

## Contributions

Feel free to submit issues and pull requests for improvements or new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Enjoy using brat, your personalized AI assistant!

