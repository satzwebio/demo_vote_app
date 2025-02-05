#!/bin/bash

NAMESPACE="cohesity-demo"

# Check if namespace exists, then delete it
if kubectl get namespace $NAMESPACE >/dev/null 2>&1; then
    echo "Namespace $NAMESPACE exists. Deleting..."
    kubectl delete namespace $NAMESPACE
    echo "Waiting for namespace deletion..."
    sleep 5
fi

# Apply namespace
echo "Creating namespace..."
kubectl apply -f namespace.yaml

# Wait for namespace to be ready
echo "Pausing for namespace to be created..."
sleep 5

# Apply Persistent Volume Claims (PVCs)
kubectl apply -f pvc-block.yaml
kubectl apply -f pvc-fs.yaml

# Apply database-related configurations
kubectl apply -f db-secret.yaml
kubectl apply -f db-config.yaml
kubectl apply -f db-init-config.yaml

# Deploy the StatefulSet and its service
kubectl apply -f db-statefulset.yaml
kubectl apply -f db-service.yaml

# Wait for PostgreSQL to be ready
echo "Waiting for database to initialize..."
sleep 10

# Run the database initialization job
kubectl apply -f db-init-job.yaml

# Deploy the application and its service
kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml

echo "All Kubernetes resources have been applied successfully!"
