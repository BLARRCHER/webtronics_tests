from flask import Flask, request


app = Flask(__name__)

@app.route('/encode', methods=['GET'])
def encode_url():
    unencoded_url = request.args.get('url')
    encoded_url = urllib.parse.quote(unencoded_url)
    return encoded_url

if __name__ == '__main__':
    app.run()
