import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from extensions import mongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize MongoDB connection
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)
collection = mongo.db.events

@app.route('/')
def index():
    """Render the main UI."""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming GitHub webhooks and store them in MongoDB."""
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        payload = {
            "author": data['pusher']['name'],
            "to_branch": data['ref'].split('/')[-1],
            "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC'),
            "action": "push"
        }
    elif event_type == 'pull_request':
        payload = {
            "author": data['pull_request']['user']['login'],
            "from_branch": data['pull_request']['head']['ref'],
            "to_branch": data['pull_request']['base']['ref'],
            "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC'),
            "action": "pull_request"
        }
    elif event_type == 'pull_request_review':
        if data['pull_request']['merged']:
            payload = {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC'),
                "action": "merge"
            }
        else:
            return jsonify({"message": "Not a merge event"}), 200
    else:
        return jsonify({"message": "Event not handled"}), 400

    collection.insert_one(payload)
    return jsonify({"message": "Event received and stored"}), 200

@app.route('/get-events', methods=['GET'])
def get_events():
    """Retrieve and return all events from MongoDB."""
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG', 'False') == 'True')
