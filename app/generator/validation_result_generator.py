from sqlalchemy.orm import Session
from app.models.validation_model import ValidationResult
import random


def create_validation_result(session: Session, all_validation_jobs: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Create Validations Result.

    Args:
        session (Session): SQLAlchemy session object.
        all_validation_jobs (dict[str,list[str]]): Dict storing the mapping of validations and its multiple jobs.


    Returns:
        dict[str, list[str]]: Dictionary of failed validations with validation key and list of failed job_ids.
    """

    failed_validation = {}
    for validation, jobs in all_validation_jobs.items():
        validation_id, validation_name = validation.split('/')
        validation_key = f"{validation_id}/{validation_name}"
        
        for job in jobs:
            job_id = job
            reason = ""
            status = random.randint(0, 1)
            value = random.randint(100, 10000)

            validation_result = ValidationResult(
                value=value,
                status="pass" if status == 1 else "fail",
                reason=reason,
                validation_id=validation_id,
                job_id=job_id
            )
            session.add(validation_result)
            session.flush()
            
            if status == 0:
                if validation_key not in failed_validation:
                    failed_validation[validation_key] = []
                failed_validation[validation_key].append(job_id)
    
    return failed_validation