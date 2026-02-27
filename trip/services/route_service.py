# import requests
# import polyline
# from django.conf import settings


# class RouteService:

#     BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

#     @staticmethod
#     def get_route(start_coords, end_coords):

#         headers = {
#             "Authorization": settings.ORS_API_KEY,
#             "Content-Type": "application/json",
#         }

#         body = {
#             "coordinates": [
#                 list(start_coords),
#                 list(end_coords),
#             ]
#         }

#         response = requests.post(
#             RouteService.BASE_URL,
#             json=body,
#             headers=headers,
#         )

#         response.raise_for_status()

#         data = response.json()

#         # Extract route safely
#         route = data["routes"][0]
#         summary = route["summary"]

#         distance_meters = summary["distance"]
#         duration_seconds = summary["duration"]

#         encoded_geometry = route["geometry"]

#         # Decode polyline
#         decoded_coords = polyline.decode(encoded_geometry)

#         coordinates = [
#             {"lat": lat, "lng": lng}
#             for lat, lng in decoded_coords
#         ]

#         return {
#             "distance_miles": round(distance_meters / 1609.34, 2),
#             "duration_hours": round(duration_seconds / 3600, 2),
#             "coordinates": coordinates,
#         }



import requests


class RouteService:

    BASE_URL = "https://router.project-osrm.org/route/v1/driving"

    @staticmethod
    def get_route(start_coords, end_coords):
        """
        Uses OSRM public routing API.
        No API key required.
        """

        start_lng, start_lat = start_coords
        end_lng, end_lat = end_coords

        url = (
            f"{RouteService.BASE_URL}/"
            f"{start_lng},{start_lat};{end_lng},{end_lat}"
            f"?overview=full&geometries=geojson"
        )

        print("hitting this URL", url)

        response = requests.get(url, timeout=10)

        print("response from osrm", response)
        
        response.raise_for_status()

        data = response.json()

        if not data.get("routes"):
            raise Exception("No route returned from OSRM")

        route = data["routes"][0]

        distance_meters = route["distance"]
        duration_seconds = route["duration"]

        coords = route["geometry"]["coordinates"]

        # OSRM returns [lng, lat]
        coordinates = [
            {"lat": float(c[1]), "lng": float(c[0])}
            for c in coords
            if len(c) >= 2
        ]

        if len(coordinates) < 2:
            raise Exception("Invalid coordinates from OSRM")

        return {
            "distance_miles": round(distance_meters / 1609.34, 2),
            "duration_hours": round(duration_seconds / 3600, 2),
            "coordinates": coordinates,
        }