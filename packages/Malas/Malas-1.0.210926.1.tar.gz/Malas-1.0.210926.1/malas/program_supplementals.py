import os
import sys
import shutil
import getpass
import subprocess
import pkg_resources

def exit_and_cleanup():
    target = os.path.join("malas", "__pycache__")
    # Delete pycache folder and its content
    shutil.rmtree(target)
    # Exit program
    sys.exit()

def enter_key_only():
    # Expect the user to press Enter key and suppress the output
    getpass.getpass("")

def enter_key_confirmation():
    print("Press \'Enter\' to continue or \'CTRL+C\' to abort the program", end="", flush=True)
    # Expect the user to press Enter key and suppress the output
    getpass.getpass("")

def input_option():
    # Capture any inputs
    return str(input(""))

def exception_translator():
    # Get the raised exception error messages values
    exc_type, exc_value, _ = sys.exc_info()
    # Store the raised exception error messages values
    exception_name = exc_type.__name__
    exception_explanation = str(exc_value)
    # Output for blank raised exception error explanation
    if len(exception_explanation) == 0:
        exception_explanation = "There's no explanation provided for this exception."
    # Pass these values
    return exception_name, exception_explanation

def module_verifier(module):
    try:
        # Get installed module's name
        module_name = pkg_resources.get_distribution(module).key
        # Get installed module's version
        module_version = pkg_resources.get_distribution(module).version
        # Pass these values
        return module_name, module_version
    except:
        # Pass these values when the module is not installed
        return False, False

def install_requirements(module):
    print("Installing required module: ", end="", flush=True)
    try:
        # Install the module and suppress outputs
        subprocess.check_call([sys.executable, "-m", "pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("Done, " + module + " " + module_verifier(module)[1], flush=True)
        return True
    # Module installations failed due to an Internet problem
    except:
        print("Failed (" + module + ")", flush=True)
        return False

def program_requirements():
    # Required modules
    prerequisites = ["netmiko", "pythonping", "bcrypt", "cffi", "cryptography", "future", "ntc-templates", "paramiko", "pycparser", "pynacl", "pyserial", "scp", "setuptools", "six", "tenacity", "textfsm"]
    # Initial variables
    module_results = []
    module_installs = []
    # Loop for every required module in the list
    for module in prerequisites:
        # Verify if modules are installed and store results in a list
        module_results.append([module, bool(module_verifier(module)[0])])
    # Loop for every module check results. If the module is not installed, store the module name in a list
    if all([module_installs.append(result[0]) if result[1] == False else True for result in module_results]):
        # All required modules are installed
        pass
    # Install the required modules
    else:
        print("\n \  Self-diagnostics and Self-recovery")
        print("  \___________________________________________________________________\n")
        # Initial variables
        install_results = []
        # Loop for every module in the list
        for module in module_installs:
            # Execute install_requirements to install the required modules and store results in a list
            install_results.append(install_requirements(module))
        # Loop for every module installation result
        if all([True if result == True else False for result in install_results]):
            print("\nDiagnostics and recovery are completed")
        # Module installations failed due to an Internet problem
        else:
            print("\nPlease check the Internet connection and try again!")
            print("Alternatively, please perform manual module installation!")
            # Execute exit_and_cleanup
            exit_and_cleanup()

def powered_by(module):
    # Execute module_verifier to get the installed module's name and version
    module_name, module_version = module_verifier(module)
    # Pass the value
    return (module_name + " " + module_version)

def program_cancellation():
    print("\nEXIT: I\'ll see you again :)")
    # Execute exit_and_cleanup
    exit_and_cleanup()