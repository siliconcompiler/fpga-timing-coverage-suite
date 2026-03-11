# Running the Syntax Suite

Follow the steps below to generate SDC files and run the syntax validation tests.


## 1. Generate SDC Files
First, generate the SDC constraints using the following command:

```bash
python generate_sdc.py --sdc_name <sdc_name>
```
This script creates SDCs compatible with the BLIF netlist files included in the suite. The generated files are saved to ```$Project_ROOT/auto_generated/sdc_files/<sdc_name>```. If the target directory already exists, the script will overwrite the existing files with the newly generated SDCs.

## 2. Execute the Syntax Suite
Once the SDCs are generated, run the test with the following command:

```bash
python run_syntax.py --sdc_name <sdc_name>
```
**Targeted Tests:** Specify the name of the constraint you wish to verify.

**Batch Tests:** Use ```--sdc_name all``` to run all tests defined in the ```SYNTAX_TESTS``` list within ```config.py```.

The script will run VPR until the packing stage with the provided SDCs and BLIF netlist. 

## 3. Viewing the Results
The script will keep track of any errors reported by VPR. All output files are saved to a directory named ```syntax_<sdc_name>```, located directly under the ```RESULTS_DIR``` defined in ```config.py```.

The script generates the following summary and log files: 

```error_log.txt```: Contains the SDC and error logs reported by VPR during execution.

```passed_test.txt```: Lists all SDCs that passed the syntax check successfully.

```summary.csv```: Provides a summary of how many SDCs have passed or failed the test. 