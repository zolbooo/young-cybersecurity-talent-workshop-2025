# /// script
# dependencies = [
#   "flask",
#   "pymongo"
# ]
# ///
import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB setup
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/ctfdb")
client = MongoClient(MONGO_URI)
db = client.get_database()
flags_collection = db.flags

# Initialize flag
if flags_collection.count_documents({}) == 0:
    flags_collection.insert_one({"flag": "ctf{n0sql_injection_is_fun}"})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/check_flag", methods=["POST"])
def check_flag():
    try:
        # Expecting JSON data
        data = request.get_json()
        if not data or "flag" not in data:
            return jsonify({"message": "Missing flag in request"}), 400

        user_input = data["flag"]

        # Vulnerable query: passing user input directly to the query
        # If user_input is a dictionary like {"$ne": "wrong"}, it will bypass the check
        query = {"flag": user_input}

        result = flags_collection.find_one(query)

        if result:
            return jsonify({"message": "Correct! You found the flag."}), 200
        else:
            return jsonify({"message": "Incorrect. Try again."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
