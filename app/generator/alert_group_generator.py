from sqlalchemy.orm import Session
from app.models.alert_model import AlertGroup
import random


def create_alert_group(session: Session, failed_jobs: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Create alert groups from failed jobs.

    Args:
        session (Session): SQLAlchemy session object.
        failed_jobs (dict[str, list[str]]): Dictionary of failed validation jobs.

    Returns:
        dict[str, list[str]]: Mapped alert groups with their corresponding failed job IDs.
    """
    mapped_alertgroup_to_alerts = {}
    for failed_job_key, failed_job_ids in failed_jobs.items():  
        failed_validation_id, failed_validation_name = failed_job_key.split('/')
        alert_group = AlertGroup(
            name=failed_validation_name,
            is_incident=False,
            status="NO_STATUS",
            validation_id=failed_validation_id,
        )
        session.add(alert_group)
        session.flush()
        new_alert_key = f"{alert_group.id}/{failed_validation_id}/{failed_validation_name}"
        mapped_alertgroup_to_alerts[new_alert_key] = failed_job_ids
    return mapped_alertgroup_to_alerts