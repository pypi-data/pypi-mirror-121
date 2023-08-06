def malas():
    # Import function from module
    from .program_supplementals import program_requirements

    # Execute program_requirements
    program_requirements()

    # Import function from module
    from .connection_ssh import connection_futures
    from .connection_validator import connection_validator
    from .device_info_validator import device_info_validator
    from .configuration_type_validator import configuration_type_validator
    from .ip_addr_validator import ip_addr_validator, ip_addr_list_validator
    from .file_validator import device_info_list_validator, configuration_file_validator
    from .program_supplementals import exit_and_cleanup, enter_key_confirmation, powered_by, program_cancellation

    print("\n \  Malas (Multi-vendor automation leverage at slouching)")
    print("  \  Version 1.0 build 210926.0001 by Ade Destrianto")
    print("   \__________________________________________________________________\n")
    print("Please follow the instructions below. Thank you!\n")
    print("1. The device information list file\'s format is a set of three\n   that contains IP address, username (has privilege), and password separated by double colons \'::\'\n   per line in row formats, for example (Ignore the bracket):\n")
    print("   #==== Device Information List.txt ====#\n   #10.0.0.2::netadmin::password         #\n   #10.0.0.3::netadmin::password         #\n   #=====================================#\n")
    print("2. The configuration file\'s format is one command per line in row formats, for example (Ignore the bracket):\n")
    print("   #========= Configuration.txt =========#\n   #interface GigabitEthernet0/11        #\n   #description Guest_Networks           #\n   #IP address 192.168.1.1 255.255.255.0 #\n   #no shutdown                          #\n   #exit                                 #\n   #do write                             #\n   #=====================================#\n")
    print("3. What is \'Malas\'?")
    print("   Malas is a word from Bahasa Indonesia. The \'Malas\' word meaning is \'Lazy\' (Too inclined to avoid hard work.)\n")

    # Execute user confirmation to continue, then execute configuration_type_validator
    try:
        print("4. Shall we continue?\n   ", end="")
        # Execute enter_key_confirmation
        enter_key_confirmation()
        print("")
        configuration = configuration_type_validator()
        device = configuration[0]
        command = configuration[1]
        delay = configuration[2]
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # Execute program_cancellation
        print("")
        program_cancellation()

    # Execute file_validator
    try:
        print(" \  File validator")
        print("  \___________________________________________________________________")
        device_info_list = device_info_list_validator()
        command_list = configuration_file_validator(command)
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # Execute program_cancellation
        program_cancellation()

    # Execute device_info_validator
    try:
        print("\n \  Device information validator")
        print("  \___________________________________________________________________")
        ip_addr_list, username_list, password_list = device_info_validator(device_info_list)
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # Execute program_cancellation
        program_cancellation()

    # Execute ip_addr_validator
    try:
        print("\n \  IP address validator")
        print("  \___________________________________________________________________")
        # Verify the first try of validation with a flag. Return none if correct or return a new list if corrected
        ip_addr_list_fix = ip_addr_validator("PASS", ip_addr_list)
        # Execute ip_addr_list_validator
        ip_addr_list = ip_addr_list_validator(ip_addr_list_fix, ip_addr_list)
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # Execute program_cancellation
        program_cancellation()

    # Execute connection_validator
    try:
        print("\n \  Connection validator powered by", powered_by("pythonping"))
        print("  \___________________________________________________________________")
        # Verify the first try of validation with a flag. Return none if correct or return a new list if corrected
        ip_addr_list_fix = connection_validator("PASS", ip_addr_list)
        # Execute ip_addr_list_validator
        ip_addr_list = ip_addr_list_validator(ip_addr_list_fix, ip_addr_list)
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # Execute program_cancellation
        program_cancellation()

    # Execute user confirmation to execute connection_futures
    try:
        print("\n \  SSH remote configuration powered by", powered_by("netmiko"))
        print("  \___________________________________________________________________\n")
        print("Confirmation to proceed:")
        # Execute enter_key_confirmation
        enter_key_confirmation()
        connection_futures(device, command, delay, ip_addr_list, username_list, password_list, command_list)
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # Execute program_cancellation
        print("")
        program_cancellation()

    # Execute exit_and_cleanup
    exit_and_cleanup()