import matplotlib.pyplot as plt
import numpy as np

nhom = "Nhóm tìm kiếm không có thông tin"

algorithms = ['BFS', 'DFS', 'UCS', 'IDS']
execution_times_ms = np.array([793.113, 892.348, 1128.698, 685.428])

plt.figure(figsize=(10, 6))
bars = plt.bar(algorithms, execution_times_ms, color='darkcyan')

max_time = np.max(execution_times_ms)
text_offset = max_time * 0.01

for bar in bars:
    yval = bar.get_height()
    label = f'{yval:.2f} ms'
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + text_offset, label, ha='center', va='bottom', fontsize=10)

plt.title(f'Thời gian thực thi  - {nhom}', fontsize=15, pad=20)
plt.xlabel('Thuật toán', fontsize=13, labelpad=15)
plt.ylabel('Thời gian thực thi (ms)', fontsize=13, labelpad=15)
plt.xticks(rotation=45, ha="right") 
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, max_time * 1.15)

plt.tight_layout()
plt.show()