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
    avg_duration = round(total_duration / total_workouts, 1) if total_workouts else 0
    
    now = datetime.now()
    
    workouts_this_week = 0
    for w in workouts:
        if "date" in w:
            try:
                w_date = datetime.strptime(w["date"], "%Y-%m-%d")
            except ValueError:
                w_date = datetime.strptime(w["date"], "%Y-%m-%d %H:%M:%S")
            
            if(now - w_date).days <= 7:
                workouts_this_week += 1
    
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

# Live metrics yippeee! Arrow would never do this...
@app.route('/api/metrics/workouts')
def workouts_chart_data():
    response = table.scan()
    workouts = response.get("Items", [])

    now = datetime.now()
    counts = {}
    
    for w in workouts:
        w_date_str = w.get("date")
        if not w_date_str or not isinstance(w_date_str, str):
            continue

        try:
            w_date = datetime.strptime(w_date_str.split()[0], "%Y-%m-%d")
        except ValueError:
            continue
        
        if (now - w_date).days <= 7:
            key = w_date.strftime("%Y-%m-%d")
            counts[key] = counts.get(key, 0) + 1
    
    sorted_dates = sorted(counts.keys())
    chart_data = {
        "dates": sorted_dates,
        "values": [counts[d] for d in sorted_dates]
    }
    
    return jsonify(chart_data)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    print("Hello world")

# Next steps

# 1. Documentation & Professional Presentation

# TODO Tasks:
# Update README

    #! Screenshots of the dashboard + chart !
    #! “Architecture Overview” section (maybe make into a gif?)
    #! Deployment flow diagram (GitHub → EC2 → Docker → CloudWatch)
    #! Live metrics demo screenshots from CloudWatch
    #! Add a “Tech Stack” badge section
    #! Add a step-by-step setup guide (local run + AWS deploy)
    #! Add a short “Why I built this” paragraph (ties back to Amazon)

# 2. Polishing the Frontend (make it feel like a dashboard)

    #! A summary card at the top (total workouts this week, average duration, etc.)
    #! Filter dropdowns (e.g., show only “Cardio” or “Weights”)
    #! A theme toggle (lmao)
    #! A small logo or favicon

# 3. Advanced DevOps 

    #! Host your Docker image in ECR (Amazon Elastic Container Registry)
    #! Deploy via ECS or Elastic Beanstalk
    #! Add IAM best practices
    #! Connect CloudWatch Dashboard


# 4. Optional extras 

    #! Add user accounts
    #! Add API Gateway + Lambda backend instead of Flask 
    #! Create custom CloudWatch alarms 