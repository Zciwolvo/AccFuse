from flask import Flask, request

app = Flask(__name__)

@app.route('/get_code', methods=['GET'])
def get_code():
    # Retrieve the value of the 'code' parameter from the URL
    code = request.args.get('code')

    if code:
        return f'The value of the "code" parameter is: {code}'
    else:
        return 'No code parameter provided in the URL'

if __name__ == '__main__':
    app.run(debug=True)
