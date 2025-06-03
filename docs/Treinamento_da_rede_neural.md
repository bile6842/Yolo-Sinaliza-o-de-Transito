# Treinamento da rede neural

O treinamento da rede YOLO é realizado a partir de um conjunto de dados composto por imagens previamente processadas. Durante esse processo, a rede ajusta os pesos por meio de operações matemáticas complexas,
visando minimizar o erro de classificação. 

O treinamento foi conduzido em duas etapas. Na primeira, não foi utilizado um modelo pré-treinado COCO para o treinamento. Já na segunda etapa, o modelo COCO foi incorporado ao processo, possibilitando
a comparação entre os resultados obtidos com e sem o aprendizado prévio.

O modelo COCO (Common Objects in Context) é um conjunto de dados utilizado para o treinamento de redes neurais em tarefas de detecção de objetos, segmentação e classificação. Ele contém mais de 330.000 
imagens, cada uma anotada com 80 categorias de objetos, permitindo que os modelos adquiram um conhecimento prévio sobre padrões visuais comuns. A incorporação do modelo COCO no treinamento auxilia na melhoria da
capacidade do sistema de reconhecer a sinalização viária, pois o aprendizado prévio proporciona uma base mais refinada para a detecção de objetos, reduzindo erros e aumentando a precisão na identificação das placas
de trânsito.

Os modelos COCO pretreinados foram baixados diretamenta da documentação da ULTRALYTICS, YOLO ([v8s](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt), [v10s](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov10s.pt)
e [11s](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt)).

Após a configuração do ambiente, o Quadro mostra o script Python com o comando necessário para iniciar os treinamentos. Nesse script, foram ajustados apenas o modelo utilizado (yolov8s, yolov10s e yolo11s), o parâmetro name,
que especifica o nome da pasta destinada ao armazenamento da rede e o parâmetro batch, a fim de otimizar de maneira mais eficiente o uso da memória da GPU.

~~~Python
from ultralytics import YOLO  

# Carregar o modelo YOLOv8 
model = YOLO('yolov8s.yaml') 
# Treinar o modelo 
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8, patience=10, amp=False, name=’yolov8s_seed’) 

# Carregar o modelo YOLOv10 
model = YOLO('yolov10s.yaml') 
# Treinar o modelo 
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8, patience=10, amp=False, name=’yolov10s_seed’)  

# Carregar o modelo YOLO11s 
model = YOLO('yolo11s.yaml')
# Treinar o modelo 
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8, patience=10, amp=False, name=’yolo11s_seed’)  

# Carregar o modelo YOLOv8 COCO 
model = YOLO('yolov8s.pt') 
# Treinar o modelo 
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8, patience=10, amp=False, name=’yolov8s_coco’) 

# Carregar o modelo YOLOv10 COCO 
model = YOLO('yolov10s.pt') 
# Treinar o modelo 
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8, patience=10, amp=False, name=’yolov10s_coco’)  

# Carregar o modelo YOLO11s COCO 
model = YOLO('yolo11s.pt') 
# Treinar o modelo 
model.train(data='data.yaml', epochs=1000, imgsz=640, device='cuda', batch=0.9, workers=8, patience=10, amp=False, name=’yolo11s_coco’)
~~~


Onde:
- `model`: Usando um ficheiro `.yaml` treina do zero e Usando um ficheiro `.pt` treinado no conjunto de dados COCO.
- `data`: Indica o ficheiro de configuração do conjunto de dados no daso o `data.yaml`.
- `epochs`: Número de vezes que o modelo verá todo o conjunto de dados durante o treino.
- `imgsz`: Redimensiona todas as imagens de entrada para 640x640 pixels para o treino.
- `device`: Especifica que o treino será executado numa GPU NVIDIA.
- `batch`: O treino utilizará o modo automático para o tamanho do lote, configurado para tentar utilizar `90%` da memória da GPU disponível para alocar o maior número de imagens possível por lote dentro desse limite.
- `workes`: Número de processos paralelos para carregar os dados, acelerando o pré-processamento.
- `patience`: Parada antecipada (Early Stopping). O treino será interrompido se não houver melhoria numa métrica de avaliação (como mAP) por 10 épocas consecutivas.
- `amp`: Desativa o Treino com Precisão Mista Automática (AMP)..
- `name`: Define o nome da pasta onde os resultados do treino (pesos, logs, etc.) serão guardados. O sufixo `_seed` indica treino a partir do zero, enquanto `_coco` indica treino a partir do modelo pré-treinado em COCO.

## Proximo Topico

- [Metricas](./metricas.md)
  
