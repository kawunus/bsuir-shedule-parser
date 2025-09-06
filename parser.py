from auth import get_service
import asyncio
from datetime import datetime, timezone

CALENDAR_ID = "494ee131891f8083b956f503604cd52858f2be874c0ef1b759f91b099e817c34@group.calendar.google.com"

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
