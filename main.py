from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return "Game Slot Generator is live!"

@app.route('/generate-game-slots', methods=['POST'])
def generate_game_slots():
    data = request.get_json(force=True)

    # Detect if data is a single booking or a list of bookings
    if isinstance(data.get('bookings'), list):
        bookings = data['bookings']
    else:
        bookings = [data]  # wrap single Zoho-style booking in a list

    game_duration = int(data.get('default_game_duration', 60))
    game_slots = []

    for booking in bookings:
        try:
            start = datetime.strptime(booking['start_time'], '%H:%M')
            end = datetime.strptime(booking['end_time'], '%H:%M')
            booking_duration = int((end - start).total_seconds() / 60)

            num_slots = booking_duration // game_duration
            for i in range(num_slots):
                slot_start = (start + timedelta(minutes=i * game_duration)).strftime('%H:%M')
                slot_end = (start + timedelta(minutes=(i + 1) * game_duration)).strftime('%H:%M')
                game_slots.append({
                    "league": booking.get('league'),
                    "date": booking.get('date'),
                    "week": booking.get('week'),
                    "arena": booking.get('arena'),
                    "pad": booking.get('pad'),
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
