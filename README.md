# Flask + MongoDB on Kubernetes (Minikube)

A containerized Flask application integrated with MongoDB, deployed on a local Kubernetes cluster using Minikube. The project demonstrates containerization with Docker, database authentication, Kubernetes deployments, persistent storage, Secrets management, and CPU-based Horizontal Pod Autoscaling (HPA).

## 🚀 Project Overview

This project demonstrates how to deploy a Flask web application backed by MongoDB on Kubernetes using Minikube.

The Flask application provides REST API endpoints to interact with MongoDB. MongoDB uses authentication and persistent storage to ensure database security and data retention.

### Key Features

- Flask REST API application.
- MongoDB integration with username and password authentication.
- Docker containerization.
- Kubernetes deployment using Minikube.
- Kubernetes PersistentVolume and PersistentVolumeClaim.
- Kubernetes Secrets for database credentials.
- Kubernetes Services for application and database communication.
- Horizontal Pod Autoscaling (HPA) based on CPU utilization.
- Containerized deployment using Docker Hub.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Backend Framework:** Flask
- **Database:** MongoDB
- **Containerization:** Docker
- **Container Orchestration:** Kubernetes
- **Local Kubernetes Cluster:** Minikube
- **Kubernetes CLI:** kubectl
- **Container Registry:** Docker Hub

## 🏗️ Project Architecture

```text
              User / Browser
                    |
                    v
              Flask Service
                    |
                    v
             Flask Deployment
                    |
                    v
               Flask Pod
                    |
                    v
             MongoDB Service
                    |
                    v
              MongoDB Pod
                    |
                    v
           Persistent Storage
```

## 📁 Project Structure

```text
flask-mongodb-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
│
└── kubernetes/
    ├── mongodb-secret.yaml
    ├── mongodb-pv.yaml
    ├── mongodb-pvc.yaml
    ├── mongodb-deployment.yaml
    ├── mongodb-service.yaml
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    └── flask-hpa.yaml
```

*Update the filenames according to your actual project structure.*

## 📋 Prerequisites

Install the following tools:

1. Docker Desktop
2. Minikube
3. kubectl
4. Python 3.x
5. Docker Hub account

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd flask-mongodb-app
```

## 2. Build and Push Docker Image

Build the Docker image:

```bash
docker build -t pavanvbhavsar2003/flask-mongodb-app:1.1 .
```

Log in to Docker Hub:

```bash
docker login
```

Push the image:

```bash
docker push pavanvbhavsar2003/flask-mongodb-app:1.1
```

Docker Hub Image:

`pavanvbhavsar2003/flask-mongodb-app:1.1`

## 3. Start Minikube

```bash
minikube start --driver=docker
```

Verify the cluster:

```bash
kubectl get nodes
```

## 4. Deploy MongoDB

Apply MongoDB configuration files:

```bash
kubectl apply -f kubernetes/mongodb-secret.yaml
kubectl apply -f kubernetes/mongodb-pv.yaml
kubectl apply -f kubernetes/mongodb-pvc.yaml
kubectl apply -f kubernetes/mongodb-deployment.yaml
kubectl apply -f kubernetes/mongodb-service.yaml
```

Verify MongoDB:

```bash
kubectl get pods
kubectl get services
kubectl get pvc
```

## 5. Deploy Flask Application

```bash
kubectl apply -f kubernetes/flask-deployment.yaml
kubectl apply -f kubernetes/flask-service.yaml
```

Verify deployment:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

## 6. Configure Horizontal Pod Autoscaling

Apply the HPA configuration:

```bash
kubectl apply -f kubernetes/flask-hpa.yaml
```

Check autoscaling status:

```bash
kubectl get hpa
```

For CPU-based autoscaling, ensure the Kubernetes Metrics Server is enabled and resource requests are configured.

```bash
minikube addons enable metrics-server
```

## 7. Access the Application

Get the application URL:

```bash
minikube service flask-service --url
```

Open the generated URL in your browser.

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check application status |
| GET | `/data` | Retrieve data from MongoDB |

*Add POST or other endpoints if they are implemented in your application.*

## 🔍 Testing and Verification

Check running pods:

```bash
kubectl get pods
```

Check services:

```bash
kubectl get svc
```

Check persistent storage:

```bash
kubectl get pv
kubectl get pvc
```

Check application logs:

```bash
kubectl logs deployment/flask-deployment
```

Check MongoDB logs:

```bash
kubectl logs deployment/mongodb
```

Check HPA:

```bash
kubectl get hpa
```

## 🔐 Security

- MongoDB authentication enabled.
- Database credentials managed through Kubernetes Secrets.
- Persistent storage configured for MongoDB.
- Avoid committing actual passwords or sensitive credentials to GitHub.
- Use environment variables to configure database connections.


## 👨‍💻 Author

Pavan Bhavsar


GitHub: https://github.com/pavanvbhavsar2003

## 📄 License

This project is developed for educational and learning purposes. You may add an MIT License if you intend to distribute it under that license.
