from flask import Flask, request, jsonify, render_template, redirect, url_for
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import uuid

app = Flask(__name__)

# Dynamo Connection
dynamodb = boto3.resource('dynamodb', region_name='eu-west-2') # London region
table = dynamodb.Table('Workouts')

workouts = []

# Home
@app.route('/')
def home():
    response = table.scan()
    workouts = response.get("Items", [])
    return render_template("index.html", workouts=workouts)

# Add workout
@app.route('/workout', methods=['POST'])
def add_workout():
    data = request.get_json()
    
    if not data or 'exercise' not in data or 'sets' not in data or 'reps' not in data:
        return jsonify({"error:" "You have missed an exercise, set or rep"}), 400
    
    workout_id = str(uuid.uuid4())
    name = request.form["name"]
    duration = request.form["duration"]
    wtype = request.form["type"]
    date = request.form["date"]
    
    # item = {
    #     'userId': data['userId'],
    #     'date': date,
    #     'workoutId': workout_id,
    #     'exercise': data['exercise'],
    #     'sets': str(data['sets']),
    #     'reps': str(data['reps'])
    # }
    
    table.put_item(Item={
        "workoutId": workout_id,
        "name": name,
        "duration": duration,
        "type": wtype,
        "date": date
    })
    
    return redirect(url_for("index"))
    
    # workout = {
    #     "exercise": data['exercise'],
    #     "sets": data['sets'],
    #     "reps": data['reps']
    # }
    
    # workouts.append(workout)
    # return jsonify({"message": "Workout added.", "workout": item}), 201

# Get workout
@app.route('/workouts/<userId>', methods=['GET'])
def get_workout(userId):
    response = table.query(
        KeyConditionExpression=Key('userId').eq(userId)
    )
    return jsonify(response['Items']), 200

# Delete Workout
@app.route('/workout/<userId>/<workoutId>', methods=['DELETE'])
def delete_workout(userId, workoutId):
    response = table.query(
        KeyConditionExpression=Key('userId').eq(userId))
    
    items = response['Items'] 
    target_item = next((item for item in items if item.get('workoutId') == workoutId), None)
    
    if not target_item:
        return jsonify({"error": "Workout not found, enter a valid workout ID"}), 404
    
    table.delete_item(
        Key={
            'userId': userId,
            'date': target_item['date']
        }
    )
    return jsonify({"message": f"Workout {workoutId} deleted"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    print("Hello world")

