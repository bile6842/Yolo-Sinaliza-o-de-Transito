# Analise dos modelos nos trajetos

Será realizada uma análise comparativa dos modelos ao longo de trajetos previamente gravado, com duração de 2.595 segundos, passando por diversas sinalizações entre elas
sinalizações que estavam no treinadas e sinalização que não estavam presentes no treinamento. O objetivo é estabelecer uma segunda parametrização para avaliar o desempenho dos modelos
em produção, determinando qual deles apresenta maior eficiência. Esse processo permitirá ajustes e melhorias, garantindo a otimização dos resultados obtidos na aplicação prática dos modelos.

Ao finalziar o teste dos modelos no modulo hailo a pasta ´run´ foi copiada para o pc onde foram realizado os treinamentos e renomeado para `Resultados`, as pastas com o nome teste foram renomeadas para seus respectivos modelos de teste.
Obtevese um total de 37.462 crops (frames que tiviream detecção de alguma classe).

## Tratamento dos dados

Para conseguirmos analisar os dados primeirao vamos precisar tratar eles, na seguinte ordem.

1. Triagem dos crops das previsões.
2. Preparação dos dados
3. Classificar ´TP´ de cada modelo.
4. Classificar ´FP´ de cada modelo.
5. Classificar ´FN´ de cada modelo.
6. Classificar ´TN´ de cada modelo.


### Triagem dos crops

Cada pasta de previsao foi aberta com os icones no modo visualização ´Icones Grandes´, agora foi visualizado os crops que estavao corretos e movido para uma nova ainda dentro da previsao com o mesmo nome da previsao
os crops errados foram criadas novas pastas com os nomes das classes certas e colocado cada crop em sua devida pasta ainda dentro da pasta de previsao, abaixo segue um exemplo da estrutura antiga e da nova estrutura de pastas.

#### Estrutura antiga

 ```
  run
  ├── teste
  ├── teste1
  ├── teste2
  │   ├── 20km-h
  │   │   └── video_trajeto2_frame_7592_label_20km-h_conf_0.76.jpg
  │   ├── 50km-h
  │   │   ├── video_trajeto7_frame_5007_label_50km-h_conf_0.75.jpg
  │   │   ├── video_trajeto7_frame_5011_label_50km-h_conf_0.72.jpg
  │   │   ├── video_trajeto7_frame_5013_label_50km-h_conf_0.79.jpg
  │   │   ├── video_trajeto7_frame_33623_label_50km-h_conf_0.80.jpg
  │   │   ├── video_trajeto7_frame_39892_label_50km-h_conf_0.71.jpg
  │   │   └── video_trajeto7_frame_19176_label_50km-h_conf_0.73.jpg 
  │   └── pare
  │       ├── video_trajeto7_frame_34261_label_Pare_conf_0.90.jpg
  │       ├── video_trajeto7_frame_34262_label_Pare_conf_0.88.jpg
  │       ├── video_trajeto7_frame_34263_label_Pare_conf_0.90.jpg
 
  ```

#### Estrutura nova

 ```
  Resultados
  ├── yolov8s_coco
  ├── yolov8s_seed
  ├── yolov10s_coco
  │   ├── 20km-h
  │   │   └── 20km-h
  │   │       └── video_trajeto2_frame_7592_label_20km-h_conf_0.76.jpg
  │   ├── 50km-h
  │   │   ├── 50km-h
  │   │   │   ├── video_trajeto7_frame_5007_label_50km-h_conf_0.75.jpg
  │   │   │   ├── video_trajeto7_frame_5011_label_50km-h_conf_0.72.jpg
  │   │   │   └── video_trajeto7_frame_5013_label_50km-h_conf_0.79.jpg
  │   │   ├── background
  │   │   │   └── video_trajeto7_frame_33623_label_50km-h_conf_0.80.jpg
  │   │   └── 60km-h
  │   │       ├── video_trajeto7_frame_39892_label_50km-h_conf_0.71.jpg
  │   │       └── video_trajeto7_frame_19176_label_50km-h_conf_0.73.jpg 
  │   └── pare
  │       ├── pare
  │       │   ├── video_trajeto7_frame_34262_label_Pare_conf_0.88.jpg
  │       │   └── video_trajeto7_frame_34263_label_Pare_conf_0.90.jpg
  │       └── background
  │           └── video_trajeto7_frame_34261_label_Pare_conf_0.90.jpg
  │       
 
  ```


### Preparação dos dados

Essa parte esta em [Preparando os dados no Excel](./excel.md)

### Valores (TP,FP,TN e FN)

- `TP` Sempre que um frame previsto for a mesma classe do True é cotabilizado no `TP`.
- `FP` Sempre que um frame previsto for de classe diferente do True é cotabilizado no `FP`.
- `TN` O total de frame do trajeto - `TP` - `FP` - `FN`
- `FN` Foi criado uma lista de frames detectados True e foram verificados quais frames os modelos não identificaram

Exemplo FN: 

modelo1 detectou uma placa (Valida) de para no trajeto 2 do frame 250 ate 252 e depois 254 ate 260

modelo2 detectou uma placa (Valida) de para no trajeto 2 do frame 252 ate 270

modelo3 detectou uma placa (Valida) de para no trajeto 2 do frame 255 ate 260 

Com a informação acima conseguimos saber que do trajeto 2 do frame 250 ate 270 continha uma placa

sendo assim atribui 11 frames (FN) para o modelo 1 pois a detecção começava no frame 250 e ia até o  270 

sendo assim atribui 2 frames (FN) para o modelo 2 pois a detecção começava no frame 250 e nao 270

sendo assim atribui 15 frames (FN) para o modelo 3 pois a detecção começava no frame 250 e nao 270

