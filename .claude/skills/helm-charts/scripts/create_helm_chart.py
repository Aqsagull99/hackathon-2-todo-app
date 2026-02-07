#!/usr/bin/env python3
"""
Automated Helm chart generator for Kubernetes applications
Supports multiple configurations: simple, with dependencies, production-ready
"""

import argparse
import os
import yaml
from pathlib import Path

def create_chart_structure(chart_name, chart_type="simple"):
    """Create the basic Helm chart structure"""

    # Create main chart directory
    chart_dir = Path(chart_name)
    chart_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (chart_dir / "templates").mkdir(exist_ok=True)
    (chart_dir / "tests").mkdir(exist_ok=True)
    (chart_dir / "charts").mkdir(exist_ok=True)

    # Create Chart.yaml
    chart_yaml = {
        'apiVersion': 'v2',
        'name': chart_name,
        'description': f'A Helm chart for {chart_name}',
        'type': 'application',
        'version': '0.1.0',
        'appVersion': '1.0.0'
    }

    if chart_type == "production":
        chart_yaml.update({
            'kubeVersion': '>=1.24.0',
            'keywords': ['web', 'frontend'],
            'home': f'https://github.com/example/{chart_name}',
            'sources': [f'https://github.com/example/{chart_name}'],
            'maintainers': [
                {'name': 'Your Name', 'email': 'your.email@example.com'}
            ],
            'icon': f'https://example.com/{chart_name}/icon.png',
            'dependencies': [
                {
                    'name': 'common',
                    'version': '^1.0.0',
                    'repository': 'https://charts.bitnami.com/bitnami'
                }
            ]
        })

    with open(chart_dir / "Chart.yaml", 'w') as f:
        yaml.dump(chart_yaml, f, default_flow_style=False)

    # Create values.yaml
    if chart_type == "simple":
        values_yaml = {
            'replicaCount': 1,
            'image': {
                'repository': 'nginx',
                'pullPolicy': 'IfNotPresent',
                'tag': 'latest'
            },
            'imagePullSecrets': [],
            'nameOverride': '',
            'fullnameOverride': ''
        }
    elif chart_type == "production":
        values_yaml = {
            'replicaCount': 1,
            'image': {
                'repository': 'nginx',
                'pullPolicy': 'IfNotPresent',
                'tag': 'latest'
            },
            'imagePullSecrets': [],
            'nameOverride': '',
            'fullnameOverride': '',
            'serviceAccount': {
                'create': True,
                'annotations': {},
                'name': ''
            },
            'podAnnotations': {},
            'podSecurityContext': {
                'fsGroup': 2000
            },
            'securityContext': {
                'capabilities': {
                    'drop': ['ALL']
                },
                'readOnlyRootFilesystem': True,
                'runAsNonRoot': True,
                'runAsUser': 1000
            },
            'service': {
                'type': 'ClusterIP',
                'port': 80
            },
            'ingress': {
                'enabled': False,
                'className': '',
                'annotations': {},
                'hosts': [
                    {
                        'host': 'chart-example.local',
                        'paths': [
                            {
                                'path': '/',
                                'pathType': 'ImplementationSpecific'
                            }
                        ]
                    }
                ],
                'tls': []
            },
            'resources': {
                'limits': {
                    'cpu': '100m',
                    'memory': '128Mi'
                },
                'requests': {
                    'cpu': '100m',
                    'memory': '128Mi'
                }
            },
            'autoscaling': {
                'enabled': False,
                'minReplicas': 1,
                'maxReplicas': 100,
                'targetCPUUtilizationPercentage': 80
            },
            'nodeSelector': {},
            'tolerations': [],
            'affinity': {}
        }

    with open(chart_dir / "values.yaml", 'w') as f:
        yaml.dump(values_yaml, f, default_flow_style=False)

    # Create .helmignore
    helmignore_content = """# Patterns to ignore when building packages.
# This supports shell glob matching, relative path matching, and
# negation (prefixed with !). Only one pattern per line.
.DS_Store
# Common VCS dirs
.git/
.gitignore
.bzr/
.bzrignore
.hg/
.hgignore
.svn/
# Common backup files
*.swp
*.bak
*.tmp
*~
# Various IDEs
.project
.idea/
*.tmproj
.vscode/
# Temporary build files
tmp/
dist/
build/
"""

    with open(chart_dir / ".helmignore", 'w') as f:
        f.write(helmignore_content)

    # Create basic templates
    create_basic_templates(chart_dir)

    # Create environment-specific values files
    create_env_values_files(chart_dir)

    return chart_dir

