# Conversão dos modelos

Na etapa de conversão do modelo, foi realizada a conversão para o formato ONNX por meio de um script em Python mostrado no Quadro.
A única modificação aplicada durante esse processo foi a definição da pasta de armazenamento de cada modelo, com os respectivos nomes determinados pelo parâmetro name.

~~~python
from ultralytics import YOLO 

model = YOLO("runs/detect/yolov8s_seed/weights/best.pt") 
model.export(format="onnx") 
~~~

Onde:

- `model` o local do arquivo `.pt` modelo treinado.
- `format` o formato que desejo converter no caso `onnx`.

Repeti esse comando para cada modelo mudando apenas o `model`.

Após a conversão para ONNX, iniciou-se o processo de conversão para o formato HEF, compatível com o módulo de aceleração HAILO. 

O Quadro apresenta os comandos utilizados. Para realizar a conversão, os arquivos convertidos são copiados para dentro do contêiner.

1. Copia a Pasta do Modelo para o Container Docker. 
```bash
sudo docker cp yolov8s_coco hailo_ai_sw_suite_2025-04_container:/local/workspace/yolo/ 
```

2. Copia a Pasta com as Imagens para Calibração.
```bash
sudo docker cp train hailo_ai_sw_suite_2025-04_container:/local/workspace/yolo/ 
```

3. Executa o Container Docker.
```bash
sudo docker start hailo_ai_sw_suite_2025-04_container && sudo docker exec -it hailo_ai_sw_suite_2025-04_container /bin/bash 
```

4. Roda o Comando para Conversão do Modelo
```bash
hailomz compile yolov10s --ckpt=best.onnx --hw-arch hailo8l --calib-path train/images --classes 18 --performance 
```

Onde:

hailomz compile `model` --ckpt=`modelo` --hw-arch `arch` --calib-path `train` --classes `classes` --performance

- `model` modelo de origem a ser convertido.
- `modelo` arquivo do modelo `.onnx` do treinamento convertido.
- `arch` arquitetura do modulo hailo.
- `train` local das imagens de treinamento.
- `classes` numero de classes.

Após a conversão, os modelos HEF finalizados foram copiados para o desktop utilizando o comando apresentado no Quadro, fora do contêiner Docker.
Em seguida, os modelos convertidos foram transferidos para o Raspberry Pi 5, garantindo que estejam prontos para execução no dispositivo.
As configurações restantes serão aplicadas diretamente no Raspberry Pi 5, com ajustes nos parâmetros conforme necessário para assegurar o funcionamento adequado do modelo.


1. Copia o Modelo Convertido. 
```bash
Dockercphailo_ai_sw_suite_2025-04_container:/local/workspace/yolo/yolov8s_coco/weights/best.hef ~/Área\ de\ Trabalho/yolov8s_coco/weights/
```

# Proximo Topico

- [Ambiente de Validação](./ambiente_de_validacao.md)

 
