# AI-Assisted Kubernetes Operations Guide

## Overview

This document provides comprehensive guidance for using AI-assisted tools to manage the Todo App Kubernetes deployment. It covers kubectl-ai and kagent usage patterns, best practices, and integration with the existing deployment.

## Available AI Tools

### 1. kubectl-ai
Natural language interface for kubectl commands that translates plain English into kubectl operations.

### 2. kagent
AI-powered Kubernetes agent for advanced operations including analysis, optimization, and troubleshooting.

## Prerequisites for AI Tools

Before using AI-assisted operations, ensure:

1. **kubectl-ai Installation**:
   ```bash
   # Install kubectl-ai plugin
   curl -LO https://github.com/itaysk/kubectl-ai/releases/latest/download/kubectl-ai_linux_amd64
   chmod +x kubectl-ai_linux_amd64
   sudo mv kubectl-ai_linux_amd64 /usr/local/bin/kubectl-ai
   ```

2. **kagent Installation**:
   ```bash
   # Install kagent (if available)
   # Check for latest release on GitHub
   ```

3. **API Access**: Ensure proper API key configuration for AI tools

## Common AI Operations for Todo App

### Using kubectl-ai

#### Basic Resource Queries
```bash
# Get resources with natural language
kubectl ai get pods in todo-app namespace
kubectl ai show me deployments in todo-app
kubectl ai list services in todo-app namespace

# Get specific resources
kubectl ai get pods with label app=todo-frontend
kubectl ai show deployments with more than 1 replica
kubectl ai list all resources in default namespace
```

#### Status and Description
```bash
# Describe issues
kubectl ai describe why todo-frontend is not running
kubectl ai explain the status of backend deployment
kubectl ai show me the configuration of todo-backend service

# Check events
kubectl ai show events for todo-frontend deployment
kubectl ai explain recent errors in default namespace
```

#### Scaling Operations
```bash
# Scale resources
kubectl ai scale frontend deployment to 2 replicas
kubectl ai increase backend replicas to 3
kubectl ai set frontend replicas to 1
kubectl ai scale deployment todo-frontend --replicas=2
```

#### Log Viewing
```bash
# View logs
kubectl ai show me logs from frontend pods
kubectl ai get logs from backend in default namespace
kubectl ai show recent errors from todo-frontend
kubectl ai tail logs from backend pods
```

#### Debugging and Troubleshooting
```bash
# Debugging
kubectl ai help me debug why frontend can't connect to backend
kubectl ai what's wrong with the todo-app namespace
kubectl ai explain why pods are in CrashLoopBackOff
kubectl ai show me unhealthy pods in default namespace
```

### Using kagent

#### Cluster Health Checks
```bash
# Perform cluster health checks
kagent check cluster health
kagent analyze todo-app namespace
kagent diagnose cluster issues
kagent report cluster status
```

#### Resource Optimization
```bash
# Optimize resources
kagent optimize resource usage in todo-app
kagent suggest improvements for deployments
kagent analyze resource consumption
kagent recommend resource limits
```

#### Advanced Operations
```bash
# Advanced operations
kagent create a backup plan for todo-app
kagent monitor application performance
kagent suggest security improvements
kagent analyze deployment patterns
```

## AI-Powered Deployment Tasks

Based on the spec requirements, here are the tasks that should be performed using AI tools:

### User Story 3 Tasks

- **[T035]** Use kubectl-ai to scale frontend deployment to 2 replicas
  ```bash
  kubectl ai scale deployment todo-frontend --replicas=2
  ```

- **[T036]** Use kubectl-ai to check status of all pods and services
  ```bash
  kubectl ai get all in default namespace
  ```

- **[T037]** Use kubectl-ai to get logs from backend pod
  ```bash
  kubectl ai show logs from deployment/todo-backend
  ```

- **[T038]** Use kubectl-ai to describe deployment configuration
  ```bash
  kubectl ai describe deployment todo-backend
  ```

- **[T039]** Use kagent to perform cluster health check
  ```bash
  kagent check cluster health
  ```

- **[T040]** Use kagent to optimize resource usage
  ```bash
  kagent analyze resource usage in default namespace
  ```

