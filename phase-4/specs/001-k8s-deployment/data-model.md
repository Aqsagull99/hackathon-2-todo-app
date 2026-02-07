# Data Model: Phase IV — Local Kubernetes Deployment

## Overview
Data model for Kubernetes deployment configuration of the Todo Chatbot application.

## Entities

### Container Image
**Description**: Represents the packaged application with all dependencies for deployment
**Fields**:
- image_name: string (e.g., "todo-frontend", "todo-backend")
- tag: string (version identifier)
- registry: string (Docker Hub repository)
- build_context: string (path to Dockerfile context)
- environment_variables: map<string, string> (runtime configuration)

**Validation Rules**:
- image_name must be alphanumeric with hyphens only
- tag must follow semantic versioning or "latest"
- registry must be a valid Docker registry URL

### Helm Chart
**Description**: Represents the Kubernetes deployment configuration for applications
**Fields**:
- name: string (chart name)
- version: string (chart version)
- app_version: string (application version)
- templates: list<string> (Kubernetes manifest templates)
- values: map<string, any> (configuration parameters)
- dependencies: list<HelmDependency> (other charts this chart depends on)

**Validation Rules**:
- name must be DNS-1123 compliant
- version must follow semantic versioning
- values must pass schema validation

### Kubernetes Deployment
**Description**: Represents the running application instances in the cluster
**Fields**:
- name: string (deployment name)
- replicas: integer (desired number of pods)
- container_images: list<string> (image references)
- resources: ResourceRequirements (CPU/memory limits)
- environment: map<string, string> (pod environment variables)
- health_checks: HealthCheckConfig (readiness/liveness probes)

**Validation Rules**:
- replicas must be >= 0
- resources must not exceed node capacity
- health checks must have appropriate timeouts and thresholds

### Service Configuration
**Description**: Represents network connectivity between applications
**Fields**:
- name: string (service name)
- type: ServiceType (ClusterIP, NodePort, LoadBalancer, ExternalName)
- ports: list<ServicePort> (port mappings)
- selector: map<string, string> (pod selector labels)
- external_connectivity: boolean (whether service is exposed externally)

**Validation Rules**:
- port numbers must be valid (1-65535)
- service type must be one of the allowed values
- selector labels must match deployment labels

## Relationships
- One Container Image can be used by multiple Kubernetes Deployments
- One Helm Chart contains multiple Kubernetes Deployments and Service Configurations
- Multiple Kubernetes Deployments communicate via Service Configurations
- Service Configurations provide network connectivity between deployments

## State Transitions (for Deployments)
- Pending → Running (when all pods are ready)
- Running → Updating (during rolling updates)
- Updating → Running (when update completes)
- Running → Failed (when health checks fail persistently)