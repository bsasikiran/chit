from datetime import date, timedelta
from io import BytesIO
import unittest
from unittest.mock import patch

from run import read_calendar_events


class CalendarFeedTests(unittest.TestCase):
    def test_reads_near_term_all_day_and_timed_events(self):
        tomorrow = date.today() + timedelta(days=1)
        next_day = tomorrow + timedelta(days=1)
        calendar_data = (
            "BEGIN:VCALENDAR\r\n"
            "VERSION:2.0\r\n"
            "BEGIN:VEVENT\r\n"
            "UID:waste-1\r\n"
            "DTSTART;VALUE=DATE:%s\r\n"
            "DTEND;VALUE=DATE:%s\r\n"
            "SUMMARY:Restmüll\r\n"
            "END:VEVENT\r\n"
            "BEGIN:VEVENT\r\n"
            "UID:activity-1\r\n"
            "DTSTART:%sT173000Z\r\n"
            "DTEND:%sT183000Z\r\n"
            "SUMMARY:Swimming\r\n"
            "END:VEVENT\r\n"
            "END:VCALENDAR\r\n"
        ) % (
            tomorrow.strftime("%Y%m%d"),
            next_day.strftime("%Y%m%d"),
            tomorrow.strftime("%Y%m%d"),
            tomorrow.strftime("%Y%m%d"),
        )

        class Response(BytesIO):
            status = 200

        with patch("run.urlopen", return_value=Response(calendar_data.encode("utf-8"))):
            events = read_calendar_events("webcal://calendar.example/private.ics", "Europe/Berlin")

        self.assertEqual([event["title"] for event in events], ["Restmüll", "Swimming"])
        self.assertTrue(events[0]["all_day"])
        self.assertFalse(events[1]["all_day"])
        self.assertIn("T19:30:00+02:00", events[1]["start"])


if __name__ == "__main__":
    unittest.main()