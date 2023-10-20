import json

import boto3

from datadog_checks.base import AgentCheck


class AwsPricingCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = "aws.pricing"

    def __init__(self, name, init_config, instances):
        super(AwsPricingCheck, self).__init__(name, init_config, instances)

        self.region = self.instance.get("region_name") or "us-east-1"
        self.services = self.instance.get("services") or []
        self.filters = [
            {"Field": filter["Key"], "Type": "TERM_MATCH", "Value": filter["Value"]}
            for filter in self.instance.get("filters")
        ]

        if not self.services:
            self.service_check(
                "status",
                self.WARNING,
                message="No services defined; add at least one service in conf.yaml to collect pricing data.",
            )

        self.tag_fields = [
            "enhancedNetworkingSupported",
            "memory",
            "vcpu",
            "capacitystatus",
            "instanceFamily",
            "operatingSystem",
            "regionCode",
            "networkPerformance",
            "instanceType",
            "tenancy",
            "usagetype",
            "licenseModel",
            "marketoption",
            "termType",
            "leaseContractLength",
            "purchaseOption",
            "unit",
            "currency",
        ]

        self.client = boto3.client("pricing", region_name=self.region)

    def check(self, _):
        try:
            for service in self.services:
                products = self.get_aws_products(service)
                flattened_products = self.flatten_products(products)
                for product in flattened_products:
                    name = service.lower()
                    price = float(product["price"])
                    tags = [
                        f'{self.lowercase(key)}:{value}'
                        for key, value in product.items()
                        if self.lowercase(key) in self.tag_fields
                    ]
                    self.gauge(name, price, tags)

            self.service_check("status", self.OK)
        except Exception as e:
            self.service_check("status", self.CRITICAL, message=str(e))

    def lowercase(self, string):
        return string[0].lower() + string[1:]

    def flatten_products(self, raw_products):
        products = []
        for product in raw_products:
            product_obj = json.loads(product)
            products.extend(self.flatten_product(product_obj))
        return products

    def get_aws_products(self, service_code):
        params = {
            "ServiceCode": service_code,
            "Filters": self.filters,
            "FormatVersion": "aws_v1",
        }

        # Create an empty list to store the aggregated results
        aggregated_results = []

        while True:
            response = self.client.get_products(**params)
            aggregated_results.extend(response["PriceList"])

            # Check if 'NextToken' exists in the response for pagination
            if "NextToken" in response and response["NextToken"]:
                params["NextToken"] = response["NextToken"]
            else:
                break

        return aggregated_results

    def flatten_product(self, product):
        flattened_pricing_terms = []

        # Loop through the "terms" which can be "OnDemand" or "Reserved"
        for term_type, term_values in product["terms"].items():
            # Loop through each SKU under "OnDemand" or "Reserved"
            for sku, sku_values in term_values.items():
                # Loop through each price dimension
                for _, rate_values in sku_values["priceDimensions"].items():
                    # Loop through each currency in pricePerUnit
                    for currency, price in rate_values["pricePerUnit"].items():
                        # Flatten attributes and rate_values into a single dictionary
                        flattened_term = {
                            **product["product"]["attributes"],  # Include all product attributes
                            "termType": term_type,  # Include term type (OnDemand/Reserved)
                            **sku_values.get("termAttributes", {}),  # Include any term attributes
                            **rate_values,  # Include rate values like unit, endRange, etc.
                            "currency": currency,  # Include the currency type
                            "price": price,  # Include price for this currency
                            "sku": sku,
                            "effectiveDate": sku_values.get("effectiveDate", "N/A"),
                            "offerTermCode": sku_values.get("offerTermCode", "N/A"),
                        }
                        # Remove the original pricePerUnit dictionary to prevent nested objects
                        del flattened_term["pricePerUnit"]

                        flattened_pricing_terms.append(flattened_term)
        return flattened_pricing_terms
