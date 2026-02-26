import { useMap } from "react-leaflet"
import { useState, useEffect } from "react"

import {
    MapContainer,
    TileLayer,
    Polyline,
    Marker,
    Popup,
  } from "react-leaflet";
  
  import "../mapFix";
  
  import {
    pickupIcon,
    fuelIcon,
    breakIcon,
    dropIcon,
    truckIcon
  } from "../mapIcons";
  
  
  export default function MapView({ route, stops, layoutTrigger, hoverSegment   }) {

    if (!route?.coordinates?.length) return null;
    
    const coordinates = route.coordinates;
  
    const [animatedRoute, setAnimatedRoute] = useState([]);
    const [showStops, setShowStops] = useState(false);
    const [mapReady, setMapReady] = useState(false);
    const [truckPosition, setTruckPosition] = useState(null);   
    const [highlightRoute, setHighlightRoute] = useState([]);

    useEffect(() => {
        if (!mapReady) return;
        if (!coordinates) return;
      
        let index = 0;
        const CHUNK_SIZE = 80;
      
        const interval = setInterval(() => {
      
          const slice = coordinates.slice(index, index + CHUNK_SIZE);
      
          const nextChunk = slice.map(c => [c.lat, c.lng]);
      
          setAnimatedRoute(prev => [...prev, ...nextChunk]);
      
          // 🚛 move truck
          if (slice.length > 0) {
            const lastPoint = slice[slice.length - 1];
            setTruckPosition([lastPoint.lat, lastPoint.lng]);
          }
      
          index += CHUNK_SIZE;
      
          if (index >= coordinates.length) {
            clearInterval(interval);
      
            setTimeout(() => {
              setShowStops(true);
            }, 300);
          }
      
        }, 16);
      
        return () => clearInterval(interval);
      
    }, [coordinates, mapReady]);

    useEffect(() => {
        if (!hoverSegment || !route?.coordinates) {
          setHighlightRoute([]);
          return;
        }
      
        // simple proportional mapping
        const totalPoints = route.coordinates.length;
      
        const startIndex = Math.floor(
          (hoverSegment.start / 24) * totalPoints
        );
      
        const endIndex = Math.floor(
          (hoverSegment.end / 24) * totalPoints
        );
      
        const segment = route.coordinates
          .slice(startIndex, endIndex)
          .map(c => [c.lat, c.lng]);
      
        setHighlightRoute(segment);
      
    }, [hoverSegment, route]);

    useEffect(() => {
        setAnimatedRoute([]);
        setShowStops(false);
        setTruckPosition(null);
        setMapReady(false);
    }, [route]);

    const positions = route.coordinates.map(
      (c) => [c.lat, c.lng]
    );
  
    const getIcon = (type) => {
      switch (type) {
        case "pickup":
          return pickupIcon;
        case "fuel":
          return fuelIcon;
        case "break":
          return breakIcon;
        case "dropoff":
          return dropIcon;
        default:
          return pickupIcon;
      }
    };
  
    return (
      <MapContainer
        center={positions[0]}
        zoom={5}
        className="h-full w-full"
      >

        <MapResizeHandler trigger={layoutTrigger} />
        
        <AutoFitBounds
            coordinates={coordinates}
            onReady={() => setMapReady(true)}
        />

        <TileLayer
          attribution="OpenStreetMap"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
  
        {/* Route */}
        <Polyline
            positions={animatedRoute}
            pathOptions={{
                color: "#2563eb",
                weight: 5,
            }}
        />

        <Polyline
        positions={highlightRoute}
        pathOptions={{
            color: "orange",
            weight: 7,
        }}
        />

        {/* Moving Truck */}
        {truckPosition && (
        <Marker position={truckPosition} icon={truckIcon}>
            <Popup>Truck En Route</Popup>
        </Marker>
        )}
  
        {/* Stops */}
        {showStops &&
        stops.filter(
          s => Number.isFinite(s.lat) && Number.isFinite(s.lng)
        ).map((stop, index) => (
            <Marker
            key={index}
            position={[stop.lat, stop.lng]}
            icon={getIcon(stop.type)}
            >
            <Popup>
                <strong>{stop.type}</strong>
                <br />
                Day {stop.day}
            </Popup>
            </Marker>
        ))}
      </MapContainer>
    );
  }

  function AutoFitBounds({ coordinates, onReady }) {
    const map = useMap();
  
    useEffect(() => {
      if (!coordinates?.length) return;
  
      const bounds = coordinates
        .filter(
          c =>
            Number.isFinite(c.lat) &&
            Number.isFinite(c.lng)
        )
        .map(c => [c.lat, c.lng]);
  
      if (!bounds.length) return;
  
      map.flyToBounds(bounds, {
        padding: [60, 60],
        duration: 2,
      });
  
      const handleMoveEnd = () => {
        onReady();
        map.off("moveend", handleMoveEnd);
      };
  
      map.on("moveend", handleMoveEnd);
  
    }, [coordinates, map, onReady]);
  
    return null;
  }

  function MapResizeHandler({ trigger }) {
    const map = useMap();
  
    useEffect(() => {
      setTimeout(() => {
        map.invalidateSize();
      }, 300); // wait for panel animation
    }, [trigger, map]);
  
    return null;
  }