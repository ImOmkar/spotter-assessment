class HOSValidator:

    MAX_DRIVING = 11
    MAX_DUTY = 14
    BREAK_AFTER = 8
    MAX_CYCLE = 70

    @staticmethod
    def validate(logs, final_cycle_hours):

        violations = []

        for log in logs:

            driving = log["driving_hours"]
            duty = log["on_duty_hours"]

            # 11 hour driving rule
            if driving > HOSValidator.MAX_DRIVING:
                violations.append(
                    f"Day {log['day']}: Driving exceeded 11 hours"
                )

            # 14 hour duty window
            if duty > HOSValidator.MAX_DUTY:
                violations.append(
                    f"Day {log['day']}: Duty window exceeded 14 hours"
                )

            # Break validation
            driving_since_break = 0
            break_found = False

            for event in log["timeline"]:

                if event["status"] == "driving":
                    driving_since_break += (
                        event["end"] - event["start"]
                    )

                if event["status"] == "break":
                    break_found = True
                    driving_since_break = 0

                if driving_since_break > HOSValidator.BREAK_AFTER:
                    violations.append(
                        f"Day {log['day']}: Missing 30 min break before 8 driving hours"
                    )
                    break

        # Cycle rule
        if final_cycle_hours > HOSValidator.MAX_CYCLE:
            violations.append(
                "70-hour cycle limit exceeded"
            )

        return {
            "valid": len(violations) == 0,
            "violations": violations
        }