import psutil
import time

def main():
    while True:
        # Проходим по всем запущенным процессам
        for proc in psutil.process_iter():
            try:
                # Проверяем, содержит ли имя процесса указанный подстроку
                if any(procstr in proc.name() for procstr in ['CrossDeviceService.exe']) or any(procstr in proc.name() for procstr in ['RF4Launcher.exe']):
                    print(f'Killing {proc.name()} (PID: {proc.pid})')
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Процесс уже завершился или доступ запрещен
                pass
        time.sleep(5)  # Проверяем каждые 5 секунд

if __name__ == "__main__":
    main()