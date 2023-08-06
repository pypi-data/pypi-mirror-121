import re

# Import function from module
from .program_supplementals import input_option, powered_by

def supported_device_types():
    # For supported device types information, please visit 'https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py' in CLASS_MAPPER_BASE dictionary
    supported_device_types = ["a10", "accedian", "adtran_os", "alcatel_aos", "alcatel_sros", "allied_telesis_awplus", "apresia_aeos", "arista_eos", "aruba_os", "aruba_osswitch", "aruba_procurve", "avaya_ers", "avaya_vsp", "broadcom_icos", "brocade_fos", "brocade_fastiron", "brocade_netiron", "brocade_nos", "brocade_vdx", "brocade_vyos", "checkpoint_gaia", "calix_b6", "cdot_cros", "centec_os", "ciena_saos", "cisco_asa", "cisco_ftd", "cisco_ios", "cisco_nxos", "cisco_s300", "cisco_tp", "cisco_wlc", "cisco_xe", "cisco_xr", "cloudgenix_ion", "coriant", "dell_dnos9", "dell_force10", "dell_os6", "dell_os9", "dell_os10", "dell_powerconnect", "dell_isilon", "dlink_ds", "endace", "eltex", "eltex_esr", "enterasys", "ericsson_ipos", "extreme", "extreme_ers", "extreme_exos", "extreme_netiron", "extreme_nos", "extreme_slx", "extreme_vdx", "extreme_vsp", "extreme_wing", "f5_ltm", "f5_tmsh", "f5_linux", "flexvnf", "fortinet", "generic", "generic_termserver", "hp_comware", "hp_procurve", "huawei", "huawei_smartax", "huawei_olt", "huawei_vrpv8", "ipinfusion_ocnos", "juniper", "juniper_junos", "juniper_screenos", "keymile", "keymile_nos", "linux", "mikrotik_routeros", "mikrotik_switchos", "mellanox", "mellanox_mlnxos", "mrv_lx", "mrv_optiswitch", "netapp_cdot", "netgear_prosafe", "netscaler", "nokia_sros", "oneaccess_oneos", "ovs_linux", "paloalto_panos", "pluribus", "quanta_mesh", "rad_etx", "raisecom_roap", "ruckus_fastiron", "ruijie_os", "sixwind_os", "sophos_sfos", "supermicro_smis", "tplink_jetstream", "ubiquiti_edge", "ubiquiti_edgerouter", "ubiquiti_edgeswitch", "ubiquiti_unifiswitch", "vyatta_vyos", "vyos", "watchguard_fireware", "zte_zxros", "yamaha"]
    # Pass the value
    return supported_device_types

def command_types():
    # For more information about these command types, please visit 'https://ktbyers.github.io/netmiko/docs/netmiko/index.html#netmiko.BaseConnection.send_command' and 'https://ktbyers.github.io/netmiko/docs/netmiko/index.html#netmiko.BaseConnection.send_config_set'
    command_types = ["send_command", "send_config_set"]
    # Pass the value
    return command_types

def device_type_check():
    # Prompt user for
    device_type = input("Enter the name of the device type: ")
    # Device type match is accepted
    if device_type in supported_device_types():
        print("PASS: \'{}\' is supported".format(device_type), "\n")
        # Pass the value
        return device_type
    # Device type not match is not accepted
    else:
        print("FAIL: \'{}\' is not supported!".format(device_type), "\n")
        # Repeat execute configuration_type_validator and then pass the value
        return device_type_check()

def command_type_check():
    # Prompt user for
    command_type = input("Enter the name of the command type: ")
    # Command type match is accepted
    if command_type in command_types():
        print("PASS: \'{}\' is valid".format(command_type), "\n")
        # Pass the value
        return command_type
    # Command type not match is not accepted
    else:
        print("FAIL: \'{}\' is invalid!".format(command_type), "\n")
        # Repeat execute configuration_type_validator and then pass the value
        return command_type_check()

