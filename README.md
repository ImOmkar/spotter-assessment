<!-- 🚛 Trip Planner & FMCSA HOS Log Simulator

This project is a full-stack application built with Django (backend) and React (frontend) that plans long-haul truck trips, applies FMCSA Hours of Service (HOS) regulations, and generates multi-day Electronic Logging Device (ELD) log sheets. The application accepts trip inputs, calculates a route using a free map API, simulates driver duty status over multiple days, and renders both the route and the daily log sheets visually.

🎯 Objective

The objective of this project is to build an application that:

Accepts trip details as inputs

Calculates the route between pickup and dropoff

Applies FMCSA HOS rules

Generates daily log sheets (multiple days if required)

Draws ELD graph grids programmatically

Displays route, stops, and rest periods on a map

The system simulates a property-carrying interstate driver under a 70-hour / 8-day cycle rule.

📥 Inputs

The application accepts the following inputs:

Current location (latitude & longitude) – optional

Pickup location (latitude & longitude)

Dropoff location (latitude & longitude)

Current Cycle Used (Hours)

Locations are provided as coordinates instead of addresses to keep routing deterministic and avoid adding external geocoding dependencies. If current location is not provided, the driver is assumed to start at the pickup location.

📤 Outputs

After submitting trip details, the application generates:

🗺 Route Visualization

Full route drawn on interactive map

Pickup marker

Dropoff marker

Fuel stop markers (at least once every 1,000 miles)

30-minute break markers

Animated route progression

Highlighting of route segments during log hover

📋 Daily ELD Log Sheets

24-hour graph grid (Off Duty / Sleeper / Driving / On Duty)

Multi-day log generation for long trips

Pickup and dropoff included as on-duty events

30-minute break automatically inserted

Fuel stops reflected in remarks

Driving and on-duty totals calculated per day

Driver remarks automatically generated

Compliance validation response returned from backend

🚦 FMCSA Assumptions Implemented

The system follows these assumptions exactly as specified:

Property-carrying driver

70 hours / 8-day cycle rule

No adverse driving conditions

11-hour driving limit

14-hour duty window

30-minute break required after 8 cumulative driving hours

Fuel stop at least once every 1,000 miles

1 hour for pickup

1 hour for dropoff

10-hour off-duty reset

🧠 HOS Engine Logic Overview

The HOS simulation runs day-by-day until the trip is complete or the 70-hour cycle limit is reached.

Daily flow:

Driver begins day at 06:00 after overnight off-duty.

Pickup event occurs (1 hour on-duty, first day only).

Driving begins.

After 8 hours of cumulative driving → 30-minute break inserted.

Fuel stops inserted automatically every 1,000 miles.

Driving ends when:

11 driving hours reached

14-hour duty window reached

Or trip miles complete

Dropoff occurs on final day.

10-hour off-duty reset applied.

Cycle hours accumulate and are validated against 70-hour limit.

The system generates multiple daily log sheets automatically when required.

🏗 Backend Architecture

The Django backend is structured with service-based separation of responsibilities:

route_service.py → Handles external routing API call and coordinate decoding

hos_engine.py → Core FMCSA simulation logic

stop_service.py → Generates map markers for pickup, fuel, break, and dropoff

hos_validator.py → Validates compliance with 11-hour, 14-hour, and 70-hour rules

API Endpoint

```
POST /api/plan-trip/
```

Returns:

Route data

HOS simulation results

Generated stop markers

Compliance validation response

Backend includes defensive validation for:

Missing required fields

Invalid numeric values

Invalid cycle hours

Route failure protection

Returns:

Route data

HOS simulation results

Generated stop markers

Compliance validation response

Backend includes defensive validation for:

Missing required fields

Invalid numeric values

Invalid cycle hours

Route failure protection

🧪 Compliance Validation

A compliance validator verifies:

No day exceeds 11 driving hours

No day exceeds 14 on-duty hours

Total cycle hours do not exceed 70

The validation result is returned in the API response.

▶ How To Run Locally

