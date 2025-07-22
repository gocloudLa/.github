import yaml
import json
import argparse
from jinja2 import Template

parser = argparse.ArgumentParser(description="Genera README.md a partir de templates y datos YAML/JSON.")
parser.add_argument('--yaml', default='.readme/README.yaml')
parser.add_argument('--template', default='.readme-generic/README.md.gotmpl')
parser.add_argument('--external_modules', default='.readme/external_modules.json')
parser.add_argument('--output', default='README.md')
args = parser.parse_args()

# --- FUNCION PARA GENERAR TABLA MARKDOWN ALINEADA ---
def prettify_markdown_table(rows, header):
    # rows: lista de listas (cada fila)
    # header: lista de strings
    all_rows = [header] + rows
    col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(header))]
    def fmt_row(row):
        return '| ' + ' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + ' |'
    sep = '| ' + ' | '.join('-' * col_widths[i] for i in range(len(header))) + ' |'
    return '\n'.join([
        fmt_row(header),
        sep,
        *(fmt_row(row) for row in rows)
    ])

# Cargar datos específicos
data = {}
with open(args.yaml) as f:
    data = yaml.safe_load(f)

# Cargar external_modules desde JSON externo
try:
    with open(args.external_modules) as f:
        data['external_modules'] = json.load(f)
except FileNotFoundError:
    data['external_modules'] = []

# --- GENERAR TABLA DE VARIABLES ALINEADA ---
header = ["Name", "Description", "Type", "Default", "Required"]
rows = []
if 'inputs_plain' in data and data['inputs_plain']:
    # Parsear las filas plain (asume formato markdown sin header)
    for line in data['inputs_plain'].splitlines():
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            parts = [cell.strip() for cell in line[1:-1].split('|')]
            if len(parts) == len(header):
                rows.append(parts)
if 'inputs_yaml' in data and data['inputs_yaml']:
    for var in data['inputs_yaml']:
        rows.append([
            var.get('name', ''),
            var.get('description', ''),
            var.get('type', ''),
            str(var.get('default', '')),
            str(var.get('required', ''))
        ])
if rows:
    data['inputs_table_pretty'] = prettify_markdown_table(rows, header)
else:
    data['inputs_table_pretty'] = ''

# Leer template
with open(args.template) as f:
    template_content = f.read()

# Renderizar
template = Template(template_content)
readme = template.render(**data)

# Guardar README.md
with open(args.output, 'w') as f:
    f.write(readme) 