import requests
import polyline
from django.conf import settings


class RouteService:

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

    @staticmethod
    def get_route(start_coords, end_coords):

        headers = {
            "Authorization": settings.ORS_API_KEY,
            "Content-Type": "application/json",
        }

        body = {
            "coordinates": [
                list(start_coords),
                list(end_coords),
            ]
        }

        response = requests.post(
            RouteService.BASE_URL,
            json=body,
            headers=headers,
        )

        response.raise_for_status()

        data = response.json()

        # Extract route safely
        route = data["routes"][0]
        summary = route["summary"]

        distance_meters = summary["distance"]
        duration_seconds = summary["duration"]

        encoded_geometry = route["geometry"]

        # Decode polyline
        decoded_coords = polyline.decode(encoded_geometry)

        coordinates = [
            {"lat": lat, "lng": lng}
            for lat, lng in decoded_coords
        ]

        return {
            "distance_miles": round(distance_meters / 1609.34, 2),
            "duration_hours": round(duration_seconds / 3600, 2),
            "coordinates": coordinates,
        }