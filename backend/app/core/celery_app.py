"""
Celery application configuration for background tasks.

Handles email processing, paper analysis, and other asynchronous operations.
"""

from celery import Celery
from kombu import Queue

from .config import settings


def create_celery_app() -> Celery:
    """
    Create and configure Celery application.
    
    Returns:
        Configured Celery app instance
    """
    celery_app = Celery(
        "paper_agent",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=[
            "app.tasks.email_tasks",
            "app.tasks.paper_tasks", 
            "app.tasks.ai_tasks",
            "app.tasks.maintenance_tasks"
        ]
    )
    
    # Configure Celery
    celery_app.conf.update(
        # Task settings
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        
        # Task execution settings
        task_always_eager=False,  # Set to True for testing
        task_eager_propagates=True,
        task_ignore_result=False,
        task_store_eager_result=True,
        
        # Task routing and queues
        task_default_queue="default",
        task_default_exchange="default",
        task_default_exchange_type="direct",
        task_default_routing_key="default",
        
        # Define queues
        task_routes={
            "app.tasks.email_tasks.*": {"queue": "email"},
            "app.tasks.paper_tasks.*": {"queue": "papers"},
            "app.tasks.ai_tasks.*": {"queue": "ai"},
            "app.tasks.maintenance_tasks.*": {"queue": "maintenance"},
        },
        
        # Worker settings
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=1000,
        worker_disable_rate_limits=False,
        
        # Result backend settings
        result_expires=3600,  # 1 hour
        result_backend_transport_options={
            "master_name": "mymaster",
        },
        
        # Beat schedule for periodic tasks
        beat_schedule={
            "check-emails": {
                "task": "app.tasks.email_tasks.check_all_email_configs",
                "schedule": 300.0,  # Every 5 minutes
                "options": {"queue": "email"}
            },
            "process-pending-papers": {
                "task": "app.tasks.paper_tasks.process_pending_papers",
                "schedule": 600.0,  # Every 10 minutes
                "options": {"queue": "papers"}
            },
            "cleanup-old-tasks": {
                "task": "app.tasks.maintenance_tasks.cleanup_old_task_results",
                "schedule": 3600.0,  # Every hour
                "options": {"queue": "maintenance"}
            },
            "update-paper-stats": {
                "task": "app.tasks.maintenance_tasks.update_paper_statistics",
                "schedule": 1800.0,  # Every 30 minutes
                "options": {"queue": "maintenance"}
            },
        },
        
        # Monitoring
        worker_send_task_events=True,
        task_send_sent_event=True,
        
        # Security
        worker_hijack_root_logger=False,
        worker_log_color=False,
        
        # Error handling
        task_reject_on_worker_lost=True,
        task_acks_late=True,
    )
    
    # Define queues explicitly
    celery_app.conf.task_queues = [
        Queue("default", routing_key="default"),
        Queue("email", routing_key="email"),
        Queue("papers", routing_key="papers"),
        Queue("ai", routing_key="ai"),
        Queue("maintenance", routing_key="maintenance"),
    ]
    
    return celery_app


# Create the Celery app instance
celery_app = create_celery_app()


# Celery signals for monitoring and logging
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery configuration."""
    print(f"Request: {self.request!r}")
    return "Debug task completed"


# Task failure handler
@celery_app.task(bind=True)
def handle_task_failure(self, task_id: str, error: str, traceback: str):
    """
    Handle task failures by logging and potentially notifying admins.
    
    Args:
        task_id: Failed task ID
        error: Error message
        traceback: Error traceback
    """
    print(f"Task {task_id} failed: {error}")
    print(f"Traceback: {traceback}")
    # In production, you might want to send notifications or log to external service


# Celery events monitoring
@celery_app.task(bind=True)
def monitor_task_events(self):
    """Monitor Celery task events for health checks."""
    # This could integrate with monitoring systems
    pass


if __name__ == "__main__":
    # Start Celery worker
    celery_app.start()