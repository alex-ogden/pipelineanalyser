import sys
import yaml
import pathlib

from os.path import exists

def opening_dialogue(pipeline_file):
    analysis_dialogue = f"Analysing file: {pipeline_file}"
    print(f"\n{analysis_dialogue}")
    for i in range(0, len(analysis_dialogue)):
        print("-", end="")
    print("\n\n")

def check_provided_file(file):
    yaml_exts = [ ".yml", ".yaml" ]
    pipeline_file_ext = pathlib.Path(file).suffix
    
    if pipeline_file_ext not in yaml_exts:
        print(f"Provided file extension [ {pipeline_file_ext} ] does not match one of: {yaml_exts}")
        exit(1)

    if not exists(pipeline_file):
        print(f"Provided file [ {pipeline_file} ] does not exist!")
        exit(1)

def check_for_triggers(value):
    print("Triggers:")
    print("---------")

    if value == "none":
        print("No defined triggers")
    else:
        for trigger_type in value:
            print(f"{trigger_type.capitalize()}:")
            for trigger_subtype in value[trigger_type]:
                print(f"\t{trigger_subtype.capitalize()}:")
                for trigger_val in value[trigger_type][trigger_subtype]:
                    print(f"\t\t{trigger_val}")
    
    print()

def check_for_resources(value):
    print("Resources:")
    print("----------")

    for resource_type in value:
        print(f"{resource_type.capitalize()}:")
        for resource_subtype in value[resource_type]:
            for resource_val in resource_subtype:
                print("\t{:<15}{:<15}".format(f"{resource_val.capitalize()}:", str(resource_subtype[resource_val])))
            print()

    print()

def check_for_parameters(value):
    print("Parameters:")
    print("-----------")

    for parameter in value:
        for sub_param in parameter:
            if type(parameter[sub_param]) is list:
                print(f"\t{sub_param.capitalize()}:")
                for param_val in parameter[sub_param]:
                    print(f"\t\t[-] {param_val}")
            else:
                print("\t{:<15}{:<15}".format(f"{sub_param.capitalize()}:", parameter[sub_param]))
        print()
    print()

def check_for_variables(value):
    print("Variables:")
    print("----------")

    for variable in value:
        for sub_var in variable:
            print("\t{:<15}{:<15}".format(f"{sub_var.capitalize()}:", variable[sub_var]))
        print()

    print()

def stage_analysis(value):
    print("Stages:")
    print("-------")

    for stage in value:
        for item in stage:
            if type(stage[item]) is list:
                for sub_item in stage[item]:
                    print(sub_item)
                    for element in sub_item:
                        print("\t\t{:<15}{:<15}".format(f"{element.capitalize()}:", sub_item[element]))
            else:
                print("\t{:<15}{:<15}".format(f"{item.capitalize()}:", stage[item]))
        print()
    print()

if __name__ == "__main__":
    pipeline_file = sys.argv[1]
    opening_dialogue(pipeline_file)

    # Ensure provided file exists and is yaml file
    check_provided_file(pipeline_file)

    with open(pipeline_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in data.items():
            # Triggers
            if key == "trigger":
                check_for_triggers(value)
            elif key == "resources":
                check_for_resources(value)
            elif key == "parameters":
                check_for_parameters(value)
            elif key == "variables":
                check_for_variables(value)
            elif key == "stages":
                stage_analysis(value)