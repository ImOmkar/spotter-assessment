# class StopService:

#     AVG_SPEED = 50
#     FUEL_INTERVAL = 1000

#     @staticmethod
#     def generate_stops(hos_logs, coordinates, total_miles):

#         stops = []

#         total_coords = len(coordinates)
#         miles_progress = 0
#         next_fuel_at = StopService.FUEL_INTERVAL

#         # ✅ Pickup marker
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

#                 # Driving progress
#                 if event["status"] == "driving":
#                     miles_progress += duration * StopService.AVG_SPEED

#                     # Fuel stop detection
#                     while miles_progress >= next_fuel_at:
#                         progress_ratio = next_fuel_at / total_miles
#                         coord_index = int(
#                             progress_ratio * (total_coords - 1)
#                         )

#                         coord = coordinates[coord_index]

#                         stops.append({
#                             "type": "fuel",
#                             "lat": coord["lat"],
#                             "lng": coord["lng"],
#                             "day": log["day"],
#                         })

#                         next_fuel_at += StopService.FUEL_INTERVAL

#                 # Break detection
#                 if event["status"] == "break":

#                     progress_ratio = min(
#                         miles_progress / total_miles, 1
#                     )

#                     coord_index = int(
#                         progress_ratio * (total_coords - 1)
#                     )

#                     coord = coordinates[coord_index]

#                     stops.append({
#                         "type": "break",
#                         "lat": coord["lat"],
#                         "lng": coord["lng"],
#                         "day": log["day"],
#                     })
#                     progress_ratio = min(
#                         miles_progress / total_miles, 1
#                     )

#                     coord_index = int(
#                         progress_ratio * (total_coords - 1)
#                     )

#                     coord = coordinates[coord_index]

#                     stops.append({
#                         "type": "break",
#                         "lat": coord["lat"],
#                         "lng": coord["lng"],
#                         "day": log["day"],
#                     })

#         # ✅ Dropoff marker
#         end_coord = coordinates[-1]
#         stops.append({
#             "type": "dropoff",
#             "lat": end_coord["lat"],
#             "lng": end_coord["lng"],
#             "day": hos_logs[-1]["day"],
#         })

#         return stops


class StopService:

    AVG_SPEED = 50
    FUEL_INTERVAL = 1000

    @staticmethod
    def generate_stops(hos_logs, coordinates, total_miles):

        stops = []

        if not coordinates:
            return stops

        total_coords = len(coordinates)
        miles_progress = 0
        next_fuel_at = StopService.FUEL_INTERVAL

        # ✅ Pickup
        start_coord = coordinates[0]
        stops.append({
            "type": "pickup",
            "lat": start_coord["lat"],
            "lng": start_coord["lng"],
            "day": 1,
        })

        for log in hos_logs:

            for event in log["timeline"]:

                duration = event["end"] - event["start"]

                # ---------------- DRIVING ----------------
                if event["status"] == "driving":
                    miles_progress += duration * StopService.AVG_SPEED

                    # Fuel stops
                    while miles_progress >= next_fuel_at:

                        progress_ratio = min(
                            next_fuel_at / total_miles,
                            1
                        )

                        coord_index = max(
                            0,
                            min(
                                int(progress_ratio * (total_coords - 1)),
                                total_coords - 1,
                            ),
                        )

                        coord = coordinates[coord_index]

                        if coord:
                            stops.append({
                                "type": "fuel",
                                "lat": coord["lat"],
                                "lng": coord["lng"],
                                "day": log["day"],
                            })

                        next_fuel_at += StopService.FUEL_INTERVAL

                # ---------------- BREAK ----------------
                if event["status"] == "break":

                    progress_ratio = min(
                        miles_progress / total_miles,
                        1
                    )

                    coord_index = max(
                        0,
                        min(
                            int(progress_ratio * (total_coords - 1)),
                            total_coords - 1,
                        ),
                    )

                    coord = coordinates[coord_index]

                    if coord:
                        stops.append({
                            "type": "break",
                            "lat": coord["lat"],
                            "lng": coord["lng"],
                            "day": log["day"],
                        })

        # ✅ Dropoff
        end_coord = coordinates[-1]

        stops.append({
            "type": "dropoff",
            "lat": end_coord["lat"],
            "lng": end_coord["lng"],
            "day": hos_logs[-1]["day"],
        })

        return stops