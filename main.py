from flask import Flask, request, jsonify, render_template, redirect, url_for
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import uuid

app = Flask(__name__)

# Dynamo Connection
dynamodb = boto3.resource('dynamodb', region_name='eu-west-2') # London region
table = dynamodb.Table('Workouts')
cloudwatch = boto3.client('cloudwatch', region_name='eu-west-2')

workouts = []

# Home
@app.route('/')
def home():
    response = table.scan()
    workouts = response.get("Items", [])
    return render_template("index.html", workouts=workouts)

# Add workout
@app.route('/add', methods=['POST'])
def add_workout():    
    workout_id = str(uuid.uuid4())
    name = request.form["name"]
    duration = request.form["duration"]
    wtype = request.form["type"]
    date = request.form["date"]
    
    table.put_item(Item={
        "userId": "default-user",
        "workoutId": workout_id,
        "name": name,
        "duration": duration,
        "type": wtype,
        "date": date
    })
    
    publish_workout_metric()
    
    return redirect(url_for("home"))
    
def publish_workout_metric():
    cloudwatch.put_metric_data(
        Namespace='GymTracker',
        MetricData=[
            {
                'MetricName': 'WorkoutsAdded',
                'Value': 1,
                'Unit': 'Count'
            },
        ]
    )

# Get workout
@app.route('/workouts/<userId>', methods=['GET'])
def get_workout(userId):
    response = table.query(
        KeyConditionExpression=Key('userId').eq(userId)
    )
    return jsonify(response['Items']), 200

# Delete Workout
@app.route('/delete/<workoutId>/<date>', methods=['POST'])
def delete_workout(workoutId, date):
    table.delete_item(
        Key={
            'userId': "default-user",
            'date': date
        }
    )
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    print("Hello world")

