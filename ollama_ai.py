import ollama

# Memory storage for interaction history
interaction_history = []

# Function to interact with Ollama's AI model
def get_ai_response(prompt: str):
    try:
        # Only include a short context or recent interactions to reduce overhead
        context_window = 3  # Adjust based on desired history depth
        messages = [{"role": "system", "content": "You are a helpful AI."}]
        for interaction in interaction_history[-context_window:]:
            messages.append({"role": "user", "content": interaction["user"]})
            messages.append({"role": "assistant", "content": interaction["ai"]})
        
        # Add the current prompt
        messages.append({"role": "user", "content": prompt})

        # Send a request to the Ollama model and fetch the response
        response = ollama.chat(model="mistral-nemo:12b", messages=messages)

        # Extract and validate the AI's reply
        ai_reply = response.get("message", {}).get("content", "Error: No valid response received.")
        
        # Update the interaction history
        interaction_history.append({"user": prompt, "ai": ai_reply})
        
        return ai_reply

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    while True:
        prompt = input("Enter a prompt for the AI (or 'exit' to quit): ")
        if prompt.lower() == "exit":
            break
        response = get_ai_response(prompt)
        print(f"AI Response: {response}")