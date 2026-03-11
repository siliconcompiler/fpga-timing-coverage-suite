from pathlib import Path
from config import RESULTS_DIR, SYNTAX_DIR, ARCH_FILE, VTR_ROOT
import config
import os
import subprocess
import csv
import re
import argparse

def run_syntax_suite(config):
    '''
    Run place and route on the given test case with VPR.
    VPR will generate post-implementation netlists and timing analysis files that can be analyzed later on. 
    
    Args:
        constraing_config (dict): Constraint test configuration (Defined in 'TEST_DICT').
        sdc (Path): Single SDC file to test.
        random_seed (bool): Determines whether or not to use random seed for placement.
      
    Returns:
        constraint_config (dict):
        temp_dir (Path): 
        place_file (Path):
        
    '''
    # Path definitions
    result_dir = RESULTS_DIR / config['type']
    sdc_dir = SYNTAX_DIR / 'sdc_files' / config['sdc_name']
    blif_file = SYNTAX_DIR / 'netlist_files' / config['blif']
    architecture_file = ARCH_FILE
    
    csv_path = result_dir / 'summary.csv'
    pass_path = result_dir / 'passed_test.txt'
    err_path = result_dir / 'error_log.txt'
    
    result_dir.mkdir(parents=True, exist_ok=True)
    
    assert os.path.exists(blif_file)
    assert os.path.exists(sdc_dir)
    
    # Search for SDCs and add the paths to a list
    sdc_list = list(sdc_dir.glob(f'{config['sdc_name']}*.sdc'))
    
    # Tracks parse results
    summary = {}
    # Tracks passing SDC contents
    pass_log = {}
    # Tracks error messages for parse failures
    error_log = {}
    # Regex to look for in vpr.out
    error_pattern = re.compile(r"--- SDC TCL Parse Error ---(.*?)-{20,}", re.DOTALL)
    
    # Test for all SDCs found
    for sdc in sdc_list:
        # Prepare VTR arguments
        cmd = [
        f'{VTR_ROOT}/vtr_flow/scripts/run_vtr_flow.py',
        f'{blif_file}',
        f'{architecture_file}',
        '-starting_stage', 'abc', # Technology mapping with ABC
        '-ending_stage', 'vpr', 
        '-temp_dir', f'{result_dir}',
        '--pack',  # Run the pack stage of VPR
        '--device', f'vtr_medium', 
        '--route_chan_width', '100',
        '--sdc_file', f'{sdc}'
        ]
        
        # Run subprocess
        try:
            print(f"Running Syntax Suite (SDC: {sdc.name})")
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"    [PASSED] {sdc.name}")
            summary[sdc.name] = "PASS"
            try: 
                sdc_content = sdc.read_text()
            except Exception:
                sdc_content = "Could Not Read SDC"
            pass_log[sdc.name] = sdc_content
            
        except subprocess.CalledProcessError as e:
            print(f"    [FAILED] {sdc.name}")
            summary[sdc.name] = "FAIL"
            
            try:
                sdc_content = sdc.read_text()
            except Exception:
                sdc_content = "Could Not Read SDC"

            # Capture error message
            with open(result_dir / 'vpr.out') as f:
                vpr_content = f.read()
            
            errors = error_pattern.findall(vpr_content)
            err_msg = [error.strip() for error in errors]
            
            # Save to error log
            error_log[sdc.name] = {
                'sdc': sdc_content, 
                'error': err_msg
            }
    
    # Write summary CSV
    with open(csv_path, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['SDC_Filename', 'Result'])
        for name, status in summary.items():
            writer.writerow([name, status])
            
    print(f"Summary saved to: {csv_path}")
    
    # Write pass log
    if pass_log:
        with open(pass_path, 'w') as f:
            f.write(f"Passed SDCs\n\n")
            for name, content in pass_log.items():
                f.write(f"File: {name}\n")
                f.write(f"{content}\n")
                f.write('-'*30+'\n')
        print(f"Pass log saved to: {pass_path}")
    
    # Write error log
    if error_log:
        with open(err_path, 'w') as f:
            f.write(f"Error Log for '{config['sdc_name']}'\n\n")
            for name, error in error_log.items():
                f.write(f"SDC Content:\n")
                f.write(f"{error['sdc']}")
                f.write('-'*30+'\n')
                f.write(f"Error Message:\n")
                for line in error['error']:
                    f.write(f"{line}\n")
                f.write('-'*30+'\n\n')
                
        print(f"Error log saved to: {err_path}")
        
    return None

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Runs syntax test")
    parser.add_argument('--sdc_name', type=str, required=True, help="Type of SDC to test")
    
    args = parser.parse_args()
    sdc_name = args.sdc_name
    
    # Run all tests
    if sdc_name == "all":
        for test in config.SYNTAX_TESTS:
            run_syntax_suite(test)
    
    # Bring the configuration object from config.py using getattr
    try:
        sdc_config = getattr(config, sdc_name)
    except AttributeError:
        print(f"Error: '{sdc_name}' doesn't exist in the config file")
        exit(1)
    
    run_syntax_suite(sdc_config)