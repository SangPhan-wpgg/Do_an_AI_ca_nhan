import matplotlib.pyplot as plt
nhom = "Nhóm tìm kiếm có ràng buộc"

algorithms = ['Backtracking', 'Test', 'AC3']
execution_times = [13.777, 584.995, 9.125]
plt.figure(figsize=(10, 6))
bars = plt.bar(algorithms, execution_times, color='blue')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval} ms', ha='center', va='bottom')

plt.title(f'Thời gian thực thi  - {nhom}', fontsize=14)
plt.xlabel('Thuật toán', fontsize=12)
plt.ylabel('Thời gian (ms)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45, ha="right") 
plt.tight_layout()
plt.show()
