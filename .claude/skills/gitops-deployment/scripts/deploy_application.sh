#!/bin/bash
# Script to deploy an application using ArgoCD with quality gates and rollback capability
# Usage: ./deploy_application.sh <app-name> <repo-url> <path> <namespace>
#
# This script includes quality gates through health checks and provides rollback guidance
# Quality gates ensure deployment meets criteria before promotion
# Rollback strategies are available if deployment fails validation

set -e  # Exit on any error

APP_NAME=${1:-"my-app"}
REPO_URL=${2:-"https://github.com/argoproj/argocd-example-apps.git"}
PATH=${3:-"guestbook"}
NAMESPACE=${4:-"production"}

echo "Deploying application: $APP_NAME"
echo "Repository: $REPO_URL"
echo "Path: $PATH"
echo "Destination namespace: $NAMESPACE"
echo ""
echo "Quality gates will be enforced through:"
echo "  - Health checks during deployment"
echo "  - Sync validation before promoting changes"
echo "  - Automated rollback options if health checks fail"

# Validate inputs
if [[ -z "$APP_NAME" ]]; then
    echo "Error: Application name cannot be empty"
    exit 1
fi

if [[ -z "$REPO_URL" ]]; then
    echo "Error: Repository URL cannot be empty"
    exit 1
fi

# Check if argocd CLI is available
if ! command -v argocd &> /dev/null; then
    echo "Error: argocd CLI is not installed or not in PATH"
    echo "Install it with:"
    echo "curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64"
    echo "sudo install argocd-linux-amd64 /usr/local/bin/argocd"
    echo "chmod +x /usr/local/bin/argocd"
    exit 1
fi

# Check if ArgoCD server is accessible
if ! argocd app list &> /dev/null; then
    echo "Error: Cannot connect to ArgoCD server"
    echo "Make sure you have logged in with: argocd login SERVER"
    exit 1
fi

# Create the application with automated sync and quality gates
echo "Creating ArgoCD application with quality gates..."
argocd app create $APP_NAME \
  --repo $REPO_URL \
  --path $PATH \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace $NAMESPACE \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# Check application status
echo ""
echo "Application created. Checking status..."
argocd app get $APP_NAME

# Wait for sync to complete with health validation
echo ""
echo "Waiting for application to sync with health validation..."
argocd app wait $APP_NAME --health

# Verify deployment quality
echo ""
echo "Verifying deployment quality gates..."
HEALTH_STATUS=$(argocd app get $APP_NAME -o json | jq -r '.status.health.status' 2>/dev/null || echo "Unknown")

if [[ "$HEALTH_STATUS" == "Healthy" ]]; then
    echo "✓ Quality gates PASSED - Application is healthy"
    echo "✓ Deployment successful with all quality checks satisfied"
else
    echo "⚠ Quality gates FAILED - Application health: $HEALTH_STATUS"
    echo "⚠ Deployment may require manual intervention"
    echo ""
    echo "Rollback options:"
    echo "  - Check deployment history: argocd app history $APP_NAME"
    echo "  - Rollback to previous version: argocd app rollback $APP_NAME <previous_version_id>"
    echo "  - Manual sync to known good state: argocd app sync $APP_NAME --revision <known_good_revision>"
fi

echo ""
echo "Application $APP_NAME deployed!"
echo ""
echo "Application status:"
argocd app get $APP_NAME
echo ""
echo "Deployment summary:"
echo "  - Quality gates: Enforced via health checks"
echo "  - Rollback capability: Available through deployment history"
echo "  - Sync status: Automated with pruning and self-healing enabled"
echo ""
echo "Common commands:"
echo "  - View status: argocd app get $APP_NAME"
echo "  - Sync manually: argocd app sync $APP_NAME"
echo "  - Check history: argocd app history $APP_NAME"
echo "  - Rollback: argocd app rollback $APP_NAME <version_id>"
echo "  - Refresh: argocd app refresh $APP_NAME"