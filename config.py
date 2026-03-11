
# 4. Clean this config and run_benchmark.py []

from pathlib import Path

### DIRECTORIES ###
# Edit 'VTR_ROOT' to the actual directory in which it is located.

VTR_ROOT = Path('~/VTR/vtr-verilog-to-routing').expanduser()
BENCHMARK_ROOT = Path(__file__).parent
MICRO_ROOT = BENCHMARK_ROOT / 'fpga_timing_benchmarks' / 'benchmarks' / 'basic' / 'netlist_files'
ARCH_DIR = BENCHMARK_ROOT / 'arch'
RESULTS_DIR = BENCHMARK_ROOT / 'results'
SYNTHESIS_DIR = RESULTS_DIR / 'blif'
SYNTAX_DIR = BENCHMARK_ROOT / 'auto_generated'

ARCH_FILE = ARCH_DIR / 'k6_frac_N10_frac_chain_mem32K_40nm.xml'
LIBERTY_FILE = VTR_ROOT / 'vtr_flow' / 'primitives.lib'

### BASIC TIMING SUITE CONFIGURATION ###

# TIMING_TESTS: A list of per constraint timing test configurations.
# The entries of the list 'TIMING_TESTS' are dictionaries that define a single or multiple test cases. 

# Dictionary Format: 
# 'type' (str): A unique name for a test case. Used to create the output directory.
# 'blif' (str): Path to the BLIF file to test, relative to 'MICRO_ROOT'.
# 'top_level_module' (str): Name of the top level module of the design.
# 'sdc' (str): A template for the SDC to test. Use placeholders '<param_name>' to substitute with varying values. 
# 'param' (list|None): A list of dictionaries for parameter sweeping. Each dictionary must have keys 'name' and 'values'.
#   'name': The placeholder string in the SDC template to be replaced. 
#   'default': Default value for the parameter. Set to 'None' if no other parameter sweeping is required.  
#   'values': A list of values to iterate through when creating the SDCs.
# 'layout' (str): Fixed device layout as defined in the architecture description file (.xml).
# 'graphics' (bool): Enable VPR graphics and save PnR results as a PNG.

