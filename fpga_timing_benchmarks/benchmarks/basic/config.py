from pathlib import Path
import sys

# DIRECTORIES
BENCHMARK_ROOT = Path(__file__).parent
MICRO_ROOT = BENCHMARK_ROOT / 'micro'
ARCH_DIR = BENCHMARK_ROOT / 'arch'

RESULTS_DIR = BENCHMARK_ROOT / 'results'
SYNTHESIS_DIR = RESULTS_DIR / 'blif'

CIRCUITS_DIR = Path('./micro')
OUTPUT_DIR = Path('./run')
VTR_ROOT = Path('~/VTR/vtr-verilog-to-routing').expanduser()

ARCH_FILE = ARCH_DIR / 'k6_frac_N10_frac_chain_mem32K_40nm.xml'
PARSE_FILE_PATH = Path('./')


# METRICS

# TESTS
# Format:
# TEST_DICT = { 
# 'constraint_0': [{'type': str,
#                   'blif': str, 
#                   'sdc': str, 
#                   'param': list, 
#                   'metrics': list,    
#                   'frontend': str, 
#                   'layout': str,
#                   'graphics': Bool,
#                   'constrained': Bool}, 
#                   {}], 
# 'constraint_1': [{}], 
#  ... 
# }
TEST_DICT = {
# 1. create_clock
'create_clock': [
    {
    'type': 'create_clock_rca', # Must be a unique name for that test case
    'blif': 'create_clock/rca.blif',
    'sdc': """
create_clock -period <period> -name clk
create_clock -period 11.0 [get_ports clk*]
    """.strip(),
    'param': [{'name': '<period>', 'default': None, 'values': [1.0, 3.0, 5.0, 10.0, 20.0]}],
    'metrics': ['cpd', 'setup_slack', 'hold_slack'],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 2. create_generated_clock
'create_generated_clock': [
    {
    'type': 'create_generated_clock',
    'circuit': 'create_generated_clock/clock_divider.v',
    'sdc': 'create_generated_clock/clock_divider.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    },
    {
    'circuit': 'create_generated_clock/multiplexed_clock.v',
    'sdc': 'create_generated_clock/multiplexed_clock.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 3. set_clock_groups
'set_clock_groups': [
    {
    'circuit': 'create_generated_clock/multiclock_cdc.v',
    'sdc': 'create_generated_clock/multiclock_cdc.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'odin',
    'layout': 'vtr_medium'
    }
    ],
# 4. set_clock_latency
'set_clock_latency': [
    {
    'circuit': 'set_clock_latency/adc_to_dac.v',
    'sdc': 'set_clock_latency/adc_to_dac.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    },
    {
    'circuit': 'set_clock_latency/skewed_clock.v',
    'sdc': 'set_clock_latency/skewed_clock.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 5. set_clock_uncertainty
'set_clock_uncertainty': [
    {
    'circuit': 'set_clock_uncertainty/dot_product_pipe.v',
    'sdc': 'set_clock_uncertainty/dot_product_pipe.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 6. set_false_path
'set_false_path': [
    {
    'type': 'set_false_path_multiclock_cdc',
    'circuit': 'set_false_path/multiclock_cdc.v',
    'sdc': """
set_false_path -from -to
    """.strip(),
    'param': None,
    'metrics': [],
    'frontend': 'odin',
    'layout': 'vtr_medium'
    },
    {
    'type': 'set_false_path_multibit_rca',
    'circuit': 'set_false_path/multibit_rca.v',
    'sdc': """
set_false_path -from -to
    """.strip(),
    'param': None,
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 7. set_input_delay
'set_input_delay': [
    {
    'circuit': 'set_input_delay/hamming_distance.v',
    'sdc': 'set_input_delay/hamming_distance.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 8. set_output_delay
'set_output_delay': [
    {
    'circuit': 'set_output_delay/hamming_distance.v',
    'sdc': 'set_output_delay/hamming_distance.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ],
# 9. set_max_delay
'set_max_delay': [
    {
    'circuit': 'set_max_delay/barrel_shifter.v',
    'sdc': 'set_max_delay/barrel_shifter.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    },
    {
    'circuit': 'set_max_delay/multiclock_cdc.v',
    'sdc': 'set_max_delay/multiclock_cdc.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'odin',
    'layout': 'vtr_medium'
    }
    ],
# 10. set_min_delay
'set_min_delay': [
    {
    'circuit': 'set_min_delay/alu_4bit.v',
    'sdc': 'set_min_delay/alu_4bit.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    },
    {
    'circuit': 'set_min_delay/multiclock_cdc.v',
    'sdc': 'set_min_delay/multiclock_cdc.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'odin',
    'layout': 'vtr_medium'
    }
    ],
# 11. set_multicycle_path
'set_multicycle_path': [
    {
    'circuit': 'set_multicycle_path/multi_rca.v',
    'sdc': 'set_multicycle_path/multi_rca.sdc',
    'param': [],
    'metrics': [],
    'frontend': 'parmys',
    'layout': 'vtr_medium'
    }
    ]
}
# 12. set_disable_timing

# 13. setup_violation

# 14. hold_violation

# PARSE CONFIGURATION
# field_name = 
