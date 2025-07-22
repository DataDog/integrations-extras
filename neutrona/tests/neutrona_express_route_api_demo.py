import random

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
                "egress_bps": random.randrange(0, 50) * 1000 * 1000,
                "egress_interface_errors": False,
                "ingress_bps": random.randrange(0, 50) * 1000 * 1000,
                "ingress_interface_errors": False,
                "output_optical_power": random.randrange(-200, -100) / 100,
                "receiver_optical_power": random.randrange(-500, -400) / 100,
                "tags": ["primary", "ctag_500"],
            },
            {"tags": ["performance"]},
            {
                "egress_bps": random.randrange(0, 50) * 1000 * 1000,
                "egress_interface_errors": False,
                "ingress_bps": random.randrange(0, 50) * 1000 * 1000,
                "ingress_interface_errors": False,
                "output_optical_power": random.randrange(-200, -100) / 100,
                "receiver_optical_power": random.randrange(-500, -400) / 100,
                "tags": ["secondary", "ctag_500"],
            },
        ]
    )
