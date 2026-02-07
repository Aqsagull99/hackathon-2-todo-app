#!/usr/bin/env python3
"""
Docker Compose generator for multi-service Python/FastAPI applications
"""

import argparse
import yaml
from pathlib import Path

def generate_compose_file(services_config):
    """Generate Docker Compose file based on services configuration"""

    compose_data = {
        'version': '3.8',
        'services': {},
        'volumes': {}
    }

    # Add web service
    compose_data['services']['web'] = {
        'build': {
            'context': '.',
            'target': 'final'
        },
        'ports': ['8000:8000'],
        'environment': [
            'DATABASE_URL=postgresql://user:password@db:5432/myapp',
            'REDIS_URL=redis://redis:6379'
        ],
        'env_file': ['.env'],
        'restart': 'unless-stopped'
    }

    depends_conditions = []

    # Add database service if requested
    if 'postgres' in services_config:
        compose_data['services']['db'] = {
            'image': 'postgres:15',
            'restart': 'unless-stopped',
            'volumes': ['postgres_data:/var/lib/postgresql/data/'],
            'environment': [
                'POSTGRES_DB=myapp',
                'POSTGRES_USER=user',
                'POSTGRES_PASSWORD=password'
            ],
            'healthcheck': {
                'test': ['CMD-SHELL', 'pg_isready -U user -d myapp'],
                'interval': '10s',
                'timeout': '5s',
                'retries': 5
            }
        }
        compose_data['volumes']['postgres_data'] = None
        depends_conditions.append({'db': {'condition': 'service_healthy'}})

    # Add Redis service if requested
    if 'redis' in services_config:
        compose_data['services']['redis'] = {
            'image': 'redis:7-alpine',
            'restart': 'unless-stopped',
            'healthcheck': {
                'test': ['CMD', 'redis-cli', 'ping'],
                'interval': '10s',
                'timeout': '5s',
                'retries': 5
            }
        }
        depends_conditions.append({'redis': {'condition': 'service_healthy'}})

    # Add dependency conditions to web service
    if depends_conditions:
        compose_data['services']['web']['depends_on'] = {}
        for dep in depends_conditions:
            compose_data['services']['web']['depends_on'].update(dep)

    return yaml.dump(compose_data, default_flow_style=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Generate Docker Compose file for Python/FastAPI applications')
    parser.add_argument('--services', nargs='+', choices=['postgres', 'redis'],
                       default=['postgres'], help='Services to include in compose')
    parser.add_argument('--output', default='docker-compose.yml', help='Output filename')

    args = parser.parse_args()

    compose_content = generate_compose_file(args.services)

    with open(args.output, 'w') as f:
        f.write(compose_content)

    print(f"Docker Compose file generated successfully: {args.output}")
    print(f"Included services: {', '.join(args.services)}")

if __name__ == "__main__":
    main()
