"""Event Publisher for Dapr/Kafka integration."""
import httpx
from datetime import datetime
from typing import Dict, Any

DAPR_HTTP_PORT = 3500
PUBSUB_NAME = "pubsub"

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
