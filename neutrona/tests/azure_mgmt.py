from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/subscriptions/my_subscription_id/providers/Microsoft.Network/expressRouteCircuits', methods=['GET'])
def expressroute_circuits():
    if not request.args.get('api-version') == '2018-08-01':
        return 'error', 400

    if not request.headers['Authorization'] == 'Bearer my_access_token':
        return 'error', 400

    return jsonify(
        {
            "value": [
                {
                    "name": "MyName",
                    "id": "/subscriptions/my_subscription_id/resourceGroups/my_resource_group/providers/Microsoft.Network/expressRouteCircuits/MyName",  # noqa: E501
                    "etag": "W/\"\"",
                    "type": "Microsoft.Network/expressRouteCircuits",
                    "location": "eastus",
                    "properties": {
                        "provisioningState": "Succeeded",
                        "resourceGuid": "my_resource_guid",
                        "peerings": [
                            {
                                "name": "MicrosoftPeering",
                                "id": "/subscriptions/my_subscription_id/resourceGroups/my_resource_group/providers/Microsoft.Network/expressRouteCircuits/MyName/peerings/MicrosoftPeering",  # noqa: E501
                                "etag": "W/\"\"",
                                "properties": {
                                    "provisioningState": "Succeeded",
                                    "peeringType": "MicrosoftPeering",
                                    "azureASN": 12076,
                                    "peerASN": 65001,
                                    "primaryPeerAddressPrefix": "10.0.0.0/30",
                                    "secondaryPeerAddressPrefix": "10.1.0.0/30",
                                    "primaryAzurePort": "PRI-A",
                                    "secondaryAzurePort": "SEC-A",
                                    "state": "Enabled",
                                    "vlanId": 1234,
                                    "gatewayManagerEtag": "1",
                                    "lastModifiedBy": "Customer",
                                    "microsoftPeeringConfig": {
                                        "advertisedPublicPrefixes": ["10.0.0.0/30", "10.1.0.0/30"],
                                        "advertisedCommunities": ["12076:51001"],
                                        "advertisedPublicPrefixesState": "ValidationNeeded",
                                        "customerASN": 65001,
                                        "legacyMode": 0,
                                        "routingRegistryName": "ARIN",
                                    },
                                    "routeFilter": {
                                        "id": "/subscriptions/my_subscription_id/resourceGroups/my_resource_group/providers/Microsoft.Network/routeFilters/route_filter_east_us"  # noqa: E501
                                    },
                                    "connections": [],
                                },
                                "type": "Microsoft.Network/expressRouteCircuits/peerings",
                            },
                            {
                                "name": "AzurePrivatePeering",
                                "id": "/subscriptions/my_subscription_id/resourceGroups/my_resource_group/providers/Microsoft.Network/expressRouteCircuits/MyName/peerings/AzurePrivatePeering",  # noqa: E501
                                "etag": "W/\"\"",
                                "properties": {
                                    "provisioningState": "Succeeded",
                                    "peeringType": "AzurePrivatePeering",
                                    "azureASN": 12076,
                                    "peerASN": 55259,
                                    "primaryPeerAddressPrefix": "10.255.0.0/30",
                                    "secondaryPeerAddressPrefix": "10.255.0.100/30",
                                    "primaryAzurePort": "PRI-A",
                                    "secondaryAzurePort": "SEC-A",
                                    "state": "Enabled",
                                    "vlanId": 1235,
                                    "gatewayManagerEtag": "1",
                                    "lastModifiedBy": "Customer",
                                    "microsoftPeeringConfig": {
                                        "advertisedPublicPrefixes": [],
                                        "advertisedCommunities": [],
                                        "advertisedPublicPrefixesState": "NotConfigured",
                                        "customerASN": 0,
                                        "legacyMode": 0,
                                        "routingRegistryName": "NONE",
                                    },
                                    "connections": [],
                                },
                                "type": "Microsoft.Network/expressRouteCircuits/peerings",
                            },
                        ],
                        "authorizations": [],
                        "serviceProviderProperties": {
                            "serviceProviderName": "Neutrona Networks",
                            "peeringLocation": "Miami",
                            "bandwidthInMbps": 50,
                        },
                        "circuitProvisioningState": "Enabled",
                        "allowClassicOperations": True,
                        "gatewayManagerEtag": "2",
                        "serviceKey": "my_service_key",
                        "serviceProviderProvisioningState": "NotProvisioned",
                        "allowGlobalReach": False,
                        "stag": 10,
                    },
                    "sku": {"name": "Standard_MeteredData", "tier": "Standard", "family": "MeteredData"},
                }
            ]
        }
    )
