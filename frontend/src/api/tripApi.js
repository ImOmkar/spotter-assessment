import axios from "axios";

const API = "https://SpotterAssessment.pythonanywhere.com/api";

export const planTrip = async (tripData) => {
    const response = await axios.post(`${API}/plan-trip/`, tripData);
    return response.data;
  };