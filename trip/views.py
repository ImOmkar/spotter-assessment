from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.route_service import RouteService
from .services.hos_engine import HOSEngine
from .services.stop_service import StopService
from .services.hos_validator import HOSValidator


class PlanTripAPIView(APIView):

    def post(self, request):

        data = request.data

        # Field validation
        required_fields = [
            "pickup_lat",
            "pickup_lng",
            "drop_lat",
            "drop_lng",
            "current_cycle_hours",
        ]

        for field in required_fields:
            if data.get(field) in [None, ""]:
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
        # Numeric Conversion
        try:
            pickup_lat = float(data.get("pickup_lat"))
            pickup_lng = float(data.get("pickup_lng"))
            drop_lat = float(data.get("drop_lat"))
            drop_lng = float(data.get("drop_lng"))
            current_cycle_hours = float(
                data.get("current_cycle_hours")
            )
        except ValueError:
            return Response(
                {"error": "Invalid numeric values"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # FMCSA Validation
        if current_cycle_hours < 0 or current_cycle_hours > 70:
            return Response(
                {"error": "Cycle hours must be between 0 and 70"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Current Location
        current_lat = data.get("current_lat")
        current_lng = data.get("current_lng")

        try:
            if current_lat and current_lng:
                current_lat = float(current_lat)
                current_lng = float(current_lng)
            else:
                # fallback - driver assumed at pickup
                current_lat = pickup_lat
                current_lng = pickup_lng
        except ValueError:
            return Response(
                {"error": "Invalid current location"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Route Service
        route = RouteService.get_route(
            start_coords=(pickup_lng, pickup_lat),
            end_coords=(drop_lng, drop_lat),
        )

        if not route or not route.get("coordinates"):
            return Response(
                {"error": "Route generation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # HOS Engine
        engine = HOSEngine(
            total_miles=route["distance_miles"],
            current_cycle_hours=current_cycle_hours,
        )

        hos_result = engine.run()

        # Compliance Validation
        validation = HOSValidator.validate(
            hos_result["logs"],
            hos_result["summary"]["final_cycle_hours"],
        )

        # Stop Generation
        stops = StopService.generate_stops(
            hos_result["logs"],
            route["coordinates"],
            route["distance_miles"],
        )

        # Final Response
        return Response(
            {
                "route": route,
                "hos": hos_result,
                "stops": stops,
                "compliance": validation,
            },
            status=status.HTTP_200_OK,
        )