# Kubernetes Automation Scripts

This document contains scripts for automated Kubernetes deployment, scaling, and management operations.

## Deployment Automation Script

```python
#!/usr/bin/env python3
"""
Kubernetes Deployment Automation Script
Automates the creation of deployments, services, and autoscalers
"""

import argparse
import yaml
import subprocess
import sys
from pathlib import Path

def create_deployment_manifest(name, image, replicas=1, port=8080, resources=None):
    """Create a Kubernetes deployment manifest"""

    if resources is None:
        resources = {
            'requests': {
                'memory': '64Mi',
                'cpu': '250m'
            },
            'limits': {
                'memory': '128Mi',
                'cpu': '500m'
            }
        }

    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'labels': {
                'app': name
            }
        },
        'spec': {
            'replicas': replicas,
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
                    'containers': [
                        {
                            'name': name,
                            'image': image,
                            'ports': [
                                {
                                    'containerPort': port
                                }
                            ],
                            'resources': resources
                        }
                    ]
                }
            }
        }
    }

    return deployment

def create_service_manifest(name, port=80, target_port=8080, service_type='ClusterIP'):
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
                    'targetPort': target_port
                }
            ],
            'type': service_type
        }
    }

    return service

def create_hpa_manifest(name, min_replicas=1, max_replicas=10, cpu_percent=50):
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
            ]
        }
    }

    return hpa

def apply_manifest(manifest, dry_run=False):
    """Apply a Kubernetes manifest using kubectl"""

    cmd = ['kubectl', 'apply', '-f', '-']
    if dry_run:
        cmd.insert(2, '--dry-run=client')

    try:
        result = subprocess.run(cmd, input=yaml.dump(manifest), text=True, capture_output=True, check=True)
        print(f"Applied {manifest['kind']} {manifest['metadata']['name']}")
        if dry_run:
            print("Dry run completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error applying manifest: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Automate Kubernetes deployments')
    parser.add_argument('name', help='Name of the application')
    parser.add_argument('--image', required=True, help='Container image to deploy')
    parser.add_argument('--replicas', type=int, default=1, help='Number of replicas (default: 1)')
    parser.add_argument('--port', type=int, default=8080, help='Container port (default: 8080)')
    parser.add_argument('--service-port', type=int, default=80, help='Service port (default: 80)')
    parser.add_argument('--min-replicas', type=int, default=1, help='Min replicas for HPA (default: 1)')
    parser.add_argument('--max-replicas', type=int, default=10, help='Max replicas for HPA (default: 10)')
    parser.add_argument('--cpu-percent', type=int, default=50, help='CPU threshold for HPA (default: 50)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without applying')
    parser.add_argument('--namespace', help='Namespace to deploy to (default: current namespace)')

    args = parser.parse_args()

    # Add namespace to manifests if specified
    def add_namespace(manifest, namespace):
        if namespace:
            manifest['metadata']['namespace'] = namespace
        return manifest

    # Create manifests
    deployment = add_namespace(create_deployment_manifest(
        args.name, args.image, args.replicas, args.port
    ), args.namespace)

    service = add_namespace(create_service_manifest(
        args.name, args.service_port, args.port
    ), args.namespace)

    hpa = add_namespace(create_hpa_manifest(
        args.name, args.min_replicas, args.max_replicas, args.cpu_percent
    ), args.namespace)

    # Apply manifests
    success = True
    success &= apply_manifest(deployment, args.dry_run)
    success &= apply_manifest(service, args.dry_run)
    success &= apply_manifest(hpa, args.dry_run)

    if success:
        print(f"\nDeployment {args.name} created successfully!")
        print(f"To check status: kubectl get pods -l app={args.name}")
        print(f"To scale: kubectl scale deployment {args.name} --replicas=<number>")
        print(f"To check HPA: kubectl get hpa {args.name}-hpa")
    else:
        print("\nSome resources failed to apply.")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## Kubernetes Validation Script

```python
#!/usr/bin/env python3
"""
Kubernetes Configuration Validator
Validates Kubernetes manifests for best practices and common issues
"""

import argparse
import yaml
import json
from pathlib import Path

