from auth import get_service
import asyncio
from config import COLORS, TARGET_CALENDAR_ID

CALENDAR_ID = TARGET_CALENDAR_ID

def get_color(summary: str) -> str:
    for key, color_id in COLORS.items():
        if key in summary:
            return color_id
    return None

def _sync_insert_event(summary, start, end, description=None, location=None):
    service = get_service()
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'Europe/Minsk'},
        'end': {'dateTime': end, 'timeZone': 'Europe/Minsk'},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]},
    }
    color_id = get_color(summary)
    if color_id:
        event['colorId'] = str(color_id)
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print(f"✅ Событие создано: {event_result.get('htmlLink')}")

async def add_event(summary, start, end, description=None, location=None):
    await asyncio.to_thread(_sync_insert_event, summary, start, end, description, location)
