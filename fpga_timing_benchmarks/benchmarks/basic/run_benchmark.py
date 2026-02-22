import os
import subprocess
import re
import csv
import sys
import argparse
import random
from pathlib import Path
from string import Template
from subprocess import Popen, PIPE, TimeoutExpired
from typing import List
# from fpga_timing_benchmarks.benchmarks.basic import BasicBenchmark
# from fpga_timing_benchmarks.benchmarks.benchmark import NetlistType
from config import RESULTS_DIR, MICRO_ROOT, CIRCUITS_DIR, OUTPUT_DIR, ARCH_FILE, PARSE_FILE_PATH, TEST_DICT, VTR_ROOT

sys.path.insert(0, str(VTR_ROOT / 'vtr_flow/scripts/python_libs'))
import vtr

# 0. Maintain a .txt file that has a list of circuits(constraints) to test - DONE (maintains a config.py file instead)
# 1. Run the circuits through VTR without the constraints
# 2. Parse the VPR and STA results (CPD, wirelength, slack, hold/setup, PnR)
# 3. Run the circuits again through VTR with the constraints
# 4. Parse the VPR and STA results and compare with the unconstrained results

'''
Metrics
VTR
-With SDC vs Without SDC
-CPD, wirelength, slack, hold/setup, PnR result
-But, metrics differ for each constraint

OpenSTA
-Collect CPD, wirelength, slack, hold/setup

Files to look at:
temp/report_timing.hold.rpt
temp/report_timing.setup.rpt
'''

# For constraints like set_input_delay, run the VTR flow multiple times to see how PnR changes. 

# Should I make this in CLI? 

# python run_benchmark.py --<SDC_name> --<blif> vs <verilog> --<architecture> -- 

######## FUNCTION DEFINITIONS ########

def construct_sdc(constraint_config):
    '''
    Constructs multiple SDCs with different parameters and returns a list of generated SDC file names.
    
    Args: 
      constraint_config: Constraint Configuration
      out_dir: Directory the SDC will be saved in
    
    Returns:
      A list containing the paths to the generated SDCs
    '''
    # List contains generated sdc file names
    generated_sdc_list = []
    
    for test in constraint_config:
        # Create out_dir (e.g. ./results/create_clock_rca/sdc)
        out_dir = RESULTS_DIR / test['type'] / 'sdc'
        os.makedirs(out_dir, exist_ok=True)
        
        # Arguments
        sdc_template = test['sdc'] # SDC template
        params = test['param'] # Parameters
        
        # SDC does not require edits, We can use the SDC template
        if params is None: 
            out_filename = test['type'] + '.sdc'
            out_filepath = os.path.join(out_dir, out_filename)
            
            with open(out_filepath, 'w') as out_sdc:
                out_sdc.write(sdc_template)
            
            generated_sdc_list.append(out_filepath)
            print(f"Generated SDC: {out_filepath}")
        
        else: 
            # Save default value for all params
            defaults = {p['name']: p['default'] for p in params} 
            
            # Iterate over all params
            for param in params:
                param_name = param['name']
                
                # Iterate over all values of each param
                for val in param['values']:
                    current_values = defaults.copy() # Copy the default values to 'current_values'
                    current_values[param_name] = val # Substitute default value of current param
                    
                    new_constraint = sdc_template # Copy sdc template
                    filename_parts = [] # List for file name generation
                    
                    # Substitute the parameters in the SDC with actual values
                    for p_name, p_val in current_values.items():
                        str_val = str(p_val)
                        new_constraint = new_constraint.replace(p_name, str_val)
                        
                        # Remove '<>' from filename_parts 
                        clean_name = p_name.strip('<>') 
                        filename_parts.append(f"{clean_name}_{str_val}")
                    
                    # Create file name (e.g. period_10.0.sdc)
                    out_filename = "_".join(filename_parts) + ".sdc"
                    out_filepath = os.path.join(out_dir, out_filename)
                    
                    # Output the generated SDC
                    with open(out_filepath, 'w') as out_sdc:
                        out_sdc.write(new_constraint)
                    
                    # Save the out file path to a list
                    generated_sdc_list.append(out_filepath)    
                    print(f"Generated SDC: {out_filepath}")
                
    return generated_sdc_list 

# No need for synthesis. All SDCs are blif-specific. 
def run_synthesis(constraint_config):
    '''
    Synthesizes circuit described in Verilog using Parmys or Odin II.
    
    Args:
      test: constraint_config
    
    Returns:
      Path to created blif file
    '''
    blif_list = []
    
    for test in constraint_config:
        # Prepare arguments for parmys/odin
        architecture_path = ARCH_FILE
        verilog_path = MICRO_ROOT / test['circuit']
        frontend = test['frontend']
        output_path = RESULTS_DIR / 'blif' / f'{test['type']}.blif'
        temp_dir = RESULTS_DIR / 'blif' / 'temp'
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Commands to run synthesis
        cmd = []
        
        if frontend == 'parmys':
            cmd = [
                f'{VTR_ROOT}/vtr_flow/scripts/run_vtr_flow.py',
                f'{verilog_path}',
                f'{architecture_path}',
                '-starting_stage', 'parmys',
                '-ending_stage', 'parmys',
                '-temp_dir', f'{temp_dir}'
            ]
            print(f"Running Parmys to synthesize {test['circuit']}")
        
        elif frontend == 'odin':
            cmd = [
                f'{VTR_ROOT}/odin_ii/odin_ii',
                '-a', f'{architecture_path}',
                '-V', f'{verilog_path}',
                '-o', f'{output_path}'
            ]
            print(f"Running Odin II to synthesize {test['circuit']}")
            
        else:
            print("Unknown Synthesis Tool")
        try:
            result = subprocess.run(cmd, check=True, capture_output= True, text=True)
            print(f"Synthesis Complete: {output_path.name}")
            blif_list.append(output_path)
        except subprocess.CalledProcessError as e:
            print(f"Error during synthesis with {frontend}")
            print(f"Command: {e.cmd}")
            print(f"Exit Code: {e.returncode}")
            print(f"Stderr: {e.stderr}")
    
    return blif_list

def run_constrained_test(sdc_dir):
    '''
    
    '''
    run_vpr()

def run_unconstrained_test():
    '''
    
    '''

def run_vpr(constraint_config, sdc_list):
    '''
    
    Args:
      constraing_config:
      sdc_list: List of SDC files to test
    '''
    
    
    for test in constraint_config:
        # Prepare VPR arguments
        blif_file = MICRO_ROOT / test['blif']
        layout = test['layout']
        vpr_args = {'device': layout}
        
        if test['graphics'] == True:
            cmd = [
                f'{VTR_ROOT}/vtr_flow/scripts/run_vtr_flow.py',
                f'{verilog_path}',
                f'{architecture_path}',
                '-starting_stage', 'parmys',
                '-ending_stage', 'parmys',
                '-temp_dir', f'{temp_dir}'
            ]
        elif test['graphics'] == False:
            cmd = [
                f'{VTR_ROOT}/vtr_flow/scripts/run_vtr_flow.py',
                f'{verilog_path}',
                f'{architecture_path}',
                '-starting_stage', 'parmys',
                '-ending_stage', 'parmys',
                '-temp_dir', f'{temp_dir}'
            ]
            

def run_vpr_save_graphics(constraint_config):
    '''
    
    '''
    
if __name__ == "__main__":
    set_false_path_sdc = construct_sdc(TEST_DICT['set_false_path'])
    print(set_false_path_sdc)
    set_false_path_blif = run_synthesis(TEST_DICT['set_false_path'])
    print(set_false_path_blif)