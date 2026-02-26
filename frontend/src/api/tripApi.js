import axios from "axios";

const API = "http://127.0.0.1:8000/api";

export const planTrip = async (tripData) => {
    const response = await axios.post(`${API}/plan-trip/`, tripData);
    return response.data;
  };