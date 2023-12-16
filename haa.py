from flask import Flask, request, Response, jsonify, send_file
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import io
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000/dashboard"}},
            allow_headers=["Content-Type", "Authorization"],
            supports_credentials=True)

def connect_to_database():
    connection = psycopg2.connect(
        host="localhost",
        database="MyZoo",
        user="postgres",
        password="uwuwuwuwuwu"
    )
    return connection

@app.route('/chart1', methods=['GET'])
@cross_origin()
def get_chart1_data():
    try:

        connection = connect_to_database()

        cursor = connection.cursor()
        cursor.execute("""
            SELECT transaction_date, SUM(ticket_count) AS total_tickets
            FROM zoo_transaction_summary
            GROUP BY transaction_date
            ORDER BY transaction_date
        """)

        data = pd.DataFrame(cursor.fetchall(), columns=['transaction_date', 'total_tickets'])

        cursor.close()
        connection.close()

        plt.figure(figsize=(15, 6))
        plt.plot(data['transaction_date'], data['total_tickets'], marker='o')
        plt.xlabel('Date')
        plt.ylabel('Total Visitors')
        plt.title('Number of People Visiting the Zoo Daily')
        plt.grid(True)

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        return send_file(img_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chart2', methods=['GET'])
@cross_origin()
def get_chart2_data():
    try:
        connection = connect_to_database()

        cursor = connection.cursor()
        cursor.execute("""
            SELECT country, SUM(ticket_count) AS total_visitors
            FROM zoo_transaction_summary
            GROUP BY country
            ORDER BY total_visitors DESC
        """)

        data = pd.DataFrame(cursor.fetchall(), columns=['name_country', 'total_visitors'])

        cursor.close()
        connection.close()

        plt.figure(figsize=(15, 12))
        plt.bar(data['name_country'], data['total_visitors'])
        plt.xlabel('Country')
        plt.ylabel('Total Visitors')
        plt.title('Comparison of Total Visitors by Country')
        plt.xticks(rotation=45, ha='right')

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        return send_file(img_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
