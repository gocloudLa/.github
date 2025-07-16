import yaml
import json
import argparse
from jinja2 import Template

parser = argparse.ArgumentParser(description="Genera README.md a partir de templates y datos YAML/JSON.")
parser.add_argument('--yaml', default='.readme/README.yaml')
parser.add_argument('--general', default='.readme-generic/README.general.yaml')
parser.add_argument('--template', default='.readme-generic/README.md.gotmpl')
parser.add_argument('--external', default='.readme/external_modules.json')
parser.add_argument('--output', default='README.md')
args = parser.parse_args()

# Cargar datos específicos
data = {}
with open(args.yaml) as f:
    data = yaml.safe_load(f)

# Cargar datos generales
with open(args.general) as f:
    general = yaml.safe_load(f)

data.update(general)

# Cargar external_modules desde JSON externo
try:
    with open(args.external) as f:
        data['external_modules'] = json.load(f)
except FileNotFoundError:
    data['external_modules'] = []

# Leer template
with open(args.template) as f:
    template_content = f.read()

# Renderizar
template = Template(template_content)
readme = template.render(**data)

# Guardar README.md
with open(args.output, 'w') as f:
    f.write(readme) 