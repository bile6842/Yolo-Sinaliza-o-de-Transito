# Yolo-Sinaliza-o-de-Transito

## 1-Comandos Instalação Framework ULTRALYTICS

  A instalação do framework ULTRALYTICS é realizada por meio do comando apresentado abaixo.

```bash
pip install ultralytics
```

  A utilização da versão em Docker para o framework HAILO DATAFLOW COMPILER é recomendada para garantir maior compatibilidade. Para isso, a imagem do contêiner Docker é obtida no site oficial na versão 2025-04, 
  e os comandos necessários para sua execução estão abaixo.


```bash
1. Adicionar a chave GPG oficial do Docker:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

2. Adicionar o repositório Docker:
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee/etc/apt/sources.list.d/docker.list > /dev/null

3. Atualizar a lista de pacotes:
sudo apt update

4. Instalar o Docker:
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

5. Adicionando o Container Hailo:
docker run --runtime=nvidia --gpus all -it hailo_ai_sw_suite_2025-04:1 /bin/bash
```
  
## 2-Comandos Instalação Framework ULTRALYTICS

Após a configuração do ambiente, utilizei o script Python com
o comando necessário para iniciar os treinamentos. Nesse script, foram ajustados
apenas o modelo utilizado (yolov8s, yolov10s e yolo11s), o parâmetro name, que
especifica o nome da pasta destinada ao armazenamento da rede e o parâmetro
batch, a fim de otimizar de maneira mais eficiente o uso da memória da GPU.

 ~~~Python
from ultralytics import YOLO
# Carregar o modelo YOLOv8
model = YOLO('yolov8s.yaml')
# Treinar o modelo
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8,patience=10, amp=False, name=’yolov8s_seed’)

# Carregar o modelo YOLOv10
model = YOLO('yolov10s.yaml')
# Treinar o modelo
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8,patience=10, amp=False, name=’yolov10s_seed’)

# Carregar o modelo YOLOv11s
model = YOLO('yolo11s.yaml')
# Treinar o modelo
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8,patience=10, amp=False, name=’yolo11s_seed’)

# Carregar o modelo YOLOv8 COCO
model = YOLO('yolov8s.pt')
# Treinar o modelo
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8,patience=10, amp=False, name=’yolov8s_coco’)

# Carregar o modelo YOLOv10 COCO
model = YOLO('yolov10s.pt')
# Treinar o modelo
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8,patience=10, amp=False, name=’yolov10s_coco’)

# Carregar o modelo YOLO11s COCO
model = YOLO('yolo11s.pt')
# Treinar o modelo
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8,patience=10, amp=False, name=’yolo11s_coco’)

~~~

A seleção do modelo mais adequado entre YOLOv8s, YOLOv10s e
YOLOv11s pode ser realizada com base na análise de diversas métricas
fundamentais, que avaliam a eficiência da rede neural na classificação de placas de
trânsito. As principais métricas consideradas incluem precisão (precision), acurácia
(accuracy), matriz de confusão e F1 Score.

## 3-Conversão para o modulo de aceleração Hailo

Na etapa de conversão do modelo, foi realizada a conversão para o formato
ONNX por meio de um script em Python abaxio. A única modificação
aplicada durante esse processo foi a definição da pasta de armazenamento de cada
modelo, com os respectivos nomes determinados pelo parâmetro name.

 ~~~Python
from ultralytics import YOLO
model = YOLO("runs/detect/yolov8s_seed/weights/best.pt")
model.export(format="onnx", dynamic=False, simplify=False)
~~~

Após a conversão para ONNX, iniciou-se o processo de conversão para o
formato HEF, compatível com o módulo de aceleração HAILO.

O comando abaixo foi utilizado para realizar a conversão,
os arquivos convertidos são copiados para dentro do contêiner. Em seguida, o
contêiner é executado, e o comando correspondente é inserido para iniciar o
processo, especificando os parâmetros: o modelo de origem a ser convertido; ckpt,
que define o local do arquivo "best.onnx"; hw-arch, ao módulo de aceleração; calib-
path, que especifica o caminho de calibração contendo as imagens originais utilizadas
no treinamento do modelo; e classes, referente à quantidade de classes do modelo.


```bash
1. Copia a Pasta do Modelo para o Container Docker.
sudo docker cp yolov8s_coco hailo_ai_sw_suite_2025-04_container:/local/workspace/yolo/

2. Copia a Pasta com as Imagens para Calibração.
sudo docker cp train hailo_ai_sw_suite_2025-04_container:/local/workspace/yolo/

3. Executa o Container Docker.
sudo docker start hailo_ai_sw_suite_2025-04_container && sudo docker exec -it
hailo_ai_sw_suite_2025-04_container /bin/bash

4. Roda o Comando para Conversão do Modelo
hailomz compile yolov10s --ckpt=best.onnx --hw-arch hailo8l --calib-path train/images --
classes 18 --performance
```

Após a conversão, os modelos HEF finalizados foram copiados para o
desktop utilizando o comando abaixo, fora do contêiner Docker.
Em seguida, os modelos convertidos foram transferidos para o Raspberry Pi 5,
garantindo que estejam prontos para execução no dispositivo. As configurações
restantes serão aplicadas diretamente no Raspberry Pi 5, com ajustes nos parâmetros
conforme necessário para assegurar o funcionamento adequado do modelo.

```bash
1. Copia o Modelo Convertido.
Dockercphailo_ai_sw_suite_2025-04_container:/local/workspace/yolo/yolov8s_coco/weights/best.hef ~/Área\ de\Trabalho/yolov8s_coco/weights/
```











 ~~~Python
Esta é uma linha de código em Javascript.
~~~

```bash
sudo apt update
sudo apt install git
```
