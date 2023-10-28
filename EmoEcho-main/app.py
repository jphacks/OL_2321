from flask import Flask, render_template, request, jsonify
import openai
import os
import re
import json

app = Flask(__name__)
CONVERSATION_FILE = 'conversation.json'

def save_conversation():
    with open(CONVERSATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# Set your OpenAI API key
openai.api_key = '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'

# Initialize the conversation with the system role
messages = [
    {
        "role": "system",
        "content": '''You are a virtual interviewer. Your main role is to ask relevant questions based on the user's responses and provide feedback. Please use Japanese for all of your responses. 

Example 1: If the user starts with introducing themselves for a job interview, you might ask, "Can you please tell me about your past work experience?"
Example 2: If the user talks about their technical experience, you might ask, "What challenges did you face in your last project and how did you overcome them?"

Keep each response concise and to the point. Your primary role is to facilitate the interview and gather relevant information from the candidate.'''
    }
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['POST'])
def message():
    global messages
    data = request.get_json()
    user_message = data.get('message')
    messages.append({"role": "user", "content": user_message})

    ai_message = ""
    try:
        completions_generator = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        # Handle streamed responses; combine content chunks
        for chunk in completions_generator:
            content_chunk = chunk.get('choices', [{}])[0].get('delta', {}).get('content', "")
            ai_message += content_chunk

        # Formatting the response
        ai_message = ai_message.replace('\n', '<br/>')  # New line formatting

        messages.append({"role": "assistant", "content": ai_message})
    except Exception as e:
        ai_message = "Error: " + str(e)

    return jsonify({'message': ai_message})

@app.route('/end_interview', methods=['POST'])
def end_interview():
    global messages
    save_conversation()
    # Optionally, clear the messages or do other housekeeping
    messages = [messages[0]]  # Reset to just the system message
    return jsonify({'status': 'success', 'message': 'Conversation saved!'})

if __name__ == '__main__':
    app.run(debug=True)
