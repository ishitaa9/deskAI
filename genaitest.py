import os
import google.generativeai as genai
from config import gemini_api_key

# Set up the Gemini API client
genai.configure(api_key=gemini_api_key)

# Generation configuration (fine-tune settings if needed)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model for the conversation
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # You can change to a different model if necessary
    generation_config=generation_config,
)

# Start a new chat session with an empty history
chat_session = model.start_chat(history=[])

print("Chat with Gemini AI started! Type 'exit' to end the conversation.\n")

# Loop to keep the conversation going
while True:
    # Get user input
    user_input = input("You: ")

    # If user types 'exit', break the loop and end the conversation
    if user_input.lower() == "exit":
        print("Ending the conversation. Goodbye!")
        break

    # Add the user input to the conversation history
    chat_session.history.append({
        "role": "user",
        "parts": [user_input],
    })

    # Send the message to the model
    response = chat_session.send_message(user_input)

    # Print the AI's response
    print(f"Gemini: {response.text}\n")

    # Optionally, you could append the model's response to history if you want context for future inputs
    chat_session.history.append({
        "role": "model",
        "parts": [response.text],
    })