def global_delay_factor():
    # Prompt user for
    delay = input("Enter the delay value [0.1–100] or press \'Enter\' for default value [1.2]: ")
    # Zero value is not accepted
    if bool(re.match(r"(^(0|00)[.](0|00)$|^00$|^0$)", delay)):
        print("FAIL: \'{}\' is invalid!".format(delay), "\n")
        # Repeat execute global_delay_factor and then pass the value
        return global_delay_factor()
    # Value 0.1–100 and empty string 'enter key' is accepted
    elif bool(re.match(r"((^([1-9]|[0-9][0-9])[.]([0-9]|[0-9][0-9])$)|(^100$)|(^[0-9][0-9]$)|(^[1-9]$))", delay)) or bool(delay == ""):
        # Default value
        if (not delay) or (delay == "1.2") or (delay == "1.20"):
            print("PASS: global_delay_factor: default\n")
            # Pass the default value
            return float(1.2)
        # The default value of netmiko
        elif (delay == "1") or (delay == "1.0") or (delay == "1.00"):
            print("PASS: global_delay_factor: netmiko's default\n")
            # Pass the netmiko's value
            return float(delay)
        # User value
        else:
            print("PASS: global_delay_factor: \'" + str(float(delay)) + "\'\n")
            # Pass the user value
            return float(delay)
    # A value greater than 100, trailing and leading zero more than 2 is not accepted
    else:
        print("FAIL: \'{}\' is invalid!".format(delay), "\n")
        # Repeat execute global_delay_factor and then pass the value
        return global_delay_factor()

def configuration_type_validator():
    print(" \  Configuration type validator")
    print("  \___________________________________________________________________\n")
    print("[A] Enter the device type and the command type")
    print("[B] Show the list of supported device type")
    print("[C] Show the list of supported command type")
    print("\nPlease choose one of the options above or Press \'CTRL+C\' to abort the program: ", end="", flush=True)
    # Capture any inputs and suppress the output
    key = input_option()
    # Compare the chosen option with the available options
    if (key == "a") or (key == "A"):
        print("")
        # Verify the support of the device type and validity of the command type
        device_type = device_type_check()
        command_type = command_type_check()
        # If the user has chosen send_command, use the netmiko's global_delay_factor default value
        if bool(command_type == "send_command"):
            return device_type, command_type, float(1.0)
        # If the user has chosen send_config_set, execute global_delay_factor
        elif bool(command_type == "send_config_set"):
            return device_type, command_type, global_delay_factor()
    elif (key == "b") or (key == "B"):
        print("\n \  Supported device types are powered by", powered_by("netmiko"))
        print("  \___________________________________________________________________\n")
        # Loop for every device type in the supported device types list
        for device_type in supported_device_types():
            print(">", device_type)
        print("")
        # Repeat execute configuration_type_validator and then pass the value
        return configuration_type_validator()
    elif (key == "c") or (key == "C"):
        print("\n \  Command types are powered by", powered_by("netmiko"))
        print("  \___________________________________________________________________\n")
        print(">", command_types()[0] + "\n  TL;DR      : Send one command and wait until the information is entirely received.\n  Explanation: Use to execute a command on the SSH channel to show information.\n               This method will keep waiting to receive data until the network device prompt is detected.")
        print(">", command_types()[1] + "\n  TL;DR      : Send one or a set of commands in configuration mode.\n  Explanation: Use to send configuration commands down the SSH channel and will be executed one after the other.\n               Automatically exits/enters configuration mode.")
        print("  >> global_delay_factor\n     TL;DR      : Set a multiplication value for additional delays in netmiko's command execution.\n     Explanation: Multiplication factor affecting Netmiko delays with the default value is set on \'1.0\'.\n                  The higher value will result in the program being slow in the process hence too long to complete.\n                  This program wisely set the default value on \'1.2\'.\n")
        # Repeat execute configuration_type_validator and then pass the value
        return configuration_type_validator()
    else:
        print("\nFAIL: Please choose \'A\' or \'B\' or \'C\'!\n")
        # Repeat execute configuration_type_validator and then pass the value
        return configuration_type_validator()