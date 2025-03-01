from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"
NOTION_API_URL = "https://api.notion.com/v1/pages"

@app.route("/")
def home():
    return "Notion Recipe Uploader is running!"

@app.route("/add-recipe", methods=["POST"])
def add_recipe():
    try:
        data = request.json
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION
        }

        payload = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Recipe Name": {
                    "title": [{"text": {"content": data["name"]}}]
                },
                "Ingredients": {
                    "rich_text": [{"text": {"content": data["ingredients"]}}]
                },
                "Instructions": {
                    "rich_text": [{"text": {"content": data["instructions"]}}]
                },
                "Images": {
                    "files": [{"name": "recipe_image", "external": {"url": data["images"][0]}}]
                },
                "Preparation Time": {
                    "number": data["preparation_time"]
                },
                "Difficulty Level": {
                    "multi_select": [{"name": data["difficulty_level"]}]
                },
                "Chef Notes": {
                    "rich_text": [{"text": {"content": data["chef_notes"]}}]
                }
            }
        }

        response = requests.post(NOTION_API_URL, json=payload, headers=headers)
        notion_response = response.json()

        if response.status_code == 200:
            return jsonify({"message": "Recipe added successfully!", "notion_response": notion_response})
        else:
            return jsonify({"error": "Failed to add recipe", "notion_error": notion_response}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
