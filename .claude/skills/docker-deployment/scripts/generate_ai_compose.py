#!/usr/bin/env python3
"""
Script to generate Docker Compose configuration with resource constraints for AI services
"""

import argparse
import yaml

def generate_ai_compose_config(service_name, memory_limit="8G", cpu_limit="4.0", gpu_enabled=False):
    """Generate Docker Compose configuration with AI service resource constraints"""

    compose_config = {
        'version': '3.8',
        'services': {
            service_name: {
                'build': '.',
                'deploy': {
                    'resources': {
                        'limits': {
                            'cpus': cpu_limit,
                            'memory': memory_limit,
                            'pids': 300
                        },
                        'reservations': {
                            'cpus': str(float(cpu_limit) / 2),
                            'memory': str(int(memory_limit.replace('G', '')) // 2) + 'G'
                        }
                    }
                }
            }
        }
    }

    # Add GPU configuration if enabled
    if gpu_enabled:
        compose_config['services'][service_name]['deploy']['resources']['reservations']['devices'] = [{
            'driver': 'nvidia',
            'count': 'all',
            'capabilities': ['gpu', 'compute', 'utility']
        }]
        compose_config['services'][service_name]['environment'] = [
            'NVIDIA_VISIBLE_DEVICES=all',
            'NVIDIA_DRIVER_CAPABILITIES=compute,utility'
        ]

    return yaml.dump(compose_config, default_flow_style=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Generate Docker Compose config for AI services with resource constraints')
    parser.add_argument('--service-name', default='ai-service', help='Name of the service')
    parser.add_argument('--memory-limit', default='8G', help='Memory limit (e.g., 4G, 8G)')
    parser.add_argument('--cpu-limit', default='4.0', help='CPU limit (e.g., 2.0, 4.0)')
    parser.add_argument('--enable-gpu', action='store_true', help='Enable GPU support')
    parser.add_argument('--output', default='docker-compose-ai.yml', help='Output filename')

    args = parser.parse_args()

    compose_content = generate_ai_compose_config(
        args.service_name,
        args.memory_limit,
        args.cpu_limit,
        args.enable_gpu
    )

    with open(args.output, 'w') as f:
        f.write(compose_content)

    print(f"Docker Compose AI config generated successfully: {args.output}")
    print(f"Service: {args.service_name}, Memory: {args.memory_limit}, CPU: {args.cpu_limit}")
    if args.enable_gpu:
        print("GPU support enabled")

if __name__ == "__main__":
    main()
