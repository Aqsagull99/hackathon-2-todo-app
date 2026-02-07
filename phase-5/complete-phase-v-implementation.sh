#!/bin/bash
# Phase V Complete Implementation Script
# Run this to create all remaining Phase V files

set -e  # Exit on error

PROJECT_ROOT="/home/aqsagulllinux/projects/hackathon-2-todo-app"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "  Phase V Implementation Script"
echo "=========================================="
echo ""

# Phase 6: Create Event System
echo "📦 Phase 6: Creating Event System..."

mkdir -p phase-2/backend/app/events

# publisher.py
cat > phase-2/backend/app/events/publisher.py << 'EOF'
"""Event Publisher for Dapr/Kafka integration."""
import httpx
from datetime import datetime
from typing import Dict, Any

DAPR_HTTP_PORT = 3500
PUBSUB_NAME = "kafka-pubsub"

async def publish_task_event(topic: str, event_type: str, task_data: Dict[str, Any]):
    """Publish task event to Kafka via Dapr."""
    event = {
        "event_type": event_type,
        "task_data": task_data,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "todo-backend"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/{topic}",
            json=event
        )
        return response.json() if response.status_code == 200 else None
EOF

# consumer.py
cat > phase-2/backend/app/events/consumer.py << 'EOF'
"""Event Consumer for Dapr callbacks."""
from fastapi import APIRouter, Request
from app.events.handlers import on_task_completed, on_task_due_soon

router = APIRouter(prefix="/events")

