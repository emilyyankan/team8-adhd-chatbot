# ADHD Advisor Chatbot

The **ADHD Advisor Chatbot** is designed to help individuals with ADHD by providing tailored, evidence-based advice to manage common challenges like poor time management, forgetfulness, and trouble focusing. Built using Python and Flask, it utilizes Perplexity AI for sourcing information from credible resources and provides an intuitive user interface for seamless interaction.

---

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Launching the Application](#launching-the-application)
- [Admin Dashboard](#admin-dashboard)
---

## Features
- **Personalized Advice**: Tailored responses using credible sources like Healthline and Harvard Health.
- **Real-Time Interaction**: Dynamic responses via Perplexity AI API.
- **Performance Metrics**: Admin dashboard displays user satisfaction, response times, and keyword insights.
- **Secure & Lightweight**: No personal data storage, low memory usage.

---

## Prerequisites
Before setting up the ADHD Advisor chatbot, ensure the following dependencies are installed on your system:

- **Python**: Version 3.13.1 or above. [Download Python](https://www.python.org/downloads/)
- **pip**: Version 24.3.1 or above (comes with most Python installations).
- Required Python Libraries:
  - Flask==2.2.3
  - Flask-CORS==3.0.10
  - requests==2.31.0
  - python-dotenv==1.0.0
  - pandas==2.1.1
  - wordcloud==1.9.2
  - statistics==1.0.3.5

---

## Setup Instructions

### Step 1: Clone the Repository
Clone the project repository from GitHub:
```bash
git clone <repository-link>
cd <project-name>
```
## Step 2: Install Dependencies

Install the required dependencies:

```bash
pip install Flask Flask-CORS requests python-dotenv pandas wordcloud statistics
```
## Step 3: Set Up API Key
Create a `.env` file in the project’s root directory and add your API key:
```bash
API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Replace xxxxxxxxxxxxxxxxxxxxxxxxxxxx with your actual API key.

## Launching the Application
Step 1: Start the Flask Application
Run the application using the following command:
```bash
python app.py
```

Step 2: Access the Chatbot
Once the application is running, open a web browser and navigate to:
```bash
http://127.0.0.1:5000/
```
You will see the chatbot interface where you can start interacting by entering your queries.

## Admin Dashboard
Accessing the Admin Page
To access the admin dashboard, navigate to:
```bash
http://127.0.0.1:5000/admin
```
