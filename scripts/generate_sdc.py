import os
import random
from itertools import product
from itertools import combinations

'''
TODO
-get_ commands
-set_operating_conditions
-THE LIST OPERATING_CONDITIONS
-Minor fixes/cleanup
'''


#PATH CONFIGURATION
##################################################################################################################################################
script_dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir_path)
intermediate_dir = os.path.join(parent_dir, "auto_generated", "SDC")
temp_output_path = os.path.join(script_dir_path, "outputs")

#PARAMETERS
##################################################################################################################################################
PERIODS = [5, 10, 20]
PINS = ["[get_pins *]", "[get_pins pin1]", "[get_pins ff_pin/pin1]", "[get_pins ff_pin/pin2]", "[get_pins ff_pin/*]"]
#PINS = ["*", "ff_pin/pin1", "ff_pin/pin2", "ff_pin/*", "[get_pins {pin1}]", "[get_pins ff_pin/*]", "[get_pins ff_pin/pin1]"] 
NETS = ["*", "net1", "net2", "net*", "{net1, net2}"]
CELLS = ["cell1", "cell2", "cell*"]
INSTANCES = ["xor1", "and1", "ff1", "adder1", "xor*", "*", "ff*"]
DELAYS = [4.0, 10, 30]
PORTS = ["*", "[get_ports port1]", "[get_ports port2]", "port1", "port2", "port*", "[get_ports port*]"]
CLOCKS = ["*", "clk1", "clk2", "clk*", "[get_clocks clk1]", "[get_clocks clk2]", "{clk1}"] 
FILTER_VAL = []
SEPARATOR = ["/", ".", "|"]
CELL_INSTANCES = ["*", "reg*", "inst*", "buff*", "reg1", "inst1", "buff1", "inv1", "u1"]
UNCERTAINTIES = [0.1, 1, 0.5, 0.2]
DIVISORS = [2, 4, 5]
EDGES = ["{1 3 5}", "{1 2 3}", "{2 4 6}", "{1 4 7}"]
CLOCK_GROUP_1 = ["[get_clocks -filter period==6]", "{clk1 clk2}", "{clk1 clk3}", "{clk2 clk4}", "{clk1 clk3 clk4}"] 
CLOCK_GROUP_2 = ["clk1", "clk5", "{clk2 clk3}", "[get_clocks clk4]"] #Designed to prevent redundancy
LIBRARIES = ["lib1", "lib2", "lib3"] #For set_operating_condition, these libraries should contain 'condition'
OPERATING_CONDITIONS = [""]



FILTER_TYPE = {"singular", "value", "pattern", "compound"}
OBJ_TYPE = ["cell", "clock", "pin", "port", "net"]
'''
CELL_PROPERTIES = {
    "boolean" : [],
    "value" : {},
    "pattern" : {"base_name", "filename", "full_name", "name"}
    "library"
}
CLOCK_PROPERTIES = {
    "boolean" : ["is_generated", "is_propagated", "is_virtual"],
    "value" : {"period" : [2, 5, 10, 20]}
    "pattern" : ["full_name", "name"]
    "sources"
}
PIN_PROPERTIES = {
    "boolean" : ["is_hierarchical", "is_port", "is_register_clock"],
    "value" : {"slew_max_fall" : [], "slew_max_rise" : [], "slew_min_fall" : [], "slew_min_rise" : [],  
              "slack_max" : [], "slack_max_fall" : [], "slack_max_rise" : [], "slack_min" : [],
              "slack_min_fall" : [], "slack_min_rise" : [], "direction" : ["input", "output", "inout", "internal"]},
    "pattern" : ["full_name", "lib_pin_name", "name"]
    "activity"
    "clocks",
    "clock_domains"
}
PORT_PROPERTIES = {
    "boolean" : [],
    "value" : {"slew_max_fall" : [], "slew_max_rise" : [], "slew_min_fall" : [], "slew_min_rise" : [],  
              "slack_max" : [], "slack_max_fall" : [], "slack_max_rise" : [], "slack_min" : [],
              "slack_min_fall : [], slack_min_rise : []},
    "pattern" : ["full_name", "name"]
    "activity",
    "direction",
    "liberty_port",
}
NET_PROPERTIES = {
    "boolean" : [],
    "value" : [],
    "pattern" : ["full_name", "name"]
}

INSTANCE_PROPERTIES = {
    "boolean": ["is_buffer", "is_clock_gate", "is_hierarchical", "is_inverter", "is_macro", "is_memory"],
    "value": ["full_name", "name", "ref_name"],
    "pattern": ["cell", "liberty_cell"]
}

PROPERTIES = {
    "clock": CLOCK_PROPERTIES,
    "port": PORT_PROPERTIES,
    "pin": PIN_PROPERTIES,
    "cell": CELL_PROPERTIES,
    "net": NET_PROPERTIES
}

'''
PATTERNS = {
    "clock": ["clk*", "clk_gen", "clock", "clk1"],
    "port": ["data*", "*in", "*out", "valid_in"],
    "pin": ["u1/*", "*/Q", "u2/D", "*/clk"],
    "cell": ["inst*", "reg_*", "*_buffer"],
    "net": ["net*", "n[0-9]*", "*_data"]
    }
#HELPER FUNCTIONS
##################################################################################################################################################
def choose_object_type():
    '''
    Returns a random choice from list OBJ_TYPE = ["clock", "port", "pin", "cell", "net"]
    '''
    return random.choice(OBJ_TYPE)

def choose_filter_type():
    '''
    Returns a random choice from list FILTER_TYPE = ["singular", "value", "pattern", "compound"]
    '''
    return random.choice(FILTER_TYPE)

