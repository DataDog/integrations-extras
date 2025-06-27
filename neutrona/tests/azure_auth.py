from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/my_directory_id/oauth2/token', methods=['POST'])
def auth_token():
    if not request.args.get('api-version') == '1.0':
        return 'error', 400

    if not request.form['grant_type'] == 'client_credentials':
        return 'error', 400

    if not request.form['resource'] == 'https://management.core.windows.net/':
        return 'error', 400

    if not request.form['client_id'] == 'my_application_id':
        return 'error', 400

    if not request.form['client_secret'] == 'my_application_key':
        return 'error', 400

    return jsonify(
        {
            'token_type': 'Bearer',
            'expires_in': '3600',
            'ext_expires_in': '3600',
            'expires_on': '1546552915',
            'not_before': '1546549015',
            'resource': 'https://management.core.windows.net/',
            'access_token': 'my_access_token',
        }
    )
