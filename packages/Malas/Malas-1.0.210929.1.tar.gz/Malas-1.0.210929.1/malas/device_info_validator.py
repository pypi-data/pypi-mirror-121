import re

# Import function from module
from .file_validator import device_info_list_validator

def is_complete(device_info_elements):
    # Device information must have 3 elements
    result = len(device_info_elements) == 3
    # Pass the value
    return result

def is_empty(device_info_elements):
    if is_complete(device_info_elements):
        regex_results = []
        # No-empty element patterns
        regex_results.append(not re.match(r"^.{0}$", device_info_elements[0]))
        regex_results.append(not re.match(r"^.{0}$", device_info_elements[1]))
        regex_results.append(not re.match(r"^.{0}$", device_info_elements[2]))
        # When all patterns match, all Results should be True
        if all(regex_results):
            result = True
        else:
            result = False
        # Pass the value
        return result
    # Invalid device information if the elements are not 3
    else:
        # Pass the value
        return False

def device_info_validator(device_info_list):
    # Progress dot
    print("\nValidating device(s) information. Please wait", end = "", flush = True)
    # An empty device information list is not accepted
    if len(device_info_list) == 0:
        print("\n\nFAIL: The device information list is empty!")
        # Repeat execute device_info_validator and then pass the value
        return device_info_validator(device_info_list_validator())
    else:
        # Initial variables
        ip_addr_list = []
        username_list = []
        password_list = []
        invalid_formats = []
        results = []
        # Loop for every device information in the list
        for device_info in device_info_list:
            # Strip newline at the end of the device information then split the device information into IP address, username, and password format
            device_info_elements = device_info.rstrip("\n").split("::")
            # Device information must have an IP address, a username, and a password
            if is_empty(device_info_elements):
                results.append("PASS")
                # Split elements of the device information and store them in their new group list
                ip_addr_list.append(device_info_elements[0])
                username_list.append(device_info_elements[1])
                password_list.append(device_info_elements[2])
                # Progress dot
                print(".", end = "", flush = True)
                continue
            # Device information that is not complete or contains an empty IP address or/and username or/and password is invalid
            else:
                results.append("FAIL")
                invalid_formats.append(device_info.rstrip("\n"))
                # Progress dot
                print(".", end = "", flush = True)
                continue
        # Unacceptable results
        if "FAIL" in results:
            # Initial variables
            obscured_formats = []
            # Loop for every device information in the list
            for device_info in invalid_formats:
                # Obscure device information
                obscured_info = re.sub(r"([^::])", "*", device_info, 0, re.MULTILINE)
                # Store obscured device information in the new list
                obscured_formats.append(obscured_info)
            print("\n\nFAIL: Invalid device(s) information format: " + str(obscured_formats)[1:-1])
            print("FAIL: Please correct the device information list and try again!")
            # Repeat execute device_info_validator and then pass the value
            return device_info_validator(device_info_list_validator())
        # Acceptable results
        else:
            print("\n\nPASS: The device information list is valid")
            # Pass these values
            return ip_addr_list, username_list, password_list