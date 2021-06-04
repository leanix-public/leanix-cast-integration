from requests.auth import HTTPBasicAuth
import click
import json
import requests
import datetime
from decimal import *


@click.group()
def cli():
    """Command Line Program for developing CNS (e.g. processors)"""
    pass


@cli.command('get-metrics', help="")
def cli_get_metrics():
    base_url = 'https://rpa.casthighlight.com/WS2/domains/4/'
    headers = {"Authorization": "Bearer <TOKEN>"}

    applications = requests.get(base_url + 'applications', headers=headers)
    content = []
    components = []
    for app in applications.json():
        # if app['id'] != 29554:
        #    continue

        application = requests.get(base_url + 'applications/' + str(app['id']), headers=headers).json()
        if 'metrics' in application:
            metrics = application['metrics'][0]
        else:
            metrics = {}
        rec = requests.get(base_url + 'applications/' +
                           str(app['id']) + '/recommendation', headers=headers).json()
        recommendations = []
        for r in rec:
            recommendations += r['recommendations']
            for component in recommendations:
                if component not in components:
                    components.append(component)
                    content.append({"id": component["name"], "type": "Component", "data": {}})

        # print(json.dumps(metrics, indent=2))
        content.append({"id": app['id'], "type": "Application", "data": {
            "name": app['name'],
            "softwareHealth": float(round(Decimal(metrics['softwareHealth'] * 100), 1)) if 'softwareHealth' in metrics else None,
            "businessImpact": float(round(Decimal(metrics['businessImpact'] * 100), 1)) if 'businessImpact' in metrics else None,
            "technicalDebt": metrics['technicalDebt'] if 'technicalDebt' in metrics else None,
            "softwareResiliency": float(round(Decimal(metrics['softwareResiliency'] * 100), 1)) if 'softwareResiliency' in metrics else None,
            "softwareAgility": float(round(Decimal(metrics['softwareAgility'] * 100), 1)) if 'softwareAgility' in metrics else None,
            "softwareElegance": float(round(Decimal(metrics['softwareElegance'] * 100), 1)) if 'softwareElegance' in metrics else None,
            "roadblocks": metrics['roadblocks'] if 'roadblocks' in metrics else None,
            "cloudEffort": metrics['cloudEffort'] if 'cloudEffort' in metrics else None,

            "cloudReady": float(round(Decimal(metrics['cloudReady'] * 100), 1)) if 'cloudReady' in metrics else None,
            "recommendations": [s['name'] for s in recommendations]
        }})
        # break

    print(json.dumps({
        "connectorType": "cast-showcase",
        "connectorId": "cast-showcase",
        "connectorVersion": "1.0.0",
        "lxVersion": "1.0.0",
        "description": "Imports Kubernetes data into LeanIX",
        "processingDirection": "inbound",
        "processingMode": "partial",
        "customFields": {},
        "content": content
    }, indent=2))


def main():
    cli()


if __name__ == '__main__':
    cli()
