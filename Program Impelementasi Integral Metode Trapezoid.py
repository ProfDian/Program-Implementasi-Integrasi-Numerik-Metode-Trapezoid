import numpy as np
import timeit
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Banner
banner = """
=========================================================
||      Program Implementasi Integrasi Numerik         ||
||                 Metode Trapezoid                    ||
||            Metode Numerik - Kelas B                 ||
||     Abdul Fattah Rahmadiansyah - 21120122120028     ||
=========================================================
"""

print(banner)

# Nilai referensi pi
pi_reference = 3.14159265358979323846

# Variasi nilai N
N_values = [10, 100, 1000, 10000]
pi_approximations = []
execution_times = []
rms_errors = []

# Definisikan fungsi f(x)
def f(x):
    return 4 / (1 + x**2)

# Metode Trapezoid
def trapezoid_integration(a, b, N):
    delta_x = (b - a) / N
    x = np.linspace(a, b, N+1)
    y = f(x)
    integral = (delta_x / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral

# Hitung galat RMS
def calculate_rms_error(pi_approx):
    return np.sqrt(mean_squared_error([pi_reference] * len(pi_approx), pi_approx))

# Jalankan perhitungan
for N in N_values:
    execution_time = timeit.timeit(lambda: trapezoid_integration(0, 1, N), number=100)
    pi_approx = trapezoid_integration(0, 1, N)
    
    pi_approximations.append(pi_approx)
    execution_times.append(execution_time)

    print(f"N = {N}:")
    print(f"π Approximation = {pi_approx}")
    print(f"Execution Time = {execution_time:.8f} detik")

    rms_error = calculate_rms_error([pi_approx])
    rms_errors.append(rms_error)
    print(f"Error RMS = {rms_error}")
    
    rms_error_percent = (abs(pi_reference - pi_approx) / pi_reference) * 100
    print(f"Error RMS in percentage = {rms_error_percent:.10f}%\n")

print(f"π Reference = {pi_reference}")

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

current_plot = 0

def update_plot():
    ax.clear()
    if current_plot == 0:
        ax.plot(N_values, pi_approximations, marker='o', color='blue', label='π Approximation')
        ax.axhline(y=pi_reference, color='RED', linestyle='--', label='π Reference')
        ax.set_xscale('log')
        ax.set_xlabel('N (Number of intervals)')
        ax.set_ylabel('π value')
        ax.set_title('Comparison of π Approximation with Reference')
        ax.legend()
    elif current_plot == 1:
        ax.plot(N_values, rms_errors, marker='o', color='red', label='RMS Error')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('N (Number of intervals)')
        ax.set_ylabel('RMS Error')
        ax.set_title('RMS Error vs N')
        ax.legend()
    elif current_plot == 2:
        ax.plot(N_values, execution_times, marker='o', color='purple', label='Execution Time')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('N (Number of intervals)')
        ax.set_ylabel('Execution Time (seconds)')
        ax.set_title('Comparison of Execution Time with N')
        ax.legend()
    ax.grid(True)
    fig.canvas.draw_idle()

def next_plot(event):
    global current_plot
    current_plot = (current_plot + 1) % 3
    update_plot()

def prev_plot(event):
    global current_plot
    current_plot = (current_plot - 1) % 3
    update_plot()

update_plot()

axprev = plt.axes([0.1, 0.05, 0.1, 0.075])
axnext = plt.axes([0.21, 0.05, 0.1, 0.075])

bnext = Button(axnext, 'Next')
bprev = Button(axprev, 'Previous')

bnext.on_clicked(next_plot)
bprev.on_clicked(prev_plot)

plt.show()
