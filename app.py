from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import json
import pandas as pd
from wordcloud import WordCloud
import time
import statistics
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='app/static')
CORS(app)

survey_data_path = 'survey_data.json'
responses_log_path = 'responses.log'
response_time_data_path = 'response_time_data.json'

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
    chatbot_instructions = "You are a chatbot with the goal of providing assistance and advice to managing symptoms of ADHD. Your responses should be empathetic with the user's issues and encourage them to take the next steps towards better mental health. All of your responses must advise the user in one of the following categories: time management, focus strategies, emotional regulation, organizational skills, and ADHD-friendly apps or tools. If a user asks any question that doesn't relate to one of these categories, you must say that you are not qualified to answer that question. If a question asked is not related to ADHD, you MUST not give an answer. You are not authorized to give any responses that are not related to ADHD. Under no circumstances will you provide assistance outside of advice with handling ADHD.  Redit and other social media posts can never be used as a source. All information must come from reputable articles and websites. Some reputable sources that must be prioritized when possible are as follows: Healthline, Medical New Today, Calm, GoodRX, Harvard.Health, and Positive Psychology."
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you please repeat?"})
    
    start_time = time.time()  # Start timing
    
    query = chatbot_instructions + " Question: " + user_message
    
    try:
        # Use Perplexity API to get a response
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system", 
                    "content": chatbot_instructions
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "max_tokens": 1000,
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

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        response_data = response.json()

        # Extract the response content
        assistant_response = response_data.get('choices', [{}])[0].get('message', {}).get('content', "I'm not sure how to answer that.")
        assistant_response = clean_response(assistant_response)
        
        # Handle citations
        citations = response_data.get('citations', [])
        if citations:
            citation_map = {f"[{i+1}]": f"{[i+1]}" for i in range(len(citations))}
            assistant_response = append_citations(assistant_response, citation_map)
            assistant_response += "\n\nSources:\n" + "\n".join([f"[{i+1}] {citations[i]}" for i in range(len(citations))])
        
        # End timing
        end_time = time.time()
        response_time = end_time - start_time

        # Track response time
        with open(response_time_data_path, 'a') as rt_file:
            rt_file.write(json.dumps({"time": response_time}) + '\n')
        
        with open(responses_log_path, 'a') as log_file:
            log_file.write(assistant_response + '\n')

        return jsonify({"response": assistant_response})
    except Exception as e:
        print(f"Error during API call: {e}")
        return jsonify({"response": "I'm having trouble processing your request right now. Please try again later."})

@app.route('/survey', methods=['POST'])
def survey():
    survey_data = request.json
    try:
        # Append survey data to the JSON file
        with open(survey_data_path, 'a') as file:
            file.write(json.dumps(survey_data) + '\n')
        return jsonify({"message": "Survey submitted successfully!"})
    except Exception as e:
        return jsonify({"error": "Failed to save survey data."})


@app.route('/admin')
def admin_page():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/survey-results', methods=['GET'])
def survey_results():
    try:
        # Check if the survey data file exists
        if os.path.exists(survey_data_path):
            try:
                # Read JSON file into a DataFrame
                df = pd.read_json(survey_data_path, lines=True)  # Handles JSON Lines format
            except ValueError as e:
                print(f"Error reading JSON file: {e}")
                return jsonify({"error": "Survey data is improperly formatted."})
        else:
            return jsonify({"error": "No survey data file found."})

        # Check if the DataFrame is empty
        if df.empty:
            return jsonify({"error": "No survey data available."})

        # Count responses for each question
        q1_counts = df['q1'].value_counts().to_dict()
        q2_counts = df['q2'].value_counts().to_dict()
        q3_counts = df['q3'].value_counts().to_dict()

        # Return survey counts as JSON
        return jsonify({"q1_counts": q1_counts, "q2_counts": q2_counts, "q3_counts": q3_counts})

    except Exception as e:
        print(f"Error generating survey results: {e}")
        return jsonify({"error": "Failed to generate survey data."})


@app.route('/generate-wordcloud', methods=['GET'])
def generate_wordcloud():
    try:
        # Read responses from log file
        if not os.path.exists(responses_log_path):
            return jsonify({"error": "No responses log found."})

        with open(responses_log_path, 'r') as file:
            text = file.read()

        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        wordcloud_path = os.path.join(app.static_folder, 'wordcloud.png')
        wordcloud.to_file(wordcloud_path)

        # Return path to word cloud image
        return jsonify({"wordcloud_url": "/static/wordcloud.png"})

    except Exception as e:
        return jsonify({"error": "Failed to generate word cloud.", "details": str(e)})
    
@app.route('/response-times', methods=['GET'])
def response_times():
    try:
        response_times = []
        if os.path.exists(response_time_data_path):
            with open(response_time_data_path, 'r') as file:
                for line in file:
                    data = json.loads(line.strip())
                    if "time" in data:
                        response_times.append(data["time"])

        if not response_times:
            return jsonify({"error": "No response time data available."})

        # Compute average response time
        avg_time = statistics.mean(response_times)

        return jsonify({
            "times": response_times, 
            "average_time": avg_time
        })

    except Exception as e:
        print(f"Error generating response times data: {e}")
        return jsonify({"error": "Failed to generate response times data."})    
 

def clean_response(response):
    # Remove markdown headers (###, ##, #)
    response = re.sub(r"^#+\s", "", response, flags=re.MULTILINE)
    # Remove bold/italic syntax (** or *)
    response = re.sub(r"(\*\*|__)(.*?)\1", r"\2", response)
    response = re.sub(r"(\*|_)(.*?)\1", r"\2", response)
    # Remove list markers (-, *)
    response = re.sub(r"^[-*]\s+", "", response, flags=re.MULTILINE)
    return response.strip()

def append_citations(response, citation_map):
    for citation_key, citation_value in citation_map.items():
        response = response.replace(citation_key, citation_value)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)