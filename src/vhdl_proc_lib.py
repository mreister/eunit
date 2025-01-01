import re

#from hdl import *


import json

def generate_vhdl_instantiation(json_data, instance_name="identifier_inst"):
    # Parse the JSON data
    data = json.loads(json_data)

    # Extract entity name, generics, and ports
    entity_name = data.get("entity_name", "Unnamed_Entity")
    generics = data.get("generics", [])
    ports = data.get("ports", [])

    # Generate VHDL instantiation
    instantiation_lines = []
    instantiation_lines.append(f"{entity_name}_inst : entity work.{entity_name}")

    # Add generics if present
    if generics:
        instantiation_lines.append("generic map (")
        generic_mappings = []
        for generic in generics:
            generic_name = generic["name"]
            generic_mappings.append(f"    {generic_name} => {generic_name}")
        instantiation_lines.append(",\n".join(generic_mappings))
        instantiation_lines.append(")")

    # Add ports
    instantiation_lines.append("port map (")
    port_mappings = []
    for port in ports:
        port_name = port["name"]
        port_type = port["data_type"]
        port_mappings.append(f"    {port_name} => {port_name} -- {port_type}")
    instantiation_lines.append(",\n".join(port_mappings))
    instantiation_lines.append(");")

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

def extract_vhdl_generics_and_ports(vhdl_file_path):
    # Read the VHDL file
    with open(vhdl_file_path, 'r') as file:
        vhdl_content = file.read()

    # Regex to extract entity section
    entity_pattern = r"entity\s+(\w+)\s+is.*?generic\s*\((.*?)\);.*?port\s*\((.*?)\);"  # Capture entity, generics, and ports
    entity_match = re.search(entity_pattern, vhdl_content, re.DOTALL | re.IGNORECASE)

    if not entity_match:
        return json.dumps({"error": "No entity found in the VHDL file."})

    entity_name = entity_match.group(1).strip()
    generic_content = entity_match.group(2)
    port_content = entity_match.group(3)

    # Regex to extract generic names and types
    generic_pattern = r"(\w+)\s*:\s*([^;]+);?"
    generics = re.findall(generic_pattern, generic_content, re.IGNORECASE)

    # Regex to extract port names, directions, and data types
    port_pattern = r"(\w+)\s*:\s*(in|out)\s+([^;]+);?"
    ports = re.findall(port_pattern, port_content, re.IGNORECASE)

    # Prepare JSON output
    generic_info = []
    for name, data_type in generics:
        generic_info.append({
            "name": name.strip(),
            "data_type": data_type.strip()
        })

    port_info = []
    for name, direction, data_type in ports:
        port_info.append({
            "name": name.strip(),
            "direction": direction.strip().lower(),
            "data_type": data_type.strip()
        })

    result = {
        "entity_name": entity_name,
        "generics": generic_info,
        "ports": port_info
    }

    return json.dumps(result, indent=4)

def extract_sv_ports(sv_file_path):
    # Read the SystemVerilog file
    with open(sv_file_path, 'r') as file:
        sv_content = file.read()

    # Regex to extract module and parameter section
    module_pattern = r"module\s+(\w+)\s*(#\s*\((.*?)\))?\s*\((.*?)\);"  # Captures module name, parameters, and ports
    module_match = re.search(module_pattern, sv_content, re.DOTALL | re.IGNORECASE)

    if not module_match:
        return json.dumps({"error": "No module found in the SystemVerilog file."})

    module_name = module_match.group(1).strip()
    parameter_content = module_match.group(3) if module_match.group(3) else ""
    port_content = module_match.group(4)

    # Regex to extract parameters
    parameter_pattern = r"parameter\s+(\w+)\s*=\s*([^,\n]+)"
    parameters = re.findall(parameter_pattern, parameter_content, re.IGNORECASE)

    # Regex to extract port names, directions, and data types
    port_pattern = r"(input|output|inout)\s+(logic|wire|reg|\[.*?\])?\s*(\w+)"  # Handles types and names
    ports = re.findall(port_pattern, port_content, re.IGNORECASE)

    # Prepare JSON output
    parameter_info = []
    for name, default_value in parameters:
        parameter_info.append({
            "name": name.strip(),
            "default_value": default_value.strip()
        })

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
        "parameters": parameter_info,
        "ports": port_info
    }

    return json.dumps(result, indent=4)
