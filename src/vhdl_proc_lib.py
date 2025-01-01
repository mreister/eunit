import re

#from hdl import *


import json

def generate_vhdl_instantiation(json_data, instance_name="identifier_inst"):
    # Parse the JSON data
    data = json.loads(json_data)

    # Extract entity name and ports
    entity_name = data.get("entity_name", "Unnamed_Entity")
    ports = data.get("ports", [])

    # Generate VHDL instantiation
    instantiation_lines = []
    instantiation_lines.append(f"{entity_name}_inst : entity work.{entity_name}")
    instantiation_lines.append("port map (")

    port_mappings = []
    for port in ports:
        port_name = port["name"]
        port_type = port["data_type"]
        port_mappings.append(f"     {port_name} => {port_name} -- {port_type}")

    # Join ports with commas and add to instantiation
    instantiation_lines.append(",\n".join(port_mappings))
    instantiation_lines.append(");\n")

    # Combine all lines into a single string
    vhdl_instantiation = "\n".join(instantiation_lines)

    return vhdl_instantiation


def extract_vhdl_ports(vhdl_file_path):
    # Read the VHDL file
    with open(vhdl_file_path, 'r') as file:
        vhdl_content = file.read()

    # Regex to extract entity section with optional entity name
    entity_pattern = r"entity\s*(\w*)\s*is.*?port\s*\((.*?)\);"  # Modified to handle missing entity names
    entity_match = re.search(entity_pattern, vhdl_content, re.DOTALL | re.IGNORECASE)

    if not entity_match:
        return json.dumps({"error": "No entity found in the VHDL file."})

    entity_name = entity_match.group(1).strip() if entity_match.group(1).strip() else "Unnamed_Entity"
    port_content = entity_match.group(2)

    # Regex to extract port names, directions, and data types
    port_pattern = r"(\w+)\s*:\s*(in|out)\s+([^;]+);?"
    ports = re.findall(port_pattern, port_content, re.IGNORECASE)

    # Prepare JSON output
    port_info = []
    for name, direction, data_type in ports:
        port_info.append({
            "name": name.strip(),
            "direction": direction.strip().lower(),
            "data_type": data_type.strip()
        })

    result = {
        "entity_name": entity_name,
        "ports": port_info
    }

    return json.dumps(result, indent=4)

def extract_sv_ports(sv_file_path):
    # Read the SystemVerilog file
    with open(sv_file_path, 'r') as file:
        sv_content = file.read()

    # Regex to extract module section with optional ports
    module_pattern = r"module\s+(\w+)\s*\((.*?)\);"  # Captures module name and ports block
    module_match = re.search(module_pattern, sv_content, re.DOTALL | re.IGNORECASE)

    if not module_match:
        return json.dumps({"error": "No module found in the SystemVerilog file."})

    module_name = module_match.group(1).strip()
    port_content = module_match.group(2)

    # Regex to extract port names, directions, and data types
    port_pattern = r"(input|output|inout)\s+(logic|wire|reg|\[.*?\])?\s*(\w+)"  # Handles types and names
    ports = re.findall(port_pattern, port_content, re.IGNORECASE)

    # Prepare JSON output
    port_info = []
    for direction, data_type, name in ports:
        # Normalize data type (handle cases where it might be empty)
        data_type = data_type.strip() if data_type else "logic"
        port_info.append({
            "name": name.strip(),
            "direction": direction.strip().lower(),
            "data_type": data_type
        })

    result = {
        "module_name": module_name,
        "ports": port_info
    }

    return json.dumps(result, indent=4)
