import gi

gi.require_version('Gst', '1.0')

from gi.repository import Gst

import hailo
import cv2
import numpy as np
import os
import sys
import argparse # Adicionado para parsear argumentos da linha de comando

from hailo_apps_infra.hailo_rpi_common import app_callback_class, get_caps_from_pad, get_numpy_from_buffer
from hailo_apps_infra.detection_pipeline_simple import GStreamerDetectionApp

# Criando a pasta principal "run"
MAIN_FOLDER = "run"
os.makedirs(MAIN_FOLDER, exist_ok=True)

# Descobrindo o nÃºmero da prÃ³xima execuÃ§Ã£o
existing_runs = [d for d in os.listdir(MAIN_FOLDER) if d.startswith("teste")]
run_number = len(existing_runs) + 1  # PrÃ³ximo nÃºmero disponÃ­vel

# Criando a subpasta para esta execuÃ§Ã£o
CURRENT_RUN_FOLDER = os.path.join(MAIN_FOLDER, f"teste{run_number}")
os.makedirs(CURRENT_RUN_FOLDER, exist_ok=True)

class user_app_callback_class(app_callback_class):
    def __init__(self, video_name_arg): # Modificado para aceitar o nome do vídeo
        super().__init__()
        self.video_name = video_name_arg # Armazena o nome do vídeo
        self.previous_frame = 0  # Inicializa variÃ¡vel para rastrear o Ãºltimo frame processado

def app_callback(pad, info, user_data):
    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    user_data.increment()
    current_frame = user_data.get_count()
    video_name = user_data.video_name # Obtém o nome do vídeo a partir de user_data

    format, width, height = get_caps_from_pad(pad)
    frame = get_numpy_from_buffer(buffer, format, width, height)

    if frame is None:
        print("Erro ao obter o frame do buffer")
        return Gst.PadProbeReturn.OK

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    user_data.previous_frame = current_frame  # Atualiza o Ãºltimo frame processado

    for detection in hailo.get_roi_from_buffer(buffer).get_objects_typed(hailo.HAILO_DETECTION):
        bbox = detection.get_bbox()
        x_min = int(bbox.xmin() * width)
        x_max = int(bbox.xmax() * width)
        y_min = int(bbox.ymin() * height)
        y_max = int(bbox.ymax() * height)

        x_min = max(0, min(x_min, width))
        x_max = max(0, min(x_max, width))
        y_min = max(0, min(y_min, height))
        y_max = max(0, min(y_max, height))

        cropped_img = frame[y_min:y_max, x_min:x_max]

        if cropped_img.size > 0:
            label = detection.get_label()
            
            # --- Obter valor de confiança ---
            # ADVERTÊNCIA: O método detection.get_confidence() é uma suposição.
            # Verifique a documentação da API Hailo para o método correto.
            # Pode ser detection.score(), detection.get_score(), ou um atributo.
            try:
                confidence = detection.get_confidence() 
            except AttributeError:
                print("AVISO: O método 'detection.get_confidence()' não foi encontrado.")
                print("Verifique a API Hailo para o método correto de obter a confiança da detecção.")
                print("Usando confiança = 0.00 como padrão.")
                confidence = 0.00 # Valor padrão caso o método não seja encontrado

            category_folder = os.path.join(CURRENT_RUN_FOLDER, label)
            os.makedirs(category_folder, exist_ok=True)

            # --- Nome do arquivo modificado ---
            # Inclui nome do vídeo, número do frame, label e confiança (formatada com 2 casas decimais)
            filename = os.path.join(category_folder, 
                                    f"video_{video_name}_frame_{current_frame}_label_{label}_conf_{confidence:.2f}.jpg")
            cv2.imwrite(filename, cropped_img)
            print(f"Saved cropped image in {category_folder}: {filename}")
        else:
            print("Erro: Tentativa de recorte de uma regiÃ£o vazia!")

    return Gst.PadProbeReturn.OK

def eos_callback(bus, message):
    if message.type == Gst.MessageType.EOS:
        print("Fim do vÃ­deo detectado! Encerrando execuÃ§Ã£o corretamente...")
        sys.exit(0)

if __name__ == "__main__":
    # --- Parseamento de Argumentos para obter o nome do vídeo de entrada ---
    # Criamos um parser temporário para pegar o argumento --input
    # sem interferir com o parser de GStreamerDetectionApp.
    video_name_str = "unknown_video" # Valor padrão
    temp_parser = argparse.ArgumentParser(add_help=False) # add_help=False para não conflitar
    temp_parser.add_argument('--input', type=str)
    
    try:
        # parse_known_args pega os argumentos conhecidos e ignora o resto,
        # que será processado por GStreamerDetectionApp.
        known_args, _ = temp_parser.parse_known_args()
        if known_args.input:
            input_video_path = known_args.input
            # Extrai o nome base do arquivo e remove a extensão
            video_name_str = os.path.splitext(os.path.basename(input_video_path))[0]
            # Sanitiza o nome do vídeo para uso em nomes de arquivo (remove espaços e pontos extras)
            video_name_str = video_name_str.replace(" ", "_").replace(".", "_")
        else:
            print("AVISO: Argumento --input não fornecido ou não encontrado pelo parser temporário. Usando 'unknown_video' no nome dos arquivos.")
            
    except Exception as e:
        print(f"AVISO: Não foi possível parsear o argumento --input para nomeação customizada (erro: {e}). Usando 'unknown_video'.")
        # GStreamerDetectionApp ainda fará seu próprio parseamento e reportará erros se --input for crucial para ele.

    # Inicializa user_data com o nome do vídeo
    user_data = user_app_callback_class(video_name_str)
    
    # GStreamerDetectionApp provavelmente fará seu próprio parseamento de sys.argv
    app = GStreamerDetectionApp(app_callback, user_data)
    
    print(f"Iniciando execuÃ§Ã£o {run_number}: imagens serÃ£o salvas em '{CURRENT_RUN_FOLDER}'")
    print(f"Nome do vídeo para salvamento nos arquivos: '{video_name_str}'") # Confirmação
    
    # ðŸ”¹ Capturando evento de EOS no pipeline
    bus = app.pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", eos_callback)
    
    app.run()  # Executa a pipeline
    
    print("ExecuÃ§Ã£o finalizada! Encerrando o programa...")
    sys.exit(0)  # Finaliza o script corretamente