# class StopService:

#     AVG_SPEED = 50
#     FUEL_INTERVAL = 1000

#     @staticmethod
#     def generate_stops(hos_logs, coordinates, total_miles):

#         print("Total miles:", total_miles)

#         stops = []

#         if not coordinates:
#             return stops

#         total_coords = len(coordinates)
#         miles_progress = 0
#         next_fuel_at = StopService.FUEL_INTERVAL

#         # ✅ Pickup
#         start_coord = coordinates[0]
#         stops.append({
#             "type": "pickup",
#             "lat": start_coord["lat"],
#             "lng": start_coord["lng"],
#             "day": 1,
#         })

#         for log in hos_logs:

#             for event in log["timeline"]:

#                 duration = event["end"] - event["start"]

#                 # ---------------- DRIVING ----------------
#                 if event["status"] == "driving":
#                     miles_progress += duration * StopService.AVG_SPEED

#                     # Fuel stops
#                     while miles_progress >= next_fuel_at:

#                         progress_ratio = min(
#                             next_fuel_at / total_miles,
#                             1
#                         )

#                         coord_index = max(
#                             0,
#                             min(
#                                 int(progress_ratio * (total_coords - 1)),
#                                 total_coords - 1,
#                             ),
#                         )

#                         coord = coordinates[coord_index]

#                         if coord:
#                             stops.append({
#                                 "type": "fuel",
#                                 "lat": coord["lat"],
#                                 "lng": coord["lng"],
#                                 "day": log["day"],
#                             })

#                         next_fuel_at += StopService.FUEL_INTERVAL

#                 # ---------------- BREAK ----------------
#                 if event["status"] == "break":

#                     progress_ratio = min(
#                         miles_progress / total_miles,
#                         1
#                     )

#                     coord_index = max(
#                         0,
#                         min(
#                             int(progress_ratio * (total_coords - 1)),
#                             total_coords - 1,
#                         ),
#                     )

#                     coord = coordinates[coord_index]

#                     if coord:
#                         stops.append({
#                             "type": "break",
#                             "lat": coord["lat"],
#                             "lng": coord["lng"],
#                             "day": log["day"],
#                         })

#         # ✅ Dropoff
#         end_coord = coordinates[-1]

#         stops.append({
#             "type": "dropoff",
#             "lat": end_coord["lat"],
#             "lng": end_coord["lng"],
#             "day": hos_logs[-1]["day"],
#         })

#         return stops


class StopService:

    AVG_SPEED = 50  # mph
    FUEL_INTERVAL = 1000  # miles

    @staticmethod
    def generate_stops(hos_logs, coordinates, total_miles):

        print("total miles", total_miles)

        stops = []

        # Basic Safety Checks
        if not coordinates or len(coordinates) < 1:
            return stops

        if not hos_logs:
            return stops

        if not total_miles or total_miles <= 0:
            return stops

        total_coords = len(coordinates)
        miles_progress = 0
        next_fuel_at = StopService.FUEL_INTERVAL

        # Helper to safely get coordinate
        def get_safe_coord(index):
            if index < 0:
                index = 0
            if index >= total_coords:
                index = total_coords - 1

            coord = coordinates[index]

            # Final validation
            if (
                not coord
                or not isinstance(coord.get("lat"), (int, float))
                or not isinstance(coord.get("lng"), (int, float))
            ):
                return None

            return coord

        # Pickup Stop
        start_coord = get_safe_coord(0)
        if start_coord:
            stops.append({
                "type": "pickup",
                "lat": start_coord["lat"],
                "lng": start_coord["lng"],
                "day": 1,
            })

        # Iterate Through HOS Logs
        for log in hos_logs:

            day = log.get("day", 1)
            timeline = log.get("timeline", [])

            for event in timeline:

                duration = event.get("end", 0) - event.get("start", 0)
                status = event.get("status")

                if duration <= 0:
                    continue

                # Driving Events
                if status == "driving":

                    miles_progress += duration * StopService.AVG_SPEED

                    # Generate fuel stops
                    while miles_progress >= next_fuel_at:

                        progress_ratio = min(
                            next_fuel_at / total_miles,
                            1
                        )

                        coord_index = int(
                            progress_ratio * (total_coords - 1)
                        )

                        coord = get_safe_coord(coord_index)

                        if coord:
                            stops.append({
                                "type": "fuel",
                                "lat": coord["lat"],
                                "lng": coord["lng"],
                                "day": day,
                            })

                        next_fuel_at += StopService.FUEL_INTERVAL

                # Break Events
                if status == "break":

                    progress_ratio = min(
                        miles_progress / total_miles,
                        1
                    )

                    coord_index = int(
                        progress_ratio * (total_coords - 1)
                    )

                    coord = get_safe_coord(coord_index)

                    if coord:
                        stops.append({
                            "type": "break",
                            "lat": coord["lat"],
                            "lng": coord["lng"],
                            "day": day,
                        })

        # Dropoff Stop
        end_coord = get_safe_coord(total_coords - 1)

        if end_coord:
            last_day = hos_logs[-1].get("day", 1)
            stops.append({
                "type": "dropoff",
                "lat": end_coord["lat"],
                "lng": end_coord["lng"],
                "day": last_day,
            })

        return stops