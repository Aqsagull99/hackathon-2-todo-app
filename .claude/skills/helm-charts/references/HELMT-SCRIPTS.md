# Helm Chart Scripts for Kubernetes Applications

This document contains scripts for automated Helm chart creation, validation, and management for Kubernetes applications.

## Automated Helm Chart Generator Script

```python
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
spec:
  replicas: {{{{ .Values.replicaCount }}}}
  selector:
    matchLabels:
      {{{{- include "{chart_dir.name}.selectorLabels" . | nindent 6 }}}}
  template:
    metadata:
      labels:
        {{{{- include "{chart_dir.name}.selectorLabels" . | nindent 8 }}}}
    spec:
      containers:
        - name: {{{{ .Chart.Name }}}}
          image: "{{{{ .Values.image.repository }}}}{{{{- if .Values.image.tag }}}}{{{{ .Values.image.tag }}}}{{{{- else }}}}{{{{ .Chart.AppVersion }}}}{{{{- end }}}}"
          imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{{{- toYaml .Values.resources | nindent 12 }}}}
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
spec:
  type: {{{{ .Values.service.type }}}}
  ports:
    - port: {{{{ .Values.service.port }}}}
      targetPort: http
      protocol: TCP
      name: http
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
```

## Helm Chart Validator Script

```python
#!/usr/bin/env python3
"""
Helm chart validator and security scanner
Checks for best practices, security issues, and production readiness
"""

import argparse
import subprocess
import sys
import yaml
from pathlib import Path

def run_helm_lint(chart_path):
    """Run helm lint on the chart"""
    print("Running helm lint...")
    result = subprocess.run(['helm', 'lint', chart_path],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Helm lint failed:")
        print(result.stdout)
        print(result.stderr)
        return False
    else:
        print("✅ Helm lint passed")
        return True

def validate_chart_yaml(chart_path):
    """Validate Chart.yaml content"""
    print("Validating Chart.yaml...")

    chart_yaml_path = Path(chart_path) / "Chart.yaml"
    if not chart_yaml_path.exists():
        print("❌ Chart.yaml not found")
        return False

    with open(chart_yaml_path, 'r') as f:
        try:
            chart_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML in Chart.yaml: {e}")
            return False

    # Check required fields
    required_fields = ['apiVersion', 'name', 'version']
    for field in required_fields:
        if field not in chart_data:
            print(f"❌ Missing required field in Chart.yaml: {field}")
            return False

    # Check for best practices
    issues = []
    if 'description' not in chart_data:
        issues.append("Missing description in Chart.yaml")

    if 'appVersion' not in chart_data:
        issues.append("Missing appVersion in Chart.yaml")

    if chart_data.get('apiVersion') != 'v2':
        issues.append("Use apiVersion v2 for Helm 3 charts")

    if issues:
        print("⚠️  Best practice issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ Chart.yaml validation passed")

    return len(issues) == 0

def validate_values_yaml(chart_path):
    """Validate values.yaml content"""
    print("Validating values.yaml...")

    values_yaml_path = Path(chart_path) / "values.yaml"
    if not values_yaml_path.exists():
        print("❌ values.yaml not found")
        return False

    with open(values_yaml_path, 'r') as f:
        try:
            values_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML in values.yaml: {e}")
            return False

    # Check for security best practices
    issues = []

    # Check if securityContext is defined
    if 'securityContext' not in values_data:
        issues.append("Consider adding securityContext to values.yaml for security")

    # Check if resources are defined
    if 'resources' not in values_data:
        issues.append("Consider defining resource limits and requests in values.yaml")

    # Check for imagePullPolicy
    image_policy = values_data.get('image', {}).get('pullPolicy', '')
    if image_policy == 'Always':
        issues.append("Using Always for imagePullPolicy may not be optimal for production")

    if issues:
        print("⚠️  Best practice issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ values.yaml validation passed")

    return len(issues) == 0

def check_templates_security(chart_path):
    """Check templates for security issues"""
    print("Checking templates for security issues...")

    templates_dir = Path(chart_path) / "templates"
    if not templates_dir.exists():
        print("❌ templates directory not found")
        return False

    issues = []

    # Look for common security issues in templates
    for template_file in templates_dir.rglob("*.yaml"):
        with open(template_file, 'r') as f:
            content = f.read()

            # Check for privileged containers
            if 'privileged: true' in content:
                issues.append(f"Template {template_file} contains privileged containers")

            # Check for hostNetwork
            if 'hostNetwork: true' in content:
                issues.append(f"Template {template_file} uses hostNetwork (security risk)")

            # Check for hostPID
            if 'hostPID: true' in content:
                issues.append(f"Template {template_file} uses hostPID (security risk)")

    if issues:
        print("❌ Security issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Template security check passed")
        return True

def main():
    parser = argparse.ArgumentParser(description='Validate Helm chart for security and best practices')
    parser.add_argument('chart_path', help='Path to the Helm chart directory')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings as well as errors')

    args = parser.parse_args()

    print(f"Validating Helm chart: {args.chart_path}")
    print("-" * 50)

    results = []
    results.append(run_helm_lint(args.chart_path))
    results.append(validate_chart_yaml(args.chart_path))
    results.append(validate_values_yaml(args.chart_path))
    results.append(check_templates_security(args.chart_path))

    passed = sum(results)
    total = len(results)

    print("-" * 50)
    print(f"Validation results: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All validations passed!")
        sys.exit(0)
    else:
        print("❌ Some validations failed!")
        sys.exit(1 if not args.strict or passed == 0 else 0)

if __name__ == "__main__":
    main()
```