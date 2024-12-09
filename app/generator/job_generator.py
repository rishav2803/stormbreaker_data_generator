import random
import string
from sqlalchemy.orm import Session
from app.models.job_model import Job


def create_job(session: Session, all_tasks: list[str], type: str) -> dict[str, list[str]]:
    """
    Creates multiple jobs for each task and maps task IDs to their respective job IDs.

    Args:
        session (Session): SQLAlchemy session object.
        all_tasks (list[str]): List of task IDs to create jobs for.
        type (str): Type of job ("comparison" or "validation").

    Returns:
        dict[str, list[str]]: A dictionary where keys are task IDs, and values are lists of job IDs.
    """
    task_to_jobs = {}

    for task_id in all_tasks:
        # randomly get number of jobs between 30 to 40
        no_of_jobs = random.randint(30, 40)

        # no_of_jobs = 2
        job_ids = []

        for _ in range(no_of_jobs):
            name = ''.join(random.choices(string.ascii_lowercase, k=4))

            job = Job(
                name=name,
                meta={},
                comparison_id=task_id if type == "comparison" else None,
                validation_id=task_id if type == "validation" else None,
                is_interactive=True,
                origin="WEB",
            )

            session.add(job)
            session.flush()

            job_ids.append(job.id)

        task_to_jobs[task_id] = job_ids

    return task_to_jobs

