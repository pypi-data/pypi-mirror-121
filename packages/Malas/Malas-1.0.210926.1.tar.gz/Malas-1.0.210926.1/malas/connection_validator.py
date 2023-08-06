import os
import time
import concurrent.futures

# Import function from module
from .ip_addr_validator import ip_addr_validator
from .file_validator import device_info_list_validator
from .device_info_validator import device_info_validator
from .program_supplementals import enter_key_only, exception_translator, program_cancellation

# Import function from 3rd party module
from pythonping import ping

def connection_ping(ip):
    try:
        # Strip newline at the end of IP address
        ip_addr = ip.rstrip("\n")
        # Ping every 3 seconds for 10 times
        replies = ping(ip_addr, count = 1, interval = 1)
        # No reply is not accepted
        # 3 = SuccessOn.All = All pings are replies
        if replies.success(3) == False:
            # Progress dot
            print(".", end = "", flush = True)
            # Pass values to threading result
            return "FAIL3", ip_addr
        # Less than 6 replies are not accepted
        # 2 = SuccessOn.Most = The total reply is half of the total ping + 1
        elif replies.success(2) == False:
            # Progress dot
            print(".", end = "", flush = True)
            # Pass values to threading result
            return "FAIL2", ip_addr
        # All pings are replies or more than 5 replies are accepted
        else:
            # Progress dot
            print(".", end = "", flush = True)
            # Pass values to threading result
            return "PASS", ip_addr
    except:
        # Progress dot
        print(".", end="", flush=True)
        # Execute exception_translator
        exception_explained = exception_translator()
        # Pass values to threading result
        return "FAIL4", exception_explained

def connection_validator(flag, ip_addr_list):
    # Progress dot with threading capability
    print("\nConcurrently determining per", min(32, os.cpu_count() + 4), "IP addresses. Please wait", end = "", flush = True)
    # Ping-threading stopwatch start
    threading_start = time.time()
    # Ping-threading process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute threading process
        try:
            # Initial variables
            threads = []
            thread_results = []
            # Loop for every IP address in the list
            for ip_addr in ip_addr_list:
                # Execute ping test for every IP address in the list concurrently
                threads.append(executor.submit(connection_ping, ip = ip_addr))
            # Loop for every result from ping-threading process
            for thread in concurrent.futures.as_completed(threads):
                thread_results.append(thread.result())
        # Cancel the remaining threads by keyboard (e.g. CTRL+C)
        except KeyboardInterrupt:
            executor.shutdown(wait = True, cancel_futures = True)
            # Execute program_cancellation
            program_cancellation()
    # Ping-threading stopwatch end
    print("\n\nPing-threading processed for:", "%.2f" % (time.time() - threading_start), "secs")
    # Loop for every result from ping-threading process results
    if bool([True for result in thread_results if "PASS" not in result[0]]) == True:
        # Expect the raised exception flag
        if "FAIL4" in thread_results[0][0]:
            try:
                # Print the raised exception error messages values
                print("\nFAIL: " + thread_results[0][1][0] + "\n\n" + thread_results[0][1][1])
                # Execute user confirmation to retry connection test
                print("\nPress \'Enter\' to retry connection test or \'CTRL+C\' to end the program", end="", flush=True)
                # Expect the user to press Enter key
                enter_key_only()
                # Repeat execute connection_validator with a flag
                connection_validator("FAIL", ip_addr_list)
            except KeyboardInterrupt:
                # Execute program_cancellation
                print("")
                program_cancellation()
        else:
            # Loop for every result from ping-threading process results. All pings are replies or more than 5 replies are accepted
            print("PASS: Reachable IP address(es): " + str([result[1] for result in thread_results if "PASS" in result[0]])[1:-1])
            # Loop for every result from ping-threading process results. Less than 6 replies are not accepted
            print("FAIL: Flapping IP address(es): " + str([result[1] for result in thread_results if "FAIL2" in result[0]])[1:-1])
            # Loop for every result from ping-threading process results. No reply is not accepted
            print("FAIL: Timed IP address(es): " + str([result[1] for result in thread_results if "FAIL3" in result[0]])[1:-1])
            print("FAIL: Please remove flapping/timed IP address(es) in the list and try again!")
            # Repeat execute device_info_list_validator then device_info_validator then ip_addr_validator with a fail flag and then connection_validator with a flag
            return connection_validator("FAIL", ip_addr_validator("FAIL", device_info_validator(device_info_list_validator())[0]))
    # All pings are replies or more than 5 replies are accepted
    else:
        # IP address list with correction flag
        if flag == "FAIL":
            print("PASS: IP address(es) in the list is reachable")
            # Pass the value
            return ip_addr_list
        # IP address list with no correction flag
        elif flag == "PASS":
            print("PASS: IP address(es) in the list is reachable")