import matplotlib.pyplot as plt
import numpy as np

nhom = "Nhóm tìm kiếm cục bộ"

algorithms = ['SHC', 'SAHC', 'StochasticHC', 'Simulated annealing', 'Genetic algorithm', 'Beam search']
execution_times_seconds = np.array([4718e-05, 9180e-05, 7098e-05, 0.964, 0.0997, 2.145])
execution_times_ms = execution_times_seconds * 1000

plt.figure(figsize=(12, 7))
bars = plt.bar(algorithms, execution_times_ms, color='steelblue')

max_time = np.max(execution_times_ms)
text_offset = max_time * 0.01

for bar in bars:
    yval = bar.get_height()
    if yval < 1:
        label = f'{yval:.4f} ms'
    elif yval < 100:
        label = f'{yval:.2f} ms'
    else:
        label = f'{yval:.0f} ms'
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + text_offset, label, ha='center', va='bottom', fontsize=9)

plt.title(f'Thời gian thực thi - {nhom}', fontsize=15, pad=20)
plt.xlabel('Thuật toán', fontsize=13, labelpad=15)
plt.ylabel('Thời gian thực thi (ms)', fontsize=13, labelpad=15)
plt.xticks(rotation=15, ha="right")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, max_time * 1.15)

plt.tight_layout()
plt.show()