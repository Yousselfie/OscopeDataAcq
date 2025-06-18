# plc_symbolic_executor.py

from z3 import *
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import json
import csv
import serial.tools.list_ports
import time



# ---------------------- Structured Text to Python Translator ----------------------
def translate_st_to_python(st_code: str) -> str:
    lines = st_code.strip().splitlines()
    python_lines = []
    indent_level = 0

    def indent():
        return "    " * indent_level

    for line in lines:
        line = line.strip().rstrip(";")
        if not line or line.startswith("(*"):
            continue

        if line.startswith("IF") and "THEN" in line:
            cond = line[2:line.index("THEN")].strip()
            python_lines.append(f"{indent()}if {translate_condition(cond)}:")
            indent_level += 1
        elif line.startswith("ELSIF"):
            cond = line[5:line.index("THEN")].strip()
            indent_level -= 1
            python_lines.append(f"{indent()}elif {translate_condition(cond)}:")
            indent_level += 1
        elif line.startswith("ELSE"):
            indent_level -= 1
            python_lines.append(f"{indent()}else:")
            indent_level += 1
        elif line.startswith("END_IF"):
            indent_level -= 1
        elif ":=" in line:
            lhs, rhs = [x.strip() for x in line.split(":=")]
            python_lines.append(f"{indent()}{lhs.lower()} = {translate_rhs(rhs)}")
        else:
            python_lines.append(f"{indent()}{line.lower()}")

    return "\n".join(python_lines)

def translate_condition(cond: str) -> str:
    return cond.replace("=", "==").replace("<>", "!=")

def translate_rhs(rhs: str) -> str:
    val = rhs.lower()
    if val == "true":
        return "True"
    elif val == "false":
        return "False"
    return val

# ---------------------- Symbolic Model ----------------------
def traffic_timer_symbolic():
    IN = [Bool(f'IN{i}') for i in range(8)]
    TimerElapsed = [Bool(f'Timer{i}_Elapsed') for i in range(5)]
    Q = [Bool(f'Q{i}') for i in range(8)]
    s = Solver()
    s.add(If(IN[0], Q[0] == TimerElapsed[0], Q[0] == False))
    s.add(If(IN[1], Q[1] == TimerElapsed[1], Q[1] == False))
    s.add(If(IN[2], Q[2] == TimerElapsed[2], Q[2] == False))
    s.add(Q[3] == IN[3])
    s.add(If(IN[4], Q[4] == TimerElapsed[3], Q[4] == False))
    s.add(Q[5] == IN[5])
    s.add(If(IN[6], Q[6] == TimerElapsed[4], Q[6] == False))
    s.add(Q[7] == IN[7])
    return s, IN, Q, TimerElapsed

# ---------------------- Full Path Enumeration ----------------------
def enumerate_all_paths(max_paths=None):
    s, IN, Q, TimerElapsed = traffic_timer_symbolic()
    results = []

    for in_vals in itertools.product([True, False], repeat=8):
        for timer_vals in itertools.product([True, False], repeat=5):
            s.push()
            for i in range(8):
                s.add(IN[i] == in_vals[i])
            for t in range(5):
                s.add(TimerElapsed[t] == timer_vals[t])

            if s.check() == sat:
                m = s.model()
                result = {
                    "inputs": {f"IN{i}": in_vals[i] for i in range(8)},
                    "outputs": {f"Q{i}": is_true(m.evaluate(Q[i], model_completion=True)) for i in range(8)},
                    "timers": {f"Timer{i}_Elapsed": timer_vals[i] for i in range(5)}
                }
                results.append(result)
            s.pop()

            if max_paths is not None and len(results) >= max_paths:
                return results

    return results

# ---------------------- Visualizer for Symbolic I/O ----------------------
def visualize_io_tree(results):
    G = nx.DiGraph()
    for idx, r in enumerate(results):
        label = f"Case {idx}"\
              + "\nIN: " + str([int(r['inputs'][f"IN{i}"]) for i in range(8)])\
              + "\nQ:  " + str([int(r['outputs'][f"Q{i}"]) for i in range(8)])
        G.add_node(label)
        if idx > 0:
            G.add_edge(f"Case {idx-1}\n...", label)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=8)
    plt.title("Symbolic I/O Execution Tree")
    plt.show()

# ---------------------- EM Trace Integration ----------------------
def integrate_em_traces(results, em_trace_dict):
    for case in results:
        for i in range(5):
            em_value = em_trace_dict.get(f"Timer{i}_Elapsed", None)
            if em_value is not None:
                case["timers"][f"Timer{i}_Elapsed"] = em_value
    return results

# ---------------------- Output to CSV/JSON ----------------------
def write_to_json(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

def write_to_csv(results, filename):
    keys = list(results[0]['inputs'].keys()) + list(results[0]['timers'].keys()) + list(results[0]['outputs'].keys())
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in results:
            combined = {**row['inputs'], **row['timers'], **row['outputs']}
            writer.writerow(combined)

# ---------------------- Main Execution ----------------------
if __name__ == "__main__":
    paths = enumerate_all_paths(max_paths=100)  # Set to None for full space

    em_trace = {
        "Timer0_Elapsed": True,
        "Timer1_Elapsed": True,
        "Timer2_Elapsed": False,
        "Timer3_Elapsed": True,
        "Timer4_Elapsed": False
    }

    enriched_paths = integrate_em_traces(paths, em_trace)

    #----------------------- Establishing Serial Connection to Arduino -----------------
    serialInstance = serial.Serial()
    serialInstance.baudrate = 9600
    serialInstance.port = "COM4"
    serialInstance.open()
    time.sleep(2)

        

    # visualize_io_tree(enriched_paths)
    # write_to_json(enriched_paths, "symbolic_io_paths.json")
    # write_to_csv(enriched_paths, "symbolic_io_paths.csv")

    while True:
        counter = 1
        for p in enriched_paths:
            serialInstance.write((str(counter)+"\n").encode('utf-8'))
            serialInstance.write(("--- Symbolic Execution Path ---\n").encode('utf-8'))
            serialInstance.write(f"Inputs: {p['inputs']}\n".encode('utf-8'))
            serialInstance.write(f"Outputs: {p['outputs']}\n".encode('utf-8'))
            serialInstance.write(f"Timers: {p['timers']}\n".encode('utf-8'))
            serialInstance.flush()
            counter+=1
            time.sleep(5)  # Give Arduino time to process and respond


            # Read back Arduino's response (optional)
            print("Arduino:")
            while serialInstance.in_waiting > 0:
                print("\t", serialInstance.readline().decode('utf-8').strip())
            