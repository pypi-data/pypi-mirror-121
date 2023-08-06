import re

# Import function from module
from .file_validator import device_info_list_validator
from .device_info_validator import device_info_validator

def is_octet(ip_octets):
    # IP address must have 4 octets
    result = len(ip_octets) == 4
    # Pass the value
    return result

def is_empty(ip_octets):
    if is_octet(ip_octets):
        regex_results = []
        # No-empty octet patterns
        regex_results.append(not re.match(r"^.{0}$", ip_octets[0]))
        regex_results.append(not re.match(r"^.{0}$", ip_octets[1]))
        regex_results.append(not re.match(r"^.{0}$", ip_octets[2]))
        regex_results.append(not re.match(r"^.{0}$", ip_octets[3]))
        # When all patterns match, all Results should be True
        if all(regex_results):
            result = True
        else:
            result = False
        # Pass the value
        return result
    # Invalid IP address if the octets are not 4
    else:
        # Pass the value
        return False

def is_digit(ip_octets):
    if is_octet(ip_octets):
        regex_results = []
        # Octet patterns contain no other than digit
        regex_results.append(not re.match(r"(?!^\d+$)^.+$", ip_octets[0]))
        regex_results.append(not re.match(r"(?!^\d+$)^.+$", ip_octets[1]))
        regex_results.append(not re.match(r"(?!^\d+$)^.+$", ip_octets[2]))
        regex_results.append(not re.match(r"(?!^\d+$)^.+$", ip_octets[3]))
        # When all patterns match, all Results should be True
        if all(regex_results):
            result = True
        else:
            result = False
        # Pass the value
        return result
    # Invalid IP address if the octets are not 4
    else:
        # Pass the value
        return False

def is_unspecified_address(ip_octets):
    regex_results = []
    # Unspecified address patterns
    regex_results.append(re.match(r"0", ip_octets[0]))
    regex_results.append(re.match(r"0", ip_octets[1]))
    regex_results.append(re.match(r"0", ip_octets[2]))
    regex_results.append(re.match(r"0", ip_octets[3]))
    # When all patterns match, all Results should be True
    if all(regex_results):
        result = True
    else:
        result = False
    # Pass the value
    return result

def is_linklocal_address(ip_octets):
    regex_results = []
    # Link-local address patterns
    regex_results.append(re.match(r"169", ip_octets[0]))
    regex_results.append(re.match(r"254", ip_octets[1]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[2]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[3]))
    # When all patterns match, all Results should be True
    if all(regex_results):
        result = True
    else:
        result = False
    # Pass the value
    return result

def is_localhost_address(ip_octets):
    regex_results = []
    # Localhost address patterns
    regex_results.append(re.match(r"127", ip_octets[0]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[1]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[2]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[3]))
    # When all patterns match, all Results should be True
    if all(regex_results):
        result = True
    else:
        result = False
    # Pass the value
    return result

def is_multicast_address(ip_octets):
    regex_results = []
    # Multicast address patterns
    regex_results.append(re.match(r"(22[4-9]|23[0-5]|239)", ip_octets[0]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[1]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[2]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[3]))
    # When all patterns match, all Results should be True
    if all(regex_results):
        result = True
    else:
        result = False
    # Pass the value
    return result

def is_unassigned_address(ip_octets):
    regex_results = []
    # Unassigned address patterns
    regex_results.append(re.match(r"(24[0-9]|25[0-5])", ip_octets[0]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[1]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[2]))
    regex_results.append(re.match(r"([0-9]|[1-9][0-9]|[1-2][0-9][0-9])", ip_octets[3]))
    # When all patterns match, all Results should be True
    if all(regex_results):
        result = True
    else:
        result = False
    # Pass the value
    return result

def ip_addr_validator(flag, ip_addr_list):
    # Progress dot
    print("\nValidating IP address(es). Please wait", end = "", flush = True)
    # Initial variables
    valid_ips = []
    invalid_ips = []
    invalid_formats = []
    results = []
    # Loop for every IP address in the list
    for ip in ip_addr_list:
        # Strip newline at the end of IP address then split IP address to octets
        ip_octets = ip.rstrip("\n").split(".")
        # IP address must have 4 octets, an octet cannot be empty, and octets must be a digit
        if all([is_empty(ip_octets), is_digit(ip_octets)]):
            # Network address other than Private address and Public address is not allowed
            if any([is_unspecified_address(ip_octets), is_linklocal_address(ip_octets), is_localhost_address(ip_octets), is_multicast_address(ip_octets), is_unassigned_address(ip_octets)]):
                results.append("FAIL")
                invalid_ips.append(ip)
                # Progress dot
                print(".", end = "", flush = True)
                continue
            # Private address or Public address is allowed
            else:
                results.append("PASS")
                valid_ips.append(ip)
                # Progress dot
                print(".", end = "", flush = True)
                continue
        # IP address must have 4 octets, an octet cannot be empty, and octets must be a digit
        else:
            results.append("FAIL")
            invalid_formats.append(ip)
            # Progress dot
            print(".", end = "", flush = True)
            continue
    # Unaccepted IP address list results
    if "FAIL" in results:
        print("\n\nPASS: Valid IP address(es): " + str(valid_ips)[1:-1])
        print("FAIL: Invalid IP address(es): " + str(invalid_ips)[1:-1])
        print("FAIL: Invalid IP address(es) format: " + str(invalid_formats)[1:-1])
        print("FAIL: Please correct the IP address list and try again!")
        # Repeat execute device_info_list_validator then device_info_validator and then ip_addr_validator with a flag
        return ip_addr_validator("FAIL", device_info_validator(device_info_list_validator())[0])
    # Accepted IP address list results
    else:
        # IP address list with correction flag
        if flag == "FAIL":
            print("\n\nPASS: The IP address list is valid")
            # Pass the value
            return ip_addr_list
        # IP address list with no correction flag
        elif flag == "PASS":
            print("\n\nPASS: The IP address list is valid")

def ip_addr_list_validator(ip_addr_list_fix, ip_addr_list):
    # If a new list exists, replace the existing ip_addr_list with the corrected one
    if bool(ip_addr_list_fix) == True:
        ip_addr_list = ip_addr_list_fix
        # Pass the value
        return ip_addr_list
    # If there's no new list exists, pass the existing list
    else:
        # Pass the value
        return ip_addr_list