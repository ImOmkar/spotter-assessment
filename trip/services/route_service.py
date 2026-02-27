import requests
import polyline
import math
from django.conf import settings


class RouteService:

    ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
    OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

    @staticmethod
    def get_route(start_coords, end_coords):
        """
        Routing:
        1️. OpenRouteService
        2️. OSRM
        3️. Internal mock fallback
        """

        # Try ORS
        if hasattr(settings, "ORS_API_KEY") and settings.ORS_API_KEY:
            try:
                print("Trying OpenRouteService...")
                return RouteService._get_ors_route(start_coords, end_coords)
            except Exception as e:
                print("ORS failed:", str(e))

        # Try OSRM
        try:
            print("Trying OSRM...")
            return RouteService._get_osrm_route(start_coords, end_coords)
        except Exception as e:
            print("OSRM failed:", str(e))

        # Final fallback
        print("Using internal mock fallback...")
        return RouteService._get_mock_route(start_coords, end_coords)

    # OPEN ROUTE SERVICE
    @staticmethod
    def _get_ors_route(start_coords, end_coords):

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
            RouteService.ORS_URL,
            json=body,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        route = data["routes"][0]
        summary = route["summary"]

        distance_meters = summary["distance"]
        duration_seconds = summary["duration"]

        encoded_geometry = route["geometry"]
        decoded_coords = polyline.decode(encoded_geometry)

        coordinates = [
            {"lat": lat, "lng": lng}
            for lat, lng in decoded_coords
        ]

        if len(coordinates) < 2:
            raise Exception("Invalid ORS coordinates")

        return {
            "distance_miles": round(distance_meters / 1609.34, 2),
            "duration_hours": round(duration_seconds / 3600, 2),
            "coordinates": coordinates,
        }

    # OSRM
    @staticmethod
    def _get_osrm_route(start_coords, end_coords):

        start_lng, start_lat = start_coords
        end_lng, end_lat = end_coords

        url = (
            f"{RouteService.OSRM_URL}/"
            f"{start_lng},{start_lat};{end_lng},{end_lat}"
            f"?overview=full&geometries=geojson"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("routes"):
            raise Exception("No route returned from OSRM")

        route = data["routes"][0]

        distance_meters = route["distance"]
        duration_seconds = route["duration"]

        coords = route["geometry"]["coordinates"]

        coordinates = [
            {"lat": float(c[1]), "lng": float(c[0])}
            for c in coords
            if len(c) >= 2
        ]

        if len(coordinates) < 2:
            raise Exception("Invalid OSRM coordinates")

        return {
            "distance_miles": round(distance_meters / 1609.34, 2),
            "duration_hours": round(duration_seconds / 3600, 2),
            "coordinates": coordinates,
        }

    # INTERNAL MOCK ROUTE
    @staticmethod
    def _get_mock_route(start_coords, end_coords):
        """
        Straight-line fallback with haversine distance.
        Always works.
        """

        start_lng, start_lat = start_coords
        end_lng, end_lat = end_coords

        points = 200
        coordinates = []

        for i in range(points + 1):
            ratio = i / points
            lat = start_lat + (end_lat - start_lat) * ratio
            lng = start_lng + (end_lng - start_lng) * ratio

            coordinates.append({
                "lat": float(lat),
                "lng": float(lng),
            })

        distance_miles = RouteService._haversine(
            start_lat, start_lng, end_lat, end_lng
        )

        # Assume avg 50mph for duration fallback
        duration_hours = distance_miles / 50

        return {
            "distance_miles": round(distance_miles, 2),
            "duration_hours": round(duration_hours, 2),
            "coordinates": coordinates,
        }

    # HAVERSINE DISTANCE
    @staticmethod
    def _haversine(lat1, lon1, lat2, lon2):
        R = 3958.8  # Earth radius in miles

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c