import subprocess
import time
import itertools
import csv
import os
import random

#Funciones:
#Camilo Alvarez Muñoz
#Daniel Cano Restrepo

def lista_aleatoria(tamano):
    #Funcion para generar un estado aleatorio de la DSE para utilizar como punto inicial del recocido simulado
    return [random.randint(0, 2) for _ in range(tamano)]

def run_bash_command(command):
    #Ejecuta un comando de bash en el sistema
    process = subprocess.Popen(command, shell=True)
    return process

def are_processes_running(processes):
    #Verifica si los procesos de bash siguen ejecutandose
    return any(process.poll() is None for process in processes)

def mcpat():
    #Esta función ejecuta McPAT para extraer los resultados de potencia y energia de cada programa
    programs = [
    "h264_dec",
    "h264_enc",
    "jpg2k_dec",
    "jpg2k_enc",
    "mp3_dec",
    "mp3_enc"
    ]

    #Lista de comandos para ejecutar McPAT para cada programa
    mcpatpy_commands = [
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[0]}/stats.txt {programs[0]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[1]}/stats.txt {programs[1]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[2]}/stats.txt {programs[2]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[3]}/stats.txt {programs[3]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[4]}/stats.txt {programs[4]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml",
        f"python3 ../scripts/McPAT/gem5toMcPAT_cortexA76.py {programs[5]}/stats.txt {programs[5]}/config.json ../scripts/McPAT/ARM_A76_2.1GHz.xml"
    ]
    #./mcpat -infile <*.xml>  -print_level < level of detailed output>
    mcpat_commands = "./../mcpat/mcpat -infile config.xml"
    i=0
    #Ejecuta en primer lugar el archivo de python para generar el archivo config.xml y luego ejecuta McPAT con este mismo archivo
    for comands in mcpatpy_commands:
        subprocess.run(comands, shell=True )
        subprocess.run(mcpat_commands+ f"> {programs[i]}/energy.txt", shell=True )
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

    return resultado

def extract_stats(file_path):
    #Esta función lee los archivos stats.txt de cada programa y extrae los valores de simInsts, system.cpu.cpi y system.cpu.ipc
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
    #Lista de los programas a ejecutar
    programs = [
    "h264_dec",
    "h264_enc",
    "jpg2k_dec",
    "jpg2k_enc",
    "mp3_dec",
    "mp3_enc"
    ]

    #Espacio de diseño: 
    #Parametros a modificar del procesador
    parametros=[
        "--num_fu_intALU=",
        "--num_fu_read=",
        "--num_fu_write=",
        "--num_fu_FP_SIMD_ALU=",
        "--l1i_size=",
        "--l1i_assoc=",
        "--l1d_size=",
        "--l1d_assoc="
        ]
    
    #Valores de cada parametro:
    parametro0=["2 ","4 ","6 "]#Numero de unidades funcionales para las instrucciones de ALU enteros 
    parametro1=["2 ","4 ","6 "]#Numero de unidades funcionales para las instrucciones Load
    parametro2=["2 ","4 ","6 "]#Numero de unidades funcionales para las instrucciones store
    parametro3=["1 ","2 ","4 "]#Numero de unidades funcionales para las instrucciones float y SIMD
    parametro4=["64kB ","128kB ","256kB "]#Tamaño de la cache de instrucciones L1
    parametro5=["4 ","8 ","16 "]#Asociatividad de la cache de instrucciones L1
    parametro6=["64kB ","128kB ","256kB "]#Tamaño de la cache de datos L1
    parametro7=["4 ","8 ","16 "]#Asociatividad de la cache de datos L1

    #Rutas de los programas a ejecutar en la carpeta workloads
    programs_path = [
        "../workloads/h264_dec/",
        "../workloads/h264_enc/",
        "../workloads/jpeg2k_dec/",
        "../workloads/jpeg2k_enc/",
        "../workloads/mp3_dec/",
        "../workloads/mp3_enc/"
    ]
    
    #Opciones adicionales de los programas a ejecutar
    program_options = [
        f"{programs_path[0]}h264dec_testfile.264 {programs_path[0]}h264dec_outfile.yuv",
        f"{programs_path[1]}h264enc_configfile.cfg -org {programs_path[1]}h264enc_testfile.yuv -bf {programs_path[1]}h264enc_testfile.264 ",
        f"-i {programs_path[2]}jpg2kdec_testfile.j2k -o {programs_path[2]}jpg2kdec_outfile.bmp",
        f"-i {programs_path[3]}jpg2kenc_testfile.bmp -o {programs_path[3]}jpg2kenc_outfile.j2k",
        f"-w {programs_path[4]}mp3dec_outfile.wav {programs_path[4]}mp3dec_testfile.mp3",
        f"{programs_path[5]}mp3enc_testfile.wav {programs_path[5]}mp3enc_outfile.mp3",
    ]
    #Ruta del gem5.fast
    gem5_path = "../gem5/build/ARM"
    #Ruta del script de python para parametros del procesador CortexA76
    python_cortex_path = "../scripts/CortexA76_scripts_gem5"
    parametros_str = parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4] + parametro4[estado[4]] + parametros[5] + parametro5[estado[5]] + parametros[6] + parametro6[estado[6]] + parametros[7] + parametro7[estado[7]]

    #Comandos de bash para ejecutar los programas en gem5
    bash_commands = [
        f"{gem5_path}/gem5.fast -d {programs[0]} {python_cortex_path}/CortexA76.py --cmd={programs_path[0]+programs[0]} --options=\"{program_options[0]}\" {parametros_str} && echo 'Terminó el proceso 1'",
        f"{gem5_path}/gem5.fast -d {programs[1]} {python_cortex_path}/CortexA76.py --cmd={programs_path[1]+programs[1]} --options=\"{program_options[1]}\" {parametros_str} && echo 'Terminó el proceso 2'",
        f"{gem5_path}/gem5.fast -d {programs[2]} {python_cortex_path}/CortexA76.py --cmd={programs_path[2]+programs[2]} --options=\"{program_options[2]}\" {parametros_str} && echo 'Terminó el proceso 3'",
        f"{gem5_path}/gem5.fast -d {programs[3]} {python_cortex_path}/CortexA76.py --cmd={programs_path[3]+programs[3]} --options=\"{program_options[3]}\" {parametros_str} && echo 'Terminó el proceso 4'",
        f"{gem5_path}/gem5.fast -d {programs[4]} {python_cortex_path}/CortexA76.py --cmd={programs_path[4]+programs[4]} --options=\"{program_options[4]}\" {parametros_str} && echo 'Terminó el proceso 5'",
        f"{gem5_path}/gem5.fast -d {programs[5]} {python_cortex_path}/CortexA76.py --cmd={programs_path[5]+programs[5]} --options=\"{program_options[5]}\" {parametros_str} && echo 'Terminó el proceso 6'"
    ]

    processes = []
    #Este ciclo ejecuta todos los programas bash de la lista de forma simultanea
    for command in bash_commands:
        processes.append(run_bash_command(command))
        time.sleep(5)

    print("Los procesos de Bash están corriendo...")

    seg = 0
    minutes = 0
    #Este ciclo verifica si los procesos de bash han terminado, cuando acabe la simulación de mayor tiempo se saldrá del ciclo
    while are_processes_running(processes):
        if seg == 60:
            minutes += 1
            seg = 0
            print(f"Al menos un proceso sigue corriendo... lleva {minutes} minutos")
        time.sleep(1)
        seg += 1

    print("Todos los procesos han terminado.")

