# RECONHECIMENTO DE SINALIZAÇÃO VIÁRIA UTILIZANDO ALGORITMO DE DETECÇÃO YOLO E VISÃO COMPUTACIONAL NO AUXÍLIO DA MOBILIDADE ELÉTRICA EM VEÍCULOS AUTÔNOMOS

## Resumo

A mobilidade autônoma exige sistemas avançados de percepção ambiental, como o reconhecimento de sinalização viária, para garantir operações seguras e eficientes. Este trabalho teve como objetivo desenvolver e avaliar um sistema de reconhecimento de sinalização viária em tempo real utilizando a arquitetura YOLO, visando aprimorar a percepção e a segurança de veículos autônomos. Para isso, seis modelos YOLO (v8s, v10s, 11s), com e sem pré-treinamento no conjunto de dados COCO, foram treinados e seus desempenhos comparados após validação em uma plataforma Raspberry Pi 5 com módulo de aceleração Hailo. Os resultados da validação demonstraram que o modelo YOLOv8s_coco pré-treinado alcançou o melhor desempenho geral, com um F1 Score de 0,8342 e Acurácia de 0,9602, enquanto o YOLOv8s_seed (treinado do zero) exibiu a maior Precisão (0,8812). A análise confirmou o impacto positivo do aprendizado prévio na confiabilidade da detecção, e, crucialmente, todos os modelos operaram a 30 FPS no módulo Hailo, atestando a viabilidade da solução para aplicações embarcadas em tempo real. Conclui-se que a abordagem YOLO implementada no módulo Hailo é promissora e viável para o desenvolvimento de sistemas de mobilidade autônoma mais eficientes e seguros, com futuras pesquisas podendo direcionar-se a exploração de versões mais avançadas do YOLO e a fusão de sensores complementares, como LiDAR e RADAR, a fim de ampliar a percepção do ambiente e otimizar a tomada de decisão em veículos inteligentes. 


## Procedimento Experiental 

Neste guia sera descrito o procedimento utilizado para a configuração, treinamento, execução e analise dos modelos YOLO v8s, v10s e 11s, assim como disponibilizado os arquivos utilizados.

Esta seção descreve detalhadamente os procedimentos experimentais adotados para o desenvolvimento, implementação e validação do sistema proposto, incluindo os materiais utilizados, a configuração do ambiente de testes e a metodologia aplicada para coleta e análise dos dados. 
  
Para o desenvolvimento do projeto e experimentos, utilizou-se dos laboratórios de Engenharia Mecatrônica do centro universitário UniSATC, campus Criciúma. Todos os materiais, incluindo o Raspberry PI 5 8 GB, Cartão de memória 64 GB, Raspberry Pi M.2 HAT+, Módulo de aceleração Hailo AI e a câmera modelo V2 com 8 Mpx, serão fornecidos pela instituição conforme apresentado na Figura. 


![Equipmaento Montado](https://raw.githubusercontent.com/bile6842/Yolo-Sinaliza-o-de-Transito/refs/heads/main/img/Equipamento_Montado.png)

As classes a serem treinadas são: a) 10 km/h, b) 20 km/h, c) 30 km/h, d) 40 km/h, e) 50 km/h, f) 60 km/h, g) 70 km/h, h) 80 km/h, i) 90 km/h, j) 100 km/h, k) 110 km/h, l) 120 km/h, m) Estacionamento, n) Lombada, o) p) Pare, q) Proibido Estacionar, r) Proibido Estacionar e Parar e s) Rotatória.

![Classes_Treinadas](https://raw.githubusercontent.com/bile6842/Yolo-Sinaliza-o-de-Transito/refs/heads/main/img/classes_treinadas.png)

Serão utilizadas bibliotecas na linguagem de programação Python, o treinamento da rede neural para o reconhecimento das placas de trânsito e a etapa posterior de reconhecimento das placas de sinalização viária. 

O desenvolvimento do projeto será realizado em duas etapas distintas e complementares. A primeira etapa corresponde ao ambiente de treinamento e análise, no qual serão desenvolvidos os algoritmos, configurados os sensores e simuladas as condições operacionais do sistema. Nessa fase, serão realizados testes preliminares com foco na calibração dos parâmetros e na análise de desempenho em ambiente controlado. A segunda etapa refere-se ao ambiente de validação, em que o sistema será submetido a testes práticos em condições mais próximas das reais, visando verificar sua robustez, confiabilidade e aderência aos requisitos definidos. Essa abordagem em etapas permite uma avaliação progressiva e criteriosa da solução proposta, assegurando maior consistência nos resultados obtidos. Os procedimentos detalhados são apresentados nas seções subsequentes. 

## Ambiente de Treinamento

A Figura, descreve o fluxo do ambiente de treinamento dos modelos YOLO, que antecede os testes no módulo Hailo. Esta etapa inicia-se com a preparação do banco de imagens de placas de trânsito. Segue-se a Configuração do Ambiente de treinamento em um notebook com GPU e sistema Ubuntu, incluindo a instalação dos frameworks ULTRALYTICS e HAILO DATAFLOW COMPILER. Com o ambiente pronto, ocorre o Treinamento do Modelo, onde diferentes versões do YOLO (v8s, v10s, 11s, com e sem pré-treinamento COCO) são treinadas com o dataset preparado. Após o treinamento, realiza-se a Avaliação do Modelo utilizando métricas como precisão, acurácia e F1 Score para verificar seu desempenho. Finalmente, a etapa crucial de Conversão do Modelo para o HAILO é executada, onde os modelos são primeiramente convertidos para o formato ONNX e depois para o formato HEF, compatível com o módulo de aceleração Hailo, utilizando o HAILO DATAFLOW COMPILER e preparando-os para os testes subsequentes no Raspberry Pi 5.

![Diagrama_etapa_1](https://github.com/bile6842/Yolo-Sinaliza-o-de-Transito/blob/main/img/diagrama_etapa_1.png)

## Proximos Topicos

- [Banco de imagens ](./docs/preparacao_database.md)
- [Configuração do ambiente para treinamento YOLO](./docs/configuracao_do_ambiente_para_treinamento_yolo.md)




### 1-Configuração do Database

### 1-Comandos Instalação Framework ULTRALYTICS

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
  
### 2-Comandos Instalação Framework ULTRALYTICS

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

### 3-Conversão para o modulo de aceleração Hailo

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





[Texto do link](./caminho/para/seu/outro_arquivo.md)





 ~~~Python
Esta é uma linha de código em Javascript.
~~~

```bash
sudo apt update
sudo apt install git
```
