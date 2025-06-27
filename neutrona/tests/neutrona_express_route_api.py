from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/client/', methods=['GET'])
def expressroute_metrics():
    service_key = request.args.get('')

    if not service_key == 'my_service_key':
        return 'error', 400

    return jsonify(
        [
            {
                "egress_bps": 0,
                "egress_interface_errors": False,
                "ingress_bps": 0,
                "ingress_interface_errors": False,
                "output_optical_power": 0,
                "receiver_optical_power": 0,
                "tags": ["primary", "ctag_500"],
            },
            {"tags": ["performance"]},
            {
                "egress_bps": 0,
                "egress_interface_errors": False,
                "ingress_bps": 0,
                "ingress_interface_errors": False,
                "output_optical_power": 0,
                "receiver_optical_power": 0,
                "tags": ["secondary", "ctag_500"],
            },
        ]
    )
