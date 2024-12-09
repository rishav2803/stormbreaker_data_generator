from sqlalchemy.orm import Session
from app.models.job_model import Job
from constants import COMMON_COLUMNS
import random
import string


def create_job(session: Session, all_tasks:list[str],type:str)->list[list[str]]:

    all_task_id=[]
    for task_id in all_tasks:
        name = ''.join(random.choices(string.ascii_lowercase, k=4))
        job=Job(
            name=name,
            meta={},
            comparison_id=task_id if (type=="comparison") else None,
            validation_id=task_id if (type=="validation") else None,
            is_interactive=True,
            origin="WEB",
        )
        session.add(job)
        session.flush()
        all_task_id.append([job.id,task_id])
    return all_task_id



    



    