def generate_filter(filter_type, object_type):
    '''
    Generates a filter expression for get_ variants
    
    Args: 
        filter_type: a filter type(string) returned by choose_filter_type()
        object_type: an string in the list ["clock", "port", "pin", "cell", "net"]
    
    Returns:
        A filter expression string
    '''
    
    if filter_type == "singular":
        if not PROPERTIES[object_type]["boolean"]:  #If no "boolean" property exists
            return generate_filter("value", object_type) #Create a filter expression with the property "value"
            
        return random.choice(PROPERTIES[object_type]["boolean"]) 
    
    
    elif filter_type == "value":
        if not PROPERTIES[object_type]["value"]:    #If no "value" property exists
            return generate_filter("pattern", object_type) #Create a filter expression with the property "pattern"
            
        op = random.choice(["==", "!="])
        prop = random.choice(list(PROPERTIES[object_type]["value"].keys()))
        
        if PROPERTIES[object_type]["value"][prop]: 
            val = random.choice(PROPERTIES[object_type]["value"][prop])
        else:
            val = "1" #Default value
        return f'{prop}{op}"{val}"'
    
    
    elif filter_type == "pattern":
        if not PROPERTIES[object_type]["pattern"]:  #If no "pattern" property exists
            return generate_filter("singular", object_type) #Create a filter expression with the property "singular", may be dangerous if no properties exist for the object_type
            
        op = random.choice(["=~", "!~"])
        prop = random.choice((PROPERTIES[object_type]["pattern"]))
        
        if PATTERNS[object_type]:
            pat = random.choice(PATTERNS[object_type])
        else:
            pat = "*" #Default pattern
        return f'{prop}{op}"{pat}"'

    
    elif filter_type == "compound":
        new_filter1 = random.choice(["singular", "value", "pattern"]) 
        new_filter2 = random.choice(["singular", "value", "pattern"])
        
        #This recursion is guaranteed to find a property
        expr1 = generate_filter(new_filter1, object_type)
        expr2 = generate_filter(new_filter2, object_type)
        op = random.choice(["&&", "||"])
        
        return f"({expr1}){op}({expr2})"
        
def generate_pattern(object_type):
    '''
    Args:
        object_type: a string in the list ["clock", "port", "pin", "cell", "net"]
        
    Returns: 
        A pattern that belongs to the object type (string)
        Currently only returns one pattern but should be able to return lists as well
    '''
    if object_type not in PATTERNS or not PATTERNS[object_type]: #Invalid object_type or pattern non-existent
        return "*" 
    
    return random.choice(PATTERNS[object_type])
    

#GENERATOR FUNCTIONS
##################################################################################################################################################
def generate_create_clock():
    '''
    Required: -period
    Optional: -name, -waveform, -add, pin_list
    '''
    #List containing all possible combinations of options
    commands = []
    optional_options = ["-name", "-waveform", "-add", "pin_list"]
    pin_list = ["clk1", "clk2", "[get_ports clk1]", "[get_pins dff2/clk]", "[get_pins dff1/clk]", "{clk1 clk2}"] #"{[get_pins dff1/clk] [get_pins dff2/clk]}"
    
    for i in range(len(PERIODS)):
        period = PERIODS[i]
        
        for j in range(len(optional_options) + 1):
            for option_combination in combinations(optional_options, j):
                pieces = [f"create_clock -period {period}"]
                
                if "-name" in option_combination:
                    pieces.append(f"-name clk_{period}")
                    
                if "-waveform" in option_combination:
                    #FIXME: Do not make this random.
                    rise_time = round(random.uniform(0, period/2))
                    fall_time = round(random.uniform(period/2, period))
                    pieces.append(f"-waveform {{{rise_time} {fall_time}}}")
                    
                if "-add" in option_combination:
                    pieces.append("-add")

                if "pin_list" in option_combination: 
                    #A list of pins driven by the clock
                    pin = random.choice(pin_list)
                    pieces.append(f"{pin}")

                commands.append(" ".join(pieces))
        
    return commands             

def generate_get_ports():
    '''
    Optional: -regexp, -nocase(Legal only with -regexp), -quiet
    '''
    commands = [] #List containing all possible combinations of options
    
    optional_options = ["-regexp", "-nocase", "-quiet"]

    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):
            
            #The option -nocase is only valid with -regexp
            if "-nocase" in option_combination and "-regexp" not in option_combination:
                continue 
                
            pieces = ["get_ports"]

            if "-regexp" in option_combination:
                pieces.append("-regexp")
                
            if "-nocase" in option_combination:
                pieces.append("-nocase")

            if "-quiet" in option_combination:
                pieces.append("-quiet")
                
            #A list of port name patterns
            pattern = generate_pattern("port")
            pieces.append(pattern)
            
            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk [get_ports clk]\n" + pieces)
            commands.append(pieces)
            
    return commands

def generate_get_clocks():
    '''
    Optional: -regexp, -nocase(Legal only with -regexp), -quiet
    '''
    commands = [] #List containing all possible combinations of options
    optional_options = ["-regexp", "-nocase", "-quiet"]

    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):

            #Constraint: -nocase is only valid with -regexp
            if "-nocase" in option_combination and "-regexp" not in option_combination:
                continue

            pieces = ["get_clocks"]

            if "-regexp" in option_combination:
                pieces.append("-regexp")

            if "-nocase" in option_combination:
                pieces.append("-nocase")

            if "-quiet" in option_combination:
                pieces.append("-quiet")

            pattern = generate_pattern("clock")
            pieces.append(pattern)
            
            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk1 [get_ports clk1]\n" + 
                      "create_clock -period 10 -name clk2 [get_ports clk2]\n" + 
                      "create_clock -period 10 -name clk_gen [get_ports clk_gen]\n" +
                      "create_clock -period 10 -name clock [get_ports clock]\n" + 
                      pieces)
            commands.append(pieces)

    return commands
    
def generate_get_pins():
    '''
    Required:
    Optional: -hierarchical, -hsc, -filter, -regexp, -nocase(Valid only with -regexp), -quiet, -of_objects, patterns
    Note: -hierarchical cannot be used with -of_objects
    '''
    commands = [] #List containing all possible combinations of options
    optional_options = ["-hierarchical", "-hsc", "-filter", "-regexp", "-nocase", "-quiet", "-of_objects", "patterns"]

    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):

            #Constraint 1: -nocase is only valid with -regexp
            if "-nocase" in option_combination and "-regexp" not in option_combination:
                continue #Skip this invalid combination

            pieces = ["get_pins"]

            if "-regexp" in option_combination:
                pieces.append("-regexp")

            if "-nocase" in option_combination:
                pieces.append("-nocase")

            if "-quiet" in option_combination:
                pieces.append("-quiet")

            pattern = generate_pattern("pin")
            pieces.append(pattern)

            
            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk [get_ports clk]\n" + pieces)
            commands.append(pieces)

    return commands

