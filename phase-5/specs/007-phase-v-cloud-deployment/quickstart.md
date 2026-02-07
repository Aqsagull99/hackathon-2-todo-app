# Quickstart: Advanced Cloud Deployment of AI-Native Todo Chatbot

## Prerequisites

- Docker and Docker Compose
- kubectl
- Helm
- Dapr CLI
- Minikube (for local development)
- DigitalOcean account with API token
- GitHub account for Actions

## Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install Dapr locally:
   ```bash
   dapr init
   ```

3. Start Minikube:
   ```bash
   minikube start
   ```

4. Install Dapr on Minikube:
   ```bash
   dapr init -k
   ```

5. Set up the development environment:
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ../frontend
   npm install
   ```

## Local Development

1. Start the backend service:
   ```bash
   cd backend
   dapr run --app-id backend --app-port 8000 --dapr-http-port 3500 -- uvicorn main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## Cloud Deployment (DOKS)

1. Configure kubectl for DOKS:
   ```bash
   doctl kubernetes cluster kubeconfig save <cluster-name>
   ```

2. Deploy Dapr to DOKS:
   ```bash
   dapr init -k
   ```

3. Deploy the application using Helm:
   ```bash
   helm install todo-app ./helm-charts/todo-app
   ```

4. Monitor the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   ```

## Configuration

Environment variables needed for the application:

**Backend (.env):**
```
DATABASE_URL=<neon-db-connection-string>
OPENAI_API_KEY=<openai-api-key>
REDPANDA_BROKERS=<redpanda-brokers-list>
DAPR_SIDECAR_HOST=localhost
DAPR_SIDECAR_PORT=3500
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_DAPR_SIDECAR_HOST=localhost
NEXT_PUBLIC_DAPR_SIDECAR_PORT=3500
```

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Troubleshooting

- If Dapr sidecar is not starting, check if Dapr is properly initialized
- If Kafka connection fails, verify Redpanda Cloud configuration
- For Kubernetes deployment issues, check the Dapr placement service is running