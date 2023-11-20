from accounts.models import User
from courses.models import Material
from ioc.models import IoCodeSubmissionSummary, IoCodeSubmission, MaterialIoCode


def update_submission_summary(user: User, material: Material, submission: IoCodeSubmission) -> None:
    """Method that updates the submission summary of a user for a material"""

    summary: IoCodeSubmissionSummary = IoCodeSubmissionSummary.objects.filter(
        user=user, material=material
    ).first()
    io_code: MaterialIoCode = material.materialiocode

    if summary:
        if submission.response_char == "A" and (not summary.hits):
            # First hit
            summary.hits = 1
            summary.points = (
                    max(io_code.max_points - (io_code.points_penalty * summary.attempts),
                        io_code.min_points)
            )
            summary.min_execution_time = submission.execution_time
            summary.min_execution_memory = submission.execution_memory
            summary.max_completion_rate = 0
        elif submission.response_char == "A" and summary.hits:
            # Second or more hit
            summary.hits += 1
            summary.min_execution_time = min(
                summary.min_execution_time, submission.execution_time
            )
            summary.min_execution_memory = min(
                summary.min_execution_memory, submission.execution_memory
            )
            summary.max_completion_rate = max(
                summary.max_completion_rate, 0
            )
        summary.attempts += 1
        summary.save()
    else:
        # First attempt
        summary = IoCodeSubmissionSummary(
            user=user,
            material=material,
            hits=1 if submission.response_char == "A" else 0,
            points=io_code.max_points
            if submission.response_char == "A"
            else io_code.min_points,
            min_execution_time=submission.execution_time,
            min_execution_memory=submission.execution_memory,
            max_completion_rate=0,
        )
        summary.save()

