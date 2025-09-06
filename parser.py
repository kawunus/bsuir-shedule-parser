from auth import get_service
import asyncio
from datetime import datetime, timezone
from config import SOURCE_CALENDAR_ID 

CALENDAR_ID = SOURCE_CALENDAR_ID

def iso_today():
    return datetime.now(timezone.utc).isoformat()


async def parse_schedule():
    service = get_service()
    time_min = iso_today()
    events_result = await asyncio.to_thread(
        lambda: service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
    )
    events = events_result.get("items", [])
    filtered_events = [e for e in events if "1 подгр." not in e.get("summary", "")]
    parsed_events = []
    for e in filtered_events:
        parsed_events.append({
            "summary": e.get("summary", "Без названия"),
            "start": e["start"],
            "end": e["end"],
            "description": e.get("description", ""),
            "location": e.get("location"),
        })
    return parsed_events
