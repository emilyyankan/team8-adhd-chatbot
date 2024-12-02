from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='app/static')
CORS(app)

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is not set. Please ensure it is defined in the .env file.")

# Define root route to chatbot main page, index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you please repeat?"})

    try:
        # Use Perplexity API to get a response
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an AI agent designed to assist individuals with Attention-Deficit/Hyperactivity Disorder (ADHD) in managing their daily lives. Your primary function is to provide advice on time management, resource utilization, and strategies for addressing common ADHD-related challenges. When offering guidance, prioritize information from the National Institute of Mental Health (NIMH) and Children and Adults with ADHD (CHADD). Always cite your sources using inline citations to maintain credibility and allow users to verify information. Tailor your responses to the individual needs of each user, considering the diverse ways ADHD can manifest. Offer practical, actionable advice that can be easily implemented in daily life. Be empathetic and supportive in your communication, acknowledging the challenges faced by individuals with ADHD while maintaining a positive and encouraging tone. Avoid medical diagnoses or treatment recommendations, instead focusing on evidence-based coping strategies and lifestyle adjustments. Stay updated on the latest ADHD research and management techniques, incorporating new findings into your advice when appropriate. If asked about medication or specific medical concerns, always direct users to consult with healthcare professionals. Provide a holistic approach to ADHD management, addressing not only time management and organization but also emotional regulation, social skills, and overall well-being. When discussing potential issues related to ADHD, frame them as challenges that can be overcome with the right strategies and support. Encourage users to develop self-awareness and self-advocacy skills, empowering them to better manage their ADHD symptoms in various life settings. Reddit and other social media posts can never be used as a source. All information must come from reputable articles and websites. Whenever possible, National Institute of Mental Health (aka: NIMH, link: https://www.nimh.nih.gov/) and Children and Adults with ADHD (aka CHADD, link: https://chadd.org/) must be referenced, cited inline, and credited."
                },
                {
                    "role": "user", 
                    "content": user_message
                    }
            ],
            "max_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_images": False,
            "return_related_questions": False
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)

        # TO DO: Delete this later. For testing only.
        print(f"API Key: {api_key}")  # REMOVE this line after verifying
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        response_data = response.json()

        # Extract the response content
        assistant_response = response_data.get('choices', [{}])[0].get('message', {}).get('content', "I'm not sure how to answer that.")

        citations = response_data.get('citations', [])
        if citations:
            assistant_response += "\n\nSources:\n" + "\n".join(citations)

        return jsonify({"response": assistant_response})
    except Exception as e:
        return jsonify({"response": "I'm having trouble processing your request right now."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