def generate_set_input_delay():
    '''
    Note
    -clock_fall should be used with -clock
    -max, -min are exclusive
    -reference_pin cannot be used with latency options
    
    '''
    commands = []
    optional_options = ["-rise", "-fall", "-max", "-min", "-clock", "-clock_fall", "-reference_pin", "-source_latency_included", "-network_latency_included", "-add_delay"]
    
    for i in range(len(DELAYS)): 
        delay = DELAYS[i]
        
        for j in range(len(optional_options) + 1):
            for option_combination in combinations(optional_options, j):
                
                if "-clock_fall" in option_combination and "-clock" not in option_combination:
                    continue
                if "-max" in option_combination and "-min" in option_combination:
                    continue
                if "-reference_pin" in option_combination:
                    if "-source_latency_included" in option_combination or "-network_latency_included" in option_combination:
                        continue
            
                #Delay value required
                pieces = [f"set_input_delay", f"{delay}"]

                if "-rise" in option_combination:
                    pieces.append("-rise")
            
                if "-fall" in option_combination:
                    pieces.append("-fall")
                
                if "-max" in option_combination:
                    pieces.append("-max")
                
                if "-min" in option_combination:
                    pieces.append("-min")

                if "-clock" in option_combination:
                    pieces.append(f"-clock [get_clocks src_clk]")

                if "-clock_fall" in option_combination:
                    pieces.append("-clock_fall")
                    
                if "-reference_pin" in option_combination:
                    pieces.append(f"-reference_pin [get_pins ff_ref/clk]")
                    
                if "-source_latency_included" in option_combination:
                    pieces.append("-source_latency_included")
                    
                if "-network_latency_included" in option_combination:
                    pieces.append("-network_latency_included")
                    
                if "-add_delay" in option_combination:
                    pieces.append("-add_delay")

                pin_port_list = random.choice(PINS + PORTS)
                pieces.append(pin_port_list)

                #Join the options to create a proper command
                pieces = " ".join(pieces)
                #Add create_clock prerequisites
                pieces = ("create_clock -period 10 -name src_clk [get_ports src_clk]\n"
                          + pieces)
                commands.append(pieces)
    
    return commands

def generate_set_output_delay():
    '''
    Note
    -clock_fall should be used with -clock
    -max, -min are exclusive
    -reference_pin cannot be used with latency options
    '''
    commands = []
    optional_options = ["-rise", "-fall", "-max", "-min", "-clock", "-clock_fall", "-reference_pin", "-source_latency_included", "-network_latency_included", "-add_delay"]
    for i in range(len(DELAYS)):
        delay = DELAYS[i]
        
        for j in range(len(optional_options) + 1):
            for option_combination in combinations(optional_options, j):
                
                if "-clock_fall" in option_combination and "-clock" not in option_combination:
                    continue
                if "-max" in option_combination and "-min" in option_combination:
                    continue
                if "-reference_pin" in option_combination:
                    if "-source_latency_included" in option_combination or "-network_latency_included" in option_combination:
                        continue

                #Delay value required
                pieces = [f"set_output_delay", f"{delay}"] 
                
                if "-rise" in option_combination:
                    pieces.append("-rise")
                
                if "-fall" in option_combination:
                    pieces.append("-fall")
                    
                if "-max" in option_combination:
                    pieces.append("-max")
                    
                if "-min" in option_combination:
                    pieces.append("-min")

                if "-clock" in option_combination:
                    #TODO: Might be [get_clocks src_clk]
                    clk = random.choice(CLOCKS)
                    pieces.append(f"-clock [get_clocks src_clk]")

                if "-clock_fall" in option_combination:
                    pieces.append("-clock_fall")
                    
                if "-reference_pin" in option_combination:
                    #TODO: Might be [get_pins ff_inst/clk]
                    pieces.append(f"-reference_pin [get_pins ff_ref/clk]") 
                    
                if "-source_latency_included" in option_combination:
                    pieces.append("-source_latency_included")
                    
                if "-network_latency_included" in option_combination:
                    pieces.append("-network_latency_included")
                    
                if "-add_delay" in option_combination:
                    pieces.append("-add_delay")

                pin_port_list = random.choice(PINS + PORTS)
                pieces.append(pin_port_list)

                #Join the options to create a proper command
                pieces = " ".join(pieces)
                #Add create_clock prerequisites
                pieces = ("create_clock -period 10 -name src_clk [get_ports src_clk]\n"
                          + pieces)
                commands.append(pieces)
    
    return commands
    
def generate_set_clock_latency():
    '''
    Required options: delay, objects
    '''
    commands = []
    optional_options = ["-source", "-rise", "-fall", "-max", "-min", "-clock"]

    for i in range(len(DELAYS)):
        delay = DELAYS[i]
        
        for j in range(len(optional_options) + 1):
            for option_combination in combinations(optional_options, j):
                
                if "-max" in option_combination and "-min" in option_combination:
                    continue
                
                pieces = ["set_clock_latency", f"{delay}"]
                
                #Handle optional arguments
                if "-source" in option_combination:
                    pieces.append(random.choice(CLOCKS))
                    pieces.append("-source")
                    
                if "-source" not in option_combination:
                    pieces.append(random.choice(CLOCKS + PINS + PORTS))
                    
                if "-rise" in option_combination:
                    pieces.append("-rise")
                    
                if "-fall" in option_combination:
                    pieces.append("-fall")
                    
                if "-max" in option_combination:
                    pieces.append("-max")
                    
                if "-min" in option_combination:
                    pieces.append("-min")

                if "-clock" in option_combination:
                    #TODO: Might be [get_clocks ]
                    #Always refer to clk1
                    pieces.append(f"-clock [get_clocks clk1]")

                #Join the options to create a proper command
                pieces = " ".join(pieces)
                #Add create_clock prerequisites
                pieces = ("create_clock -period 10 -name clk1 [get_ports clk1]\n"
                          "create_clock -period 20 -name clk2 [get_ports clk2]\n"
                          + pieces)
                commands.append(pieces)
    
    return commands

