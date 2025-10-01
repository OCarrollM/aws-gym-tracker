# HyperTrack - An AWS controlled workout tracker

HyperTrack is a cloud based workout application built using **Flask**, **DynamoDB**, **Docker**, and importantly **AWS**.
Users can log, delete, and view workouts all whilst activity is monitored on AWS dashboards.

---

## Features
- Add, view, and delete workouts via a web interface.
- Data logged inside **AWS DynamoDB**.
- **AWS Cloudwatch** metrics published for every workout both added and deleted.
- Logs tracked in Cloudwatch for easy monitoring and debugging.
- A fully automated **CI/CD** pipeline using GitHub actions which deploys onto **EC2**.
- Containerised on **Docker** for local development, anywhere, anytime.

---

## Architecture

![Architecture Diagram](/architecture.png)

---

## Stack background

- **Backend**: Python (using Flask)
- **Database**: AWS DynamoDB
- **Monitoring**: AWS CloudWatch
- **Hosting**: AWS EC2 (Using Docker)
- **CI/CD**: GitHub Actions
- **Frontend**: Bootstrap (HTML, CSS)

---

## Local setup

To run this project on your own computer, please follow the steps below, ensuring you have the prerequisites described.

### Prerequisites
- Python 3.10 or higher
- Docker & Docker Compose
- AWS Account (for DynamoDB, CloudWatch, and EC2)

Information for working with these can be found at their respective websites.

### Run locally with Docker
```bash
git clone https://github.com/OCarrollM/aws-gym-tracker.git
cd /aws-gym-tracker

# Build Image
docker build -t gymtracker .

# Run Container
docker run -p 8080:8080 gymtracker
```

Then visit http://<localhost>:8080

## Author
Morgan O'Carroll