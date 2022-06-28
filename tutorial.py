import getpass
from nornir import InitNornir                                   # Used to first initalize the Nornir object
from nornir_netmiko.tasks import netmiko_send_command           # Main netmiko command task
from nornir_utils.plugins.functions import print_result         # Ansible-esque print statement

# Color tutorial (not needed, just fancy): https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal/21786287#21786287
EMPHASIS = "\x1b[1;30;47m"
END_COLOR = "\x1b[0m"


# This function sets the credentials of the Nornir object at runtime so you don't
# need to hardcode them in somewhere. Second thing ran after InitNornir() almost always
################################################################################
def nornir_set_creds(nr, username=None, password=None):
    if not username:
        username = input("Enter username: ")
    if not password:
        password = getpass.getpass()

    for host_obj in nr.inventory.hosts.values():
        host_obj.username = username
        host_obj.password = password



def main():
    nr = InitNornir("config.yaml")                              # Creating the Nornir object based off of settings in your config.yaml file
    nornir_set_creds(nr)                                        # Entering in username and password for logging into switches

    command = "dir"                                             # Command that is passed to the netmiko_send_command task that is imported at the top
    output = nr.run(netmiko_send_command, command_string=command)# This actually runs the command, output is of type AggregatedResult (custom weird Nornir data type). Command gets ran in parallel against all hosts

    for hostname in output:                                     # Going through each host in the hosts.yaml file IN THE ORDER THEY ARE DEFINED (If you define test02 before test01 in hosts.yaml, test02 will print out first)
        print(f"This is the output for command {EMPHASIS}{command}{END_COLOR} on {EMPHASIS}{hostname}{END_COLOR}:")
        print("################################################################################")
        text = output[hostname].result                          # Grabbing the command's output and converting it into a string
        print(f"{text}\n\n\n")

    print("\n\n\nAnd this is what the print_result function looks like:\n")
    print_result(output)                                        # Printing out the task in a very similar way to how Ansible displays their tasks


if __name__ == "__main__":                              # Running main()
    main()