from matplotlib import pyplot as plt


def draw_system_usage(path, cpu_usage, ram_usage, disk_usage):
    try:
        user_time = [n for n in range(1, 61)]
        cpu_usage, ram_usage, disk_usage = list(cpu_usage)[:60], list(ram_usage)[:60], list(disk_usage)[:60]
        plt.style.use('seaborn-darkgrid')
        fig, (ax_cpu, ax_ram, ax_disk) = plt.subplots(3, 1, figsize=(8, 8))
        ax_cpu.set_xlim(0, 60)  # 최근 60초간의 데이터만 보여줄 것입니다.
        ax_ram.set_xlim(0, 60)  # 최근 60초간의 데이터만 보여줄 것입니다.
        ax_disk.set_xlim(0, 60)  # 최근 60초간의 데이터만 보여줄 것입니다.
        ax_cpu.set_ylim(0, 100)  # CPU 사용량은 0부터 100까지 표현합니다.
        ax_ram.set_ylim(0, 100)  # 램 사용량은 GB 단위로 표현합니다.
        ax_disk.set_ylim(0, 100)  # 디스크 사용량은 GB 단위로 표현합니다.

        ax_cpu.plot(user_time, cpu_usage, lw=2, label='CPU Usage (%)')
        ax_ram.plot(user_time, ram_usage, lw=2, label='RAM Usage (%)')
        ax_disk.plot(user_time, disk_usage, lw=2, label='Disk Usage (%)')

        ax_cpu.legend(loc='upper right')  # 범례 배경은 기본값으로 설정합니다.
        ax_ram.legend(loc='upper right')  # 범례 배경은 기본값으로 설정합니다.
        ax_disk.legend(loc='upper right')  # 범례 배경은 기본값으로 설정합니다.

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

        plt.savefig(f"{path}/database/viz/system_usage.png")
        plt.close()
    except Exception as e:
        print(e)