def create_basic_templates(chart_dir):
    """Create basic template files"""

    # Create _helpers.tpl
    helpers_content = f"""{{{{/*
Expand the name of the chart.
*/}}}}
{{{{- define "{chart_dir.name}.name" -}}}}
{{{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}}}{{{{- end }}}}

{{{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}}}
{{{{- define "{chart_dir.name}.fullname" -}}}}
{{{{- if .Values.fullnameOverride }}}}{{{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}}}{{{{- else }}}}{{{{- $name := default .Chart.Name .Values.nameOverride }}}}{{{{- if contains $name .Release.Name }}}}{{{{- .Release.Name | trunc 63 | trimSuffix "-" }}}}{{{{- else }}}}{{{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}}}{{{{- end }}}}{{{{- end }}}}{{{{- end }}}}

{{{{/*
Create chart name and version as used by the chart label.
*/}}}}
{{{{- define "{chart_dir.name}.chart" -}}}}
{{{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}}}{{{{- end }}}}

{{{{/*
Common labels
*/}}}}
{{{{- define "{chart_dir.name}.labels" -}}}}
helm.sh/chart: {{{{ include "{chart_dir.name}.chart" . }}}}
{{{{ include "{chart_dir.name}.selectorLabels" . }}}}
{{{{- if .Chart.AppVersion }}}}
app.kubernetes.io/version: {{{{ .Chart.AppVersion | quote }}}}
{{{{- end }}}}
app.kubernetes.io/managed-by: {{{{ .Release.Service }}}}
{{{{- end }}}}

{{{{/*
Selector labels
*/}}}}
{{{{- define "{chart_dir.name}.selectorLabels" -}}}}
app.kubernetes.io/name: {{{{ include "{chart_dir.name}.name" . }}}}
app.kubernetes.io/instance: {{{{ .Release.Name }}}}
{{{{- end }}}}

{{{{/*
Create the name of the service account to use
*/}}}}
{{{{- define "{chart_dir.name}.serviceAccountName" -}}}}
{{{{- if .Values.serviceAccount.create }}}}{{{{ include "{chart_dir.name}.fullname" . }}}}{{{{- else }}}}{{{{ .Values.serviceAccount.name }}}}{{{{- end }}}}{{{{- end }}}}
"""

    with open(chart_dir / "templates" / "_helpers.tpl", 'w') as f:
        f.write(helpers_content)

    # Create deployment.yaml
    deployment_content = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{{{ include "{chart_dir.name}.fullname" . }}}}
  labels:
    {{{{- include "{chart_dir.name}.labels" . | nindent 4 }}}}
  {{- with .Values.deployment.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{{{ .Values.replicaCount }}}}
  {{- end }}
  {{- with .Values.deployment.strategy }}
  strategy:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  selector:
    matchLabels:
      {{{{- include "{chart_dir.name}.selectorLabels" . | nindent 6 }}}}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{{{- include "{chart_dir.name}.selectorLabels" . | nindent 8 }}}}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{{{ include "{chart_dir.name}.serviceAccountName" . }}}}
      {{- with .Values.podSecurityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: {{{{ .Chart.Name }}}}
          {{- with .Values.securityContext }}
          securityContext:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          image: "{{{{ .Values.image.repository }}}}{{{{- if .Values.image.tag }}}}{{{{ .Values.image.tag }}}}{{{{- else }}}}{{{{ .Chart.AppVersion }}}}{{{{- end }}}}"
          imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
          {{- if .Values.command }}
          command:
            {{- toYaml .Values.command | nindent 12 }}
          {{- end }}
          {{- if .Values.args }}
          args:
            {{- toYaml .Values.args | nindent 12 }}
          {{- end }}
          ports:
            - name: http
              containerPort: {{{{ .Values.service.targetPort | default 80 }}}}
              protocol: TCP
          {{- if .Values.livenessProbe.enabled }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe.spec | nindent 12 }}
          {{- else if .Values.livenessProbe }}
          livenessProbe:
            httpGet:
              path: {{{{ .Values.livenessProbe.path | default "/" }}}}
              port: {{{{ .Values.service.port }}}}
          {{- end }}
          {{- if .Values.readinessProbe.enabled }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe.spec | nindent 12 }}
          {{- else if .Values.readinessProbe }}
          readinessProbe:
            httpGet:
              path: {{{{ .Values.readinessProbe.path | default "/" }}}}
              port: {{{{ .Values.service.port }}}}
          {{- end }}
          {{- if .Values.startupProbe.enabled }}
          startupProbe:
            {{- toYaml .Values.startupProbe.spec | nindent 12 }}
          {{- end }}
          resources:
            {{{{- toYaml .Values.resources | nindent 12 }}}}
          {{- with .Values.env }}
          env:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.volumeMounts }}
          volumeMounts:
            {{- toYaml . | nindent 12 }}
          {{- end }}
      {{- with .Values.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- if .Values.priorityClassName }}
      priorityClassName: {{ .Values.priorityClassName }}
      {{- end }}
      {{- if .Values.schedulerName }}
      schedulerName: {{ .Values.schedulerName }}
      {{- end }}
