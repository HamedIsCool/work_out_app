from datetime import datetime, timedelta, time, date
from fastapi import APIRouter, HTTPException, status
from ..schemas.workouts import WorkoutCreate
from ..db.supabase import supabase

router = APIRouter()

@router.post("/workouts", status_code=201)
def create_workout(body: WorkoutCreate):
    validate_workouts(body)
    payload = db_payload(body)

    result = supabase.table("workouts").insert(payload).execute()

    if getattr(result, "error", None):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save workout",
        )

    inserted = result.data[0]
    return inserted

allowed_types = {"running", "gym", "cycling"}
def validate_workouts(body:WorkoutCreate):
    if body.type not in allowed_types:
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Type must be one the followings: running, cycling, gym"
        )
    if body.duration_minutes <= 0:
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Duration can't be minus!"
        )

    if not 1<= body.mood_number <=5 :
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="mood_number must be between 1-5"
        )
def mood_label_from_number(mood_number:int) -> str:
    mapping = {
        1: "Unhappy",
        2: "Bad",
        3: "Neutral",
        4: "Good",
        5: "Happy",
    }
    return mapping[mood_number]


def db_payload(body:WorkoutCreate) -> dict:
    return {
        "type": body.type,
        "performed_at": body.performed_at.isoformat(),
        "duration_minutes": body.duration_minutes,
        "mood_number": body.mood_number,
        "mood_label_en": mood_label_from_number(body.mood_number),
        "notes": body.notes
    }


# @router.get("/workouts/today")
# def result_today():
#     now = datetime.now()
#     today_start = datetime.combine(now.date(), time.min)
#     tomorrow_start = today_start + timedelta(days=1)

#     start_iso = today_start.isoformat()
#     end_iso = tomorrow_start.isoformat()

#     response = (
#         supabase.table("workouts")
#         .select("*")
#         .gte("performed_at", start_iso)
#         .lt("performed_at", end_iso)
#         .execute()
#     )

#     if getattr(response, "error", None):   
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to fetch today's workouts",
#         )

#     return response.data               



# @router.get("/workouts/weekly")
# def result_weekly():
#     now = datetime.now()
#     end_date = datetime.combine(now.date(), time.min) + timedelta(days=1)
#     start_date = end_date - timedelta(days=7)

#     start_iso = start_date.isoformat()
#     end_iso = end_date.isoformat()

#     response = (
#         supabase.table("workouts")
#         .select("*")
#         .gte("performed_at", start_iso)
#         .lt("performed_at", end_iso)
#         .execute()
#     )

#     if getattr(response, "error", None):   
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to fetch today's workouts",
#         )

#     return response.data               



@router.get("/workouts/results")
def get_workout_results_by_duration(duration: int):
    
    now = datetime.now()
    end_date = datetime.combine(now.date(), time.min) + timedelta(days=1)
    start_date = end_date - timedelta(days=duration)

    start_iso = start_date.isoformat()
    end_iso = end_date.isoformat()

    response = (
        supabase.table("workouts")
        .select("*")
        .gte("performed_at", start_iso)
        .lt("performed_at", end_iso)
        .execute()
    )

    if getattr(response, "error", None):   
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch today's workouts",
        )

    return response.data               


@router.get("/workouts/results-by-date")
def get_workout_results_by_date(start: date, end: date):
    if start > end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start date must be <= end date"
        )

    start_date = datetime.combine(start, time.min)
    end_date = datetime.combine(end, time.min) + timedelta(days=1)

    start_iso = start_date.isoformat()
    end_iso = end_date.isoformat()

    response = (
        supabase.table("workouts")
        .select("*")
        .gte("performed_at", start_iso)
        .lt("performed_at", end_iso)
        .execute()
    )

    if getattr(response, "error", None):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch workouts for given date range",
        )

    return response.data
