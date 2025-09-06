import asyncio
from datetime import datetime, timezone
from auth import get_service
from parser import parse_schedule
from insert_event import add_event

CALENDAR_ID = "primary"
UPDATE_INTERVAL = 86400
PAUSE_BETWEEN_REQUESTS = 0.2


def iso_today():
    return datetime.now(timezone.utc).isoformat()


async def safe_execute_thread(func, *args, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            await asyncio.to_thread(func, *args)
            break
        except Exception as e:
            if "rateLimitExceeded" in str(e):
                print(f"⚠️ Rate limit exceeded, ждем {pause} секунд...")
                await asyncio.sleep(pause)
            else:
                raise e


async def safe_execute_async(func, *args, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            await func(*args)
            break
        except Exception as e:
            if "rateLimitExceeded" in str(e):
                print(f"⚠️ Rate limit exceeded, ждем {pause} секунд...")
                await asyncio.sleep(pause)
            else:
                raise e


def events_to_set(events):
    s = set()
    for e in events:
        summary = e.get("summary", "")
        start = e["start"].get("dateTime", e["start"].get("date"))
        end = e["end"].get("dateTime", e["end"].get("date"))
        location = e.get("location") or ""
        s.add((summary, start, end, location))
    return s


async def update_schedule():
    service = get_service()

    events_result = await asyncio.to_thread(
        lambda: service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=iso_today(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()
    )
    current_events = [e for e in events_result.get("items", []) if "[AUTO-UNI]" in e.get("description", "")]
    current_set = events_to_set(current_events)

    new_events_raw = await parse_schedule()
    new_events = [
        {**e, "description": (e.get("description", "") or "") + "\n[AUTO-UNI]"}
        for e in new_events_raw
    ]
    new_set = events_to_set(new_events)

    if current_set == new_set:
        print("🟢 Расписание не изменилось, обновление не требуется")
        return

    print("🔄 Обнаружены изменения в расписании, обновляем...")
    deleted = 0
    for event in current_events:
        await safe_execute_thread(
            lambda e=event: service.events().delete(calendarId=CALENDAR_ID, eventId=e["id"]).execute()
        )
        deleted += 1
        await asyncio.sleep(PAUSE_BETWEEN_REQUESTS)
    print(f"🗑 Удалено {deleted} старых событий")

    added = 0
    for e in new_events:
        summary = e.get("summary", "")
        start = e["start"].get("dateTime", e["start"].get("date"))
        end = e["end"].get("dateTime", e["end"].get("date"))
        description = e.get("description", "")
        location = e.get("location")
        await safe_execute_async(add_event, summary, start, end, description, location)
        added += 1
        await asyncio.sleep(PAUSE_BETWEEN_REQUESTS)
    print(f"✅ Добавлено {added} новых событий")


async def scheduler():
    while True:
        print("🔄 Обновление расписания...")
        await update_schedule()
        print(f"⏳ Ждём {UPDATE_INTERVAL} секунд до следующего обновления")
        await asyncio.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    asyncio.run(scheduler())
