# Ambiente de validação

O desenvolvimento do projeto segue a abordagem mostrada no diagrama apresentado na figura, que ilustra as fases essenciais do processo: ajustes e otimização, implementação,
e monitoramento e manutenção. Essas etapas estão na fase de testes práticos no Raspberry Pi 5, utilizando o módulo de aceleração Hailo, e na criação dos parâmetros do arquivo labels.

Inicialmente, a etapa de ajustes e otimização corresponde à configuração do arquivo labels para garantir um desempenho adequado. Em seguida, a implementação marca o momento em que o sistema treinado é carregado no
Raspberry Pi 5, possibilitando a execução dos testes práticos com hardware real, validando as respostas do modelo YOLO ao reconhecimento de sinalização viária.
Por fim, a fase de monitoramento e manutenção é essencial para a avaliação contínua do desempenho do sistema, garantindo que possíveis ajustes sejam realizados conforme necessário para melhorar a precisão da detecção.

![diagrame_etapa_2](https://raw.githubusercontent.com/bile6842/Yolo-Sinaliza-o-de-Transito/refs/heads/main/img/Diagrama_etapa_2.png)

## Ambiente Rapberry PI

O sistema operacional utilizado no Raspberry Pi foi o Raspberry Pi OS Bookworm (64-bit), versão lançada em 19 de novembro de 2024. A instalação foi realizada em um cartão de memória SanDisk de 64 GB,
garantindo compatibilidade e desempenho adequado para a execução do modelo e demais aplicações.

## Aquisição de Imagens

A câmera utilizada no projeto foi o Camera Module v2, um modelo compatível com o Raspberry Pi, projetado para a captura de imagens. Esse dispositivo foi utilizado com raspberry pi 5 na gravação de trajetos com 
resolução de 640x480 pixels, garantindo que todos os modelos fossem testados sob as mesmas condições. Esse processo é fundamental para a padronização da validação, permitindo uma comparação justa do desempenho entre 
os diferentes modelos analisados.

Comando utilizado para as gravações

rpicam-vid -t `tempo` --width `largura` --height `altura` -o `nome`

```bash
rpicam-vid -t 1200000000000 --width 640 --height 480 -o trajeto2.mp4
```

Onde:

- `tempo` tempo de gravação maximo, defini um valor alto para eu conseguir encerrar a gravação apertando `CTRL+C`.
- `largura` largura em px.
- `altura` altura em px.
- `nome` nome e extenção da gravação.

## Execução do Modelo

O repositório do HAILO foi clonado, permitindo acesso a exemplos de códigos prontos para a execução do modelo. O comando utilizado para a clonagem está apresentado no Quadro.
```bash
git clone https://github.com/hailo-ai/hailo-rpi5-exemples.git 
```

Foi modificado o `detection_simple.py` localizado em `hailo-rpi5-examples/basic_pipelines` fazendo que quando previse alguma classe realizava a extração das cordenadas e utlizava realizar um crop da area pervista salvando
na extrutura de pasta esta abaixo, com a extrutua do nome do arquivo assim "video`_video`_frame`_frame`_label`_calsse`_conf`_confianã`.jpg" Exemplo de nome do arquivo `video_trajeto2_frame_7527_label_20km-h_conf_0.78.jpg`.

Após a clonagem do repositória foi criado uma pasta `tcc` para salvar os arquivos que servirão para os teste dentre eles os modelos YOLO, detection.py customizado e o label.json o Quadro mostra o arquivo label.json criado contendo os parâmetros.

### label.json

```json
{ "iou_threshold": 0.45,
  "detection_threshold": 0.7,
  "max_boxes": 50,
  "labels": [
    "",
    "100km-h",
    "10km-h",
    "110km-h",
    "120km-h",
    "20km-h",
    "30km-h",
    "40km-h",
    "50km-h",
    "60km-h",
    "70km-h",
    "80km-h",
    "90km-h",
    "Estacionamento",
    "Lombada",
    "Pare",
    "Proibido Estacionar",
    "Proibido Parar e Estacionar",
    "Rotatoria"]}

```
Onde:

- `iou_threshold` Este é o limiar de Intersecção sobre União (IoU). Durante a pós-processamento das detecções, se duas caixas delimitadoras (bounding boxes) previstas para o mesmo objeto tiverem um IoU maior que este valor, a caixa com menor pontuação de confiança é geralmente suprimida. Isso ajuda a evitar múltiplas detecções para um único objeto.
- `detection_threshold` Este é o limiar de confiança da detecção. Somente as detecções com uma pontuação de confiança igual ou superior a este valor (neste caso, 70%) serão consideradas válidas. Detecções com confiança inferior a 0.7 serão descartadas. Este parâmetro é crucial para filtrar detecções fracas e reduzir falsos positivos.
- `max_boxes` Define o número máximo de caixas delimitadoras (objetos detectados) que o modelo pode retornar por imagem processada.
- `labels`  Esta lista contém os nomes das classes que o modelo foi treinado para detectar. A ordem dos rótulos nesta lista é importante, pois o índice de cada rótulo corresponde à saída numérica do modelo.
O primeiro item é uma string vazia. Isso é comum e geralmente representa a classe de ´fundo´ (background) ou é um placeholder, indicando que o índice 0 não corresponde a um objeto de interesse específico.
"100km-h", "10km-h", ..., "Rotatoria": São os nomes específicos das placas de trânsito e outros sinais que o modelo consegue identificar. Por exemplo, se o modelo detectar um objeto com o índice 1, ele será rotulado como "100km-h".

### detection modificado (detection.py)

~~~python
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
~~~

### Estrutura de salvamento dos crops

 ```
  run
  ├── teste
  ├── teste1
  ├── teste2
  │   ├── 20km-h
  │   ├── 50km-h
  │   └── pare
  │       ├── video_trajeto7_frame_34261_label_Pare_conf_0.90.jpg
  │       ├── video_trajeto7_frame_34262_label_Pare_conf_0.88.jpg
  │       ├── video_trajeto7_frame_34263_label_Pare_conf_0.90.jpg
 
  ```

-   `run/`
    -   `nome_teste/`
        -   `previsão/`
            -  `nome_do_crop.jpg`
            -  `nome_do_crop.jpg`
            -  `nome_do_crop.jpg`

Onde:

- `nome_teste` conforme a execução dos modelo ele cria a pasta com o nome `teste`, se ja existir a `teste` ele cria a `teste1` e assim sucessivamente.
- `previsão` sempre que uma previsao acontece tem uma classe vinculada e o codigo utiliza o nome da classe para verificar se a pasta ja existe se nao existir ele cria uma pasta com o nome da classe.
- `nome_do_crop.jpg` salva os crops na pastas correspondente a classe prevista.

### 

Após a conclusão da configuração, o script de criação do ambiente virtual foi executado. 
Os comando correspondente está apresentado nos Quadros.

1. Comando para executar o configurador do ambiente virtual
```bash
./install.sh
```

2. Executa o Ambiente Virtual
```bash
source setup env.sh
```

Em seguida, o script detection.py foi executado, especificando os parametros descritos abaixo. 
caminho do modelo best.hef, o trajeto gravado e o arquivo label.json, garantindo a correta aplicação dos ajustes necessários para a detecção. 
O comando correspondente está apresentado no Quadro.

1. Comado para executar o modelo.hef
```bash
python3 tcc/detection.py --hef-path tcc/yolov8s_coco.hef –input ~/Desktop/trajeto2.mp4 --labels-json tcc/labels.json --show-fps
```

Onde:
    python3 tcc/detection.py --hef-path `modelo.hef` –input `local_do_video` --labels-json `label.json` --show-fps

- `modelo.hef` caminho do modelo best.hef.
- `local_do_video` o trajeto gravado.
- `label.json` e o arquivo ´label.json´.


# Proximo Topico

- [Analise dos modelos nos trajetos](./analise_dos_modelos_nos_trajetos.md)
  
