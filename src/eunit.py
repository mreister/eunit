import click
import os 

def get_mod_name(file_path):
	# Extract the base name 'file.txt' from '/path/to/file.txt')
	base_name = os.path. basename(file_path)
	# Remove the file extension
	file_name_without_ext = os.path.splitext (base_name)[0] 
	return file_name_without_ext


def stim_create(mod_name, input_stim_file="string", output_type="logic[63:0]", libraries="p3_common"):
	mod_string ='''
/************************************************
MR:
**********************************************/
//import 13:*；
	
module {0}_stim # (
	parameter INPUT_FILE
)
	input {1} stim_file_i, 
	input clk_i, 
	input rst_i,
	// output
	output {2} data_o
);

// Custom stim logic goes here.
endmodule'''.format(mod_name, input_stim_file, output_type, libraries)
	return mod_string


def check_create(mod_name, input_type="logic[63:0]", output_file="string", libraries="p3_common"):
	mod_string = '''
/************************************************
MR:
************************************************/
//import {3}::*；

module {0}_check #(
	parameter OUTPUT_FILE 
)(
	Input {1} data_i, 
	input clk i, 
	input rst_i,
	// output
	output {2} output_file
);

// Custom checker logic goes here.
endmodule
'''.format(mod_name, input_type, output_file, libraries)
	return mod_string


def dut_create(mod_name, input_type="logic[63:0]", output_type="logic [63:0]", libraries="p3_common"):
	mod_string = '''
/***********************************************
MR:_~"~..~"~.
************************************************
//import {3}::*；

module {0}_dut (
	// inputs
	input {1} data_i, 
	input clk_i, 
	input rst_1,
	// outputs
	output {2} data_o
);

endmodule'''.format(mod_name, input_type, output_type, libraries)
	return mod_string


def dut_vhd_create(mod_name, input_type="std_logic_vector(63 downto 0)",output_type="std_logic_vector(63 downto 0)", libraries="p3_common"):
	mod_string ='''
library ieee; 
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity {0}_dut is port (
	-- inputs 
	data i ： in {1}; 
	clk_i ： in std_logic;
	rst_i ： in std_logic;

	-- outputs 
	data_o : out {2};
	data_valid : out std_logic
);
end entity; -- {0}_dut

architecture arch of {0}_dut is

begin 

end architecture ; -- arch'''.format(mod_name, input_type, output_type, libraries)
	return mod_string



def tb_create(mod_name, input_type="logic[63:0]" ,output_type="logic[63:0]",input_stim_file="input. txt",output_file="output.txt", libraries="p3_common"):
	mod_string ='''
/************************************************
MR:
*************************************************
module {0}_stim # (
parameter INPUT_FILE="" 
parameter OUTPUT_FILE=""
);

real CLOCK_PERIOD_C = 10.0;
real RESET_PERIOD_C = 50.0;
logic clk sig ='b1;
logic rst_sig = 'b1;
always clk_sig = #(CLOCK_ PERIOD_C/2) ~clk_sig;
always rst_sig = #RESET_PERIOD_C 1'b0;
logic[63:0] stim_data_sig; logic[63:0] dut_data_sig;

/***************************************
Stim
****************************************/
{0}_stim
#(
	.INPUT_FILE(INPUT_FILE)
) stim_inst (
	.clk_i (clk_sig),
	.rst_i (rst_sig),
	.data_o(stim_data_sig)
);

/****************************************
DUT
****************************************/
{0}_dut {0}_dut_inst (
	.data_i(stim_data_sig),
	.clk_i (clk_sig),
	.rst_i (rst_sig),
	.data_o(dut_data_sig)
);

/************************************
Checker
*************************************
{0}_check
#(
	.OUTPUT_FILE (OUTPUT_FILE)
){0}_check inst (
	.data_i(dut_data_sig),
	.clk_i (clk _sig),
	.rst_i (rst_sig)
)

endmodule'''.format(mod_name, input_type, output_type, input_stim_file, output_file, libraries)
	return mod_string



def compilation_create(mod_name,vhd=1):
	mod_string ='''
	vlog -sv {0}_stim. sv
	vlog -sv {0}_dut. sv -L temporal_ p
	vlog -sv {0}_check.sv -L temporal_p
	vlog -sv {0}_tb.sv -L temporal_p
	vsim {0}_sim - voptargs="+acc"
	do wave.do
	run
	50000
	'''.format(mod_name)

	hd_mod_string = '''
vlog -sv f{0}_stim.sv
vcom - 2008 {0}_dut. vhd
vlog -sv {0}_check.sv -L temporal_ p vlog -sv {0}_tb.sv -L temporal_p
vsim {0}_sim -voptargs="+acc"
do wave. do run 50000
'''.format(mod_name)

	if vhd == 1:
		return hd_mod_string 
	else:
		return mod_string

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--vhd', default=1, help='Start frame of the video')
#@click.option('--ldps_only', default=0, help='Process image with 1dps only')
def eunit (input, vhd):
	# parse file name to get module name... assume they are the same for the moment.
	# input
	mod_name = get_mod_name(input)
	os.mkdir(mod_name + "_eunit")
	# create file stings
	stim_file_s = stim_create(mod_name)
	check_file_s = check_create(mod_name)
	dut_file_s = dut_create(mod_name)

	vhd_dut_file_s = dut_vhd_create(mod_name)
	tb_file = tb_create(mod_name)

	comp_file = compilation_create(mod_name)

	# create files
	with open('{0}_eunit/{0}_stim.sv'.format(mod_name), 'w') as f:
		f.write(stim_file_s)

	with open('{0}_eunit/{0}_check.sv'.format(mod_name), 'w') as f:
		f.write(check_file_s)

	if vhd == 1:
		with open('{0}_eunit/{0}_dut.vhd'.format(mod_name), 'w') as f:
			f.write(vhd_dut_file_s)
	else:
		with open('{0}_eunit/{0}_dut.sv'.format(mod_name), 'w') as f:
			f.write(dut_file_s)

	with open ('{0}_eunit/{0}_tb.sv'. format (mod_name), 'w') as f:
		f.write(tb_file)

	with open ('{0}_eunit/compile_{0}.do'. format (mod_name), 'w') as f:
		f.write(comp_file)

if __name__ == '__main__':
	eunit()