def save_new_data(estado):

    #Llamamos la función para ejecutar McPAT y extraer los resultados de potencia y energia de cada programa
    mcpat()

    #Lista de los programas a ejecutar
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
            csv_writer.writerow(["Experimento", "Programa", "Parametro 1", "Parametro 2", "Parametro 3", "Parametro 4", "Parametro 5", "Parametro 6", "Parametro 7", "Parametro 8", "simInsts", "system_cpu_cpi", "system_cpu_ipc", "CPUtime","power","EDP"])  # Escribir los encabezados

    # Verificar si el archivo de promedios existe y escribir encabezados si no
    if not os.path.exists(avg_results_file):
        with open(avg_results_file, mode="a", newline="") as avg_file:
            avg_csv_writer = csv.writer(avg_file)
            avg_csv_writer.writerow(["Experimento", "avg_cpi", "avg_ipc", "avg_CPU_time","avg_power","avg_EDP"])  # Escribir encabezados para el CSV de promedios
    else:
        with open(avg_results_file, 'r') as avg_file:
            reader = csv.reader(avg_file)
            experimento = sum(1 for _ in reader) - 1

    #crea los archivos de potencia

    # Guardar los resultados en el archivo CSV y calcular promedios
    total_cpi = 0
    total_ipc = 0
    total_cput = 0
    total_EDP = 0
    total_energy = 0
     
    #Iterar sobre las carpetas de resultados de los 6 programas
    for i in range(6):
        simInsts, system_cpu_cpi, system_cpu_ipc = extract_stats(f"{programs[i]}/stats.txt")
        energy = extract_potencia(f"{programs[i]}/energy.txt")
        energy = energy * system_cpu_cpi
        
        # Sumar los valores de CPI e IPC para promediar en la última fila
        total_cpi += system_cpu_cpi
        total_ipc += system_cpu_ipc
        
        #CPU time = IC * CPI * CT
        cpu_time = simInsts * system_cpu_cpi * (1 / (2.1 * 10**9))
        total_cput += cpu_time
        
        #Energy = (Total leakage + Runtime Dynamic) * System.cpu.cpi
        total_energy += energy
        #Energy-Delay Product (EDP)
        EDP = energy*system_cpu_cpi
        total_EDP += EDP

        if i == 5:  # En el sexto programa, escribir promedios en el archivo avgResults
            avg_cpi = total_cpi / 6
            avg_ipc = total_ipc / 6
            avg_cpu = total_cput / 6
            avg_energy = total_energy / 6
            avg_EDP = total_EDP / 6

            #Escribir los resultados de cada simulación en el archivo de resultados
            with open(results_file, mode="a", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([experimento, programs[i], estado[0], estado[1], estado[2], estado[3], estado[4], estado[5], estado[6], estado[7], simInsts, system_cpu_cpi, system_cpu_ipc, cpu_time, energy , EDP])
            
            #Escribir los promedios al momento de tener los resultados de los 6 programas
            with open(avg_results_file, mode="a", newline="") as avg_file:
                avg_csv_writer = csv.writer(avg_file)
                avg_csv_writer.writerow([experimento, avg_cpi, avg_ipc, avg_cpu , avg_energy, avg_EDP])
        
        else:
            with open(results_file, mode="a", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([experimento, programs[i], estado[0], estado[1], estado[2], estado[3], estado[4], estado[5], estado[6], estado[7], simInsts, system_cpu_cpi, system_cpu_ipc, cpu_time, energy, EDP])
         
    return avg_EDP#Retorna el EDP promedio que servirá como función objetivo