def generate_set_clock_uncertainty():  
    '''
    Note
    the from variants are all mutually exclusive
    the to variants are all mutually exclusive
    -rise and -fall are alternatives to -rise_to and -fall_to. 
    
    from clock is always clk1, to clock is always clk2
    '''
    commands = [] #List containing all possible combinations of options
    
    optional_options = ["-rise", "-fall", "-setup", "-hold", "-from", "-rise_from", "-fall_from", "-to", "-rise_to", "-fall_to", "objects"]
    
    from_options = ["-from", "-rise_from", "-fall_from"]
    to_options = ["-to", "-rise_to", "-fall_to"]

    for i in range(len(UNCERTAINTIES)):
        uncertainty = UNCERTAINTIES[i]
        for j in range(len(optional_options) + 1):
            for option_combination in combinations(optional_options, j):
                
                from_count = sum(1 for from_opt in from_options if from_opt in option_combination)
                if from_count > 1:
                    continue
                
                to_count = sum(1 for to_opt in to_options if to_opt in option_combination)
                if to_count > 1:
                    continue
                
                if (from_count + to_count) == 1:
                    continue
                
                if "objects" in option_combination and from_count > 0:
                    continue
                
                pieces = ["set_clock_uncertainty", f"{uncertainty}"] 
                
                if "-rise" in option_combination:
                    pieces.append("-rise")
                    
                if "-fall" in option_combination:
                    pieces.append("-fall")
                    
                if "-setup" in option_combination:
                    pieces.append("-setup")
                    
                if "-hold" in option_combination:
                    pieces.append("-hold")
                    
                if "-from" in option_combination:
                    #FIXME: Maybe [get_clocks clk1] or {clk1}
                    pieces.append(f"-from [get_clocks clk1]")
                    
                if "-rise_from" in option_combination:
                    #FIXME: Maybe [get_clocks clk1] or {clk1}
                    pieces.append(f"-rise_from [get_clocks clk1]")
                    
                if "-fall_from" in option_combination:
                    #FIXME: Maybe [get_clocks clk1] or {clk1}
                    pieces.append(f"-fall_from [get_clocks clk1]")

                if "-to" in option_combination:
                    #FIXME: Maybe [get_clocks clk2] or {clk2}
                    pieces.append(f"-to [get_clocks clk2]")
                    
                if "-rise_to" in option_combination:
                    #FIXME: Maybe [get_clocks clk2] or {clk2}
                    pieces.append(f"-rise_to [get_clocks clk2]")
                    
                if "-fall_to" in option_combination:
                    #FIXME: Maybe [get_clocks clk2] or {clk2}
                    pieces.append(f"-fall_to [get_clocks clk2]")

                if "objects" in option_combination:
                    #FIXME: Do not make this random.
                    #Positional object list
                    obj = random.choice(CLOCKS + PORTS + PINS)
                    pieces.append(f"{obj}")

                #Join the options to create a proper command
                pieces = " ".join(pieces)
                #Add create_clock prerequisites
                pieces = ("create_clock -period 10 -name clk1 [get_ports clk1]\n"
                          "create_clock -period 20 -name clk2 [get_ports clk2]\n"
                          + pieces)
                commands.append(pieces)
            
    return commands

def generate_set_false_path():
    '''
    the from variants are all mutually exclusive
    the to variants are all mutually exclusive
    the through variants are all mutually exclusive
    -rise and -fall are alternatives to -rise_to and -fall_to. 
    
    setup, hold, rise, fall, reset_path, from(from_list), through(through_list), to(to_list)
    '''
    commands = [] #List containing all possible combinations of options
    
    optional_options = ["-setup", "-hold", "-rise", "-fall", "-reset_path", "-from", "-rise_from", "-fall_from", "-through", 
                        "-rise_through", "-fall_through", "-to", "-rise_to", "-fall_to"]
    
    from_list = ["[get_clocks clk1]", "u1", "[get_pins u1/pin1]", "[get_ports port1]"] #Clocks, instances, pins, ports
    through_list = ["u1", "[get_pins u1/out]", "[get_nets net1]"] #Instances, pins, nets
    to_list = ["[get_clocks clk2]", "u2", "[get_pins u2/pin2]", "[get_ports port2]"] #Clocks, instances, pins, ports
    
    from_options = ["-from", "-rise_from", "-fall_from"]
    through_options = ["-through", "-rise_through", "-fall_through"]
    to_options = ["-to", "-rise_to", "-fall_to"]
    
    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):
            
            from_count = sum(1 for from_opt in from_options if from_opt in option_combination)
            if from_count > 1:
                continue
            
            through_count = sum(1 for through_opt in through_options if through_opt in option_combination)
            if through_count > 1:
                continue
                
            to_count = sum(1 for to_opt in to_options if to_opt in option_combination)
            if to_count > 1:
                continue
            
            pieces = ["set_false_path"] #Temporary list to store command options  
            
            #FIXME: Don't make this random
            from_obj = random.choice(from_list)
            through_obj = random.choice(through_list)
            to_obj = random.choice(to_list)
            
            if "-setup" in option_combination:
                pieces.append("-setup")
                
            if "-hold" in option_combination:
                pieces.append("-hold")
                
            if "-rise" in option_combination:
                pieces.append("-rise")
                
            if "-fall" in option_combination:
                pieces.append("-fall")

            if "-reset_path" in option_combination:
                pieces.append("-reset_path")
                
            if "-from" in option_combination:
                pieces.append(f"-from {from_obj}")
                
            if "-rise_from" in option_combination:
                pieces.append(f"-rise_from {from_obj}")
                
            if "-fall_from" in option_combination:
                pieces.append(f"-fall_from {from_obj}")
                
            if "-through" in option_combination:
                pieces.append(f"-through {through_obj}")
                
            if "-rise_through" in option_combination:
                pieces.append(f"-rise_through {through_obj}")
                
            if "-fall_through" in option_combination:
                pieces.append(f"-fall_through {through_obj}")

            if "-to" in option_combination:
                pieces.append(f"-to {to_obj}")
                
            if "-rise_to" in option_combination:
                pieces.append(f"-rise_to {to_obj}")
                
            if "-fall_to" in option_combination:
                pieces.append(f"-fall_to {to_obj}")
                
            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk1 [get_pins clk1]\n"
                      "create_clock -period 20 -name clk2 [get_pins clk2]\n"
                      + pieces)
            commands.append(pieces)
            
    return commands

