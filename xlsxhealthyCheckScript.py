import paramiko
import datetime
import pandas as pd

# Define server details (IP addresses, usernames, passwords)
server_details = [
    {"ip": "192.168.20.65", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.66", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.67", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.68", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.69", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.70", "username": "oracle", "password": "oracle"}, 

]
# Commands to run for health check
commands = ["echo 'grid' | su - grid -c 'asmcmd lsdg'"] 

# Function to run commands on a remote server
def run_commands_on_server(server, commands):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh_client.connect(server["ip"], username=server["username"], password=server["password"])

        # Generate a report DataFrame
        report_data = {"Server": [], "Command": [], "Output": []}
        for command in commands:
            # Execute the command on the remote server
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode("utf-8")

            # Extract server and command information
            server_info = f"{server['username']} - {server['ip']}"

            # Extend the report_data dictionary with the server and command information
            report_data["Command"].extend([command] * len(output.split('\n')))
            report_data["Server"].extend([server_info] + [""] * (len(output.split('\n')) - 1))
            # report_data["Command"].extend([command] * len(output.split('\n')))
            report_data["Output"].extend(output.split('\n'))

        # Close the SSH connection
        ssh_client.close()

        return report_data
    except Exception as e:
        print(f"Error connecting to {server['username']} {server['ip']}: {str(e)}")
        return None

# Create an Excel writer with pandas
timestamp = datetime.datetime.now().strftime(" %d-%B-%Y [%H %M %S]")
# timestam = datetime.datetime.now().strftime("%M ")
report_filename = f"{timestamp} ASM.xlsx"
with pd.ExcelWriter(report_filename, engine='xlsxwriter') as writer:
    df_command_list = []

    for command in commands:
        # Create a DataFrame for each command
        df_command_list.append(pd.DataFrame(columns=["Server", "Command", "Output"]).copy())

        for server in server_details:
            # Perform health check for each server and command
            server_data = run_commands_on_server(server, [command])

            if server_data:
                # Create a DataFrame for each server
                df_server = pd.DataFrame(server_data)

                # Split each line into columns based on any whitespace
                output_lines = [line.split() for line in df_server["Output"]]

                # Determine the maximum number of columns
                max_columns = max(len(line) for line in output_lines)

                # Create a DataFrame for each server with dynamic column names
                df_server_columns = pd.DataFrame(output_lines, columns=[f"Column_{i}" for i in range(1, max_columns + 1)])

                # Concatenate the server and command information with the output columns
                df_final = pd.concat([df_server[["Server", "Command"]], df_server_columns], axis=1)

                # Append the DataFrame to the command-specific list
                df_command_list[-1] = pd.concat([df_command_list[-1], df_final], ignore_index=True)

    # Concatenate all DataFrames in df_command_list into one DataFrame
    df_command = pd.concat(df_command_list, ignore_index=True)

    # Write the command-specific DataFrame to Excel
    df_command.to_excel(writer, sheet_name="Commands", index=False)

print(f"Health check report for all servers created: {report_filename}")


# # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Script for Disk usage
import paramiko
import datetime
import pandas as pd

# Define server details (IP addresses, usernames, passwords)
server_details = [
    {"ip": "192.168.20.140", "username": "qmdb", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.141", "username": "ocs", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.142", "username": "stc", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.143", "username": "cvbs", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.146", "username": "med", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.147", "username": "web", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.148", "username": "web", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.149", "username": "sett", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.150", "username": "olc", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.151", "username": "olc", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.152", "username": "wholesale", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.153", "username": "wholesale", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.154", "username": "jobserver", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.155", "username": "jobserver", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.156", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.157", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.160", "username": "cache", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.161", "username": "zmq", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.162", "username": "uip", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.163", "username": "prov", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.163", "username": "cloud", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.21.129", "username": "ecare", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.21.130", "username": "ecare", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.165", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.166", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.167", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.65", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.66", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.67", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.68", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.69", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.70", "username": "oracle", "password": "oracle"}, 
]
# Commands to run for health check
commands = ["df -h | column -t"]

# Function to run commands on a remote server
def run_commands_on_server(server, commands):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh_client.connect(server["ip"], username=server["username"], password=server["password"])

        # Generate a report DataFrame
        report_data = {"Server": [], "Command": [], "Output": []}
        for command in commands:
            # Execute the command on the remote server
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode("utf-8")

            # Extract server and command information
            server_info = f"{server['username']} - {server['ip']}"

            # Extend the report_data dictionary with the server and command information
            report_data["Command"].extend([command] * len(output.split('\n')))
            report_data["Server"].extend([server_info] + [""] * (len(output.split('\n')) - 1))
            # report_data["Command"].extend([command] * len(output.split('\n')))
            report_data["Output"].extend(output.split('\n'))

        # Close the SSH connection
        ssh_client.close()

        return report_data
    except Exception as e:
        print(f"Error connecting to {server['username']} {server['ip']}: {str(e)}")
        return None

# Create an Excel writer with pandas
timestamp = datetime.datetime.now().strftime(" %d-%B-%Y [%H %M %S]")
report_filename = f"{timestamp} Disk_Usage.xlsx"
with pd.ExcelWriter(report_filename, engine='xlsxwriter') as writer:
    df_command_list = []

    for command in commands:
        # Create a DataFrame for each command
        df_command_list.append(pd.DataFrame(columns=["Server", "Command", "Output"]).copy())

        for server in server_details:
            # Perform health check for each server and command
            server_data = run_commands_on_server(server, [command])

            if server_data:
                # Create a DataFrame for each server
                df_server = pd.DataFrame(server_data)

                # Split each line into columns based on any whitespace
                output_lines = [line.split() for line in df_server["Output"]]

                # Determine the maximum number of columns
                max_columns = max(len(line) for line in output_lines)

                # Create a DataFrame for each server with dynamic column names
                df_server_columns = pd.DataFrame(output_lines, columns=[f"Column_{i}" for i in range(1, max_columns + 1)])

                # Concatenate the server and command information with the output columns
                df_final = pd.concat([df_server[["Server", "Command"]], df_server_columns], axis=1)

                # Append the DataFrame to the command-specific list
                df_command_list[-1] = pd.concat([df_command_list[-1], df_final], ignore_index=True)

    # Concatenate all DataFrames in df_command_list into one DataFrame
    df_command = pd.concat(df_command_list, ignore_index=True)

    # Write the command-specific DataFrame to Excel
    df_command.to_excel(writer, sheet_name="Commands", index=False)

print(f"Health check report for all servers created: {report_filename}")

# # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Script for Memory and CPU usage
import paramiko
import datetime
import pandas as pd

server_details = [
    {"ip": "192.168.20.140", "username": "qmdb", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.141", "username": "ocs", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.142", "username": "stc", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.143", "username": "cvbs", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.146", "username": "med", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.147", "username": "web", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.148", "username": "web", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.149", "username": "sett", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.150", "username": "olc", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.151", "username": "olc", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.152", "username": "wholesale", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.153", "username": "wholesale", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.154", "username": "jobserver", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.155", "username": "jobserver", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.156", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.157", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.160", "username": "cache", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.161", "username": "zmq", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.162", "username": "uip", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.163", "username": "prov", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.163", "username": "cloud", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.21.129", "username": "ecare", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.21.130", "username": "ecare", "password": "KTRN2023_WC@!9oW"},
    {"ip": "192.168.20.165", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.166", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.167", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.65", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.66", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.67", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.68", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.69", "username": "oracle", "password": "oracle"},
    {"ip": "192.168.20.70", "username": "oracle", "password": "oracle"},
]
# Commands to run for health check
commands = ["free -g | column -t", "mpstat | column -t"]

def run_commands_on_server(server, commands):
    try:
        
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


        ssh_client.connect(server["ip"], username=server["username"], password=server["password"])


        report_data = {"Server": [], "Output": []}
        for command in commands:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode("utf-8")


            server_info = f"{server['username']} - {server['ip']}"

            report_data["Server"].extend([server_info] + [""] * (len(output.split('\n')) - 1))
            report_data["Output"].extend(output.split('\n'))


        ssh_client.close()

        return report_data
    except Exception as e:
        print(f"Error connecting to {server['username']} {server['ip']}: {str(e)}")
        return None


timestamp = datetime.datetime.now().strftime(" %d-%B-%Y [%H %M %S]")
 
report_filename = f"{timestamp} MEMORY&CPU .xlsx"
with pd.ExcelWriter(report_filename, engine='xlsxwriter') as writer:
    for command in commands:
        df_command = pd.DataFrame(columns=["Server", "Output"]).copy()

        for server in server_details:
            server_data = run_commands_on_server(server, [command])

            if server_data:
                df_server = pd.DataFrame(server_data)

                df_final = pd.concat([df_server["Server"], df_server["Output"]], axis=1)


                df_command = pd.concat([df_command, df_final], ignore_index=True)

        df_command.to_excel(writer, sheet_name=command.strip(), index=False)

print(f"Health check report for all servers created: {report_filename}")







