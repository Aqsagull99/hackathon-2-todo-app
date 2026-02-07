#!/usr/bin/env python3
"""
Kubernetes Application Deployment Script
Automates the deployment of applications to Kubernetes clusters
"""

import argparse
import yaml
import subprocess
import sys
import tempfile
import os
from pathlib import Path

def create_deployment(name, image, replicas=3, port=8080, resources=None):
    """Create a Kubernetes deployment manifest"""

    if resources is None:
        resources = {
            'requests': {
                'memory': '256Mi',
                'cpu': '250m'
            },
            'limits': {
                'memory': '512Mi',
                'cpu': '500m'
            }
        }

    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'labels': {
                'app': name,
                'version': 'v1.0.0'
            }
        },
        'spec': {
            'replicas': replicas,
            'strategy': {
                'type': 'RollingUpdate',
                'rollingUpdate': {
                    'maxUnavailable': 1,
                    'maxSurge': 1
                }
            },
            'selector': {
                'matchLabels': {
                    'app': name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': name
                    }
                },
                'spec': {
                    'securityContext': {
                        'runAsNonRoot': True,
                        'runAsUser': 1000,
                        'fsGroup': 2000
                    },
                    'containers': [
                        {
                            'name': name,
                            'image': image,
                            'ports': [
                                {
                                    'containerPort': port
                                }
                            ],
                            'env': [
                                {
                                    'name': 'PORT',
                                    'value': str(port)
                                }
                            ],
                            'resources': resources,
                            'livenessProbe': {
                                'httpGet': {
                                    'path': '/healthz',
                                    'port': port
                                },
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10,
                                'timeoutSeconds': 5,
                                'failureThreshold': 3
                            },
                            'readinessProbe': {
                                'httpGet': {
                                    'path': '/readyz',
                                    'port': port
                                },
                                'initialDelaySeconds': 5,
                                'periodSeconds': 5,
                                'timeoutSeconds': 3,
                                'failureThreshold': 3
                            },
                            'securityContext': {
                                'allowPrivilegeEscalation': False,
                                'readOnlyRootFilesystem': True,
                                'runAsNonRoot': True,
                                'runAsUser': 1000,
                                'capabilities': {
                                    'drop': ['ALL']
                                }
                            }
                        }
                    ]
                }
            }
        }
    }

    return deployment

def create_service(name, port=80, target_port=8080, service_type='ClusterIP'):
    """Create a Kubernetes service manifest"""

    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': f'{name}-service',
            'labels': {
                'app': name
            }
        },
        'spec': {
            'selector': {
                'app': name
            },
            'ports': [
                {
                    'protocol': 'TCP',
                    'port': port,
                    'targetPort': target_port,
                    'name': 'http'
                }
            ],
            'type': service_type
        }
    }

    return service

def create_hpa(name, min_replicas=2, max_replicas=10, cpu_percent=70):
    """Create a Horizontal Pod Autoscaler manifest"""

    hpa = {
        'apiVersion': 'autoscaling/v2',
        'kind': 'HorizontalPodAutoscaler',
        'metadata': {
            'name': f'{name}-hpa'
        },
        'spec': {
            'scaleTargetRef': {
                'apiVersion': 'apps/v1',
                'kind': 'Deployment',
                'name': name
            },
            'minReplicas': min_replicas,
            'maxReplicas': max_replicas,
            'metrics': [
                {
                    'type': 'Resource',
                    'resource': {
                        'name': 'cpu',
                        'target': {
                            'type': 'Utilization',
                            'averageUtilization': cpu_percent
                        }
                    }
                }
            ],
            'behavior': {
                'scaleDown': {
                    'stabilizationWindowSeconds': 300,
                    'policies': [
                        {
                            'type': 'Percent',
                            'value': 10,
                            'periodSeconds': 60
                        }
                    ]
                },
                'scaleUp': {
                    'stabilizationWindowSeconds': 60,
                    'policies': [
                        {
                            'type': 'Percent',
                            'value': 100,
                            'periodSeconds': 15
                        },
                        {
                            'type': 'Pods',
                            'value': 4,
                            'periodSeconds': 15
                        }
                    ],
                    'selectPolicy': 'Max'
                }
            }
        }
    }

    return hpa

def apply_manifest(manifest, namespace=None, dry_run=False):
    """Apply a Kubernetes manifest using kubectl"""

    cmd = ['kubectl', 'apply', '-f', '-']
    if dry_run:
        cmd.insert(2, '--dry-run=client')
    if namespace:
        cmd.extend(['-n', namespace])

    try:
        result = subprocess.run(cmd, input=yaml.dump(manifest), text=True, capture_output=True, check=True)
        print(f"Applied {manifest['kind']} {manifest['metadata']['name']}")
        if dry_run:
            print("Dry run completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error applying manifest: {e.stderr}")
        return False