"""

    with open(chart_dir / "templates" / "deployment.yaml", 'w') as f:
        f.write(deployment_content)

    # Create service.yaml
    service_content = f"""apiVersion: v1
kind: Service
metadata:
  name: {{{{ include "{chart_dir.name}.fullname" . }}}}
  labels:
    {{{{- include "{chart_dir.name}.labels" . | nindent 4 }}}}
  {{- with .Values.service.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  type: {{{{ .Values.service.type }}}}
  {{- with .Values.service.clusterIP }}
  clusterIP: {{ . }}
  {{- end }}
  {{- if .Values.service.loadBalancerIP }}
  loadBalancerIP: {{ .Values.service.loadBalancerIP }}
  {{- end }}
  {{- with .Values.service.loadBalancerSourceRanges }}
  loadBalancerSourceRanges:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  ports:
    - name: http
      port: {{{{ .Values.service.port }}}}
      targetPort: {{{{ .Values.service.targetPort | default 80 }}}}
      protocol: TCP
      {{- if and (eq .Values.service.type "NodePort") .Values.service.nodePort }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
  selector:
    {{{{- include "{chart_dir.name}.selectorLabels" . | nindent 4 }}}}
"""

    with open(chart_dir / "templates" / "service.yaml", 'w') as f:
        f.write(service_content)

    # Create NOTES.txt
    notes_content = f"""1. Get the application URL by running these commands:
{{{{- if .Values.ingress.enabled }}}}
{{{{- range $host := .Values.ingress.hosts }}}}
  {{- range .paths }}
  http{{{{ if $.Values.ingress.tls }}}}s{{{{ end }}}}://{{{{ $host.host }}}}{{{{ .path }}}
  {{- end }}
{{{{- end }}}}
{{{{- else if contains "NodePort" .Values.service.type }}}}
  export NODE_PORT=$(kubectl get --namespace {{{{ .Release.Namespace }}}} -o jsonpath="{{{{.spec.ports[0].nodePort}}}}" services {{{{ include "{chart_dir.name}.fullname" . }}})
  export NODE_IP=$(kubectl get nodes --namespace {{{{ .Release.Namespace }}}} -o jsonpath="{{{{.items[0].status.addresses[0].address}}}}")
  echo http://$NODE_IP:$NODE_PORT
{{{{- else if contains "LoadBalancer" .Values.service.type }}}}
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status of by running 'kubectl get --namespace {{{{ .Release.Namespace }}}} svc -w {{{{ include "{chart_dir.name}.fullname" . }}}}'
  export SERVICE_IP=$(kubectl get svc --namespace {{{{ .Release.Namespace }}}} {{{{ include "{chart_dir.name}.fullname" . }}}}
  echo http://$SERVICE_IP:{{{{ .Values.service.port }}}}
{{{{- else if contains "ClusterIP" .Values.service.type }}}}
  export POD_NAME=$(kubectl get pods --namespace {{{{ .Release.Namespace }}}} -l "app.kubernetes.io/name={{{{ include "{chart_dir.name}.name" . }}}},app.kubernetes.io/instance={{{{ .Release.Name }}}}" -o jsonpath="{{{{.items[0].metadata.name}}}}")
  export CONTAINER_PORT=$(kubectl get pod --namespace {{{{ .Release.Namespace }}}} $POD_NAME -o jsonpath="{{{{.spec.containers[0].ports[0].containerPort}}}}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{{{ .Release.Namespace }}}} port-forward $POD_NAME 8080:$CONTAINER_PORT
{{{{- end }}}}
"""

    with open(chart_dir / "templates" / "NOTES.txt", 'w') as f:
        f.write(notes_content)

def create_env_values_files(chart_dir):
    """Create environment-specific values files"""

    # Development values
    dev_values = {
        'replicaCount': 1,
        'image': {
            'repository': f'my-registry.com/{chart_dir.name}-dev',
            'pullPolicy': 'Always',
            'tag': 'dev-latest'
        },
        'resources': {
            'limits': {
                'cpu': '500m',
                'memory': '512Mi'
            },
            'requests': {
                'cpu': '100m',
                'memory': '128Mi'
            }
        },
        'service': {
            'type': 'ClusterIP',
            'port': 8080
        },
        'ingress': {
            'enabled': True,
            'className': 'nginx',
            'annotations': {
                'nginx.ingress.kubernetes.io/rewrite-target': '/'
            },
            'hosts': [
                {
                    'host': f'dev.{chart_dir.name}.local',
                    'paths': [
                        {
                            'path': '/',
                            'pathType': 'ImplementationSpecific'
                        }
                    ]
                }
            ]
        },
        'env': [
            {'name': 'ENV', 'value': 'development'},
            {'name': 'LOG_LEVEL', 'value': 'debug'}
        ],
        'livenessProbe': {
            'enabled': True,
            'path': '/health'
        },
        'readinessProbe': {
            'enabled': True,
            'path': '/ready'
        },
        'nodeSelector': {},
        'tolerations': [],
        'affinity': {},
        'autoscaling': {
            'enabled': False
        },
        'logging': {
            'enabled': True,
            'sidecar': {
                'enabled': True,
                'image': 'fluent/fluent-bit:1.8',
                'config': '|-\n  [INPUT]\n      Name tail\n      Path /var/log/app/*.log\n  [OUTPUT]\n      Name forward\n      Match *'
            }
        }
    }

    with open(chart_dir / "values-dev.yaml", 'w') as f:
        yaml.dump(dev_values, f, default_flow_style=False)

    # Production values
    prod_values = {
        'replicaCount': 3,
        'image': {
            'repository': f'my-registry.com/{chart_dir.name}',
            'pullPolicy': 'IfNotPresent',
            'tag': 'v1.0.0'  # Pin to specific version
        },
        'imagePullSecrets': [
            {'name': 'production-registry-secret'}
        ],
        'resources': {
            'limits': {
                'cpu': '1000m',
                'memory': '1Gi'
            },
            'requests': {
                'cpu': '500m',
                'memory': '512Mi'
            }
        },
        'service': {
            'type': 'LoadBalancer',
            'port': 80
        },
        'ingress': {
            'enabled': True,
            'className': 'nginx',
            'annotations': {
                'cert-manager.io/cluster-issuer': 'letsencrypt-prod',
                'nginx.ingress.kubernetes.io/ssl-redirect': 'true',
                'nginx.ingress.kubernetes.io/force-ssl-redirect': 'true'
            },
            'hosts': [
                {
                    'host': f'{chart_dir.name}.example.com',
                    'paths': [
                        {
                            'path': '/',
                            'pathType': 'ImplementationSpecific'
                        }
                    ]
                }
            ],
            'tls': [
                {
                    'secretName': f'{chart_dir.name}-tls',
                    'hosts': [f'{chart_dir.name}.example.com']
                }
            ]
        },
        'autoscaling': {
            'enabled': True,
            'minReplicas': 3,
            'maxReplicas': 10,
            'targetCPUUtilizationPercentage': 70,
            'targetMemoryUtilizationPercentage': 80
        },
        'env': [
            {'name': 'ENV', 'value': 'production'},
            {'name': 'LOG_LEVEL', 'value': 'info'}
        ],
        'securityContext': {
            'runAsNonRoot': True,
            'runAsUser': 1000,
            'runAsGroup': 3000,
            'readOnlyRootFilesystem': True,
            'allowPrivilegeEscalation': False,
            'capabilities': {
                'drop': ['ALL']
            }
        },
        'podSecurityContext': {
            'fsGroup': 2000
        },
        'priorityClassName': 'high-priority',
        'nodeSelector': {
            'node-type': 'production'
        },
        'tolerations': [
            {
                'key': 'node-type',
                'operator': 'Equal',
                'value': 'production',
                'effect': 'NoSchedule'
            }
        ],
        'affinity': {
            'podAntiAffinity': {
                'preferredDuringSchedulingIgnoredDuringExecution': [
                    {
                        'weight': 100,
                        'podAffinityTerm': {
                            'labelSelector': {
                                'matchExpressions': [
                                    {
                                        'key': 'app.kubernetes.io/name',
                                        'operator': 'In',
                                        'values': [chart_dir.name]
                                    }
                                ]
                            },
                            'topologyKey': 'kubernetes.io/hostname'
                        }
                    }
                ]
            }
        },
        'livenessProbe': {
            'enabled': True,
            'spec': {
                'httpGet': {
                    'path': '/health',
                    'port': 80
                },
                'initialDelaySeconds': 30,
                'periodSeconds': 10,
                'timeoutSeconds': 5,
                'failureThreshold': 6
            }
        },
        'readinessProbe': {
            'enabled': True,
            'spec': {
                'httpGet': {
                    'path': '/ready',
                    'port': 80
                },
                'initialDelaySeconds': 5,
                'periodSeconds': 10,
                'timeoutSeconds': 5,
                'failureThreshold': 3
            }
        },
        'podDisruptionBudget': {
            'enabled': True,
            'minAvailable': 1
        },
        'logging': {
            'enabled': True,
            'sidecar': {
                'enabled': True,
                'image': 'fluent/fluent-bit:1.8',
                'config': '|-\n  [INPUT]\n      Name tail\n      Path /var/log/app/*.log\n  [OUTPUT]\n      Name forward\n      Match *\n      Host fluentd.default.svc.cluster.local\n      Port 24224'
            }
        },
        'tracing': {
            'enabled': True,
            'endpoint': 'jaeger-collector.monitoring:14268'
        }
    }

    with open(chart_dir / "values-prod.yaml", 'w') as f:
        yaml.dump(prod_values, f, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Generate Helm chart for Kubernetes applications')
    parser.add_argument('chart_name', help='Name of the Helm chart to create')
    parser.add_argument('--type', choices=['simple', 'with-deps', 'production'],
                       default='simple', help='Chart complexity level to generate')
    parser.add_argument('--output', help='Output directory (defaults to chart name)')

    args = parser.parse_args()

    chart_dir = create_chart_structure(args.chart_name, args.type)

    print(f"Helm chart '{args.chart_name}' created successfully in: {chart_dir}")
    print("Next steps:")
    print(f"1. Review and customize the generated files in {chart_dir}")
    print(f"2. Run 'helm lint {args.chart_name}' to validate the chart")
    print(f"3. Run 'helm template test-release {args.chart_name}' to render templates")
    print(f"4. Install with 'helm install my-release {args.chart_name}'")

if __name__ == "__main__":
    main()