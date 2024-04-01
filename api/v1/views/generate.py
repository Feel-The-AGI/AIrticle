"""generate view logic:
- Send topic and keywords from client to GPT-3.5-turbo
- Generate content
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from database import db

load_dotenv()
client = OpenAI()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# BLUEPRINT
from flask import Blueprint
generate = Blueprint('generate', __name__)


# ======================== Generate Article Logic ========================
# Define the generate_article function
def generate_article(topic, keywords, article_length):
    """GPT validation and generation"""
    try:
        length_dict = {
            'short': '500',
            'medium': '1000',
            'long': '2000'
        }
        selected_length = length_dict.get(article_length, '500')

        system_message = (f"Your task is to generate an article on the topic: {topic}. "
            f"Keywords: {', '.join(keywords)}. The article should be informative, engaging, "
            f"and approximately {selected_length} words long. "
            "You must include the following components:\n\n"
            "- A captivating title\n"
            "- An introduction that provides an overview of the topic\n"
            "- A main body, structured with relevant subtopics based on the provided keywords. Do not add explicitly 'Main Body' in your response"
            "Each subtopic should be discussed in detail and do not number them. put the detailed discussion of each point under the point itslef.\n"
            "- A conclusion summarizing the key points and any final thoughts.\n\n"
            "Ensure that the content flows seamlessly and maintains the reader's interest throughout, and stick to the word length. your points are not limited to the keywords")
        user_message = f"{topic} {', '.join(keywords)}"


        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            # max_tokens=int(selected_length),
            temperature=0.7,
            stream=True
        )
        generated_content = ''

        for chunk in response:
            content = chunk.choices[0].delta.content
            generated_content += str(content)

        return generated_content or 'Failed to generate an article.'
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@generate.route('/generate', methods=['POST'])
def generate_content():
    """Get article parameters from client to feed to GPT"""
    try:
        topic = request.form.get('topic')
        keywords = [k.strip() for k in request.form.get('keywords', '').split(',')]
        article_length = request.form.get('article_length')

        generated_article = generate_article(topic, keywords, article_length)

        if generated_article:
            response = jsonify({'generated_article': generated_article})
            return response
        else:
            return render_template('generate.html', generated_article="Failed to generate an article.")
    except Exception as e:
        print(f'Error: {e}')
        return render_template('generate.html', generated_article=f"Error generating article: {e}")


@generate.route('/new_article', strict_slashes=False)
def create_new_article():
    """Create new article"""
    return render_template('generate.html')
