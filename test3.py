import psutil
import matplotlib.pyplot as plt

# CPU, RAM, 디스크 사용량 데이터를 저장할 리스트
time_values = []
cpu_percentages = []
ram_percentages = []
disk_percentages = []

# 60초 짜리 데이터 생성
for _ in range(60):
    time_values.append(psutil.cpu_times().user)
    cpu_percentages.append(psutil.cpu_percent())
    ram_percentages.append(psutil.virtual_memory().percent)
    disk_percentages.append(psutil.disk_usage('/').percent)
    print("s")

# 그래프 초기화
plt.style.use('seaborn-darkgrid')
fig, (ax_cpu, ax_ram, ax_disk) = plt.subplots(3, 1, figsize=(8, 8))
ax_cpu.set_xlim(0, 60)  # 최근 60초간의 데이터만 보여줄 것입니다.
ax_ram.set_xlim(0, 60)  # 최근 60초간의 데이터만 보여줄 것입니다.
ax_disk.set_xlim(0, 60)  # 최근 60초간의 데이터만 보여줄 것입니다.
ax_cpu.set_ylim(0, 100)  # CPU 사용률은 0부터 100까지 표현합니다.
ax_ram.set_ylim(0, 100)  # RAM 사용률은 0부터 100까지 표현합니다.
ax_disk.set_ylim(0, 100)  # 디스크 사용률은 0부터 100까지 표현합니다.
ax_cpu.plot(time_values, cpu_percentages, lw=2, label='CPU Usage (%)')
ax_ram.plot(time_values, ram_percentages, lw=2, label='RAM Usage (%)')
ax_disk.plot(time_values, disk_percentages, lw=2, label='Disk Usage (%)')
ax_cpu.legend(loc='upper right')
ax_ram.legend(loc='upper right')
ax_disk.legend(loc='upper right')

# 그래프 표시
ax_cpu.set_title('CPU Usage (%)')
ax_cpu.set_xlabel('Time (seconds)')
ax_cpu.set_ylabel('CPU Usage')
ax_ram.set_title('RAM Usage (%)')
ax_ram.set_xlabel('Time (seconds)')
ax_ram.set_ylabel('RAM Usage')
ax_disk.set_title('Disk Usage (%)')
ax_disk.set_xlabel('Time (seconds)')
ax_disk.set_ylabel('Disk Usage')
plt.tight_layout()
plt.show()