def validate_deployment(deployment):
    """Validate deployment configuration"""
    issues = []

    # Check for resource requests/limits
    containers = deployment.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
    for container in containers:
        resources = container.get('resources', {})

        if 'requests' not in resources:
            issues.append(f"Container {container.get('name')} is missing resource requests")
        else:
            if 'cpu' not in resources['requests']:
                issues.append(f"Container {container.get('name')} is missing CPU request")
            if 'memory' not in resources['requests']:
                issues.append(f"Container {container.get('name')} is missing memory request")

        if 'limits' not in resources:
            issues.append(f"Container {container.get('name')} is missing resource limits")
        else:
            if 'cpu' not in resources['limits']:
                issues.append(f"Container {container.get('name')} is missing CPU limit")
            if 'memory' not in resources['limits']:
                issues.append(f"Container {container.get('name')} is missing memory limit")

    # Check for security context
    for container in containers:
        if 'securityContext' not in container:
            issues.append(f"Container {container.get('name')} is missing security context")

    # Check for health checks
    for container in containers:
        if 'livenessProbe' not in container:
            issues.append(f"Container {container.get('name')} is missing liveness probe")
        if 'readinessProbe' not in container:
            issues.append(f"Container {container.get('name')} is missing readiness probe")

    return issues

def validate_service(service):
    """Validate service configuration"""
    issues = []

    # Check for appropriate service type
    service_type = service.get('spec', {}).get('type', 'ClusterIP')
    if service_type not in ['ClusterIP', 'NodePort', 'LoadBalancer', 'ExternalName']:
        issues.append(f"Invalid service type: {service_type}")

    return issues

def validate_hpa(hpa):
    """Validate Horizontal Pod Autoscaler configuration"""
    issues = []

    spec = hpa.get('spec', {})

    if 'minReplicas' not in spec:
        issues.append("HPA is missing minReplicas")
    else:
        if spec['minReplicas'] < 1:
            issues.append("HPA minReplicas should be at least 1")

    if 'maxReplicas' not in spec:
        issues.append("HPA is missing maxReplicas")
    else:
        if spec['maxReplicas'] <= spec.get('minReplicas', 0):
            issues.append("HPA maxReplicas should be greater than minReplicas")

    if 'metrics' not in spec or len(spec['metrics']) == 0:
        issues.append("HPA should have at least one metric defined")

    return issues

def validate_manifest(manifest):
    """Validate a Kubernetes manifest"""
    kind = manifest.get('kind', '').lower()

    if kind == 'deployment':
        return validate_deployment(manifest)
    elif kind == 'service':
        return validate_service(manifest)
    elif kind == 'horizontalpodautoscaler':
        return validate_hpa(manifest)
    else:
        return []  # Skip validation for other resource types

def main():
    parser = argparse.ArgumentParser(description='Validate Kubernetes manifests')
    parser.add_argument('files', nargs='+', help='Kubernetes manifest files to validate')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings as well as errors')

    args = parser.parse_args()

    all_issues = []

    for file_path in args.files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Handle multi-document streams
            for doc in yaml.safe_load_all(content):
                if doc is None:
                    continue

                issues = validate_manifest(doc)
                if issues:
                    print(f"Issues found in {file_path} ({doc.get('kind', 'Unknown')} {doc.get('metadata', {}).get('name', 'Unknown')}):")
                    for issue in issues:
                        print(f"  - {issue}")
                    print()

                all_issues.extend(issues)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    if all_issues:
        print(f"Total issues found: {len(all_issues)}")
        if args.strict or any('missing' in issue for issue in all_issues):
            exit(1)
    else:
        print("All manifests passed validation!")

if __name__ == '__main__':
    main()
```

## Reconciliation Loop Monitoring Script

```python
#!/usr/bin/env python3
"""
Kubernetes Reconciliation Loop Monitor
Monitors and analyzes reconciliation behavior in Kubernetes clusters
"""

import argparse
import subprocess
import json
import time
from datetime import datetime
import re

def get_resource_events(resource_type, resource_name, namespace="default"):
    """Get events for a specific resource"""
    try:
        cmd = f"kubectl get {resource_type} {resource_name} -n {namespace} -o yaml"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)

        # Parse the YAML to extract resource version and status
        import yaml
        resource = yaml.safe_load(result.stdout)

        # Get related events
        cmd = f"kubectl get events -n {namespace} --field-selector involvedObject.name={resource_name},involvedObject.kind={resource_type.capitalize()} -o json"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)

        events = json.loads(result.stdout)
        return events['items']
    except subprocess.CalledProcessError:
        return []

