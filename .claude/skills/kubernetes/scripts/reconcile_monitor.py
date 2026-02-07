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
import yaml

def get_resource_events(resource_type, resource_name, namespace="default"):
    """Get events for a specific resource"""
    try:
        cmd = f"kubectl get {resource_type} {resource_name} -n {namespace} -o yaml"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)

        # Parse the YAML to extract resource version and status
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