# 1. create_clock
create_clock = [
    {
    'type': 'create_clock_rca', 
    'blif': 'create_clock/rca.blif',
    'top_level_module': 'rca',
    'sdc': """
create_clock -period <period> {clk}
create_clock -period 1.0 -name irrelevant_clock
    """.strip(),
    'param': [{'name': '<period>', 'default': None, 'values': [1.0, 3.0, 5.0, 10.0, 12.0]}],
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 2. create_generated_clock
create_generated_clock = [
    {
    'type': 'create_generated_clock_clock_divider_base',
    'blif': 'create_generated_clock/clock_divider.blif',
    'top_level_module': 'clock_divider',
    'sdc': """
create_clock -period 10.0 clk
set_clock_latency -source 5.0 [get_clocks clk]
create_generated_clock -source [get_clocks clk] -divide_by 2 {*641*.Q*}
    """.strip(),
    'param': None,
    'layout': 'vtr_medium',
    'graphics': False
    },
    
    {
    'type': 'create_generated_clock_clock_divider',
    'blif': 'create_generated_clock/clock_divider.blif',
    'top_level_module': 'clock_divider',
    'sdc': """
create_clock -period 10.0 {clk}
set_clock_latency -source 5.0 {clk}
create_clock -period 10.0 {$dff~641^Q~0}
    """.strip(),
    'param': None,
    'layout': 'vtr_medium',
    'graphics': False
    },
    
    {
    'type': 'create_generated_clock_multiplexed_clock',
    'blif': 'create_generated_clock/multiplexed_clock.v',
    'sdc': """
create_clock
create_generated_clock
    """.strip(),
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 3. set_clock_groups
set_clock_groups = [
    {
    'type': 'set_clock_groups_muticlock_cdc',
    'blif': 'set_clock_groups/multiclock_cdc.blif',
    'sdc': """
create_clock -period 10.0 {*clk_A}
create_clock -period 5.0 {*clk_B}
set_clock_groups -asynchronous -group {*clk_A} -group {*clk_B}
    """.strip(),
    'param': None,
    'layout': 'vtr_medium',
    'graphics': True
    }
    ]

# 4. set_clock_latency
set_clock_latency = [
    {
    'type': 'set_clock_latency_adc_to_dac',
    'blif': 'set_clock_latency/adc_to_dac.blif',
    'sdc': """
create_clock -period 5.0 {clk}
set_clock_latency -source <latency> {clk}
set_input_delay 1.0 adc_data* -clock {clk}
set_output_delay 1.0 [get_ports dac_data*] -clock {clk}
    """.strip(),
    'param': [{'name': '<latency>', 'default': None, 'values': [0.5, 1.0, 2.0, 3.0, 5.0]}],
    'layout': 'vtr_medium',
    'graphics': False
    },
    
    {
    'type': 'set_clock_latency_skewed_clock',
    'blif': 'set_clock_latency/skewed_clock.blif',
    'sdc': """

    """.strip(),
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 5. set_clock_uncertainty
set_clock_uncertainty = [
    {
    'type': 'set_clock_uncertainty_dot_prod',
    'blif': 'set_clock_uncertainty/dot_product_pipe.blif',
    'sdc': """
create_clock -period 15.0 {dot_product_pipe^clk}
set_clock_uncertainty -setup <uncertainty> {dot_product_pipe^clk}
    """.strip(),
    'param': [{'name': '<uncertainty>', 'default': None, 'values': [0.5, 1.0, 2.0, 3.0, 5.0]}],
    'layout': 'vtr_medium',
    'graphics': True
    }
    ]

# 6. set_false_path
set_false_path = [
    {
    'type': 'set_false_path_multiclock_cdc',
    'blif': 'set_false_path/multiclock_cdc.v',
    'sdc': """
set_false_path -from -to
    """.strip(),
    'param': None,
    'layout': 'vtr_medium',
    'graphics': True
    },
    
    {
    'type': 'set_false_path_multibit_rca',
    'blif': 'set_false_path/multibit_rca.blif',
    'sdc': """
set_false_path -from -to
    """.strip(),
    'param': None,
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 7. set_input_delay
set_input_delay = [
    {
    'type': 'set_input_delay_hamming_distance', # Must be a unique name for that test case
    'blif': 'set_input_delay/hamming_distance.blif',
    'top_level_module': 'hamming_distance',
    'sdc': """
create_clock -period 35.0 {clk}
set_input_delay <delay> -clock clk *data_in*
    """.strip(),
    'param': [{'name': '<delay>', 'default': None, 'values': [1.0, 5.0, 10.0, 20.0, 30.0, 32.0, 33.0, 34.0, 35.0, 40]}],
    'layout': 'vtr_medium',
    'graphics': True
    }
    ]

# 8. set_output_delay
set_output_delay = [
    {
    'type': 'set_output_delay_hamming_distance', # Must be a unique name for that test case
    'blif': 'set_output_delay/hamming_distance.blif',
    'top_level_module': 'hamming_distance',
    'sdc': """
create_clock -period 35.0 {clk}
set_output_delay <delay> -clock clk {data_in*}
    """.strip(),
    'param': [{'name': '<delay>', 'default': None, 'values': [10.0, 20.0, 30.0, 32.0, 33.0, 34.0, 35.0]}],
    'layout': 'vtr_medium',
    'graphics': True
    }
    ]

# 9. set_max_delay
set_max_delay = [
    {
    'type': 'set_max_delay_barrel_shifter',
    'blif': 'set_max_delay/barrel_shifter.blif',
    'sdc': """
    """.strip(),
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    },
    
    {
    'type': 'set_max_delay_multiclock_cdc',
    'blif': 'set_max_delay/multiclock_cdc.blif',
    'sdc': """
    """.strip(),
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 10. set_min_delay
set_min_delay = [
    {
    'type': 'set_min_delay_alu_4bit',
    'blif': 'set_min_delay/alu_4bit.blif',
    'sdc': """
    """.strip(),
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    },
    
    {
    'type': 'set_min_delay_multiclock_cdc',
    'blif': 'set_min_delay/multiclock_cdc.blif',
    'sdc': """
    """.strip(),
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 11. set_multicycle_path
set_multicycle_path = [
    {
    'type': 'set_multicycle_path_multi_rca',
    'circuit': 'set_multicycle_path/multi_rca.v',
    'sdc': 'set_multicycle_path/multi_rca.sdc',
    'param': [],
    'layout': 'vtr_medium',
    'graphics': False
    }
    ]

# 12. set_disable_timing

# 13. setup_violation

# 14. hold_violation

TIMING_TESTS = []

### SYNTAX TEST CONFIGURATION ###

# 'SYNTAX_TESTS': A list of syntax test configurations.
# Elements in the list 'SYNTAX_TESTS' are dictionaries, defining each syntax test case. 

# Dictionary Format:
# 'type': A unique name for the test. Used for result tracking. 
# 'blif': The name of the BLIF file to be processed by VPR. 
# 'sdc_name': Name of the timing constraint targeted for syntax validation. 

create_clock = {
    'type': 'syntax_create_clock',
    'blif': 'create_clock_netlist.blif',
    'sdc_name': 'create_clock'
}

create_generated_clock = {
    'type': 'syntax_create_generated_clock',
    'blif': 'create_generated_clock_netlist.blif',
    'sdc_name': 'create_generated_clock'
}

set_input_delay = {
    'type': 'syntax_set_input_delay',
    'blif': 'set_input_delay_netlist.blif',
    'sdc_name': 'set_input_delay'
}

set_output_delay = {
    'type': 'syntax_set_output_delay',
    'blif': 'set_output_delay_netlist.blif',
    'sdc_name': 'set_output_delay'
}

set_clock_latency = {
    'type': 'syntax_set_clock_latency',
    'blif': 'set_clock_latency_netlist.blif',
    'sdc_name': 'set_clock_latency'
}

set_clock_uncertainty = {
    'type': 'syntax_set_clock_uncertainty',
    'blif': 'set_clock_uncertainty_netlist.blif',
    'sdc_name': 'set_clock_uncertainty'
}

set_false_path = {
    'type': 'syntax_set_false_path',
    'blif': 'set_false_path_netlist.blif',
    'sdc_name': 'set_false_path'
}

set_max_delay = {
    'type': 'syntax_set_max_delay',
    'blif': 'set_max_delay_netlist.blif',
    'sdc_name': 'set_max_delay'
}

set_min_delay = {
    'type': 'syntax_set_min_delay',
    'blif': 'set_min_delay_netlist.blif',
    'sdc_name': 'set_min_delay'
}

set_multicycle_path = {
    'type': 'syntax_set_multicycle_path',
    'blif': 'set_multicycle_path_netlist.blif',
    'sdc_name': 'set_multicycle_path'
}

set_clock_groups = {
    'type': 'syntax_set_clock_groups',
    'blif': 'set_clock_groups_netlist.blif',
    'sdc_name': 'set_clock_groups'
}

set_disable_timing = {
    'type': 'syntax_set_disable_timing',
    'blif': 'set_disable_timing_netlist.blif',
    'sdc_name': 'set_disable_timing'
}

# 'run_syntax.py' will run every test in this list when given '--sdc_name all'
SYNTAX_TESTS = [create_clock, create_generated_clock, set_input_delay, set_output_delay,
                set_clock_latency, set_clock_uncertainty, set_false_path,
                set_min_delay, set_max_delay, set_multicycle_path, set_clock_groups,
                set_disable_timing]