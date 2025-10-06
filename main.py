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
    
    total_workouts = len(workouts)
    total_duration = sum(int(w.get("duration", 0)) for w in workouts)
    avg_duration = round(total_duration / total_workouts, 1) for total_workouts else 0
    
    now = datetime.now()
    workouts_this_week = sum(1 for w in workouts if "date" in w and (now - datetime.strptime(w["date"], "%Y-%m-%d")).days <= 7)
    
    return render_template("index.html",
                           workouts=workouts,
                           total_workouts = total_workouts,
                           avg_duration = avg_duration,
                           workouts_this_week = workouts_this_week)

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
    publish_delete_metric()
    return redirect(url_for("home"))

def publish_delete_metric():
    cloudwatch.put_metric_data(
        Namespace='GymTracker',
        MetricData=[
            {
                'MetricName': 'WorkoutsDeleted',
                'Value': 1,
                'Unit': 'Count'
            }
        ]
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    print("Hello world")

# Next steps

# 1 - Polish front end
# 2 - Change production, move secrects, flask server move, ACM certificate
# 3 - Scaling with AWS
# 4 - Polish