```
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend

```
cd frontend
npm install
npm run dev
```

🌍 Deployment

Frontend can be deployed on Vercel.
Backend can be deployed on Render or similar cloud provider.

The hosted version is included in submission.

🎥 Loom Walkthrough

A 3–5 minute Loom video explains:

Architecture decisions

HOS rule implementation

Multi-day log generation

Compliance validation

Map integration

Assumptions made


📌 Design Decisions

Coordinates used instead of address search to keep routing deterministic.

HOS rules implemented explicitly based on FMCSA documentation.

Fuel and break logic automated.

Multi-day logs generated dynamically.

Validation added to prevent NaN coordinate errors.

UI designed to be clean and professional while focusing on core functionality.

✅ Completion Status

This implementation satisfies:

Trip input handling

Route generation

FMCSA-compliant HOS simulation

Fuel and break enforcement

Multi-day ELD log drawing

Stop visualization on map

Compliance validation

Clean and functional UI  -->



# 🚛 Trip Planner & FMCSA HOS Log Simulator

## Overview

This project is a full-stack application built with:

- **Django** (Backend)
- **React** (Frontend)

It plans long-haul truck trips, applies FMCSA Hours of Service (HOS) regulations, and generates multi-day Electronic Logging Device (ELD) log sheets.

The system:
- Accepts trip inputs
- Calculates a route using a free map API
- Simulates driver duty status across multiple days
- Renders both the route and daily log sheets visually

The simulation follows a property-carrying interstate driver under the 70-hour / 8-day cycle rule.

---

## Objective

The objective of this application is to:

- Accept trip details as input
- Calculate the route between pickup and dropoff
- Apply FMCSA HOS rules
- Generate daily log sheets (multi-day if required)
- Draw ELD graph grids programmatically
- Display route, stops, and rest periods on a map

---

## Inputs

The application accepts:

- Current location (latitude & longitude) — optional
- Pickup location (latitude & longitude)
- Dropoff location (latitude & longitude)
- Current Cycle Used (Hours)

### Design Note

Coordinates are used instead of addresses to:
- Keep routing deterministic
- Avoid external geocoding dependencies

If current location is not provided, the driver starts at pickup.

---

## Outputs

### 🗺 Route Visualization

- Full route drawn on interactive map
- Pickup marker
- Dropoff marker
- Fuel stop markers (≥ every 1,000 miles)
- 30-minute break markers
- Animated route progression
- Route highlighting during log hover

---

### Daily ELD Log Sheets

- 24-hour graph grid (Off Duty / Sleeper / Driving / On Duty)
- Multi-day log generation for long trips
- Pickup and dropoff included as on-duty events
- 30-minute break automatically inserted
- Fuel stops reflected in remarks
- Driving and on-duty totals calculated per day
- Driver remarks auto-generated
- Compliance validation returned from backend

---

## FMCSA Assumptions Implemented

The system strictly follows:

- Property-carrying driver
- 70 hours / 8-day cycle rule
- No adverse driving conditions
- 11-hour driving limit
- 14-hour duty window
- 30-minute break after 8 cumulative driving hours
- Fuel stop at least once every 1,000 miles
- 1 hour for pickup
- 1 hour for dropoff
- 10-hour off-duty reset

---

## HOS Engine Logic Overview

The simulation runs day-by-day until:

- Trip is complete
OR
- 70-hour cycle limit is reached

### Daily Flow

1. Driver begins day at 06:00 after overnight off-duty
2. Pickup event occurs (1 hour on-duty, first day only)
3. Driving begins
4. After 8 hours cumulative driving → 30-minute break inserted
5. Fuel stops inserted automatically every 1,000 miles
6. Driving ends when:
   - 11 driving hours reached
   - 14-hour duty window reached
   - Trip miles complete
7. Dropoff occurs on final day
8. 10-hour off-duty reset applied
9. Cycle hours accumulate and validated against 70-hour limit

Multi-day logs are generated automatically when required.

---

## Backend Architecture

Backend is structured using service-based separation of responsibilities:

### Services

- `route_service.py`
  - Handles external routing API call
  - Decodes route coordinates

- `hos_engine.py`
  - Core FMCSA simulation logic

- `stop_service.py`
  - Generates map markers for pickup, fuel, break, dropoff

- `hos_validator.py`
  - Validates compliance with 11-hour, 14-hour, and 70-hour rules

---

## API Endpoint

```
POST /api/plan-trip/
```


### Returns

- Route data
- HOS simulation results
- Generated stop markers
- Compliance validation response

---

## Backend Defensive Validation

The backend validates:

- Missing required fields
- Invalid numeric values
- Invalid cycle hours
- Route failure protection

---

## Compliance Validation

Validator ensures:

- No day exceeds 11 driving hours
- No day exceeds 14 on-duty hours
- Total cycle hours do not exceed 70

Validation result is returned in the API response.

---

## How To Run Locally

### Backend

```
cd backend
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```
cd frontend
npm install
npm run dev
```


---

## Deployment

- Frontend → Vercel
- Backend → Render (or similar cloud provider)

Hosted version included in submission.

---

## Loom Walkthrough

The 3–5 minute Loom video explains:

- Architecture decisions
- HOS rule implementation
- Multi-day log generation
- Compliance validation
- Map integration
- Assumptions made

---

## Design Decisions

- Coordinates used instead of address search for deterministic routing
- HOS rules implemented explicitly from FMCSA documentation
- Fuel and break logic automated
- Multi-day logs generated dynamically
- Validation added to prevent NaN coordinate errors
- UI designed clean and professional with focus on core functionality

---

## Completion Status

This implementation satisfies:

- Trip input handling
- Route generation
- FMCSA-compliant HOS simulation
- Fuel and break enforcement
- Multi-day ELD log drawing
- Stop visualization on map
- Compliance validation
- Clean and functional UI


