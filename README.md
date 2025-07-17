# Sleep API

An intelligent REST API that recommends optimal sleep and wake times based on sleep cycle science. The API uses 90-minute sleep cycles and accounts for the 15 minutes it typically takes to fall asleep.

## Features

- **Mode 1**: Calculate ideal bedtimes from a target wake time
- **Mode 2**: Calculate ideal wake times from a target bedtime  
- **Mode 3**: Get recommended wake times starting from current time
- Input validation with informative error messages
- All times returned in 24-hour format
- Beautiful web interface with 12-hour time display
- Interactive API documentation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sleapi
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

### Simple Start
```bash
# Install Flask (if not already installed)
pip install flask

# Run the API
python3 main.py
```

The API will be available at `http://localhost:8000`

### Web Interface
Visit `http://localhost:8000/web` for a beautiful web interface to test the API with 12-hour time display.

## API Endpoints

### POST /sleep-recommendations

Get sleep time recommendations based on the specified mode.

#### Request Body
```json
{
  "mode": 1,
  "wake_time": "07:00",
  "bedtime": null
}
```

#### Mode 1: Calculate Bedtimes from Wake Time
- **Purpose**: Find ideal bedtimes for a target wake time
- **Required**: `wake_time` (HH:MM format)
- **Returns**: 3 bedtime options (4, 5, and 6 sleep cycles)

**Example Request:**
```json
{
  "mode": 1,
  "wake_time": "07:00"
}
```

**Example Response:**
```json
{
  "mode": 1,
  "input_time": "07:00",
  "recommendations": ["00:45", "23:15", "21:45"],
  "message": "Ideal bedtimes for waking up at 07:00 (4-6 sleep cycles)"
}
```

#### Mode 2: Calculate Wake Times from Bedtime
- **Purpose**: Find ideal wake times for a target bedtime
- **Required**: `bedtime` (HH:MM format)
- **Returns**: 3 wake time options (4, 5, and 6 sleep cycles)

**Example Request:**
```json
{
  "mode": 2,
  "bedtime": "23:00"
}
```

**Example Response:**
```json
{
  "mode": 2,
  "input_time": "23:00",
  "recommendations": ["05:15", "06:45", "08:15"],
  "message": "Ideal wake times for going to bed at 23:00 (4-6 sleep cycles)"
}
```

#### Mode 3: Current Time Wake Recommendations
- **Purpose**: Get wake time recommendations starting from current time
- **Required**: No input required
- **Returns**: 48 wake times in 15-minute increments (12 hours)

**Example Request:**
```json
{
  "mode": 3
}
```

**Example Response:**
```json
{
  "mode": 3,
  "input_time": "14:30",
  "recommendations": ["14:45", "15:00", "15:15", ...],
  "message": "Recommended wake times starting from current time (14:30 UTC)"
}
```

### GET /

Root endpoint with API information.

**Response:**
```json
{
  "message": "Sleep API - Intelligent sleep time recommendations",
  "version": "1.0.0",
  "endpoints": {
    "POST /sleep-recommendations": "Get sleep time recommendations",
    "GET /docs": "Interactive API documentation"
  },
  "modes": {
    "1": "Calculate bedtimes from wake time",
    "2": "Calculate wake times from bedtime",
    "3": "Get wake times from current time"
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

## Sleep Science Logic

The API uses the following sleep science principles:

- **Sleep Cycles**: 90 minutes each
- **Fall Asleep Time**: 15 minutes
- **Optimal Cycles**: 4-6 cycles per night
- **Time Format**: 24-hour format (HH:MM)
- **Rounding**: All times rounded to nearest 15-minute increment

### Calculation Examples

**Mode 1 Example** (Wake at 07:00):
- 4 cycles: 07:00 - (4×90 + 15) = 07:00 - 375 min = 00:45
- 5 cycles: 07:00 - (5×90 + 15) = 07:00 - 465 min = 23:15  
- 6 cycles: 07:00 - (6×90 + 15) = 07:00 - 555 min = 21:45

**Mode 2 Example** (Bed at 23:00):
- 4 cycles: 23:00 + (4×90 + 15) = 23:00 + 375 min = 05:15
- 5 cycles: 23:00 + (5×90 + 15) = 23:00 + 465 min = 06:45
- 6 cycles: 23:00 + (6×90 + 15) = 23:00 + 555 min = 08:15

## Web Interface

The Sleep API includes a beautiful web interface for easy testing:

- **12-hour time display** with 24-hour format in parentheses
- **Three calculation modes** with intuitive UI
- **Real-time validation** and error handling
- **Responsive design** for desktop and mobile
- **Sleep cycle information** for each recommendation

Access the web interface at `http://localhost:8000/web` after starting the server.

## Error Handling

The API provides informative error messages for:

- **Missing required fields**: "Wake time is required for mode 1"
- **Invalid time format**: "Wake time must be in HH:MM format (24-hour)"
- **Invalid mode**: "Mode must be 1, 2, or 3"
- **Invalid time values**: Validation errors for hours > 23 or minutes > 59

## Future Enhancements

The API is designed to be easily extendable for future features:

- **Timezone Support**: Add timezone awareness for global users
- **Alarm Integration**: Connect with alarm systems
- **Sleep Quality Tracking**: Store and analyze sleep patterns
- **Personalization**: User-specific sleep cycle lengths
- **Sleep History**: Track and recommend based on past sleep data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the MIT License. 
