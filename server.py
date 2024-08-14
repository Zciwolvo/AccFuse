from flask import Flask, request

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():

    code = request.args.get('code')

    if code:
        return f'{code}'
    else:
        return 'No code parameter provided in the URL'

if __name__ == '__main__':
    app.run(debug=True)
