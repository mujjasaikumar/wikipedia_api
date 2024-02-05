Word Frequency Analyzer API Documentation

Overview:
This API provides endpoints for analyzing the word frequency of a given topic on Wikipedia and maintaining a search history.

Endpoints:

1. Count Word Frequency
        Endpoint: /count_word_freq
        Method: GET
        Parameters:
                topic: The topic for which word frequency needs to be analyzed. (e.g., /count_word_freq?topic=python)
                Response:
                        If the topic is found on Wikipedia, it returns a JSON response containing the top N words and updates the search history.
                        If the topic is not found, it returns a JSON error response.
2. Search History
        Endpoint: /search_history
        Method: GET
        Response:
                Returns a JSON response containing the search history, including topics and their top words.
                If there is no search history, it returns a message indicating that no search history is available.

Example Usage:
curl -X GET "http://localhost:5000/count_word_freq?topic=python"
Response:
        {
          "topic": "python",
          "top_words": {
            "programming": 15,
            "language": 12,
            "pythonic": 8,
            "community": 7,
            "libraries": 6
          }
        }


Get Search History:
curl -X GET "http://localhost:5000/search_history"
Response:
        {
          "search_history": [
                {
              "topic": "python",
              "top_words": {
                "programming": 15,
                "language": 12,
                "pythonic": 8,
                "community": 7,
                "libraries": 6
              }
            },
            {
              "topic": "javascript",
              "top_words": {
                "web": 18,
                "language": 15,
                "javascript": 12,
                "frameworks": 9,
                "frontend": 8
              }
            }
          ]
        }
        
Search History File:
The search history is stored in a JSON file named search_history.json. Each entry in the file contains the topic and its corresponding top words.

Important Notes
Ensure that the Flask application is running (app.run(debug=True)) before making API requests.
Topics are case-sensitive; provide the topic parameter in lowercase for consistency.
