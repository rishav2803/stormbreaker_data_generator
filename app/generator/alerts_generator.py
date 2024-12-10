from sqlalchemy.orm import Session
from app.models.alert_model import Alert
import random

def create_detail(name:str):
    return {
        "reason":name,
        "value":""
    }
def create_alerts(session: Session, mapped_alertgroup_to_alerts: dict[str, list[str]]):

    for alert_group_data, alerts in mapped_alertgroup_to_alerts.items():
        alert_group_id,validation_id,validation_name=alert_group_data.split('/')
        for alert_id in alerts:
            alert=Alert(
                alert_group_id=alert_group_id,
                job_id=alert_id,
                details=create_detail(validation_name)
            )
            session.add(alert)
            session.flush()

        

    