@router.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription endpoint."""
    return [
        {"pubsubname": "kafka-pubsub", "topic": "task-events", "route": "/events/task/completed"},
        {"pubsubname": "kafka-pubsub", "topic": "task-reminders", "route": "/events/task/due-soon"},
    ]

@router.post("/task/completed")
async def task_completed_handler(request: Request):
    """Handle task completed events."""
    data = await request.json()
    await on_task_completed(data.get("data", {}))
    return {"status": "SUCCESS"}

@router.post("/task/due-soon")
async def task_due_soon_handler(request: Request):
    """Handle task due soon events."""
    data = await request.json()
    await on_task_due_soon(data.get("data", {}))
    return {"status": "SUCCESS"}

@router.post("/cron/reminder-check")
async def cron_reminder_check(request: Request):
    """Cron-triggered reminder check."""
    from app.core.database import async_session_maker
    from app.services.reminders import check_due_reminders
    async with async_session_maker() as session:
        reminders = await check_due_reminders(session)
        for reminder in reminders:
            await on_task_due_soon({"task_id": reminder.task_id})
    return {"status": "SUCCESS", "reminders_sent": len(reminders)}
EOF

# handlers.py
cat > phase-2/backend/app/events/handlers.py << 'EOF'
"""Event Handlers for business logic."""
from typing import Dict, Any

async def on_task_completed(event_data: Dict[str, Any]):
    """Handle task completed event - spawn next recurring."""
    from app.core.database import async_session_maker
    from app.services.recurring_tasks import spawn_next_occurrence

    task_id = event_data.get("task_data", {}).get("id")
    if task_id:
        async with async_session_maker() as session:
            await spawn_next_occurrence(session, task_id)

async def on_task_due_soon(event_data: Dict[str, Any]):
    """Handle task due soon event - send reminder."""
    from app.core.database import async_session_maker
    from app.services.reminders import send_reminder_notification

    task_data = event_data.get("task_data", {})
    task_id = task_data.get("id")
    user_id = task_data.get("user_id")

    if task_id and user_id:
        async with async_session_maker() as session:
            await send_reminder_notification(session, task_id, user_id)
EOF

# __init__.py
cat > phase-2/backend/app/events/__init__.py << 'EOF'
"""Event system module."""
from app.events.publisher import publish_task_event
from app.events.consumer import router as event_router

__all__ = ["publish_task_event", "event_router"]
EOF

echo "✅ Event system created (4 files)"

# Phase 6: Create Dapr Components
echo "📦 Phase 6: Creating Dapr Components..."

# pubsub-kafka.yaml
cat > phase-4/helm/dapr-components/pubsub-kafka.yaml << 'EOF'
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      secretKeyRef:
        name: kafka-credentials
        key: bootstrap-servers
    - name: consumerGroup
      value: "todo-app-group"
    - name: clientId
      value: "todo-backend-client"
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: kafka-credentials
        key: username
    - name: saslPassword
      secretKeyRef:
        name: kafka-credentials
        key: password
    - name: saslMechanism
      value: "SCRAM-SHA-256"
    - name: securityProtocol
      value: "SASL_SSL"
EOF

# state-postgres.yaml
cat > phase-4/helm/dapr-components/state-postgres.yaml << 'EOF'
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: database-credentials
        key: connection-string
    - name: tableName
      value: "dapr_state"
    - name: metadataTableName
      value: "dapr_metadata"
    - name: cleanupIntervalInSeconds
      value: "3600"
EOF

# bindings-cron.yaml
cat > phase-4/helm/dapr-components/bindings-cron.yaml << 'EOF'
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
  namespace: default
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "*/5 * * * *"
    - name: direction
      value: "input"
EOF

# secrets-kubernetes.yaml
cat > phase-4/helm/dapr-components/secrets-kubernetes.yaml << 'EOF'
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
EOF

# Chart.yaml
cat > phase-4/helm/dapr-components/Chart.yaml << 'EOF'
apiVersion: v2
name: dapr-components
version: 0.1.0
description: Dapr components for Todo App Phase V
type: application
keywords:
  - dapr
  - pub-sub
  - state-store
  - kafka
  - postgresql
  - event-driven
EOF

echo "✅ Dapr components created (5 files)"

# Phase 7: Create Helm Values Files
echo "📦 Phase 7: Creating Helm Values Files..."

# Backend values-minikube.yaml
cat > phase-4/helm/todo-backend/values-minikube.yaml << 'EOF'
replicaCount: 1

image:
  repository: todo-backend
  pullPolicy: Never
  tag: "latest"

service:
  type: NodePort
  port: 80
  targetPort: 8000

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

dapr:
  enabled: true
  appId: "todo-backend"
  appPort: "8000"
  logLevel: "debug"

database:
  deployLocal: false
  host: "host.minikube.internal"
  port: "5432"
EOF

# Backend values-doks.yaml
cat > phase-4/helm/todo-backend/values-doks.yaml << 'EOF'
replicaCount: 3

image:
  repository: registry.digitalocean.com/todo/backend
  pullPolicy: Always
  tag: "latest"

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: api.todo-app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: todo-backend-tls
      hosts:
        - api.todo-app.example.com

dapr:
  enabled: true
  appId: "todo-backend"
  appPort: "8000"
  logLevel: "info"

database:
  deployLocal: false
  # Use Neon PostgreSQL connection from secret
EOF

# Frontend values-minikube.yaml
cat > phase-4/helm/todo-frontend/values-minikube.yaml << 'EOF'
replicaCount: 1

image:
  repository: todo-frontend
  pullPolicy: Never
  tag: "latest"

service:
  type: NodePort
  port: 80
  targetPort: 3000

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

dapr:
  enabled: true
  appId: "todo-frontend"
  appPort: "3000"
  logLevel: "debug"
EOF

# Frontend values-doks.yaml
cat > phase-4/helm/todo-frontend/values-doks.yaml << 'EOF'
replicaCount: 3

image:
  repository: registry.digitalocean.com/todo/frontend
  pullPolicy: Always
  tag: "latest"

service:
  type: ClusterIP
  port: 80
  targetPort: 3000

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: todo-app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: todo-frontend-tls
      hosts:
        - todo-app.example.com

dapr:
  enabled: true
  appId: "todo-frontend"
  appPort: "3000"
  logLevel: "info"
EOF

echo "✅ Helm values files created (4 files)"

echo ""
echo "=========================================="
echo "  ✅ Phase V Files Created Successfully!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Event system: 4 files"
echo "  - Dapr components: 5 files"
echo "  - Helm values: 4 files"
echo ""
echo "Next: Run GitHub Actions workflows manually or continue with remaining files"
echo ""
