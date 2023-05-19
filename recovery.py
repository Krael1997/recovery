__author__ = "abelrodr"
__copyright__ = "Copyright 2023, Cybersec Bootcamp Malaga"
__credits__ = ["abelrodr"]
__email__ = "abelrodr42malaga@gmail.com"

print('''
@@@@@@@@@@@@@@@@@@@,**@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@,,@@@@@*******@@@@@@@@@@
@@@@@@@,,,,,@@@@@@@@@@@@@@@@@@****@/**@@
@@@@@,,,@@,,@@@@@@@@@@@@@@@@@@@@@*****@@
@@@,,,@@@@@@@@@@@###%%%%@@@@@@@*******@@
@@,,/@@@@@@@@##@@###%%%%@@%%@@@@@@@@@@@@
@,,*@@@@@@@#########%%%%%%%%%%@@@@@@@@@@
@,,@@@@@@@########@@@@@%%%%%%%%@@@@@@@**
,,,@@@@@@@@@#####@@@@@@@%%%%%@@@@@@@@@**
@,,@@@@@@@########@@@@@%%%%%%%%@@@@@@@**
@@@@@@@@@@@#########%%%%%%%%%%@@@@@@@***
@@@@@@@@@@@@@##@@###%%%%@@%%@@@@@@@@***@
@@@,,,,,,,@@@@@@@###%%%%@@@@@@@@@@@***@@
@@@,,,,,@@@@@@@@@@@@@@@@@@@@@**@@***@@@@
@@@,,@@,,,,@@@@@@@@@@@@@@@@@@*******@@@@
@@@@@@@@@@@,,,,,,,,@@@***@@@@@@@@@@@@@@@
''')

import datetime
import os
import sys
import psutil
import winreg

# Función para obtener la fecha y hora actual en un formato legible
def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Función para obtener la fecha y hora de hace un número de días dado
def get_past_time(days):
    return (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%%m-%d %H:%M:%S')

# Función para obtener la lista de programas instalados en el sistema
def get_installed_programs():
    programs = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall') as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                sub_key = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, sub_key) as sub_key:
                    program = {}
                    program['name'] = winreg.QueryValueEx(sub_key, 'DisplayName')[0]
                    program['version'] = winreg.QueryValueEx(sub_key, 'DisplayVersion')[0]
                    program['publisher'] = winreg.QueryValueEx(sub_key, 'Publisher')[0]
                    programs.append(program)
            except:
                pass
    return programs

# Función para obtener la lista de procesos en ejecución en el sistema
def get_running_processes():
    processes = []
    for proc in psutil.process_iter():
        try:
            process = {}
            process['pid'] = proc.pid
            process['name'] = proc.name()
            process['cpu_percent'] = proc.cpu_percent()
            process['memory_percent'] = proc.memory_percent()
            processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

# Función para obtener el historial de navegación de Internet Explorer
def get_ie_history(start_time, end_time):
    history = []
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\TypedURLs') as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                url = winreg.EnumValue(key, i)[1]
                timestamp = os.path.getmtime(os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'History', 'History.IE5', os.path.basename(url)))
                if start_time <= timestamp <= end_time:
                    history.append((url, timestamp))
            except:
                pass
    return history

# Función para obtener los dispositivos conectados al sistema
def get_connected_devices():
    devices = []
    for partition in psutil.disk_partitions():
        try:
            device = {}
            device['device'] = partition.device
            device['mountpoint'] = partition.mountpoint
            device['fstype'] = partition.fstype
            device['opts'] = partition.opts
            devices.append(device)
        except:
            pass
    return devices

# Función para imprimir la información obtenida
def print_info(programs, processes, history, devices, start_time, end_time):
    print(f'Información obtenida desde {start_time} hasta {end_time}:')
    print('Programas instalados:')
    for program in programs:
        print(f"Nombre: {program['name']}, Versión: {program['version']}, Publicador: {program['publisher']}")
    print('\nProcesos en ejecución:')
    for process in processes:
        print(f"PID: {process['pid']}, Nombre: {process['name']}, Uso de CPU: {process['cpu_percent']}%, Uso de memoria: {process['memory_percent']}%")
    print('\nHistorial de navegación de Internet Explorer:')
    for url, timestamp in history:
        print(f"URL: {url}, Fecha y hora: {datetime.datetime.fromtimestamp(timestamp)}")
    print('\nDispositivos conectados:')
    for device in devices:
        print(f"Dispositivo: {device['device']}, Punto de montaje: {device['mountpoint']}, Tipo de sistema de archivos: {device['fstype']}, Opciones de montaje: {device['opts']}")

# Función principal del programa
def main():
    # Obtenemos el rango de fechas a partir de los argumentos de línea de comandos
    if len(sys.argv) == 2:
        days = int(sys.argv[1])
        start_time = get_past_time(days)
        end_time = get_current_time()
    elif len(sys.argv) == 3:
        start_time = sys.argv[2]
        end_time = sys.argv[3]
    else:
        # Si no se proporciona ningún argumento, tomamos la última semana como rango de tiempo por defecto
        start_time = get_past_time(7)
        end_time = get_current_time()

    # Obtenemos la información de interés
    programs = get_installed_programs()
    processes = get_running_processes()
    history = get_ie_history(start_time, end_time)
    devices = get_connected_devices()

    # Imprimimos la información obtenida
    print_info(programs, processes, history, devices, start_time, end_time)

if __name__ == '__main__':
    main()