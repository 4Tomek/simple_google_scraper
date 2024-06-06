from flask import Flask, request, jsonify, render_template
import requests
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)


API_KEY = "AIzaSyBbylccX65EAF8Jy-Xzml_U0EbESEqFXP0"
SEARCH_ENGINE_ID = "34827c9504bea41a9"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.json
        query = data.get("query")

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        logging.info(f"Request URL: {url}")

        response = requests.get(url)

        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Text: {response.text}")

        if response.status_code != 200:
            logging.error(
                f"Google Custom Search API request failed with status code {response.status_code}"
            )
            return jsonify({"error": "Failed to retrieve search results"}), 500

        results = response.json().get("items", [])
        formatted_results = [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "description": item.get("snippet"),
            }
            for item in results
        ]

        return jsonify(formatted_results)

    except Exception as e:
        logging.exception("An error occurred during search")
        return jsonify({"error": "An internal error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True)
