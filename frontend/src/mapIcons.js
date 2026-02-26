import L from "leaflet";
import truckImg from "./assets/icons/truck.png";
import breakImg from "./assets/icons/break.png"; 
import fuelImg from "./assets/icons/fuel.png"; 
import pickupImg from "./assets/icons/pickup.png"; 



export const pickupIcon = new L.Icon({
  iconUrl: pickupImg,
  iconSize: [30, 30],
});

export const fuelIcon = new L.Icon({
  iconUrl: fuelImg,
  iconSize: [28, 28],
});

export const breakIcon = new L.Icon({
  iconUrl: breakImg,
  iconSize: [28, 28],
});

export const dropIcon = new L.Icon({
  iconUrl: pickupImg,
  iconSize: [30, 30],
});

export const truckIcon = new L.Icon({
    iconUrl: truckImg,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
  });