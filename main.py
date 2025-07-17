from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, time, timedelta
import re
import os

app = Flask(__name__)

# Sleep cycle constants
SLEEP_CYCLE_MINUTES = 90
FALL_ASLEEP_MINUTES = 15
NAP_INCREMENT_MINUTES = 15

def parse_time(time_str):
    """Parse time string in HH:MM format to time object"""
    hour, minute = map(int, time_str.split(':'))
    return time(hour, minute)

def format_time(t):
    """Format time object to HH:MM string"""
    return f"{t.hour:02d}:{t.minute:02d}"

def add_minutes_to_time(t, minutes):
    """Add minutes to a time object, handling day overflow"""
    dt = datetime.combine(datetime.today(), t)
    dt += timedelta(minutes=minutes)
    return dt.time()

def subtract_minutes_from_time(t, minutes):
    """Subtract minutes from a time object, handling day underflow"""
    dt = datetime.combine(datetime.today(), t)
    dt -= timedelta(minutes=minutes)
    return dt.time()

def round_to_nearest_15_minutes(t):
    """Round time to nearest 15-minute increment"""
    total_minutes = t.hour * 60 + t.minute
    rounded_minutes = round(total_minutes / 15) * 15
    
    if rounded_minutes >= 1440:  # 24 hours
        rounded_minutes = 0
    
    hours = rounded_minutes // 60
    minutes = rounded_minutes % 60
    return time(hours, minutes)

def calculate_bedtimes_from_wake_time(wake_time_str):
    """Mode 1: Calculate ideal bedtimes from a given wake time"""
    wake_time = parse_time(wake_time_str)
    bedtimes = []
    
    for cycles in range(4, 7):
        total_sleep_minutes = cycles * SLEEP_CYCLE_MINUTES + FALL_ASLEEP_MINUTES
        bedtime = subtract_minutes_from_time(wake_time, total_sleep_minutes)
        bedtime = round_to_nearest_15_minutes(bedtime)
        bedtimes.append(format_time(bedtime))
    
    return bedtimes

def calculate_wake_times_from_bedtime(bedtime_str):
    """Mode 2: Calculate ideal wake times from a given bedtime"""
    bedtime = parse_time(bedtime_str)
    wake_times = []
    
    for cycles in range(4, 7):
        total_sleep_minutes = cycles * SLEEP_CYCLE_MINUTES + FALL_ASLEEP_MINUTES
        wake_time = add_minutes_to_time(bedtime, total_sleep_minutes)
        wake_time = round_to_nearest_15_minutes(wake_time)
        wake_times.append(format_time(wake_time))
    
    return wake_times

def calculate_current_wake_times():
    """Mode 3: Calculate recommended wake times starting from current time"""
    current_time = datetime.now().time()
    wake_times = []
    
    for i in range(1, 49):
        wake_time = add_minutes_to_time(current_time, i * NAP_INCREMENT_MINUTES)
        wake_time = round_to_nearest_15_minutes(wake_time)
        wake_times.append(format_time(wake_time))
    
    return wake_times

@app.route('/')
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Sleep API - Intelligent sleep time recommendations",
        "version": "1.0.0",
        "endpoints": {
            "POST /sleep-recommendations": "Get sleep time recommendations",
            "GET /web": "Web interface"
        },
        "modes": {
            "1": "Calculate bedtimes from wake time",
            "2": "Calculate wake times from bedtime", 
            "3": "Get wake times from current time"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/sleep-recommendations', methods=['POST'])
def get_sleep_recommendations():
    """Get sleep time recommendations based on the specified mode"""
    try:
        data = request.get_json()
        
        if not data or 'mode' not in data:
            return jsonify({"error": "Mode is required"}), 400
        
        mode = data['mode']
        
        if mode not in [1, 2, 3]:
            return jsonify({"error": "Mode must be 1, 2, or 3"}), 400
        
        if mode == 1:
            if 'wake_time' not in data:
                return jsonify({"error": "Wake time is required for mode 1"}), 400
            
            wake_time = data['wake_time']
            if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', wake_time):
                return jsonify({"error": "Wake time must be in HH:MM format (24-hour)"}), 400
            
            recommendations = calculate_bedtimes_from_wake_time(wake_time)
            return jsonify({
                "mode": 1,
                "input_time": wake_time,
                "recommendations": recommendations,
                "message": f"Ideal bedtimes for waking up at {wake_time} (4-6 sleep cycles)"
            })
        
        elif mode == 2:
            if 'bedtime' not in data:
                return jsonify({"error": "Bedtime is required for mode 2"}), 400
            
            bedtime = data['bedtime']
            if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', bedtime):
                return jsonify({"error": "Bedtime must be in HH:MM format (24-hour)"}), 400
            
            recommendations = calculate_wake_times_from_bedtime(bedtime)
            return jsonify({
                "mode": 2,
                "input_time": bedtime,
                "recommendations": recommendations,
                "message": f"Ideal wake times for going to bed at {bedtime} (4-6 sleep cycles)"
            })
        
        elif mode == 3:
            recommendations = calculate_current_wake_times()
            current_time = datetime.now().strftime("%H:%M")
            return jsonify({
                "mode": 3,
                "input_time": current_time,
                "recommendations": recommendations,
                "message": f"Recommended wake times starting from current time ({current_time})"
            })
    
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/web')
def web_interface():
    """Serve the web interface"""
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    print("🌙 Sleep API Starting...")
    print("Web interface: http://localhost:8000/web")
    print("API endpoint: http://localhost:8000/")
    print("Press Ctrl+C to stop")
    print()
    app.run(host='0.0.0.0', port=8000, debug=True) 