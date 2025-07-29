from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return "Game Slot Generator is live!"

@app.route('/generate-game-slots', methods=['POST'])
def generate_game_slots():
    if request.content_type != 'application/json':
        print(f"❌ Unsupported Content-Type: {request.content_type}", file=sys.stderr)
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        data = request.get_json(force=True)
        print("✅ Received JSON:", data, file=sys.stderr)

        game_duration = int(data.get('default_game_duration', 60))
        bookings = data.get('bookings', [])

        game_slots = []

        for booking in bookings:
            try:
                start = datetime.strptime(booking['start_time'], '%H:%M')
                end = datetime.strptime(booking['end_time'], '%H:%M')
                booking_duration = int((end - start).total_seconds() / 60)

                num_slots = booking_duration // game_duration
                for i in range(num_slots):
                    slot_start = (
                        start + timedelta(minutes=i * game_duration)).strftime('%H:%M')
                    slot_end = (
                        start + timedelta(minutes=(i + 1) * game_duration)).strftime('%H:%M')
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
                print(f"❌ Error parsing booking: {e}", file=sys.stderr)
                return jsonify({"error": str(e)}), 400

        return jsonify(game_slots), 200

    except Exception as e:
        print(f"❌ General Error: {e}", file=sys.stderr)
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
