import time
import subprocess

def run_script():
    start_time = time.time()
    end_time = start_time + 7 * 60 * 60  # 7 horas em segundos

    while time.time() < end_time:
        try:
            subprocess.run(["python", "download_and_segment.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o script: {e}")

def comment_next_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    all_commented = True
    with open(file_path, 'w') as file:
        found_uncommented = False
        for line in lines:
            if not line.startswith("#") and not found_uncommented:
                file.write("#" + line)
                found_uncommented = True
                all_commented = False
            else:
                file.write(line)
                
    if not found_uncommented:
        print("Todas as linhas já estão comentadas.")
    
    return all_commented




while True:
    print("Iniciando execução ...")
    try:
        run_script()
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.gmtime()) - 3 * 3600)))

    print("Finalizando período de 7 horas, comentando a próxima linha.")
    all_commented = comment_next_line('input/channels_id_example.txt')
    if all_commented:
        print("Todas as linhas estão comentadas. Encerrando.")
        break
    print("Linha comentada. Reiniciando...")
