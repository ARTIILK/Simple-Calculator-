from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML Template embedded directly in Python
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full-Screen Calculator</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }

        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100vw;
            height: 100vh;
            max-width: 600px;
            background-color: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            box-sizing: border-box;
        }

        .display {
            width: 100%;
            height: 80px;
            font-size: 36px;
            text-align: right;
            padding-right: 10px;
            margin-bottom: 20px;
            border: 2px solid #ccc;
            border-radius: 10px;
            box-sizing: border-box;
        }

        .buttons {
            width: 100%;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }

        button {
            width: 100%;
            height: 60px;
            font-size: 24px;
            border: none;
            border-radius: 10px;
            background-color: #f4f4f4;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: #ddd;
        }

        .equal {
            background-color: #4caf50;
            color: white;
        }

        .recent {
            margin-top: 20px;
            width: 100%;
            text-align: left;
            font-size: 18px;
        }

        @media (max-width: 600px) {
            .container {
                border-radius: 0;
                padding: 10px;
            }

            .display {
                font-size: 28px;
                height: 60px;
            }

            button {
                height: 50px;
                font-size: 20px;
            }
        }

        @media (orientation: landscape) {
            .container {
                max-height: 100vh;
                max-width: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <input type="text" id="display" class="display" readonly>
         <div class="buttons">
            <button onclick="appendNumber('7')">7</button>
            <button onclick="appendNumber('8')">8</button>
            <button onclick="appendNumber('9')">9</button>
            <button onclick="appendOperator('/')">/</button>

            <button onclick="appendNumber('4')">4</button>
            <button onclick="appendNumber('5')">5</button>
            <button onclick="appendNumber('6')">6</button>
            <button onclick="appendOperator('*')">*</button>

            <button onclick="appendNumber('1')">1</button>
            <button onclick="appendNumber('2')">2</button>
            <button onclick="appendNumber('3')">3</button>
            <button onclick="appendOperator('-')">-</button>

            <button onclick="appendNumber('0')">0</button>
            <button onclick="appendOperator('.')">.</button>
            <button onclick="clearDisplay()">C</button>
            <button onclick="appendOperator('+')">+</button>

            <button class="equal" colspan="2" onclick="calculate()">=</button>
        </div>

        <div class="recent">
            <strong>Recent Calculations:</strong>
            <ul id="recent-calculations"></ul>
        </div>
    </div>

    <script>
        // Function to append numbers to the display
        function appendNumber(number) {
            document.getElementById('display').value += number;
        }

        // Function to append operators to the display
        function appendOperator(operator) {
            document.getElementById('display').value += operator;
        }

        // Function to clear the display
        function clearDisplay() {
            document.getElementById('display').value = '';
        }

        // Function to calculate the result
        function calculate() {
            const expression = document.getElementById('display').value;
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ expression: expression }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('display').value = data.result;

                // Save the result in local storage for recent calculations
                saveRecentCalculation(expression + ' = ' + data.result);
                displayRecentCalculations();
            })
            .catch(error => {
                document.getElementById('display').value = 'Error';
            });
        }

        // Function to save recent calculations in local storage
        function saveRecentCalculation(calculation) {
            let recentCalculations = JSON.parse(localStorage.getItem('recentCalculations')) || [];
            recentCalculations.unshift(calculation);  // Add to the beginning
            if (recentCalculations.length > 5) {
                recentCalculations.pop();  // Keep only the last 5 entries
            }
            localStorage.setItem('recentCalculations', JSON.stringify(recentCalculations));
        }

        // Function to display recent calculations
        function displayRecentCalculations() {
            const recentCalculations = JSON.parse(localStorage.getItem('recentCalculations')) || [];
            const recentList = document.getElementById('recent-calculations');
            recentList.innerHTML = '';  // Clear the list
            recentCalculations.forEach(calculation => {
                const listItem = document.createElement('li');
                listItem.textContent = calculation;
                recentList.appendChild(listItem);
            });
        }

        // Display recent calculations on page load
        document.addEventListener('DOMContentLoaded', displayRecentCalculations);
    </script>
</body>
</html>
'''

# Flask route for the calculator page
@app.route('/')
def index():
    return render_template_string(html_template)

# Route to handle the calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data['expression']
        result = eval(expression) 
        return jsonify(result=result)
    except Exception as e:
        return jsonify(result="Error")

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
