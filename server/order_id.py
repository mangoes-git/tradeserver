import shelve
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass


@dataclass
class DailyEmailTracker:
    last_date: datetime
    count: int

    def update_date(self, today):
        self.last_date = today
        self.count = 0


class TrackID:
    current_id: int
    daily_tracker: DailyEmailTracker
    shelf = None

    def __init__(self):
        self.shelf = shelve.open("./track_order_id/order_id.db", writeback=True)
        if "id" in self.shelf:
            self.current_id = self.shelf["id"]
        else:
            self.current_id = 0
            self.shelf["id"] = self.current_id

        if "daily_tracker" in self.shelf:
            self.daily_tracker = self.shelf["daily_tracker"]
        else:
            self.daily_tracker = DailyEmailTracker(
                last_date=datetime.now(timezone(timedelta(hours=8))),
                count=0,
            )
            self.shelf["daily_count"] = self.daily_tracker

    def get_next_id(self):
        self.current_id += 1
        self.shelf["id"] = self.current_id
        return self.current_id

    def get_todays_email_number(self, today):
        if today.date() != self.daily_tracker.last_date.date():
            self.daily_tracker.update_date(today)
        self.daily_tracker.count += 1

        self.shelf["daily_tracker"] = self.daily_tracker
        return self.daily_tracker.count

    def close(self):
        self.shelf.close()
