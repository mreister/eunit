import json

def generate_vhdl_instantiation(json_data, instance_name="identifier_inst"):
    # Parse the JSON data
    data = json.loads(json_data)

    # Extract entity name and ports
    entity_name = data.get("entity_name", "Unnamed_Entity")
    ports = data.get("ports", [])

    # Generate VHDL instantiation
    instantiation_lines = []
    instantiation_lines.append(f"{instance_name} : entity work.{entity_name}")
    instantiation_lines.append("port map (")

    port_mappings = []
    for port in ports:
        port_name = port["name"]
        port_mappings.append(f"    {port_name} => {port_name}")

    # Join ports with commas and add to instantiation
    instantiation_lines.append(",\n".join(port_mappings))
    instantiation_lines.append(");")

    # Combine all lines into a single string
    vhdl_instantiation = "\n".join(instantiation_lines)

    return vhdl_instantiation

# Example usage
if __name__ == "__main__":
    json_output = """
    {
        "entity_name": "example_entity",
        "ports": [
            {"name": "clk_i", "direction": "in", "data_type": "std_logic"},
            {"name": "rst_i", "direction": "in", "data_type": "std_logic"},
            {"name": "data_o", "direction": "out", "data_type": "std_logic_vector(7 downto 0)"},
            {"name": "data_valid_o", "direction": "out", "data_type": "std_logic"}
        ]
    }
    """
    vhdl_code = generate_vhdl_instantiation(json_output)
    print(vhdl_code)
