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

#         print("response from deleted API", response)

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



# import requests


# class RouteService:

#     BASE_URL = "https://router.project-osrm.org/route/v1/driving"

#     @staticmethod
#     def get_route(start_coords, end_coords):
#         """
#         Uses OSRM public routing API.
#         No API key required.
#         """

#         start_lng, start_lat = start_coords
#         end_lng, end_lat = end_coords

#         url = (
#             f"{RouteService.BASE_URL}/"
#             f"{start_lng},{start_lat};{end_lng},{end_lat}"
#             f"?overview=full&geometries=geojson"
#         )

#         print("hitting this URL", url)

#         response = requests.get(url, timeout=10)

#         print("response from osrm", response)

#         response.raise_for_status()

#         data = response.json()

#         if not data.get("routes"):
#             raise Exception("No route returned from OSRM")

#         route = data["routes"][0]

#         distance_meters = route["distance"]
#         duration_seconds = route["duration"]

#         coords = route["geometry"]["coordinates"]

#         # OSRM returns [lng, lat]
#         coordinates = [
#             {"lat": float(c[1]), "lng": float(c[0])}
#             for c in coords
#             if len(c) >= 2
#         ]

#         if len(coordinates) < 2:
#             raise Exception("Invalid coordinates from OSRM")

#         return {
#             "distance_miles": round(distance_meters / 1609.34, 2),
#             "duration_hours": round(duration_seconds / 3600, 2),
#             "coordinates": coordinates,
#         }


import requests
import polyline
from django.conf import settings


class RouteService:

    ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
    OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

    @staticmethod
    def get_route(start_coords, end_coords):
        """
        Try OpenRouteService first.
        If it fails → fallback to OSRM automatically.
        """

        # Try ORS only if API key exists
        if hasattr(settings, "ORS_API_KEY") and settings.ORS_API_KEY:
            try:
                print("Trying OpenRouteService...")
                return RouteService._get_ors_route(start_coords, end_coords)
            except Exception as e:
                print("ORS failed. Falling back to OSRM:", str(e))

        # Fallback to OSRM
        print("Using OSRM fallback...")
        return RouteService._get_osrm_route(start_coords, end_coords)

    # ---------------------------------------------------
    # 1️⃣ OPENROUTESERVICE
    # ---------------------------------------------------
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

    # ---------------------------------------------------
    # 2️⃣ OSRM FALLBACK
    # ---------------------------------------------------
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

        # OSRM returns [lng, lat]
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