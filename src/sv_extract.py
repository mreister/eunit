from vhdl_proc_lib import * 
import sys
import pyperclip




# Example usage
if __name__ == "__main__":
    file_path = sys.argv[1]
    python_script = sys.argv[0]
    print(python_script)
    #vhdl_file_path = "hdl/many_ports.vhd"  # Replace with the path to your VHDL file
    vhdl_file_path = file_path
    port_data_json = extract_sv_ports(vhdl_file_path)

    # i need to replace module_name with entity name for port_data_json
    json_data = json.dumps({("entity_name" if k == "module_name" else k): v for k, v in json.loads(port_data_json).items()})
    #print(json_data)

    vhdl_code = generate_vhdl_instantiation(json_data)
    pyperclip.copy(vhdl_code)
    #print(port_data_json)