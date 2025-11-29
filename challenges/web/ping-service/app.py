# /// script
# dependencies = [
#   "flask"
# ]
# ///
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    address = None
    if request.method == 'POST':
        address = request.form.get('address')
        if address:
            try:
                # Running the ping command
                # Note: Using shell=True allows for command injection if input is not sanitized.
                # This seems to be intended for a CTF challenge context.
                command = f"ping -c 1 {address}"
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                output = result.decode('utf-8')
            except subprocess.CalledProcessError as e:
                output = e.output.decode('utf-8') if e.output else str(e)
            except Exception as e:
                output = str(e)

    return render_template('index.html', output=output, address=address)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