def generate_set_max_delay():
    '''
    -to variants are mutually exclusive from each other
    -from variants are mutually exclusive from each other
    -through variants are mutually exclusive from each other
    -rise, -fall can only be used with plain -to, -from, -through.
    '''
    commands = [] #List containing all possible combinations of options
    
    optional_options = ["-rise", "-fall", "-from", "-rise_from", "-fall_from", "-through", "-rise_through", "-fall_through", 
                        "-to", "-rise_to", "-fall_to", "-ignore_clock_latency", "-probe", "-reset_path"]
    
    from_list = ["[get_clocks clk1]", "u1", "[get_pins u1/pin1]", "[get_ports port1]"] #Clocks, instances, pins, ports
    through_list = ["u1", "[get_pins u1/out]", "[get_nets net1]"] #Instances, pins, nets
    to_list = ["[get_clocks clk2]", "u2", "[get_pins u2/pin2]", "[get_ports port2]"] #Clocks, instances, pins, ports
    
    from_options = ["-from", "-rise_from", "-fall_from"]
    through_options = ["-through", "-rise_through", "-fall_through"]
    to_options = ["-to", "-rise_to", "-fall_to"]

    for j in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, j):
            
            from_count = sum(1 for from_opt in from_options if from_opt in option_combination)
            if from_count > 1:
                continue
            
            through_count = sum(1 for through_opt in through_options if through_opt in option_combination)
            if through_count > 1:
                continue
                
            to_count = sum(1 for to_opt in to_options if to_opt in option_combination)
            if to_count > 1:
                continue
            delay = random.choice(DELAYS)
            pieces = ["set_max_delay", f"{delay}"] 
            
            #FIXME: Don't make this random
            from_obj = random.choice(from_list)
            through_obj = random.choice(through_list)
            to_obj = random.choice(to_list)
            
            if "-rise" in option_combination:
                pieces.append("-rise")
                
            if "-fall" in option_combination:
                pieces.append("-fall")
                
            if "-from" in option_combination:
                pieces.append(f"-from {from_obj}")
                
            if "-rise_from" in option_combination:
                pieces.append(f"-rise_from {from_obj}")
                
            if "-fall_from" in option_combination:
                pieces.append(f"-fall_from {from_obj}")
                
            if "-through" in option_combination:
                pieces.append(f"-through {through_obj}")
                
            if "-rise_through" in option_combination:
                pieces.append(f"-rise_through {through_obj}")
                
            if "-fall_through" in option_combination:
                pieces.append(f"-fall_through {through_obj}")

            if "-to" in option_combination:
                pieces.append(f"-to {to_obj}")
                
            if "-rise_to" in option_combination:
                pieces.append(f"-rise_to {to_obj}")
                
            if "-fall_to" in option_combination:
                pieces.append(f"-fall_to {to_obj}")
                
            if "-ignore_clock_latency" in option_combination:
                pieces.append("-ignore_clock_latency")
                
            if "-probe" in option_combination:
                pieces.append("-probe")
                
            if "-reset_path" in option_combination:
                pieces.append("-reset_path")

            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk1 [get_pins clk1]\n"
                        "create_clock -period 20 -name clk2 [get_pins clk2]\n"
                        + pieces)
            commands.append(pieces)
            
    return commands
    
def generate_set_min_delay():
    '''
    -to variants are mutually exclusive from each other
    -from variants are mutually exclusive from each other
    -through variants are mutually exclusive from each other
    -rise, -fall can only be used with plain -to, -from, -through.
    '''
    commands = [] #List containing all possible combinations of options
    
    optional_options = ["-rise", "-fall", "-from", "-rise_from", "-fall_from", "-through", "-rise_through", "-fall_through", 
                        "-to", "-rise_to", "-fall_to", "-ignore_clock_latency", "-probe", "-reset_path"]
    
    from_list = ["[get_clocks clk1]", "u1", "[get_pins u1/pin1]", "[get_ports port1]"] #Clocks, instances, pins, ports
    through_list = ["u1", "[get_pins u1/out]", "[get_nets net1]"] #Instances, pins, nets
    to_list = ["[get_clocks clk2]", "u2", "[get_pins u2/pin2]", "[get_ports port2]"] #Clocks, instances, pins, ports
    
    from_options = ["-from", "-rise_from", "-fall_from"]
    through_options = ["-through", "-rise_through", "-fall_through"]
    to_options = ["-to", "-rise_to", "-fall_to"]
    
    for j in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, j):
            
            from_count = sum(1 for from_opt in from_options if from_opt in option_combination)
            if from_count > 1:
                continue
            
            through_count = sum(1 for through_opt in through_options if through_opt in option_combination)
            if through_count > 1:
                continue
                
            to_count = sum(1 for to_opt in to_options if to_opt in option_combination)
            if to_count > 1:
                continue
            
            delay = random.choice(DELAYS)
            pieces = ["set_min_delay", f"{delay}"]
            
            #FIXME: Don't make this random
            from_obj = random.choice(from_list)
            through_obj = random.choice(through_list)
            to_obj = random.choice(to_list)
            
            if "-rise" in option_combination:
                pieces.append("-rise")
                
            if "-fall" in option_combination:
                pieces.append("-fall")
                
            if "-from" in option_combination:
                pieces.append(f"-from {from_obj}")
                
            if "-rise_from" in option_combination:
                pieces.append(f"-rise_from {from_obj}")
                
            if "-fall_from" in option_combination:
                pieces.append(f"-fall_from {from_obj}")
                
            if "-through" in option_combination:
                pieces.append(f"-through {through_obj}")
                
            if "-rise_through" in option_combination:
                pieces.append(f"-rise_through {through_obj}")
                
            if "-fall_through" in option_combination:
                pieces.append(f"-fall_through {through_obj}")

            if "-to" in option_combination:
                pieces.append(f"-to {to_obj}")
                
            if "-rise_to" in option_combination:
                pieces.append(f"-rise_to {to_obj}")
                
            if "-fall_to" in option_combination:
                pieces.append(f"-fall_to {to_obj}")
                
            if "-ignore_clock_latency" in option_combination:
                pieces.append("-ignore_clock_latency")
                
            if "-probe" in option_combination:
                pieces.append("-probe")
                
            if "-reset_path" in option_combination:
                pieces.append("-reset_path")

            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk1 [get_pins clk1]\n"
                        "create_clock -period 20 -name clk2 [get_pins clk2]\n"
                        + pieces)
            commands.append(pieces)
            
    return commands