- **[T041]** Document effective kubectl-ai prompts and patterns

- **[T042]** Document effective kagent commands and patterns

## Effective Prompt Patterns

### kubectl-ai Patterns

**Query Patterns:**
- "kubectl ai get [resource] in [namespace]"
- "kubectl ai show me [resource] with [label] in [namespace]"
- "kubectl ai list [resource] that are [status]"

**Action Patterns:**
- "kubectl ai scale [resource] [name] to [number] replicas"
- "kubectl ai update [resource] [name] with [change]"
- "kubectl ai set [property] for [resource] [name]"

**Debug Patterns:**
- "kubectl ai describe why [resource] is [status]"
- "kubectl ai explain [problem] in [namespace]"
- "kubectl ai show me [logs/events] from [resource]"

### kagent Patterns

**Analysis Patterns:**
- "kagent check [aspect] in [namespace]"
- "kagent analyze [component] performance"
- "kagent diagnose [problem] in [namespace]"

**Optimization Patterns:**
- "kagent optimize [resource] in [namespace]"
- "kagent suggest improvements for [component]"
- "kagent recommend [setting] for [resource]"

## Example AI Operation Workflows

### Routine Operations Workflow

Once the application is deployed, you can use AI tools for routine operations:

```bash
# Daily health check
kubectl ai get pods in default namespace
kubectl ai show services in default namespace

# Scale based on demand
kubectl ai scale deployment todo-frontend --replicas=3
kubectl ai scale deployment todo-backend --replicas=2

# Debug issues
kubectl ai describe why todo-backend pods are failing
kubectl ai show recent events in default namespace

# Monitor performance
kagent analyze default namespace performance
kagent check resource usage
```

### Troubleshooting Workflow

When issues arise, use AI tools for quick diagnosis:

```bash
# Issue identification
kubectl ai show pods with status not Running
kubectl ai get failed pods in default namespace

# Root cause analysis
kubectl ai explain why todo-frontend is restarting
kubectl ai show logs from crashing backend pods

# Resolution
kubectl ai restart deployment todo-frontend
kubectl ai scale deployment todo-backend --replicas=1
```

## Integration with Helm-Based Deployment

The AI tools integrate seamlessly with the Helm-based deployment:

1. Deploy with Helm as usual
2. Use AI tools for ongoing management
3. Document effective prompts for future reference

### Pre-deployment AI Checks
```bash
# Before deploying, check cluster capacity
kubectl ai check available resources in cluster
kubectl ai analyze if there's enough capacity for deployment
```

### Post-deployment AI Validation
```bash
# After deployment, validate everything is running
kubectl ai verify all pods in default namespace are Running
kubectl ai check if services are Ready
kubectl ai show deployment status for todo-app
```

## Best Practices for AI Operations

### Prompt Engineering
- Be specific about resource names and namespaces
- Use clear action words (get, show, list, scale, describe)
- Include context when possible (namespace, labels, conditions)

### Error Handling
- If AI tools return unexpected results, fall back to traditional kubectl
- Always verify critical operations before confirming
- Use dry-run options when available

### Documentation
- Keep a log of effective prompts for your specific use cases
- Document which AI operations work well for your environment
- Share effective patterns with team members

## Success Criteria for AI Operations

According to the spec, success includes:

- Performing at least 3 Kubernetes operations using kubectl-ai successfully
- Using kagent for cluster health and optimization
- Documenting effective prompts and patterns
- Maintaining operational efficiency through AI assistance

## Limitations and Fallbacks

### When AI Tools May Not Work Well
- Complex multi-resource operations
- Custom resource definitions (CRDs)
- Network policy debugging
- Storage-related issues

### Fallback Strategies
- Traditional kubectl commands
- Manual YAML editing when needed
- Direct API calls for complex operations

## Security Considerations

- Ensure AI tools don't expose sensitive information in prompts
- Review AI-generated configurations for security compliance
- Validate that AI operations maintain proper RBAC boundaries
- Monitor API key usage and access patterns

## Performance Tips

- Use specific resource names instead of broad queries
- Leverage label selectors for targeted operations
- Combine multiple operations when possible
- Use namespace filtering to avoid cluttered results