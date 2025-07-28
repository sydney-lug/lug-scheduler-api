from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return "Game Slot Generator is live!"

@app.route('/generate-game-slots', methods=['POST'])
def generate_game_slots():
    data = request.json
    print("Received data:", data, file=sys.stderr)  # <- log raw data
    game_duration = int(data.get('default_game_duration', 60))  # in minutes
    bookings = data.get('bookings', [])

    game_slots = []

    for booking in bookings:
        try:
            # ✅ Validate required fields
            required_fields = ['start_time', 'end_time', 'league', 'date', 'week', 'arena', 'pad']
            for field in required_fields:
                if not booking.get(field):
                    raise ValueError(f"Missing required field: {field}")

            # Parse and calculate
            start = datetime.strptime(booking['start_time'], '%H:%M')
            end = datetime.strptime(booking['end_time'], '%H:%M')
            booking_duration = int((end - start).total_seconds() / 60)

            num_slots = booking_duration // game_duration
            for i in range(num_slots):
                slot_start = (start + timedelta(minutes=i * game_duration)).strftime('%H:%M')
                slot_end = (start + timedelta(minutes=(i + 1) * game_duration)).strftime('%H:%M')
                game_slots.append({
                    "league": booking['league'],
                    "date": booking['date'],
                    "week": booking['week'],
                    "arena": booking['arena'],
                    "pad": booking['pad'],
                    "start_time": slot_start,
                    "end_time": slot_end,
                    "game_type": "Regular",
                    "locked": False
                })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return jsonify(game_slots), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