def generate_set_multicycle_path():
    '''
    -setup, -hold are mutually exclusive
    -rise, -fall are mutually exclusive
    -from variants, -through variants, -to variants are mutually exclusive within each other
    '''
    commands = [] #List containing all possible combinations of options

    optional_options = ["-setup", "-hold", "-rise", "-fall", "-start", "-end", "-from", "-rise_from", "-fall_from", 
                        "-through", "-rise_through", "-fall_through", "-to", "-rise_to", "-fall_to", "-reset_path"]

    from_list = ["[get_clocks clk1]", "u1", "[get_pins u1/pin1]", "[get_ports port1]"] #Clocks, instances, pins, ports
    through_list = ["u1", "[get_pins u1/out]", "[get_nets net1]"] #Instances, pins, nets
    to_list = ["[get_clocks clk2]", "u2", "[get_pins u2/pin2]", "[get_ports port2]"] #Clocks, instances, pins, ports
    
    from_options = ["-from", "-rise_from", "-fall_from"]
    through_options = ["-through", "-rise_through", "-fall_through"]
    to_options = ["-to", "-rise_to", "-fall_to"]
    
    multiplier = random.choice(DIVISORS)
    for j in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, j):
            
            if "-start" in option_combination and "-end" in option_combination:
                continue
                
            from_count = sum(1 for from_opt in from_options if from_opt in option_combination)
            if from_count > 1:
                continue
                
            through_count = sum(1 for through_opt in through_options if through_opt in option_combination)
            if through_count > 1:
                continue
                    
            to_count = sum(1 for to_opt in to_options if to_opt in option_combination)
            if to_count > 1:
                continue

            pieces = ["set_multicycle_path", f"{multiplier}"]
                
            #FIXME: Don't make this random
            from_obj = random.choice(from_list)
            through_obj = random.choice(through_list)
            to_obj = random.choice(to_list)
                
            if "-setup" in option_combination:
                pieces.append("-setup")
                    
            if "-hold" in option_combination:
                pieces.append("-hold")
                    
            if "-rise" in option_combination:
                pieces.append("-rise")
                    
            if "-fall" in option_combination:
                pieces.append("-fall")
                    
            if "-start" in option_combination:
                pieces.append("-start")
                    
            if "-end" in option_combination:
                pieces.append("-end")
                    
            if "-from" in option_combination:
                pieces.append(f"-from {from_obj}")
                    
            if "-rise_from" in option_combination:
                pieces.append(f"-rise_from {from_obj}")
                    
            if "-fall_from" in option_combination:
                pieces.append(f"-fall_from {from_obj}")
                    
            if "-through" in option_combination:
                pieces.append(f"-through {through_obj}")
                    
            if "-rise_through" in option_combination:
                pieces.append(f"-rise_through {through_obj}")
                    
            if "-fall_through" in option_combination:
                pieces.append(f"-fall_through {through_obj}")

            if "-to" in option_combination:
                pieces.append(f"-to {to_obj}")
                    
            if "-rise_to" in option_combination:
                pieces.append(f"-rise_to {to_obj}")
                    
            if "-fall_to" in option_combination:
                pieces.append(f"-fall_to {to_obj}")
                    
            if "-reset_path" in option_combination:
                pieces.append("-reset_path")

            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk1 [get_pins clk1]\n"
                      "create_clock -period 20 -name clk2 [get_pins clk2]\n"
                      + pieces)
            commands.append(pieces)    
            
    return commands

def generate_get_cells():
    '''
    -of_objects and -hierarchcial are mutually exclusive
    '''
    commands = []
    optional_options = ["-hierarchical", "-hsc", "-filter", "-regexp", "-nocase", "-quiet", "-of_objects", "patterns"]
    
    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):
            
            #Constraint 1: -nocase is only valid with -regexp
            if "-nocase" in option_combination and "-regexp" not in option_combination:
                continue
            
            #Constraint 2: -hierarchical and -of_objects are mutually exclusive
            if "-hierarchical" in option_combination and "-of_objects" in option_combination:
                continue
                
            pieces = ["get_cells"]
            
            if "-hierarchical" in option_combination:
                pieces.append("-hierarchical")

            if "-hsc" in option_combination:
                #FIXME: Do not make this random.
                separator = random.choice(SEPARATOR)
                pieces.append(f"-hsc {separator}")

            if "-filter" in option_combination:
                #Filter expression with object type "cell"
                filter_type = choose_filter_type()
                expr = generate_filter(filter_type, "cell")
                pieces.append(f"-filter {expr}")

            if "-regexp" in option_combination:
                pieces.append("-regexp")
                
            if "-nocase" in option_combination:
                pieces.append("-nocase")

            if "-quiet" in option_combination:
                pieces.append("-quiet")

            if "-of_objects" in option_combination:
                #FIXME: Do not make this random.
                #The name or list of pins or nets.
                pin_net_list = random.choice(PINS + NETS)
                pieces.append(f"-of_objects {pin_net_list}")
                
            if "patterns" in option_combination:
                #A list of cell name patterns
                pattern = generate_pattern("cell")
                pieces.append(pattern)

            commands.append(" ".join(pieces))
    
    return commands
    
def generate_get_nets():
    '''
    -hierarchical, -of_objects mutually exclusive
    '''
    commands = []
    optional_options = ["-hierarchical", "-hsc", "-filter", "-regexp", "-nocase", "-quiet", "-of_objects", "patterns"]
    
    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):

            #Constraint 1: -nocase is only valid with -regexp
            if "-nocase" in option_combination and "-regexp" not in option_combination:
                continue
            
            #Constraint 2: -hierarchical and -of_objects are mutually exclusive
            if "-hierarchical" in option_combination and "-of_objects" in option_combination:
                continue
                
            pieces = ["get_nets"]
            
            if "-hierarchical" in option_combination:
                pieces.append("-hierarchical")

            if "-hsc" in option_combination:
                #FIXME: Do not make this random.
                separator = random.choice(SEPARATOR)
                pieces.append(f"-hsc {separator}")

            if "-filter" in option_combination:
                #Filter expression with object type "net"
                filter_type = choose_filter_type()
                expr = generate_filter(filter_type, "net")
                pieces.append(f"-filter {expr}")

            if "-regexp" in option_combination:
                pieces.append("-regexp")
                
            if "-nocase" in option_combination:
                pieces.append("-nocase")

            if "-quiet" in option_combination:
                pieces.append("-quiet")

            if "-of_objects" in option_combination:
                #FIXME: Do not make this random.
                #The name or list of pins or instances.
                pin_inst_list = random.choice(PINS + INSTANCES)
                pieces.append(f"-of_objects {pin_inst_list}")
                
            if "patterns" in option_combination:
                #FIXME: Do not make this random.
                #A list of net name patterns
                pattern = generate_pattern("net")
                pieces.append(pattern)

            commands.append(" ".join(pieces))
    
    return commands 

