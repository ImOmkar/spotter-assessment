from dataclasses import dataclass, field
from typing import List


@dataclass
class Event:
    status: str
    start: float
    end: float


@dataclass
class DayLog:
    day: int
    driving_hours: float
    on_duty_hours: float
    timeline: List[Event] = field(default_factory=list)


class HOSEngine:

    MAX_DRIVING_PER_DAY = 11
    MAX_DUTY_WINDOW = 14
    BREAK_AFTER_HOURS = 8
    BREAK_DURATION = 0.5
    FUEL_EVERY_MILES = 1000
    FUEL_DURATION = 0.5
    PICKUP_DURATION = 1
    DROPOFF_DURATION = 1
    DAILY_RESET_OFF_DUTY = 10
    MAX_CYCLE = 70

    def __init__(self, total_miles: float, current_cycle_hours: float, avg_speed: float = 50):
        self.total_miles = total_miles
        self.miles_remaining = total_miles
        self.current_cycle_hours = current_cycle_hours
        self.avg_speed = avg_speed
        self.fuel_miles_counter = 0

    def generate(self) -> List[DayLog]:

        day = 1
        logs = []

        while self.miles_remaining > 0:

            if self.current_cycle_hours >= self.MAX_CYCLE:
                break

            daily_driving = 0
            daily_on_duty = 0
            current_time = 6.0
            timeline = []
            break_taken = False

            # Off duty midnight → 6 AM
            timeline.append(Event("off_duty", 0, 6))

            # Pickup
            if day == 1:
                timeline.append(
                    Event("pickup", current_time, current_time + self.PICKUP_DURATION)
                )
                current_time += self.PICKUP_DURATION
                daily_on_duty += self.PICKUP_DURATION

            while (
                daily_driving < self.MAX_DRIVING_PER_DAY
                and daily_on_duty < self.MAX_DUTY_WINDOW
                and self.miles_remaining > 0
            ):

                # Break
                if (
                    not break_taken
                    and daily_driving >= self.BREAK_AFTER_HOURS
                ):
                    timeline.append(
                        Event("break", current_time, current_time + self.BREAK_DURATION)
                    )
                    current_time += self.BREAK_DURATION
                    daily_on_duty += self.BREAK_DURATION
                    break_taken = True
                    continue

                # Fuel stop
                if self.fuel_miles_counter >= self.FUEL_EVERY_MILES:
                    timeline.append(
                        Event("fuel", current_time, current_time + self.FUEL_DURATION)
                    )
                    current_time += self.FUEL_DURATION
                    daily_on_duty += self.FUEL_DURATION
                    self.fuel_miles_counter = 0
                    continue

                driving_chunk = 1.0

                if daily_driving + driving_chunk > self.MAX_DRIVING_PER_DAY:
                    driving_chunk = self.MAX_DRIVING_PER_DAY - daily_driving

                if daily_on_duty + driving_chunk > self.MAX_DUTY_WINDOW:
                    break

                if self.current_cycle_hours + daily_on_duty >= self.MAX_CYCLE:
                    break

                timeline.append(
                    Event("driving", current_time, current_time + driving_chunk)
                )

                current_time += driving_chunk
                daily_driving += driving_chunk
                daily_on_duty += driving_chunk

                miles_driven = min(
                    self.avg_speed * driving_chunk,
                    self.miles_remaining
                )

                self.miles_remaining -= miles_driven
                self.fuel_miles_counter += miles_driven

            # Dropoff 
            if self.miles_remaining <= 0:
                timeline.append(
                    Event("dropoff", current_time, current_time + self.DROPOFF_DURATION)
                )
                daily_on_duty += self.DROPOFF_DURATION
                current_time += self.DROPOFF_DURATION

            # Reset
            reset_end = current_time + self.DAILY_RESET_OFF_DUTY

            timeline.append(
                Event(
                    "off_duty",
                    current_time,
                    reset_end
                )
            )

            self.current_cycle_hours += daily_on_duty

            logs.append(
                DayLog(
                    day=day,
                    driving_hours=round(daily_driving, 2),
                    on_duty_hours=round(daily_on_duty, 2),
                    timeline=timeline,
                )
            )

            day += 1

        return logs
    
    def build_remarks(self, logs):
        remarks = []

        for log in logs:
            for event in log.timeline:

                if event.status in [
                    "pickup",
                    "fuel",
                    "break",
                    "dropoff",
                ]:
                    hour = int(event.start)
                    minutes = int((event.start - hour) * 60)

                    formatted_time = f"{hour:02}:{minutes:02}"
                    remarks.append({
                        "day": log.day,
                        "event": event.status,
                        "time": formatted_time
                    })

        return remarks

    def run(self) -> dict:
        logs = self.generate()
        remarks = self.build_remarks(logs)

        return {
            "summary": {
                "total_days": len(logs),
                "total_miles": round(self.total_miles, 2),
                "final_cycle_hours": round(self.current_cycle_hours, 2),
            },
            "logs": [
                {
                    "day": log.day,
                    "driving_hours": log.driving_hours,
                    "on_duty_hours": log.on_duty_hours,
                    "timeline": [
                        {
                            "status": event.status,
                            "start": event.start,
                            "end": event.end,
                        }
                        for event in log.timeline
                    ],
                }
                for log in logs
            ],
            "remarks": remarks,
        }