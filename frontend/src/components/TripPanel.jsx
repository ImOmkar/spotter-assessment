import { useState } from "react";


export default function TripPanel({ onPlan }) {

  const [form, setForm] = useState({
    current_lat: 47.6062,
    current_lng: -122.3321,
    pickup_lat: 45.5152,
    pickup_lng: -122.6784,
    drop_lat: 25.7617,
    drop_lng: -80.1918,
    current_cycle_hours: 20,
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = () => {
    onPlan({
      ...form,
      current_lat: Number(form.current_lat),
      current_lng: Number(form.current_lng),
      pickup_lat: Number(form.pickup_lat),
      pickup_lng: Number(form.pickup_lng),
      drop_lat: Number(form.drop_lat),
      drop_lng: Number(form.drop_lng),
      current_cycle_hours: Number(form.current_cycle_hours),
    });
  };

  return (
    <div className="p-5 bg-white shadow-lg h-full space-y-4">

      <h2 className="text-xl font-semibold">
        Plan Trip
      </h2>

      <h3 className="text-sm font-semibold text-gray-600 mt-2">
      Pickup Location
        </h3>

        <input
        name="current_lat"
        placeholder="Current Latitude"
        onChange={handleChange}
        value={form.current_lat}
        // defaultValue="47.6062"
        className="w-full border p-2 rounded"
        />

        <input
        name="current_lng"
        placeholder="Current Longitude"
        onChange={handleChange}
        value={form.current_lng}
        // defaultValue="-122.3321"
        className="w-full border p-2 rounded"
        />

      <input
        name="pickup_lat"
        placeholder="Pickup Latitude"
        onChange={handleChange}
        value={form.pickup_lat}
        // defaultValue="45.5152"
        className="w-full border p-2 rounded"
      />

      <input
        name="pickup_lng"
        placeholder="Pickup Longitude"
        onChange={handleChange}
        value={form.pickup_lng}
        // defaultValue="-122.6784"
        className="w-full border p-2 rounded"
      />

      <input
        name="drop_lat"
        placeholder="Drop Latitude"
        onChange={handleChange}
        value={form.drop_lat}
        // defaultValue="25.7617"
        className="w-full border p-2 rounded"
      />

      <input
        name="drop_lng"
        placeholder="Drop Longitude"
        onChange={handleChange}
        value={form.drop_lng}
        // defaultValue="-80.1918"
        className="w-full border p-2 rounded"
      />

      <input
        name="current_cycle_hours"
        placeholder="Cycle Hours Used"
        onChange={handleChange}
        value={form.current_cycle_hours}
        // defaultValue={20}
        className="w-full border p-2 rounded"
      />

      <button
        onClick={handleSubmit}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Plan Trip
      </button>
    </div>
  );
}