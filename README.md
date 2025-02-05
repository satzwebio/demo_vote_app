# Cohesiy Demo Backup

## Overview
This repository contains a demo backup application using Flask and PostgreSQL, designed for real-time interactions and automation. The application architecture includes:

- **Flask-based Python App**: Handles the backend logic and API services.
- **UI**: Connects to the backend and interacts with the PostgreSQL database in real-time.
- **PostgreSQL (StatefulSet)**: Ensures persistence and data reliability.
- **Jobs**:
  - **Database Initialization Job**: Runs at the start to set up the database schema and initial data.
  - **Cron Job**: Generates backup files every 30 seconds.
- **Kubernetes Resources**:
  - **Deployment**: Manages the Flask application instances.
  - **Service Account**: Grants necessary permissions to jobs and pods.
  - **Role & RoleBinding**: Provides the required RBAC for jobs to interact with the cluster.
  - **Services**: Exposes the application for internal and external access.

## Installation
### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Kubernetes](https://kubernetes.io/docs/setup/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/satzwebio/cohesiy_demo_backup.git
   cd cohesiy_demo_backup
   ```
2. Build the Docker image:
   ```sh
   docker build -t yourdockerhubusername/cohesiy_demo_backup:v1 .
   ```
3. Push the image to Docker Hub:
   ```sh
   docker push yourdockerhubusername/cohesiy_demo_backup:v1
   ```
4. Update `deployment.yaml` with the new Docker image tag:
   ```yaml
   spec:
     containers:
       - name: cohesiy-demo-backup
         image: yourdockerhubusername/cohesiy_demo_backup:v1
   ```
5. Deploy the application using the deployment script:
   ```sh
   ./deploy.sh
   ```
6. Forward the service port to access the UI:
   ```sh
   kubectl port-forward svc/demo-backup 32000:8080
   ```
   Access the application at `http://localhost:32000`.

## Contributors
This project is maintained by multiple contributors. See the [Contributors](https://github.com/satzwebio/cohesiy_demo_backup/graphs/contributors) page for details.

## License
This project is open-source. License details will be updated soon.

