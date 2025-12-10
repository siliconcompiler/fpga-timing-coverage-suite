# SDC Syntax

## Timing Constraints

### create_clock

```
create_clock -period <float>
            (-name <string>)?
            (-waveform {<float> <float>})?
            (-add)?
            (<pin_list>)?
```

### create_generated_clock

```
create_generated_clock (-name <string>)?
                        -source <pin>
                       (-master_clock <clock>)?
                       (-divide_by <float>)?
                       (-multiply_by <float>)?
                       (-add)?
                       <pin_list>
```

Note: There are other options. Should confirm if we want to support them.

### set_clock_groups

```
set_clock_groups (-name <string>)?
                 (-logically_exclusive)?
                 (-physically_exclusive)?
                 (-asynchronous)?
                 (-allow_paths)?
                 -group <clocks>
```

Note: VTR supports a flag called "-exclusive". Should check if we want this or not.

### set_false_path

```
set_false_path (-setup)?
               (-hold)?
               (-rise)?
               (-fall)?
               (-from <from_list>)?
               (-to <to_list>)?
               (-through <through_list>)?
```

Note: There are some extra to discuss.

### set_max_delay

```
set_max_delay (-rise)?
              (-fall)?
              (-from <from_list>)?
              (-to <to_list>)?
              (-through <through_list>)?
              <delay: float>
```

### set_min_delay

```
set_min_delay (-rise)?
              (-fall)?
              (-from <from_list>)?
              (-to <to_list>)?
              (-through <through_list>)?
              <delay: float>
```

### set_multicycle_path

```
set_multicycle_path (-setup)?
                    (-hold)?
                    (-rise)?
                    (-fall)?
                    (-from <from_list>)?
                    (-to <to_list>)?
                    <path_multiplier: float>
```

### set_input_delay

```
set_input_delay (-rise)?
                (-fall)?
                (-max)?
                (-min)?
                (-clock <clock>)?
                (-clock_fall)?
                <delay: float>
                <pin/port list>
```

### set_output_delay

```
set_output_delay (-rise)?
                 (-fall)?
                 (-max)?
                 (-min)?
                 (-clock <clock>)?
                 (-clock_fall)?
                 <delay: float>
                 <pin/port list>
```

### set_clock_uncertainty

```
set_clock_uncertainty (-from <clock>)?
                      (-to <clock>)?
                      (-rise)?
                      (-fall)?
                      (-setup)?
                      (-hold)?
                      <uncertainty: float>
                      <clocks, ports, pins>
```

### set_clock_latency

```
set_clock_latency (-source)?
                  (-rise)?
                  (-fall)?
                  (-min)?
                  (-max)?
                  <latency: float>
                  <clocks, ports, pins>
```

Note: VTR has `-early` and `-late` flags. Should decide if we want to support.

### set_disable_timing

```
set_disable_timing (-from <from_port>)?
                   (-to <to_port>)?
                   <cell, instance, port, pin>
```

## Query

### get_ports

```
get_ports (-regexp)?
          (-nocase)?
          (-quiet)?
          <patterns>
```

### get_clocks

```
get_clocks (-regexp)?
           (-nocase)?
           (-quiet)?
           <patterns>
```

### get_pins

```
get_pins (-regexp)?
         (-nocase)?
         (-quiet)?
         <patterns>
```

### get_cells

```
get_cells (-regexp)?
          (-nocase)?
          (-quiet)?
          <patterns>
```

Note: OpenSTA has special flags for hierarchical matches. Should consider adding.

### get_nets

```
get_nets (-regexp)?
         (-nocase)?
         (-quiet)?
         <patterns>
```

Note: OpenSTA has special flags for hierarchical matches. Should consider adding.

### all_inputs

```
all_inputs (-no_clocks)?
```

### all_outputs

```
all_outputs
```

### all_clocks

```
all_clocks
```
