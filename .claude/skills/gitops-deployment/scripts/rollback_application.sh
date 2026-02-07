#!/bin/bash
# Script to rollback an ArgoCD application to a previous version
# Usage: ./rollback_application.sh <app-name> [version-id]
#
# This script implements rollback strategies using versioned artifacts
# It shows how to rollback when test failures or quality gates are not met

set -e  # Exit on any error

APP_NAME=${1:-""}
VERSION_ID=${2:-""}

if [[ -z "$APP_NAME" ]]; then
    echo "Usage: $0 <app-name> [version-id]"
    echo ""
    echo "This script performs rollback operations for ArgoCD applications."
    echo "If no version ID is specified, it lists available versions for rollback."
    echo ""
    echo "Quality gates and rollback scenarios:"
    echo "  - Failed health checks trigger manual rollback"
    echo "  - PreSync hook failures block deployment"
    echo "  - Manual intervention for complex rollback situations"
    echo ""
    echo "Examples:"
    echo "  $0 my-app                    # List available versions"
    echo "  $0 my-app 2                  # Rollback to version 2"
    echo "  $0 my-app abc123def456       # Rollback to specific revision"
    exit 1
fi

# Check if argocd CLI is available
if ! command -v argocd &> /dev/null; then
    echo "Error: argocd CLI is not installed or not in PATH"
    exit 1
fi

# Check if ArgoCD server is accessible
if ! argocd app list &> /dev/null; then
    echo "Error: Cannot connect to ArgoCD server"
    echo "Make sure you have logged in with: argocd login SERVER"
    exit 1
fi

if [[ -z "$VERSION_ID" ]]; then
    echo "Listing available versions for rollback of application: $APP_NAME"
    echo ""

    # Show application history
    echo "Deployment history:"
    argocd app history $APP_NAME || {
        echo "No history found for application: $APP_NAME"
        exit 1
    }

    echo ""
    echo "To rollback to a specific version, use:"
    echo "  $0 $APP_NAME <version_id>"
    echo ""
    echo "Rollback strategies available:"
    echo "  1. Rollback to specific version ID from history"
    echo "  2. Sync to specific Git commit/revision"
    echo "  3. Use versioned artifacts from Git tags"
    exit 0
fi

echo "Preparing rollback for application: $APP_NAME to version: $VERSION_ID"
echo ""

# Show current status
echo "Current application status:"
argocd app get $APP_NAME
echo ""

# Show the target version details
echo "Target version details:"
argocd app history $APP_NAME | grep -E "(ID.*DATE|${VERSION_ID})" || echo "Version $VERSION_ID not found in history"

echo ""
read -p "Are you sure you want to rollback $APP_NAME to version $VERSION_ID? (y/N): " -n 1 -r REPLY
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled."
    exit 0
fi

# Perform the rollback
echo "Initiating rollback to version: $VERSION_ID"
argocd app rollback $APP_NAME $VERSION_ID --yes

# Wait for rollback to complete
echo ""
echo "Waiting for rollback to complete..."
argocd app wait $APP_NAME --health --timeout 300

# Show final status
echo ""
echo "Rollback completed. Final status:"
argocd app get $APP_NAME

echo ""
echo "Rollback verification:"
CURRENT_REVISION=$(argocd app get $APP_NAME -o json | jq -r '.status.sync.revision' 2>/dev/null || echo "Unknown")
if [[ "$CURRENT_REVISION" == *"$VERSION_ID"* ]]; then
    echo "✓ Rollback successful - Application is now at revision: $CURRENT_REVISION"
else
    echo "⚠ Rollback may not have completed as expected"
    echo "Current revision: $CURRENT_REVISION"
fi

echo ""
echo "Rollback summary:"
echo "  - Application: $APP_NAME"
echo "  - Target version: $VERSION_ID"
echo "  - Status: Completed"
echo ""
echo "Post-rollback actions:"
echo "  - Verify application functionality"
echo "  - Check logs for any issues"
echo "  - Update monitoring/alerting if needed"
echo "  - Document the rollback reason for audit trail"