def monitor_reconciliation_loop(resource_type, resource_name, namespace="default", duration=300):
    """Monitor reconciliation loop for a resource over time"""
    print(f"Monitoring {resource_type}/{resource_name} in namespace {namespace} for {duration} seconds...")

    start_time = time.time()
    previous_state = None

    while time.time() - start_time < duration:
        try:
            # Get current resource state
            cmd = f"kubectl get {resource_type} {resource_name} -n {namespace} -o json"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)

            current_state = json.loads(result.stdout)

            # Check for state changes
            if previous_state is not None:
                # Compare spec vs status to detect reconciliation activity
                desired_replicas = current_state.get('spec', {}).get('replicas', 1)
                current_replicas = current_state.get('status', {}).get('replicas', 0)
                ready_replicas = current_state.get('status', {}).get('readyReplicas', 0)

                if desired_replicas != current_replicas or current_replicas != ready_replicas:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Reconciliation in progress: "
                          f"Desired={desired_replicas}, Current={current_replicas}, Ready={ready_replicas}")

                # Check for resource version changes (indicating updates)
                prev_resource_version = previous_state.get('metadata', {}).get('resourceVersion', '')
                curr_resource_version = current_state.get('metadata', {}).get('resourceVersion', '')

                if prev_resource_version != curr_resource_version:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Resource version changed: {curr_resource_version}")

                    # Get events around this change
                    events = get_resource_events(resource_type, resource_name, namespace)
                    for event in events[-3:]:  # Show last 3 events
                        event_time = event.get('firstTimestamp', 'unknown')
                        event_msg = event.get('message', 'no message')
                        print(f"  Event: {event_msg} (at {event_time})")

            previous_state = current_state
            time.sleep(5)  # Check every 5 seconds

        except subprocess.CalledProcessError as e:
            print(f"Error monitoring resource: {e}")
            break
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break

def analyze_controller_performance(namespace="kube-system"):
    """Analyze controller manager performance metrics"""
    print(f"Analyzing controller performance in {namespace}...")

    try:
        # Get controller manager logs
        cmd = f"kubectl logs -n {namespace} -l component=kube-controller-manager --since=5m"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)

        logs = result.stdout

        # Look for reconciliation metrics in logs
        reconcile_pattern = r"\"reconcilerGroup\".*?\"reconcilerKind\":\"(\w+)\".*?\"name\":\"([^\"]+)\".*?\"reconcileID\""
        matches = re.findall(reconcile_pattern, logs)

        if matches:
            print("Recent reconciliations detected:")
            for resource_kind, resource_name in matches[:10]:  # Show first 10
                print(f"  - {resource_kind}: {resource_name}")

        # Look for error patterns
        error_patterns = [
            r"(?i)error.*reconcil",
            r"(?i)failed.*reconcil",
            r"(?i)reconcil.*fail"
        ]

        for pattern in error_patterns:
            errors = re.findall(pattern, logs)
            if errors:
                print(f"Found {len(errors)} potential reconciliation errors")
                break

    except subprocess.CalledProcessError as e:
        print(f"Could not access controller logs: {e}")

def main():
    parser = argparse.ArgumentParser(description='Monitor Kubernetes reconciliation loops')
    parser.add_argument('resource_type', help='Type of resource to monitor (e.g., deployment, statefulset)')
    parser.add_argument('resource_name', help='Name of the resource to monitor')
    parser.add_argument('--namespace', default='default', help='Namespace (default: default)')
    parser.add_argument('--duration', type=int, default=300, help='Duration to monitor in seconds (default: 300)')
    parser.add_argument('--analyze-controller', action='store_true', help='Analyze controller manager performance')

    args = parser.parse_args()

    if args.analyze_controller:
        analyze_controller_performance()
    else:
        monitor_reconciliation_loop(args.resource_type, args.resource_name,
                                   args.namespace, args.duration)

if __name__ == '__main__':
    main()
```