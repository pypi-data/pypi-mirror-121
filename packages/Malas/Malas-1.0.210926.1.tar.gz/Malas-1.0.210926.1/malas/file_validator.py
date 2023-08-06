import os

def command_type_validator(flag, input_data):
    # Command type send_config_set and Device information list are treatable in the same manner
    if (flag == "DEVICE") or (flag == "CONFIG_2"):
        # Pass the value
        return input_data
    # Command type send_command only accepting one command
    elif (flag == "CONFIG_1") and (len(input_data) == 1):
        # Pass the value
        return input_data[0].rstrip("\n")
    # Command type send_command not accepting multiple commands
    else:
        print("FAIL: There are " + str(len(input_data)) + " commands found in the configuration file")
        print("FAIL: Please use only one command for command type \'send_command\' and try again!")
        # Repeat execute configuration_file_validator with the same flag and then pass the value
        return configuration_file_validator(flag)

def file_validator(flag, input_file):
    # File exist is accepted
    if os.path.isfile(input_file) == True:
        print("PASS: \'" + input_file + "\' found")
        # Open the file with read permission
        with open(input_file, "r") as file:
            # Read the file from the beginning of the file
            file.seek(0)
            # Verify the configuration file's content according to the command type flag and then pass the value
            return command_type_validator(flag, file.readlines())
    # File not exist is not accepted
    else:
        print("FAIL: \'{}\' not found!".format(input_file))
        if flag == "DEVICE":
            # Repeat execute device_info_list_validator and then pass the value
            return device_info_list_validator()
        elif (flag == "CONFIG_1") or (flag == "CONFIG_2"):
            # Repeat execute configuration_file_validator with the same flag and then pass the value
            return configuration_file_validator(flag)

def device_info_list_validator():
    # Prompt user for
    device_info_list = input("\nEnter the path and the name of the device information list file: ")
    # Verify the file's existence with a flag and then pass the value
    return file_validator("DEVICE", device_info_list)

def configuration_file_validator(command):
    # Flag the configuration file based on the command type
    if command == "send_command":
        flag = "CONFIG_1"
    elif command == "send_config_set":
        flag = "CONFIG_2"
    # When configuration_file_validator executed by command_type_validator; Use the same flag
    else:
        flag = command
    # Prompt user for
    configuration_file = input("\nEnter the path and the name of the configuration file: ")
    # Verify the file's existence with a flag and then pass the value
    return file_validator(flag, configuration_file)