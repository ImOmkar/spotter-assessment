import axios from "axios";

const API = "https://spotterassessment.pythonanywhere.com/api"; PROD

// const API = "http://127.0.0.1:8000/api"; // DEV


export const planTrip = async (tripData) => {
    const response = await axios.post(`${API}/plan-trip/`, tripData);
    return response.data;
  };