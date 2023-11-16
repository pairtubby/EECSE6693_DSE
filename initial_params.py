"""
Author: Pair Phongphaew
Date: Nov 16, 2023
"""
import re
import argparse

def extract_clk_params_from_tcl(file_path):
    clk_params = {}

    # Read the Tcl file content
    with open(file_path, 'r') as tcl_file:
        tcl_content = tcl_file.read()

    # Use regular expressions to find the assignment of $clk_period and $clk_name
    clk_period_match = re.search(r'set\s+clk_period\s+(\d+)', tcl_content)
    clk_name_match = re.search(r'set\s+clk_name\s+"([^"]+)"', tcl_content)

    if clk_period_match:
        clk_params['clk_period'] = clk_period_match.group(1)
    if clk_name_match:
        clk_params['clk_name'] = clk_name_match.group(1)

    return clk_params
def get_SDC_params(tcl_file_path,sdc_file_path):
    clk_params = extract_clk_params_from_tcl(tcl_file_path)
    input_delay_params = {'input_delay_max': None, 'input_delay_min': None}
    output_delay_params = {'output_delay_max':None,'output_delay_min':None}	
    # Read the SDC file content
    with open(sdc_file_path, 'r') as sdc_file:
        sdc_content = sdc_file.read()

    # Use regular expressions to find the values of set_input_delay -max and -min
    max_input_delay_match = re.search(r'set_input_delay\s+-max\s+-clock\s+\[get_clocks\s+\$clk_name\]\s+\[expr\s+(\S+)\s*\*\s*\$clk_period\]', sdc_content)
    min_input_delay_match = re.search(r'set_input_delay\s+-min\s+-clock\s+\[get_clocks\s+\$clk_name\]\s+\[expr\s+(\S+)\s*\*\s*\$clk_period\]', sdc_content)
    max_output_delay_match = re.search(r'set_output_delay\s+-max\s+-clock\s+\[get_clocks\s+\$clk_name\]\s+\[expr\s+(\S+)\s*\*\s*\$clk_period\]', sdc_content)
    min_output_delay_match = re.search(r'set_input_delay\s+-min\s+-clock\s+\[get_clocks\s+\$clk_name\]\s+\[expr\s+(\S+)\s*\*\s*\$clk_period\]', sdc_content)
    #TO DO Uncertainty to give to clocks#
    ####################################
    if max_input_delay_match:
        numerical_value = max_input_delay_match.group(1)
        input_delay_params['input_delay_max'] = float(float(numerical_value) * float(clk_params['clk_period']))
    if min_input_delay_match:
        numerical_value = min_input_delay_match.group(1)
        input_delay_params['input_delay_min'] = float(float(numerical_value) * float(clk_params['clk_period']))
    if max_output_delay_match:
        numerical_value = max_output_delay_match.group(1)
        output_delay_params['output_delay_max'] = float(float(numerical_value) * float(clk_params['clk_period']))
    if min_output_delay_match:
        numerical_value = min_output_delay_match.group(1)
        output_delay_params['output_delay_min'] = float(float(numerical_value) * float(clk_params['clk_period']))


    return input_delay_params, output_delay_params
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Extract $clk_period and $clk_name from a Tcl file.')
    parser.add_argument('tcl_file', help='Path to the Tcl file containing $clk_period and $clk_name')
    parser.add_argument('sdc_file', help='Path to the SDC file')

    # Parse command-line arguments
    args = parser.parse_args()

    # Extract $clk_period and $clk_name from the specified Tcl file
    clk_parameters = extract_clk_params_from_tcl(args.tcl_file)

    # Print the extracted parameters
    print("Extracted Parameters:")
    print(clk_parameters)
    
    sdc_params = get_SDC_params(args.tcl_file,args.sdc_file)
    print(sdc_params)

if __name__ == "__main__":
    main()