def generate_create_generated_clock():
    '''
    -source: a pin or port in the fanout of the master clock that is the source of the generated clock
    -edge_shift: An option not supported by OpenSTA
    '''
    commands = []
    optional_options = ["-name", "-master_clock", "-divide_by", "-multiply_by", "-edges", "-duty_cycle", "-invert", "-add"]
    exclusive_options = ["-divide_by", "-multiply_by", "-edges"]
    
    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):
            
            exclusive_count = sum(1 for opt in exclusive_options if opt in option_combination)
            if exclusive_count > 1:
                continue
            
            pieces = ["create_generated_clock"]
            
            pieces.append("[get_pins reg0/clk]")
            
            #Required option -source
            #FIXME: Do not make this random
            #Port or pin that will be the source clock
            master_pin = random.choice(["[get_ports src_clk]", "[get_pins mmcm0/clkin]"])
            pieces.append(f"-source {master_pin}")

            if "-name" in option_combination:
                pieces.append(f"-name clk_gen")
            
            if "-master_clock" in option_combination:
                #Just fix a single name 
                pieces.append(f"-master_clock [get_clocks src_clk]")
                
            if "-divide_by" in option_combination:
                #FIXME: Do not make this random.
                factor = random.choice(DIVISORS)
                pieces.append(f"-divide_by {factor}")
                
            if "-multiply_by" in option_combination:
                #FIXME: Do not make this random.
                factor = random.choice(DIVISORS)
                pieces.append(f"-multiply_by {factor}")
                
            if "-edges" in option_combination: 
                #FIXME: Do not make this random.
                edge_list = random.choice(EDGES)
                pieces.append(f"-edges {edge_list}")
                
            if "-duty_cycle" in option_combination:
                #FIXME: Do not make this random.
                duty_cycle = random.randint(0, 100)
                pieces.append(f"-duty_cycle {duty_cycle}")
                
            if "-invert" in option_combination:
                pieces.append("-invert")
                
            if "-add" in option_combination:
                pieces.append("-add")
                
            #Required Pin List    
            #pieces.append("reg0/clk")

            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name src_clk [get_ports src_clk]\n"
                      + pieces)
            commands.append(pieces)
            
    return commands

def generate_all_inputs():
    return ["all_inputs", "all_inputs -no_clocks"]

def generate_all_outputs():
    return ["all_outputs"]

def generate_set_clock_groups():
    '''
    Reference on how commands can look like: 
    https://www.intel.com/content/www/us/en/docs/programmable/683243/21-3/set-clock-groups-set-clock-groups.html
    -group is specified for each clock group 
    -name, -logically_exclusive, -physically_exclusive, -asynchronous, -allow_paths are optional flags
    '''
    
    commands = []
    optional_flags = ["-name", "-logically_exclusive", "-physically_exclusive", "-asynchronous", "-allow_paths"]
    
    for num_groups in [1, 2]: 
        
        for i in range(len(optional_flags) + 1):
            for option_combination in combinations(optional_flags, i):
                
                pieces = ["set_clock_groups"] 
                
                if "-name" in option_combination:
                    #Set the group name to "group_name"
                    pieces.append("-name group_name") 
                
                if "-logically_exclusive" in option_combination:
                    pieces.append("-logically_exclusive")
                    
                if "-physically_exclusive" in option_combination:
                    pieces.append("-physically_exclusive")
                
                if "-asynchronous" in option_combination:
                    pieces.append("-asynchronous")
                    
                if "-allow_paths" in option_combination:
                    pieces.append("-allow_paths")
                
                #FIXME: Do not make this random.
                if num_groups == 1: #Choose one clock group
                    group = random.choice(CLOCK_GROUP_1)
                    pieces.append(f"-group {group}")
                if num_groups == 2: #Choose two clock groups
                    groups = random.sample(CLOCK_GROUP_2, 2)
                    for clk_group in groups:
                        pieces.append(f"-group {clk_group}")

                #Join the options to create a proper command
                pieces = " ".join(pieces)
                #Add create_clock prerequisites
                pieces = ("create_clock -period 10 -name clk1 [get_ports clk1]\n"
                          "create_clock -period 10 -name clk2 [get_ports clk2]\n"
                          "create_clock -period 6 -name clk3 [get_ports clk3]\n"
                          "create_clock -period 2 -name clk4 [get_ports clk4]\n"
                          "create_clock -period 2 -name clk5 [get_ports clk5]\n"
                          + pieces)
                commands.append(pieces)
            
    return commands

def generate_all_clocks():
    return ["create_clock -period 10 -name clk1 [get_ports clk1]\ncreate_clock -period 10 -name clk2 [get_ports clk2]\nall_clocks"]

def generate_set_operating_conditions():
    '''
    -analysis_type single|bc_wc|on_chip_variation is supposed to be mutually exclusive
    'condition' is used for single
    '-min', '-max' are used for 'bc_wc' and 'on_chip_variation' 
    '''
    commands = []
    
    #-analysis_type single
    single_options = ["condition", "-library"]
    
    for i in range(len(single_options) + 1):
        for option_combination in combinations(single_options, i):
            pieces = ["set_operating conditions", "-analysis_type single"]
            
            if "condition" in option_combination:
                #FIXME: Do not make this random
                condition = random.choice(OPERATING_CONDITIONS)
                pieces.append(condition)
                
            if "-library" in option_combination:
                #FIXME: Do not make this random
                library = random.choice(LIBRARIES)
                pieces.append(f"-library {library}")
            
            commands.append(" ".join(pieces))
    
    analysis_type = ["bc_wc", "on_chip_variation"]
    multi_options = ["-min", "max", "-min_library", "-max_library"]
    
    for type in analysis_type: 
        for i in range(len(multi_options) + 1):
            for option_combination in combinations(multi_options, i):
                pieces = ["set_operating_conditions", f"-analysis_type {type}"]
                
                if "-min" in option_combination:
                    #FIXME: Do not make this random
                    min_condition = random.choice(OPERATING_CONDITIONS)
                    pieces.append(f"-min {min_condition}")
                    
                if "-max" in option_combination:
                    #FIXME: Do not make this random
                    max_condition = random.choice(OPERATING_CONDITIONS)
                    pieces.append(f"-max {max_condition}")
                    
                if "-min_libary" in option_combination:
                    #FIXME: Do not make this random
                    min_library = random.choice(LIBRARIES)
                    pieces.append(f"-min_library {min_library}")
                
                if "-max_libary" in option_combination:
                    #FIXME: Do not make this random
                    max_library = random.choice(LIBRARIES)
                    pieces.append(f"-max_library {max_library}")
                
                commands.append(" ".join(pieces))

