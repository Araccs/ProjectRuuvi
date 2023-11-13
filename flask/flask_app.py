from flask import Flask, request, render_template

app = Flask(__name__)

# Initialize an empty list to store received data
received_data = []

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    # Store the received data in the list
    received_data.append(data)
    return "Data received successfully"

@app.route('/display_data')
def display_data():
    return render_template('data.html', data=received_data)

if __name__ == '__main__':
    app.run()
