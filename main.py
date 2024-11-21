from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import ollama

app = Flask(__name__, template_folder='templates')

# Function to interact with Ollama's AI model
def get_ai_response(prompt: str):
    try:
        # Send a request to the Ollama model and get the response
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

        # Check if the 'message' field is present and contains 'content'
        if "message" in response and "content" in response["message"]:
            ai_reply = response["message"]["content"]
        else:
            ai_reply = f"Error: Missing 'content' field in response. Full response: {response}"
        
        return ai_reply

    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

@app.route("/")
def home():
    # Serves the homepage (homePage.html)
    return render_template("homePage.html")  

@app.route('/static/<path:path>')
def send_static(path):
    # Serve static files
    return send_from_directory('static', path)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("prompt")

    def generate_response():
        for chunk in ollama.chat_stream(model="llama3.2", messages=[{"role": "user", "content": user_input}]):
            yield chunk["content"]

    return Response(generate_response(), content_type="text/plain")

@app.route("/chat-page")
def chat_page():
    # Serves the AI chat page (index.html)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)