def generate_all_registers():
    '''
    -cells, -data_pins, -clock_pins, -async_pins, -output_pins are mutually exclusive 
    '''
    commands = []
    all_options = ["-clock", "-cells", "-data_pins", "-clock_pins", "-async_pins", "-output_pins", "-level_sensitive", "-edge_triggered"]
    
    return_type_options = ["-cells", "-data_pins", "-clock_pins", "-async_pins", "-output_pins"]

    for i in range(len(all_options) + 1):
        for option_combination in combinations(all_options, i):
            
            #Check for mutual exclusion 
            exclusive_count = sum(1 for option in option_combination if option in return_type_options)
            if exclusive_count > 1:
                continue 
            
            if "-level_sensitive" in option_combination and "-edge_triggered" in option_combination:
                continue

            pieces = ["all_registers"]
            
            if "-clock" in option_combination:
                #FIXME: Do not make this random.
                clk = random.choice(CLOCKS)
                pieces.append(f"-clock {clk}")
                
            if "-level_sensitive" in option_combination:
                pieces.append("-level_sensitive")
                
            if "-edge_triggered" in option_combination:
                pieces.append("-edge_triggered")
                
            #Join the options to create a proper command
            pieces = " ".join(pieces)
            #Add create_clock prerequisites
            pieces = ("create_clock -period 10 -name clk1 [get_ports clk1]\n"
                      "create_clock -period 5 -name clk2 [get_ports clk2]\n"
                      + pieces)
            commands.append(pieces)
    
    return commands

def generate_set_disable_timing():
    '''
    From the OpenSTA reference: objects is "A list of instances, ports, pins, cells, cell/port, or library/cell/port" 
    '''
    
    commands = []
    optional_options = ["-from", "-to"] 
    
    for i in range(len(optional_options) + 1):
        for option_combination in combinations(optional_options, i):
            
            pieces = ["set_disable_timing"]
            
            #FIXME: Do not make this random.
            #Generate the required 'objects' argument 
            objects1 = random.choice(INSTANCES + PORTS + PINS + CELLS)
            objects2 = "/".join([random.choice(CELLS), random.choice(PORTS)])
            objects3 = "/".join([random.choice(LIBRARIES), random.choice(CELLS), random.choice(PORTS)])
            objects = random.choice([objects1, objects2, objects3])
            pieces.append(objects)
            
            from_port = None #To handle 'to' logic
            
            if "-from" in option_combination:
                #FIXME: Do not make this random.
                from_port = random.choice(PORTS)
                pieces.append(f"-from {from_port}") 
            
            if "-to" in option_combination:
                #FIXME: Do not make this random.
                #Ensure 'to_port' is different from 'from_port' if 'from_port' exists
                valid_ports = [p for p in PORTS if p != from_port]
                if not valid_ports:
                    valid_ports = PORTS
                to_port = random.choice(valid_ports)
                pieces.append(f"-to {to_port}") 
            
            commands.append(" ".join(pieces))
            
    return commands



    
#Reference
##################################################################################################################################################
GENERATORS = {
    "create_clock": generate_create_clock,
    "get_ports": generate_get_ports,
    "get_clocks": generate_get_clocks,
    "get_pins": generate_get_pins,
    "set_input_delay": generate_set_input_delay,
    "set_output_delay": generate_set_output_delay,
    "set_clock_latency": generate_set_clock_latency,
    "set_clock_uncertainty": generate_set_clock_uncertainty,
    "set_false_path": generate_set_false_path,
    "set_max_delay": generate_set_max_delay,
    "set_min_delay": generate_set_min_delay,
    "set_multicycle_path": generate_set_multicycle_path,
    "get_cells": generate_get_cells,
    "get_nets": generate_get_nets,
    "create_generated_clock": generate_create_generated_clock,
    "all_inputs": generate_all_inputs,
    "all_outputs": generate_all_outputs,
    "set_clock_groups": generate_set_clock_groups,
    "all_clocks": generate_all_clocks,
    "set_operating_conditions": generate_set_operating_conditions,
    "all_registers": generate_all_registers,
    "set_disable_timing": generate_set_disable_timing
}
    
    
#The generate function
##################################################################################################################################################
def generate_files(list_of_commands, batch):
    '''
    Args
    list_of_commands: list of commands we want to generate
    batch: batches for each command
    
    Returns
    .sdc files with commands specified by the input
    '''
    
    for command in list_of_commands:
        if command not in GENERATORS:
            print(f"Command '{command}' not supported. Skipped")
            continue
        
        output_dir = os.path.join(temp_output_path, str(command))
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(batch):
            gen_commands = GENERATORS[command]() #the list text contains all the commands
            for j in range(len(gen_commands)):
                filename = os.path.join(output_dir, f"{command}_{j}.sdc")
                with open(filename, "w") as f: 
                    f.write(gen_commands[j] + "\n")
        print(f"Generated {len(gen_commands)} {command} files")

#Main
##################################################################################################################################################
'''
command_list = ["create_clock", "set_input_delay", "set_output_delay", "set_clock_latency", "set_clock_uncertainty", 
                "set_false_path", "set_max_delay", "set_min_delay", "set_multicycle_path", "create_generated_clock", "all_inputs", 
                "all_outputs", "set_clock_groups", "all_clocks", "all_registers"] 
'''
command_list = ["set_false_path", "set_min_delay", "set_max_delay", "set_multicycle_path"]

generate_files(command_list, batch = 1)
