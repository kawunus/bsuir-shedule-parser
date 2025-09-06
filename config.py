from dotenv import load_dotenv
import os

load_dotenv()

SOURCE_CALENDAR_ID = os.getenv("SOURCE_CALENDAR_ID")
TARGET_CALENDAR_ID = os.getenv("TARGET_CALENDAR_ID")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 86400))
PAUSE_BETWEEN_REQUESTS = float(os.getenv("PAUSE_BETWEEN_REQUESTS", 0.2))
SUBGROUP = os.getenv("SUBGROUP","")

COLORS = {
    "ЛК": os.getenv("COLOR_LK", "9"),
    "ЛР": os.getenv("COLOR_LR", "10"),
    "ПЗ": os.getenv("COLOR_PZ", "11")
}
