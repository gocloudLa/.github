#!/usr/bin/env python3
"""
Example README Generator
Generates README.md files for examples directories using YAML data and templates.
"""

import yaml
import argparse
import os
import sys
from jinja2 import Template

def load_yaml_data(yaml_file):
    """Load data from YAML file"""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML file {yaml_file}: {e}")
        return None

def load_template(template_file):
    """Load Jinja2 template"""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            return Template(f.read())
    except Exception as e:
        print(f"Error loading template file {template_file}: {e}")
        return None

def generate_examples_readme(yaml_file, template_file, output_file):
    """Generate README.md for examples directory"""
    
    # Load YAML data
    data = load_yaml_data(yaml_file)
    if not data:
        return False
    
    # Load template
    template = load_template(template_file)
    if not template:
        return False
    
    # Validate required fields
    required_fields = ['title', 'description', 'main_purpose', 'key_features']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        print(f"Error: Missing required fields in YAML: {missing_fields}")
        return False
    
    # Ensure key_features is a list
    if not isinstance(data.get('key_features', []), list):
        print("Error: key_features must be a list")
        return False
    
    # Ensure services_used is a list (optional)
    if 'services_used' in data and not isinstance(data['services_used'], list):
        print("Error: services_used must be a list")
        return False
    
    # Render template
    try:
        readme_content = template.render(**data)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return False
    
    # Write output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ Examples README generated: {output_file}")
        return True
    except Exception as e:
        print(f"Error writing output file {output_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate README.md for examples directories")
    parser.add_argument('--yaml', required=True, help='YAML file with examples data')
    parser.add_argument('--template', required=True, help='Jinja2 template file')
    parser.add_argument('--output', required=True, help='Output README.md file')
    
    args = parser.parse_args()
    
    # Validate input files exist
    if not os.path.exists(args.yaml):
        print(f"Error: YAML file not found: {args.yaml}")
        sys.exit(1)
    
    if not os.path.exists(args.template):
        print(f"Error: Template file not found: {args.template}")
        sys.exit(1)
    
    # Generate README
    success = generate_examples_readme(args.yaml, args.template, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 