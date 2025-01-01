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

    port_data_generics_json = extract_vhdl_generics_and_ports(vhdl_file_path)

    print(port_data_generics_json)

    port_data_json = extract_vhdl_ports(vhdl_file_path)
    vhdl_code = generate_vhdl_instantiation(port_data_generics_json)
    print(vhdl_code)
    pyperclip.copy(vhdl_code)
    #print(vhdl_code)