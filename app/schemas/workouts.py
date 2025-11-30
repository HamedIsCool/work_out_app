from datetime import datetime
from pydantic import BaseModel

class WorkoutCreate(BaseModel):
    type: str
    duration_minutes: int
    mood_number: int
    performed_at: datetime
    notes: str | None = None
