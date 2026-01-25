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