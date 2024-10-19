import subprocess
import time
import itertools
import csv
import os

def run_bash_command(command):
    process = subprocess.Popen(command, shell=True)
    return process

def are_processes_running(processes):
    return any(process.poll() is None for process in processes)

def mcpat(ejemplo=0):
    programs = [
    "h264_dec",
    "h264_enc",
    "jpg2k_dec",
    "jpg2k_enc",
    "mp3_dec",
    "mp3_enc"
    ]
    if ejemplo!=0:
        comands = f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[0]}/stats.txt {programs[0]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml"
        mcpat_commands = "./../mcpat/mcpat -infile ../mcpat/ProcessorDescriptionFiles/ARM_A9_2GHz_withIOC.xml "
        subprocess.run(comands + "&&" + mcpat_commands+ f"> energy.txt", shell=True )
    return False

    
    mcpatpy_commands = [
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[0]}/stats.txt {programs[0]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[1]}/stats.txt {programs[1]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[2]}/stats.txt {programs[2]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[3]}/stats.txt {programs[3]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[4]}/stats.txt {programs[4]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[5]}/stats.txt {programs[5]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml"
    ]
    #  ./mcpat -infile <*.xml>  -print_level < level of detailed output>
    #  ./mcpat -h (or mcpat --help) will show the quick help message.
    mcpat_commands = "./../mcpat/mcpat -infile config.xml.xml "
    i=0
    for comands in mcpatpy_commands:
        subprocess.run(comands + "&&" + mcpat_commands+ f"> {programs[i]}/energy.txt", shell=True )
        i+=1

def extract_potencia(nombre_archivo):



    # Inicializar variables para almacenar los totales
    total_leakage = 0.0
    runtime_dynamic = None  # Inicializamos como None para capturar solo el primer valor

    # Leer el archivo y procesar las primeras 30 líneas
    with open(nombre_archivo, 'r') as archivo:
        for i in range(20):  # Limitar a las primeras 30 líneas
            linea = archivo.readline()
            if not linea:  # Si no hay más líneas, salir del bucle
                break
            
            # Limpiar la línea y buscar los valores
            linea = linea.strip()
            if "Total Leakage" in linea:
                # Extraer el valor de Total Leakage
                try:
                    valor = float(linea.split('=')[1].strip().split()[0])  # Usamos '=' y luego tomamos el primer valor
                    total_leakage += valor
                except ValueError:
                    print(f"Error al convertir el valor de Total Leakage en la línea: '{linea}'")
            
            elif "Runtime Dynamic" in linea and runtime_dynamic is None:
                # Extraer el primer valor de Runtime Dynamic
                try:
                    runtime_dynamic = float(linea.split('=')[1].strip().split()[0])  # Usamos '=' y luego tomamos el primer valor
                except ValueError:
                    print(f"Error al convertir el valor de Runtime Dynamic en la línea: '{linea}'")

    if runtime_dynamic==None:
        return 0.0
    # Realizar la operación
    resultado = total_leakage + runtime_dynamic

    # Imprimir el resultado
    #print(f"Total leakage: {total_leakage}")
    #print(f"Runtime Dynamic: {runtime_dynamic}")
    #print(f"Suma (Total leakage + Runtime Dynamic): {resultado}")
    return resultado

def extract_stats(file_path):
    simInsts = None
    system_cpu_cpi = None
    system_cpu_ipc = None

    with open(file_path, 'r') as file:
        for _ in range(20):
            line = file.readline()
            if not line:
                break
            if "simInsts" in line:
                simInsts = int(line.split()[1])
            elif "system.cpu.cpi" in line:
                system_cpu_cpi = float(line.split()[1])
            elif "system.cpu.ipc" in line:
                system_cpu_ipc = float(line.split()[1])

    return simInsts, system_cpu_cpi, system_cpu_ipc

def eval_state(estado):
    programs = [
    "h264_dec",
    "h264_enc",
    "jpg2k_dec",
    "jpg2k_enc",
    "mp3_dec",
    "mp3_enc"
    ]

    parametros=["--l1i_size=","--num_fu_intALU=","--num_fu_read=","--num_fu_write=","--num_fu_FP_SIMD_ALU="]
    parametro0=["32kB ","64kB ","128kB ","256kB "]
    parametro1=["2 ","4 ","6 ","8 "]
    parametro2=["2 ","4 ","6 ","8 "]
    parametro3=["2 ","4 ","6 ","8 "]
    parametro4=["1 ","2 ","4 ","8 "]

    programs_path = [
        "../workloads/h264_dec/",
        "../workloads/h264_enc/",
        "../workloads/jpeg2k_dec/",
        "../workloads/jpeg2k_enc/",
        "../workloads/mp3_dec/",
        "../workloads/mp3_enc/"
    ]
    
    program_options = [
        f"{programs_path[0]}h264dec_testfile.264 {programs_path[0]}h264dec_outfile.yuv",
        f"{programs_path[1]}h264enc_configfile.cfg -org {programs_path[1]}h264enc_testfile.yuv -org ",
        f"-i {programs_path[2]}jpg2kdec_testfile.j2k -o {programs_path[2]}jpg2kdec_outfile.bmp",
        f"-i {programs_path[3]}jpg2kenc_testfile.bmp -o {programs_path[3]}jpg2kenc_outfile.j2k",
        f"-w {programs_path[4]}mp3dec_outfile.wav {programs_path[4]}mp3dec_testfile.mp3",
        f"{programs_path[5]}mp3enc_testfile.wav {programs_path[5]}mp3enc_outfile.mp3",
    ]
    gem5_path = "../gem5/build/ARM"
    python_cortex_path = "../scripts/CortexA76_scripts_gem5"
    parametros_str = parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4] + parametro4[estado[4]]

    bash_commands = [
        f"{gem5_path}/gem5.fast -d {programs[0]} {python_cortex_path}/CortexA76.py --cmd={programs_path[0]+programs[0]} --options=\"{program_options[0]}\" {parametros_str} && echo 'Terminó el proceso 1'",
        f"{gem5_path}/gem5.fast -d {programs[1]} {python_cortex_path}/CortexA76.py --cmd={programs_path[1]+programs[1]} --options=\"{program_options[1]}\" {parametros_str} && echo 'Terminó el proceso 2'",
        f"{gem5_path}/gem5.fast -d {programs[2]} {python_cortex_path}/CortexA76.py --cmd={programs_path[2]+programs[2]} --options=\"{program_options[2]}\" {parametros_str} && echo 'Terminó el proceso 3'",
        f"{gem5_path}/gem5.fast -d {programs[3]} {python_cortex_path}/CortexA76.py --cmd={programs_path[3]+programs[3]} --options=\"{program_options[3]}\" {parametros_str} && echo 'Terminó el proceso 4'",
        f"{gem5_path}/gem5.fast -d {programs[4]} {python_cortex_path}/CortexA76.py --cmd={programs_path[4]+programs[4]} --options=\"{program_options[4]}\" {parametros_str} && echo 'Terminó el proceso 5'",
        f"{gem5_path}/gem5.fast -d {programs[5]} {python_cortex_path}/CortexA76.py --cmd={programs_path[5]+programs[5]} --options=\"{program_options[5]}\" {parametros_str} && echo 'Terminó el proceso 6'"
    ]

    processes = []
    for command in bash_commands:
        processes.append(run_bash_command(command))
        time.sleep(5)

    print("Los procesos de Bash están corriendo...")

    seg = 0
    minutes = 0
    while are_processes_running(processes):
        if seg == 60:
            minutes += 1
            seg = 0
            print(f"Al menos un proceso sigue corriendo... lleva {minutes} minutos")
        time.sleep(1)
        seg += 1

    print("Todos los procesos han terminado.")

