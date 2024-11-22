import os
import psutil
import platform
import socket
import datetime
from tkinter import Tk, Label, Button, messagebox


def clear_cache():
    """Clear cache memory."""
    try:
        if os.name == 'posix':
            os.system('sync; echo 3 > /proc/sys/vm/drop_caches')  # Linux command
        elif os.name == 'nt':
            os.system('ipconfig /flushdns')  # Windows DNS cache clear
        messagebox.showinfo("Cache Cleared", "Cache memory cleared successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")


def get_external_ip():
    """Fetch external IP address."""
    try:
        import requests
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        return "Unable to fetch external IP."


def get_system_info():
    """Retrieve detailed system information."""
    try:
        # General info
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        external_ip = get_external_ip()
        os_name = platform.system()
        os_version = platform.version()
        os_architecture = platform.architecture()[0]

        # Memory and Storage
        ram = round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)  # RAM in GB
        rom = round(psutil.disk_usage('/').total / (1024 * 1024 * 1024), 2)  # ROM in GB
        storage = f"{round(psutil.disk_usage('/').used / (1024 * 1024 * 1024), 2)} GB used of {rom} GB"

        # CPU Info
        cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq().max
        cpu_info = platform.processor()

        # Battery Info
        battery = psutil.sensors_battery()
        battery_status = f"{battery.percent}% (Plugged In)" if battery and battery.power_plugged else f"{battery.percent}%" if battery else "No Battery Detected"

        # Boot Time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        # System Info
        system_info = (
            f"Hostname: {hostname}\n"
            f"Local IP Address: {local_ip}\n"
            f"External IP Address: {external_ip}\n"
            f"OS: {os_name} {os_version} ({os_architecture})\n"
            f"CPU: {cpu_info}, {cpu_count} cores @ {cpu_freq} MHz\n"
            f"RAM: {ram} GB\n"
            f"ROM: {rom} GB\n"
            f"Storage: {storage}\n"
            f"Battery Status: {battery_status}\n"
            f"Boot Time: {boot_time}\n"
        )
        return system_info
    except Exception as e:
        return f"Error fetching system info: {str(e)}"


def show_system_info():
    """Display system information in a message box."""
    info = get_system_info()
    messagebox.showinfo("System Information", info)


# GUI Setup
root = Tk()
root.title("Enhanced Device Management Tool")
root.geometry("500x400")
root.resizable(False, False)

# Labels and Buttons
Label(root, text="Enhanced Device Management Tool", font=("Arial", 16, "bold")).pack(pady=10)

Button(root, text="Clear Cache", font=("Arial", 12), command=clear_cache).pack(pady=10)
Button(root, text="View System Info", font=("Arial", 12), command=show_system_info).pack(pady=10)

Label(
    root,
    text="Note: Ensure you run this tool as administrator for best results.",
    font=("Arial", 10),
    wraplength=450,
).pack(pady=20)

# Run the GUI loop
root.mainloop()
