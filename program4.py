import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil

# Data storage for graphs
ram_usage_history = []
rom_usage_history = []
scatter_data_x = []
scatter_data_y = []

def update_memory_info():
    # Get memory stats
    ram = psutil.virtual_memory()
    rom = psutil.disk_usage('/')
    
    # Estimate cache memory (available memory approximation)
    cache = ram.available
    
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
    
    pie_data = [used_memory, free_memory, cached_memory]
    pie_labels = ["Used Memory", "Free Memory", "Cached Memory"]
    
    ax_pie.clear()
    ax_pie.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=["red", "green", "blue"])
    ax_pie.set_title("Memory Distribution")
    
    # Update line graph (RAM usage history)
    if len(ram_usage_history) > 20:
        ram_usage_history.pop(0)  # Keep history limited to 20 points
    if len(rom_usage_history) > 20:
        rom_usage_history.pop(0)
    
    ram_usage_history.append(ram_usage)
    rom_usage_history.append(rom_usage)
    
    ax_line.clear()
    ax_line.plot(ram_usage_history, label="RAM Usage", color="blue", marker="o")
    ax_line.plot(rom_usage_history, label="ROM Usage", color="green", marker="o")
    ax_line.set_title("RAM & ROM Usage Over Time")
    ax_line.legend()
    ax_line.set_ylim(0, 100)
    ax_line.set_ylabel("Usage (%)")
    
    # Update bar graph (current values)
    ax_bar.clear()
    ax_bar.bar(["RAM", "ROM"], [ram_usage, rom_usage], color=["blue", "green"])
    ax_bar.set_title("Current RAM and ROM Usage")
    ax_bar.set_ylabel("Usage (%)")
    
    # Update scatter plot (random cached data)
    scatter_data_x.append(len(scatter_data_x) + 1)
    scatter_data_y.append(cached_memory / (1024 ** 3))  # Convert bytes to GB
    
    if len(scatter_data_x) > 20:
        scatter_data_x.pop(0)
        scatter_data_y.pop(0)
    
    ax_scatter.clear()
    ax_scatter.scatter(scatter_data_x, scatter_data_y, color="purple")
    ax_scatter.set_title("Cached Memory Scatter")
    ax_scatter.set_ylabel("Cached Memory (GB)")
    ax_scatter.set_xlabel("Time")
    
    # Redraw canvas
    canvas.draw()
    
    # Schedule the function to run again
    root.after(1000, update_memory_info)

# Create GUI window
root = tk.Tk()
root.title("Memory Monitor")
root.geometry("800x1000")  # Increased height for better graph spacing
root.resizable(False, False)

# RAM
ram_label = tk.Label(root, text="RAM Usage: 0%")
ram_label.pack(pady=5)
ram_bar = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
ram_bar.pack(pady=5)

# ROM
rom_label = tk.Label(root, text="ROM Usage: 0%")
rom_label.pack(pady=5)
rom_bar = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
rom_bar.pack(pady=5)

# Create a matplotlib figure
figure = Figure(figsize=(8, 12), dpi=100)  # Adjusted figure size for vertical stacking

# Subplots for different graphs (stacked vertically)
ax_pie = figure.add_subplot(4, 1, 1)  # Pie chart
ax_bar = figure.add_subplot(4, 1, 2)  # Bar graph
ax_line = figure.add_subplot(4, 1, 3)  # Line graph
ax_scatter = figure.add_subplot(4, 1, 4)  # Scatter plot

# Embed the figure into the Tkinter window
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()

# Start memory monitoring
update_memory_info()

# Run the application
root.mainloop()