def save_new_data(estado):

    programs = [
    "h264_dec",
    "h264_enc",
    "jpg2k_dec",
    "jpg2k_enc",
    "mp3_dec",
    "mp3_enc"
    ]
    
    results_file = "Results.csv"
    avg_results_file = "AvgResults.csv"
    csv_writer=0
    avg_csv_writer=0
    experimento=0
    # Verificar si el archivo de resultados existe y escribir encabezados si no
    if not os.path.exists(results_file):
        with open(results_file, mode="a", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Experimento", "Programa", "Parametro 1", "Parametro 2", "Parametro 3", "Parametro 4", "Parametro 5", "simInsts", "system_cpu_cpi", "system_cpu_ipc", "CPUtime","energy"])  # Escribir los encabezados
    else:
        with open(results_file, mode="a", newline="") as file:
            csv_writer = csv.writer(file)

    # Verificar si el archivo de promedios existe y escribir encabezados si no
    if not os.path.exists(avg_results_file):
        with open(avg_results_file, mode="a", newline="") as avg_file:
            avg_csv_writer = csv.writer(avg_file)
            avg_csv_writer.writerow(["Experimento", "avg_cpi", "avg_ipc", "CPU time","avg_energy"])  # Escribir encabezados para el CSV de promedios
    else:
        with open(avg_results_file, mode="a", newline="") as avg_file:
            avg_csv_writer = csv.writer(avg_file)
            experimento = sum(1 for _ in avg_csv_writer) - 1
            avg_csv_writer = csv.writer(avg_file)

    #crea los archivos de potencia
    mcpat()

    # Guardar los resultados en el archivo CSV y calcular promedios
    total_cpi = 0
    total_ipc = 0
    total_cput = 0
    total_energy = 0
    avg_DET = 0 
    for i in range(6):
        simInsts, system_cpu_cpi, system_cpu_ipc = extract_stats(f"{programs[i]}/stats.txt")
        energy = extract_potencia(f"{programs[i]}/energy.txt")
        
        # Sumar los valores de CPI e IPC para promediar en la última fila
        total_cpi += system_cpu_cpi
        total_ipc += system_cpu_ipc
        cpu_time = simInsts * system_cpu_cpi * (1 / (2.1 * 10**9))
        total_cput += cpu_time

        if i == 5:  # En el sexto programa, escribir promedios en columnas "avg_cpi" y "avg_ipc"
            avg_cpi = total_cpi / 6
            avg_ipc = total_ipc / 6
            avg_cpu = total_cput / 6
            avg_energy = total_energy / 6
            avg_DET = avg_energy*(avg_cpi**2)
            csv_writer.writerow([experimento, programs[i], estado[0], estado[1], estado[2], estado[3], estado[4], simInsts, system_cpu_cpi, system_cpu_ipc, cpu_time,energy*(system_cpu_cpi**2)])
            avg_csv_writer.writerow([experimento, avg_cpi, avg_ipc, avg_cpu, avg_DET])  # Guardar avg_cpi y avg_ipc en el nuevo CSV
        else:
            csv_writer.writerow([experimento, programs[i], estado[0], estado[1], estado[2], estado[3], estado[4], simInsts, system_cpu_cpi, system_cpu_ipc, cpu_time, cpu_time,energy*(system_cpu_cpi**2)])
        
    return avg_DET

