import os
import sys
import time
import random
import string
import datetime
import concurrent.futures

# Import function from module
from .program_supplementals import exit_and_cleanup, enter_key_only, exception_translator

# Import function from 3rd party module
from netmiko import ConnectHandler

def file_output(ssh_results, ssh_success, ssh_failed):
    # Get the current path of the running Python file
    current_path = os.path.dirname(os.path.realpath(__file__))
    # Prompt user for
    target_path = input("\nEnter the target path or leave it blank to set the default path [" + current_path + "]: ")
    # If target_path is blank, fill it with a default directory name
    if bool(target_path == ""):
        target_path = "Malas_SSH_outputs"
    try:
        # Create a new directory if not exists yet on the target path to contains all SSH output file(s)
        if bool(os.path.exists(target_path)) == False:
            os.makedirs(target_path)
        # Loop for every result in the list
        for ssh_result in ssh_results:
            # Give a unique key for the output file
            unique_key = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            # Get the current date and time
            present = datetime.datetime.now().strftime("_on_%Y-%m-%d_at_%H.%M")
            # Merge target path with the file name and its extension
            complete_path = os.path.join(target_path, ssh_result[0] + present + "_[" + unique_key + "].txt")
            # Open the file with write permission
            with open(complete_path, "w") as file:
                # Write the SSH outputs to the file
                file.write("%s" % ssh_result[1])
        # SSH attempt results
        print("\nSSH remote configuration success: " + str(ssh_success) + " host(s)")
        print("SSH remote configuration failed: " + str(ssh_failed) + " host(s)")
        # target_path is the default directory name
        if bool(target_path == "Malas_SSH_outputs"):
            print("\nPASS: The SSH output file(s) are stored in the path \'" + current_path + "\' inside the directory \'" + target_path + "\' successfully")
        # target_path is user-defined
        else:
            print("\nPASS: The SSH output file(s) are stored in the path \'" + target_path + "\' successfully")
        print("EXIT: Please review the SSH output file(s) to confirm the configured configuration, thank you!")
    except:
        # Execute exception_translator
        exception_explained = exception_translator()
        # Print the raised exception error messages values
        print("\nFAIL: " + exception_explained[0] + ":\n" + exception_explained[1])
        # Repeat execute file_output and then pass these values
        file_output(ssh_results, ssh_success, ssh_failed)

def thread_processor(threads):
    # Initial variables
    ssh_results = []
    ssh_success = 0
    ssh_failed = 0
    # Loop for every result from ssh-threading process
    for thread in threads:
        # Store the thread results values
        ssh_result = thread.result()
        # Failed SSH attempts contain 2 values in tuple formats
        if isinstance(ssh_result[1], tuple):
            # Merge raised exception error name and explanation
            result_concatenated = "FAIL: " + ssh_result[1][0] + "\n\n" + ssh_result[1][1]
            # Store the raised exception error messages values in the same index
            ssh_results.append((ssh_result[0], result_concatenated))
            # Increment of failed SSH attempts
            ssh_failed += 1
        else:
            # Store the raised exception error messages values
            ssh_results.append(ssh_result)
            # Increment of success SSH attempts
            ssh_success += 1
    try:
        # Execute user confirmation to create output file(s)
        print("\nPress \'Enter\' to create the SSH output file(s) or \'CTRL+C\' to end the program", end = "", flush = True)
        # Expect the user to press Enter key
        enter_key_only()
        # Execute file_output
        file_output(ssh_results, ssh_success, ssh_failed)
    # Stop process by keyboard (e.g. CTRL+C)
    except KeyboardInterrupt:
        # SSH attempt results
        print("\n\nSSH remote configuration success: " + str(ssh_success) + " host(s)")
        print("SSH remote configuration failed: " + str(ssh_failed) + " host(s)")
        print("\nEXIT: Please review the SSH outputs to confirm the configured configuration, thank you!")
        # Execute exit_and_cleanup
        exit_and_cleanup()

def output_processor(output, command, stopwatch):
    # Remote configuration stopwatch end
    ssh_processed = "\'%.2f\'" % (time.time() - stopwatch) + " secs"
    # Process the output according to its command type
    if command == "send_command":
        # No output process
        final_output = output
    elif command == "send_config_set":
        # Split output into a list
        disintegrate_output = output.split("\n")
        # Remove the unnecessary lines
        final_output = "\n".join(disintegrate_output[1:-1])
    # Pass these values
    return final_output, ssh_processed

def connection_ssh(dev, cmd, gdf, ip, usr, pwd, cfg):
    # Strip newline at the end of device type, command type, IP address, username, and password
    device = dev.rstrip("\n")
    command = cmd.rstrip("\n")
    ip_addr = ip.rstrip("\n")
    username = usr.rstrip("\n")
    password = pwd.rstrip("\n")
    try:
        # Remote configuration stopwatch start
        stopwatch = time.time()
        # Define the device type, the credential information, and the delay value to log in to the remote host
        session = {
            "device_type": device,
            "host": ip_addr,
            "username": username,
            "password": password,
            "global_delay_factor": gdf
        }
        # SSH to the remote host
        remote = ConnectHandler(**session)
        # Execute every command in the configuration file according to its command type
        if command == "send_command":
            output = remote.send_command(cfg)
            # Execute output_processor and retrive values
            final_output, ssh_processed = output_processor(output, command, stopwatch)
        elif command == "send_config_set":
            output = remote.send_config_set(cfg)
            # Execute output_processor and retrive values
            final_output, ssh_processed = output_processor(output, command, stopwatch)
        # Output's bracket and print the output
        print("\n\n \  Remote host \'" + ip_addr + "\' processed for " + ssh_processed + "\n  \___________________________________________________________________\n\n" + final_output, end="")
        # Pass values to threading result
        return ip_addr, final_output
    except:
        # Execute exception_translator
        exception_explained = exception_translator()
        # Output's bracket and print the output
        print("\n\n \  Remote host \'" + ip_addr + "\' failed to configure\n  \___________________________________________________________________\n\nFAIL: " + exception_explained[0] + "\n\n" + exception_explained[1], end = "")
        # Pass values to threading result
        return ip_addr, exception_explained

def connection_futures(device, command, delay, ip_addr_list, username_list, password_list, command_list):
    # Execute connection_ssh. Progress dot with threading capability
    print("\nConcurrently configuring per", min(32, os.cpu_count() + 4), "hosts. Please wait", end = "", flush = True)
    # SSH-threading stopwatch start
    threading_start = time.time()
    # Suppress raised exception error messages outputs
    sys.stderr = os.devnull
    # SSH-threading process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Initial variables
        threads = []
        ssh_attempts = 0
        # Loop for every IP address, username, and password in the list
        for ip_addr, username, password in zip(ip_addr_list, username_list, password_list):
            # Increment of SSH attempts
            ssh_attempts += 1
            # Execute configuration over SSH for every IP address, username, and password in the list concurrently
            threads.append(executor.submit(connection_ssh, dev = device, cmd = command, gdf = delay, ip = ip_addr, usr = username, pwd = password, cfg = command_list))
            # Progress dot
            print(".", end = "", flush = True)
    # Unsuppress raised exception error messages outputs
    sys.stderr = sys.__stderr__
    print("\n\n \  Completed")
    print("  \___________________________________________________________________\n")
    # SSH attempt results and ping-threading stopwatch end
    print("SSH-threading for " + str(ssh_attempts) + " host(s) processed for:", "%.2f" % (time.time() - threading_start), "secs")
    # Execute thread_processor
    thread_processor(threads)