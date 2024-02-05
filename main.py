from flask import Flask, request, jsonify
import wikipediaapi
from collections import Counter
import json

# Default topic and top n words
topic_name = "javascript"
n = 5

# Flask application setup
app = Flask(__name__)
wiki_wiki = wikipediaapi.Wikipedia('wikipedia (merlin@example.com)', 'en')

# File to store search history
search_history_file = 'search_history.json'


def load_search_history():
    # Load search history from the file or return an empty list if not found or invalid
    try:
        with open(search_history_file, 'r') as file:
            return json.loads("[" + ",".join(file.readlines()) + "]")
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_search_history(history):
    # Save search history to the file
    with open(search_history_file, 'a') as file:
        # Convert each entry to a string and write to the file
        for entry in history:
            file.write(json.dumps(entry) + ',\n')  # Add a comma and newline after each entry


# Load existing search history or initialize an empty list
search_history = load_search_history()

# Endpoint for counting word frequency
@app.route('/count_word_freq', methods=['GET'])
def word_frequency_analysis():
    # Get the topic from the request parameters
    topic = request.args.get('topic')

    # Retrieve Wikipedia page for the given topic
    page_py = wiki_wiki.page(topic)
    if not page_py.exists():
        return jsonify({"error": "Topic not found"}), 404

    # Process content for word frequency analysis
    content = page_py.text
    words = [word.strip('.,!?"()[]{}') for word in content.lower().split()]
    word_freq = Counter(words)
    top_n_words = dict(word_freq.most_common(n))  # Convert to dictionary

    # Update search history with the current analysis
    search_history.append({"topic": topic_name, "top_words": top_n_words})
    save_search_history(search_history)

    # Format response with indentation for better readability
    response = {"topic": topic_name, "top_words": top_n_words}
    return jsonify(json.loads(json.dumps(response, indent=2)))  # Use json.dumps for indentation


# Endpoint for retrieving search history
@app.route('/search_history', methods=['GET'])
def search_history_endpoint():
    # Check if there is no search history available
    if not search_history:
        return jsonify({"message": "No search history available"})

    # Format search history for response
    formatted_history = [
        {"topic": entry["topic"], "top_words": entry["top_words"]}
        for entry in search_history
    ]

    return jsonify({"search_history": formatted_history})


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
