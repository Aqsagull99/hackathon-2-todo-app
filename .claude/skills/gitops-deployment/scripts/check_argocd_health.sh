#!/bin/bash
# Script to check the health of ArgoCD and deployed applications
# Usage: ./check_argocd_health.sh
#
# This script performs quality gate checks on ArgoCD applications
# It evaluates health status, sync status, and identifies applications that fail quality gates
# Quality gates ensure applications meet predefined criteria before being considered healthy

set -e  # Exit on any error

echo "Checking ArgoCD health and quality gates..."

# Check if argocd CLI is available
if ! command -v argocd &> /dev/null; then
    echo "Error: argocd CLI is not installed or not in PATH"
    exit 1
fi

# Check if ArgoCD server is accessible
echo "Checking connection to ArgoCD server..."
if argocd account get-user-info &> /dev/null; then
    echo "✓ Connected to ArgoCD server"
else
    echo "✗ Cannot connect to ArgoCD server"
    echo "Make sure you have logged in with: argocd login SERVER"
    exit 1
fi

# Check ArgoCD system status
echo ""
echo "ArgoCD system components status:"
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-repo-server
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-application-controller

# List all applications
echo ""
echo "ArgoCD Applications:"
argocd app list --output wide

# Check health of each application
echo ""
echo "Quality gate evaluation (Health and Sync Status):"
for app in $(argocd app list --output name); do
    echo "=== Application: $app ==="
    APP_HEALTH=$(argocd app get $app -o json | jq -r '.status.health.status' 2>/dev/null || echo "Unknown")
    APP_SYNC=$(argocd app get $app -o json | jq -r '.status.sync.status' 2>/dev/null || echo "Unknown")

    echo "  Health Status: $APP_HEALTH"
    echo "  Sync Status: $APP_SYNC"

    # Evaluate quality gates
    if [[ "$APP_HEALTH" == "Healthy" && "$APP_SYNC" == "Synced" ]]; then
        echo "  ✓ Quality gates: PASSED"
    elif [[ "$APP_HEALTH" == "Degraded" ]]; then
        echo "  ✗ Quality gates: FAILED - Application is Degraded"
        echo "  ⚠ Action required: Investigate health issues"
    elif [[ "$APP_SYNC" != "Synced" ]]; then
        echo "  ⚠ Quality gates: PARTIAL - Application is not in sync"
        echo "  ⚠ Action: Review differences with argocd app diff $app"
    else
        echo "  ? Quality gates: UNKNOWN - Status unclear"
    fi
    echo ""
done

# Check for any applications that are not healthy or synced
echo "Quality gate violations:"
UNHEALTHY_APPS=$(argocd app list --query status.health.status --output json | jq -r '.[] | select(.status.health.status == "Degraded" or .status.health.status == "Unknown") | .metadata.name' 2>/dev/null)
if [[ -n "$UNHEALTHY_APPS" ]]; then
    echo "  Degraded applications (quality gates failed):"
    echo "$UNHEALTHY_APPS"
    echo ""
else
    echo "  ✓ No degraded applications found"
fi

UNSYNCED_APPS=$(argocd app list --query status.sync.status --output json | jq -r '.[] | select(.status.sync.status != "Synced") | .metadata.name' 2>/dev/null)
if [[ -n "$UNSYNCED_APPS" ]]; then
    echo "  Out-of-sync applications (quality gates partially failed):"
    echo "$UNSYNCED_APPS"
    echo ""
else
    echo "  ✓ No out-of-sync applications found"
fi

# Summary of quality gate status
TOTAL_APPS=$(argocd app list --output name | wc -l)
HEALTHY_APPS=$(argocd app list --query status.health.status --output json | jq -r '.[] | select(.status.health.status == "Healthy")' 2>/dev/null | wc -l)
SYNCED_APPS=$(argocd app list --query status.sync.status --output json | jq -r '.[] | select(.status.sync.status == "Synced")' 2>/dev/null | wc -l)

echo "Quality gate summary:"
echo "  Total applications: $TOTAL_APPS"
echo "  Healthy applications: $HEALTHY_APPS"
echo "  Synced applications: $SYNCED_APPS"
echo "  Overall quality gate compliance: $((HEALTHY_APPS + SYNCED_APPS))/$((TOTAL_APPS * 2))"

echo ""
echo "ArgoCD health and quality gate check completed."
echo ""
echo "Quality gate actions:"
echo "- To sync applications: argocd app sync <app-name>"
echo "- To refresh applications: argocd app refresh <app-name>"
echo "- To check detailed status: argocd app get <app-name>"
echo "- To see sync differences: argocd app diff <app-name>"
echo "- To rollback problematic deployments: argocd app rollback <app-name> <version-id>"
echo ""
echo "Rollback recommendations:"
echo "- Check deployment history: argocd app history <app-name>"
echo "- Identify versioned artifacts that passed quality gates"
echo "- Use versioned artifacts for rollback if current deployment fails"