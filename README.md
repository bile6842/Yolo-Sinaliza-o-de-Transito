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


