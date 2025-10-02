from sqlalchemy.orm import Session

from app.models import Task
from app.websocket import manager


def notify_task_change(task: Task) -> None:
    try:
        import anyio

        anyio.from_thread.run(manager.broadcast, {"type": "task.updated", "task_id": task.id})
    except Exception:
        pass


def notify_task_deleted(task_id: int) -> None:
    try:
        import anyio

        anyio.from_thread.run(manager.broadcast, {"type": "task.deleted", "task_id": task_id})
    except Exception:
        pass
