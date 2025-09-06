from auth import get_service
import asyncio

CALENDAR_ID = 'primary'
COLOR_LECTURE = "9"
COLOR_LAB = "10"
COLOR_PRACTICE = "11"


def get_color(summary: str) -> str:
    if "ЛК" in summary:
        return COLOR_LECTURE
    elif "ЛР" in summary:
        return COLOR_LAB
    elif "ПЗ" in summary:
        return COLOR_PRACTICE
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
    color_id = get_color(summary or description or "")
    if color_id:
        event['colorId'] = color_id
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print(f"✅ Событие создано: {event_result.get('htmlLink')}")


async def add_event(summary, start, end, description=None, location=None):
    await asyncio.to_thread(_sync_insert_event, summary, start, end, description, location)
