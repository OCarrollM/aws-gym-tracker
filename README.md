# HyperTrack 

*Built for performance, scalability, and live insights*

---

## Overview
**HyperTrack** is a full-stack project focusing on fitness tracking. A web application designed from the ground up to show end-to-end **DevOps with AWS**.

Users can log workouts, view weekly trends and track statistics seemlessly with more features coming soon.

---

## Features
- **Flask API Backend** hosted on Amazon EC2
- Data logged inside **AWS DynamoDB**.
- **AWS Cloudwatch** metrics published for every workout both added and deleted.
- Logs tracked in Cloudwatch for easy monitoring and debugging.
- A fully automated **CI/CD** pipeline using GitHub Actions.
- Containerised on **Docker** for local development, anywhere, anytime.
- **Interactive Frontend** built using Bootstrap

---

## Architecture


![Architecture Diagram](/GitHubDiagram.png)

---

## Stack background

- **Backend**: Python (using Flask)
- **Database**: AWS DynamoDB
- **Monitoring**: AWS CloudWatch
- **Hosting**: AWS EC2 (Using Docker)
- **CI/CD**: GitHub Actions
- **Frontend**: Bootstrap (HTML, CSS)

---

## Project Structure

```bash
aws-gym-tracker/
├── .github/workflows/
│   └── deploy.yml
├── templates/
│   └── index.html
├── Dockerfile       
├── GitHubDiagram.png  
├── main.py 
├── README.md
└── requirements.txt
```

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

# Install Requirements
pip install -r requirements.txt

# Build Image
docker build -t gymtracker .

# Run Container
docker run -p 8080:8080 gymtracker

# Or run locally
python3 main.py
```

Then visit http://localhost:8080

## Author
Morgan O'Carroll
[LinkedIn](https://www.linkedin.com/in/morganocarroll/)

---

## License
MIT License - Feel free to adapt to your own needs or educational purposes