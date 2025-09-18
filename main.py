from flask import Flask, request, jsonify
import boto3
from datetime import datetime

app = Flask(__name__)

# Dynamo Connection
dynamodb = boto3.resource('dynamodb', region_name='eu-west-2') # London region
table = dynamodb.Table('Workouts')

workouts = []

# Home
@app.route('/')
def home():
    return "Welcome to the Gym Tracker"

# Add workout
@app.route('/workout', methods=['POST'])
def add_workout():
    data = request.get_json()
    
    if not data or 'exercise' not in data or 'sets' not in data or 'reps' not in data:
        return jsonify({"error:" "You have missed an exercise, set or rep"}), 400
    
    date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    item = {
        'userId': data['userId'],
        'date': date,
        'exercise': data['exercise'],
        'sets': str(data['sets']),
        'reps': str(data['reps'])
    }
    
    table.put_item(Item=item)
    
    # workout = {
    #     "exercise": data['exercise'],
    #     "sets": data['sets'],
    #     "reps": data['reps']
    # }
    
    # workouts.append(workout)
    return jsonify({"message": "Workout added.", "workout": item}), 201

# Get workout
@app.route('/workouts', methods=['GET'])
def get_workout(userId):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(userId)
    )
    return jsonify(response['Items']), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
