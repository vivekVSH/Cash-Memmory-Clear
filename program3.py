import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil

def update_memory_info():
    # Get memory stats
    ram = psutil.virtual_memory()
    rom = psutil.disk_usage('/')
    
    # Estimate cache memory (used - active memory can approximate it)
    cache = ram.available  # Available memory is often closer to free + cached
    
    # Update progress bars
    ram_usage = ram.percent
    rom_usage = rom.percent
    
    ram_bar['value'] = ram_usage
    rom_bar['value'] = rom_usage
    
    ram_label.config(text=f"RAM Usage: {ram_usage:.2f}%")
    rom_label.config(text=f"ROM Usage: {rom_usage:.2f}%")
    
    # Update pie chart
    total_memory = ram.total
    used_memory = ram.used
    free_memory = ram.free
    cached_memory = cache
    
    # Data for pie chart
    pie_data = [used_memory, free_memory, cached_memory]
    pie_labels = ["Used Memory", "Free Memory", "Cached Memory"]
    
    ax.clear()
    ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=["red", "green", "blue"])
    ax.set_title("Memory Distribution")
    
    canvas.draw()
    
    # Schedule the function to run again
    root.after(1000, update_memory_info)

# Create GUI window
root = tk.Tk()
root.title("Memory Monitor")
root.geometry("500x400")
root.resizable(False, False)

# RAM
ram_label = tk.Label(root, text="RAM Usage: 0%")
ram_label.pack(pady=5)
ram_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
ram_bar.pack(pady=5)

# ROM
rom_label = tk.Label(root, text="ROM Usage: 0%")
rom_label.pack(pady=5)
rom_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
rom_bar.pack(pady=5)

# Pie Chart for Memory
figure = Figure(figsize=(5, 3), dpi=100)
ax = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()

# Start memory monitoring
update_memory_info()

# Run the application
root.mainloop()
