# AI-Assisted Kubernetes Operations Guide

This document outlines how to use AI-assisted tools for Kubernetes operations with the Todo App deployment.

## Available AI Tools

### 1. kubectl-ai
Natural language interface for kubectl commands.

### 2. kagent
AI-powered Kubernetes agent for advanced operations.

## Common AI Operations

### Using kubectl-ai

```bash
# Get resources with natural language
kubectl ai get pods in todo-app namespace
kubectl ai show me deployments in todo-app
kubectl ai list services in todo-app namespace

# Describe issues
kubectl ai describe why todo-frontend is not running
kubectl ai explain the status of backend deployment

# Scale resources
kubectl ai scale frontend deployment to 3 replicas
kubectl ai increase backend replicas to 2

# View logs
kubectl ai show me logs from frontend pods
kubectl ai get logs from backend in todo-app namespace

# Debugging
kubectl ai help me debug why frontend can't connect to backend
kubectl ai what's wrong with the todo-app namespace
```

### Using kagent

```bash
# Perform cluster health checks
kagent check cluster health
kagent analyze todo-app namespace

# Optimize resources
kagent optimize resource usage in todo-app
kagent suggest improvements for deployments

# Advanced operations
kagent create a backup plan for todo-app
kagent monitor application performance
```

## AI-Powered Deployment Tasks

Based on the spec requirements, here are the tasks that should be performed using AI tools:

### User Story 3 Tasks
- [T035] Use kubectl-ai to scale frontend deployment to 2 replicas
- [T036] Use kubectl-ai to check status of all pods and services
- [T037] Use kubectl-ai to get logs from backend pod
- [T038] Use kubectl-ai to describe deployment configuration
- [T039] Use kagent to perform cluster health check
- [T040] Use kagent to optimize resource usage
- [T041] Document effective kubectl-ai prompts and patterns
- [T042] Document effective kagent commands and patterns

## Effective Prompt Patterns

### kubectl-ai Patterns
- "kubectl ai get [resource] in [namespace]"
- "kubectl ai describe [resource] [name] in [namespace]"
- "kubectl ai show logs from [selector] in [namespace]"
- "kubectl ai explain why [resource] is [status]"

### kagent Patterns
- "kagent check [aspect] in [namespace]"
- "kagent optimize [resource] in [namespace]"
- "kagent analyze [component] performance"

## Example Workflow

Once the application is deployed, you can use AI tools for routine operations:

```bash
# Check overall health
kubectl ai get pods in todo-app namespace

# Scale based on demand
kubectl ai scale todo-frontend deployment to 3 replicas in todo-app

# Debug issues
kubectl ai describe why todo-backend pods are failing

# Monitor performance
kagent analyze todo-app namespace performance
```

## Integration with Deployment

The AI tools integrate seamlessly with the Helm-based deployment:

1. Deploy with Helm as usual
2. Use AI tools for ongoing management
3. Document effective prompts for future reference

## Success Criteria for AI Operations

According to the spec, success includes:
- Performing at least 3 Kubernetes operations using kubectl-ai successfully
- Using kagent for cluster health and optimization
- Documenting effective prompts and patterns