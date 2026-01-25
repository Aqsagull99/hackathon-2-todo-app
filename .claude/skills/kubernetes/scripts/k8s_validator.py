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
        else:
            sec_context = container['securityContext']
            if sec_context.get('runAsNonRoot') is not True:
                issues.append(f"Container {container.get('name')} should run as non-root user")
            if sec_context.get('allowPrivilegeEscalation') is not False:
                issues.append(f"Container {container.get('name')} should not allow privilege escalation")
            if sec_context.get('readOnlyRootFilesystem') is not True:
                issues.append(f"Container {container.get('name')} should use read-only root filesystem")

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

    # Check for selector
    if 'selector' not in service.get('spec', {}):
        issues.append("Service is missing selector")

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

def validate_pod(pod):
    """Validate Pod configuration"""
    issues = []

    spec = pod.get('spec', {})

    # Check for security context at pod level
    if 'securityContext' not in spec:
        issues.append("Pod is missing security context")
    else:
        pod_sec_context = spec['securityContext']
        if pod_sec_context.get('runAsNonRoot') is not True:
            issues.append("Pod should run as non-root user")

    # Check containers in pod
    containers = spec.get('containers', [])
    for container in containers:
        if 'securityContext' not in container:
            issues.append(f"Container {container.get('name')} is missing security context")

        if 'resources' not in container:
            issues.append(f"Container {container.get('name')} is missing resource requests/limits")
        else:
            resources = container['resources']
            if 'requests' not in resources:
                issues.append(f"Container {container.get('name')} is missing resource requests")
            if 'limits' not in resources:
                issues.append(f"Container {container.get('name')} is missing resource limits")

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
    elif kind == 'pod':
        return validate_pod(manifest)
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
        print("✅ All manifests passed validation!")

if __name__ == '__main__':
    main()