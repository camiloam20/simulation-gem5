import subprocess
import time

programs = [
    "h264_dec",
    "h264_enc",
    "jpg2k_dec",
    "jpg2k_enc",
    "mp3_dec",
    "mp3_enc"
]

def run_bash_command(command):
    # Iniciar el proceso de Bash sin bloquear la ejecución de Python
    process = subprocess.Popen(command, shell=True)
    return process

def are_processes_running(processes):
    # Verificar si alguno de los procesos sigue corriendo
    return any(process.poll() is None for process in processes)

def extract_stats(file_path):
    simInsts = None
    system_cpu_cpi = None
    system_cpu_ipc = None

    # Abrir el archivo y leer las primeras 20 líneas
    with open(file_path, 'r') as file:
        for _ in range(20):
            line = file.readline()
            # Verificar si se llegó al final del archivo antes de las 20 líneas
            if not line:
                break
            
            # Buscar las líneas que contienen los valores deseados
            if "simInsts" in line:
                simInsts = int(line.split()[1])
            elif "system.cpu.cpi" in line:
                system_cpu_cpi = float(line.split()[1])
            elif "system.cpu.ipc" in line:
                system_cpu_ipc = float(line.split()[1])

    return simInsts, system_cpu_cpi, system_cpu_ipc

def eval_state(estado):
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
    programs = [
        "h264_dec",
        "h264_enc",
        "jpg2k_dec",
        "jpg2k_enc",
        "mp3_dec",
        "mp3_enc"
    ]
    program_options = [
        f"{programs_path[0]}h264dec_testfile.264 {programs_path[0]}h264dec_outfile.yuv",
        f"{programs_path[1]}h264enc_configfile.cfg",
        f"-i {programs_path[2]}jpg2kdec_testfile.j2k -o {programs_path[2]}jpg2kdec_outfile.bmp",
        f"-i {programs_path[3]}jpg2kenc_testfile.bmp -o {programs_path[3]}jpg2kenc_outfile.j2k",
        f"-w {programs_path[4]}mp3dec_outfile.wav {programs_path[4]}mp3dec_testfile.mp3",
        f"{programs_path[5]}mp3enc_testfile.wav {programs_path[5]}mp3enc_outfile.mp3",
    ]
    gem5_path="../gem5/build/ARM"
    python_cortex_path="../scripts/CortexA76_scripts_gem5"


    # Lista de comandos de Bash que deseas ejecutar con un echo al final
    #$GEM5PATH/gem5.fast $SCRIPTDIR/CortexA76.py --cmd=h264_dec --options="h264dec_testfile.264 h264dec_outfile.yuv" $MOREOPTIONS
    bash_commands = [
        f"{gem5_path}/gem5.fast -d {programs[0]} {python_cortex_path}/CortexA76.py --cmd={programs_path[0]+programs[0]} --options=\"{program_options[0]}\" {parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4]+parametro4[estado[4]]} && echo 'Termino el proceso 1'",
        f"{gem5_path}/gem5.fast -d {programs[1]} {python_cortex_path}/CortexA76.py --cmd={programs_path[1]+programs[1]} --options=\"{program_options[1]}\" {parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4]+parametro4[estado[4]]} && echo 'Termino el proceso 2'",
        f"{gem5_path}/gem5.fast -d {programs[2]} {python_cortex_path}/CortexA76.py --cmd={programs_path[2]+programs[2]} --options=\"{program_options[2]}\" {parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4]+parametro4[estado[4]]} && echo 'Termino el proceso 3'",
        f"{gem5_path}/gem5.fast -d {programs[3]} {python_cortex_path}/CortexA76.py --cmd={programs_path[3]+programs[3]} --options=\"{program_options[3]}\" {parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4]+parametro4[estado[4]]} && echo 'Termino el proceso 4'",
        f"{gem5_path}/gem5.fast -d {programs[4]} {python_cortex_path}/CortexA76.py --cmd={programs_path[4]+programs[4]} --options=\"{program_options[4]}\" {parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4]+parametro4[estado[4]]} && echo 'Termino el proceso 5'",
        f"{gem5_path}/gem5.fast -d {programs[5]} {python_cortex_path}/CortexA76.py --cmd={programs_path[5]+programs[5]} --options=\"{program_options[5]}\" {parametros[0] + parametro0[estado[0]] + parametros[1] + parametro1[estado[1]] + parametros[2] + parametro2[estado[2]] + parametros[3] + parametro3[estado[3]] + parametros[4]+parametro4[estado[4]]} && echo 'Termino el proceso 6'"
    ]

    # Ejecutar todos los comandos de Bash simultáneamente
    processes = []
    for command in bash_commands:
        processes.append(run_bash_command(command))
        time.sleep(5)  # Agregar un pequeño retraso de 100 ms entre el lanzamiento de cada proceso

    print("Los procesos de Bash están corriendo...")

    # Revisar periódicamente si alguno de los procesos sigue corriendo
    seg=0
    minutes=0
    while are_processes_running(processes):
        if(seg==60):
            minutes+=1
            seg=0
            print(f"Al menos un proceso sigue corriendo... lleva {minutes} minutos")
        time.sleep(1)
        seg+=1


    print("Todos los procesos han terminado.")

estado=[1,1,1,1,1]
eval_state(estado)
for i in range(0,6):
    print(extract_stats(f"{programs[i]}/stats.txt"))