def check_cluster_health():
    """Check if the Kubernetes cluster is accessible"""

    try:
        # Check cluster info
        result = subprocess.run(['kubectl', 'cluster-info'], capture_output=True, text=True, check=True)
        print("✅ Kubernetes cluster is accessible")

        # Check nodes status
        result = subprocess.run(['kubectl', 'get', 'nodes'], capture_output=True, text=True, check=True)
        print("✅ Nodes are accessible")

        # Check current context
        result = subprocess.run(['kubectl', 'config', 'current-context'], capture_output=True, text=True, check=True)
        current_context = result.stdout.strip()
        print(f"✅ Current context: {current_context}")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error accessing cluster: {e}")
        print("Please check your kubectl configuration and cluster connectivity.")
        return False

def main():
    parser = argparse.ArgumentParser(description='Deploy applications to Kubernetes')
    parser.add_argument('name', help='Name of the application')
    parser.add_argument('--image', required=True, help='Container image to deploy')
    parser.add_argument('--replicas', type=int, default=3, help='Number of replicas (default: 3)')
    parser.add_argument('--port', type=int, default=8080, help='Container port (default: 8080)')
    parser.add_argument('--service-port', type=int, default=80, help='Service port (default: 80)')
    parser.add_argument('--min-replicas', type=int, default=2, help='Min replicas for HPA (default: 2)')
    parser.add_argument('--max-replicas', type=int, default=10, help='Max replicas for HPA (default: 10)')
    parser.add_argument('--cpu-percent', type=int, default=70, help='CPU threshold for HPA (default: 70)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without applying')
    parser.add_argument('--namespace', default='default', help='Namespace to deploy to (default: default)')
    parser.add_argument('--memory-request', default='256Mi', help='Memory request (default: 256Mi)')
    parser.add_argument('--cpu-request', default='250m', help='CPU request (default: 250m)')
    parser.add_argument('--memory-limit', default='512Mi', help='Memory limit (default: 512Mi)')
    parser.add_argument('--cpu-limit', default='500m', help='CPU limit (default: 500m)')
    parser.add_argument('--check-context', action='store_true', help='Display current kubectl context before deployment')
    parser.add_argument('--list-contexts', action='store_true', help='List all available kubectl contexts')

    args = parser.parse_args()

    # List contexts if requested
    if args.list_contexts:
        try:
            result = subprocess.run(['kubectl', 'config', 'get-contexts'], capture_output=True, text=True, check=True)
            print("Available contexts:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error listing contexts: {e}")

    # Check current context if requested
    if args.check_context:
        try:
            result = subprocess.run(['kubectl', 'config', 'current-context'], capture_output=True, text=True, check=True)
            current_context = result.stdout.strip()
            print(f"Current context: {current_context}")

            # Get cluster info for current context
            result = subprocess.run(['kubectl', 'cluster-info'], capture_output=True, text=True, check=True)
            print("Cluster info:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error getting context info: {e}")

    # Check cluster health
    if not args.dry_run and not check_cluster_health():
        sys.exit(1)

    # Define resources
    resources = {
        'requests': {
            'memory': args.memory_request,
            'cpu': args.cpu_request
        },
        'limits': {
            'memory': args.memory_limit,
            'cpu': args.cpu_limit
        }
    }

    # Create manifests
    deployment = create_deployment(
        args.name, args.image, args.replicas, args.port, resources
    )

    service = create_service(
        args.name, args.service_port, args.port
    )

    hpa = create_hpa(
        args.name, args.min_replicas, args.max_replicas, args.cpu_percent
    )

    # Apply manifests
    success = True
    success &= apply_manifest(deployment, args.namespace, args.dry_run)
    success &= apply_manifest(service, args.namespace, args.dry_run)
    success &= apply_manifest(hpa, args.namespace, args.dry_run)

    if success and not args.dry_run:
        print(f"\n🎉 Deployment {args.name} created successfully!")
        print(f"To check status: kubectl get pods -n {args.namespace} -l app={args.name}")
        print(f"To scale: kubectl scale deployment {args.name} -n {args.namespace} --replicas=<number>")
        print(f"To check HPA: kubectl get hpa {args.name}-hpa -n {args.namespace}")
        print(f"To check service: kubectl get svc {args.name}-service -n {args.namespace}")
    elif success and args.dry_run:
        print(f"\n✅ Dry run completed successfully. Resources would be created for {args.name}")
    else:
        print(f"\n❌ Some resources failed to apply.")
        sys.exit(1)

if __name__ == '__main__':
    main()