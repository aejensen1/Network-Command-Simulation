import tkinter as tk
from tkinter import messagebox
import subprocess
import time

class ProgramRunner:
    def __init__(self, server_cmd, client_cmd):
        self.server_cmd = server_cmd
        self.client_cmd = client_cmd
        self.server_process = None

    def start_server(self):
        self.server_process = subprocess.Popen(self.server_cmd.split())
        time.sleep(1)  # Wait for server to start

    def stop_server(self):
        if self.server_process:
            self.server_process.kill()
            self.server_process = None

    def run_client(self, flag=None):
        if flag is not None:
            client_cmd_with_flag = f"{self.client_cmd} -n {flag}"
        else:
            client_cmd_with_flag = self.client_cmd  # Run without flags if flag is not provided
        client_process = subprocess.Popen(client_cmd_with_flag.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = client_process.communicate()
        output = stdout.decode('utf-8') if stdout else stderr.decode('utf-8')
        return output

def run_ping_with():
    flag_value = flag_entry.get().strip()
    program_1 = ProgramRunner("python3 ping_server.py", "python3 ping_client.py")
    program_1.start_server()
    output = program_1.run_client(flag=flag_value)
    program_1.stop_server()
    show_output(output)


def run_ping_without():
    program_1 = ProgramRunner("python3 ping_server.py", "python ping_client.py")
    program_1.start_server()
    output = program_1.run_client()  # Run without flags
    program_1.stop_server()
    show_output(output)

def run_tracert():
    program_2 = ProgramRunner("python3 Receivers.py", "python3 Sender.py")
    program_2.start_server()
    output = program_2.run_client()
    program_2.stop_server()
    show_output(output)

def show_output(output):
    messagebox.showinfo("Client Output", output)

# Create GUI
root = tk.Tk()
root.title("Program Runner")
root.geometry("600x300")

label = tk.Label(root, text="Enter the number of pings:")
label.pack(pady=10)

flag_entry = tk.Entry(root)
flag_entry.pack()

button_with_flags = tk.Button(root, text="Run ping n times", command=run_ping_with, height=3, width=30)
button_with_flags.pack(pady=10)

button_without_flags = tk.Button(root, text="Run ping", command=run_ping_without, height=3, width=30)
button_without_flags.pack(pady=10)

button_2 = tk.Button(root, text="Run tracert", command=run_tracert, height=3, width=30)
button_2.pack(pady=10)

root.mainloop()

