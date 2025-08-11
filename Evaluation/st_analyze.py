import os
import json
import re

def read_file_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-16') as f:
            return f.readlines()
    except UnicodeError:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()

def filter_code_lines(lines):
    filtered = []
    for line in lines:
        l = line.strip()
        if not l:
            continue
        if l.startswith('//'):
            continue
        if set(l) <= set('-/ '):
            continue
        filtered.append(l)
    return filtered

def parse_vars(lines):
    inputs, outputs, timers = [], [], []
    current_section = None
    for line in lines:
        l = line.strip()
        if l.startswith('// Inputs'):
            current_section = 'inputs'
            continue
        elif l.startswith('// Outputs'):
            current_section = 'outputs'
            continue
        elif l.startswith('// Timers'):
            current_section = 'timers'
            continue
        elif l == 'END_VAR':
            current_section = None
            continue
        if current_section and ':' in l:
            var_name = l.split(':')[0].strip()
            if current_section == 'inputs':
                inputs.append(var_name)
            elif current_section == 'outputs':
                outputs.append(var_name)
            elif current_section == 'timers':
                timers.append(var_name)
    return inputs, outputs, timers

def parse_state_diagram(lines, inputs, outputs, timers):
    edges = []
    i = 0
    while i < len(lines):
        l = lines[i].strip()

        # Timer call
        if '(' in l and ':=' in l and any(t in l for t in timers):
            timer = l.split('(')[0].strip()
            inside = l.split('(')[1].split(')')[0]
            input_signal = None
            for part in inside.split(','):
                if ':=' in part:
                    key, val = part.split(':=', 1)
                    if key.strip() == 'IN':
                        input_signal = val.strip()
            if timer and input_signal:
                edges.append((input_signal, timer))
            i += 1
            continue

        # Assignment outside IF
        elif ':=' in l and not l.upper().startswith('IF'):
            left, right = l.split(':=', 1)
            left = left.strip()
            right = right.strip().rstrip(';')
            if '.' in right:
                src = right.split('.')[0]
                if src in timers or src in inputs:
                    edges.append((src, left))
            else:
                if right in inputs + outputs + timers:
                    edges.append((right, left))
            i += 1
            continue

        # Handle multi-line IF blocks
        elif l.upper().startswith('IF'):
            condition_lines = []
            while 'THEN' not in l.upper():
                condition_lines.append(l)
                i += 1
                if i >= len(lines):
                    break
                l = lines[i].strip()
            if i < len(lines):
                condition_lines.append(l)
            full_condition = ' '.join(condition_lines)
            m = re.search(r'IF (.+) THEN', full_condition, re.I)
            if not m:
                i += 1
                continue
            cond_str = m.group(1).strip()

            # Remove parentheses
            cond_str = cond_str.replace('(', ' ').replace(')', ' ')

            # Split by AND / OR
            cond_inputs = re.split(r'\s+AND\s+|\s+OR\s+', cond_str, flags=re.I)
            cond_inputs = [c.strip() for c in cond_inputs if c.strip() in inputs + outputs + timers]

            # Next non-empty line assumed assignment
            i += 1
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            if i < len(lines):
                assign_line = lines[i].strip()
                if ':=' in assign_line:
                    left, right = assign_line.split(':=', 1)
                    left = left.strip()
                    for inp in cond_inputs:
                        edges.append((inp, left))

            # Skip until END_IF
            while i < len(lines) and not lines[i].strip().upper().startswith('END_IF'):
                i += 1
            i += 1
            continue

        else:
            i += 1

    print(f"Found edges: {edges}")
    return edges

def enumerate_paths(edges, inputs, outputs):
    adj = {}
    for src, dst in edges:
        adj.setdefault(src, []).append(dst)
    paths = []

    def dfs(node, path):
        if node in outputs:
            paths.append(path + [node])
            return
        if node not in adj:
            return
        for nxt in adj[node]:
            if nxt in path:
                continue
            dfs(nxt, path + [node])

    for start in inputs:
        dfs(start, [])

    return paths

def analyze_file(filepath, output_root):
    print(f"\nAnalyzing {filepath}")
    lines = read_file_lines(filepath)
    code_lines = filter_code_lines(lines)
    inputs, outputs, timers = parse_vars(lines)
    loc = len(code_lines)
    branches = sum(1 for l in lines if 'IF ' in l.upper() or 'CASE ' in l.upper())
    edges = parse_state_diagram(code_lines, inputs, outputs, timers)
    paths = enumerate_paths(edges, inputs, outputs)

    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = os.path.join(output_root, base_name)
    os.makedirs(output_dir, exist_ok=True)

    summary = {
        "LOC": loc,
        "Inputs": len(inputs),
        "Outputs": len(outputs),
        "Timers": len(timers),
        "Branches": branches,
        "Edges": edges,
        "Paths": paths
    }
    json_path = os.path.join(output_dir, 'analysis.json')
    with open(json_path, 'w') as jf:
        json.dump(summary, jf, indent=2)

    dot_path = os.path.join(output_dir, 'state_diagram.dot')
    with open(dot_path, 'w') as df:
        df.write("digraph StateDiagram {\n")
        for src, dst in edges:
            df.write(f'  "{src}" -> "{dst}";\n')
        df.write("}\n")

def analyze_directory(input_directory):
    parent_dir = os.path.abspath(os.path.join(input_directory, os.pardir))
    output_root = os.path.join(parent_dir, "st_analysis_output")
    os.makedirs(output_root, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.st'):
            filepath = os.path.join(input_directory, filename)
            analyze_file(filepath, output_root)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python st_analyze.py <directory_path>")
    else:
        analyze_directory(sys.argv[1])
