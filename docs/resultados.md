# Resultados

Nesta seção, apresentam-se os resultados obtidos a partir da análise comparativa entre os modelos YOLOv8s, YOLOv10s e YOLO11s, com base nas métricas de precisão, acurácia, F1 Score, matriz de confusão e custo computacional.

## COMPARAÇÃO DOS MODELOS COM DADOS DO TREINAMENTO

Os resultados dos treinamentos, apresentados na Tabela , indicam que os modelos treinados com inicialização a partir de pesos pré-treinados na base COCO tendem a apresentar maior precisão em comparação aos modelos treinados do zero. Entre os três modelos com melhor desempenho em termos de precisão, destaca-se o YOLOv8s_seed, que atingiu 0,94872 ao final do treinamento, seguido pelo YOLOv8s_coco, com 0,90971, e pelo YOLO11s_coco, com 0,89042.


| Modelo         | Pré-treinado | Precisão | Acurácia | F1 Score | mAP50-95 |
|----------------|--------------|----------|----------|----------|----------|
| Yolov8s_coco   | Sim          | 0,90971  | 0,86     | 0,917454 | 0,82817  |
| Yolov8s_seed   | Não          | 0,94872  | 0,74866  | 0,904408 | 0,82093  |
| Yolov10s_coco  | Sim          | 0,86048  | 0,80217  | 0,84509  | 0,79744  |
| Yolov10s_seed  | Não          | 0,8039   | 0,676923 | 0,792218 | 0,74744  |
| Yolo11s_coco   | Sim          | 0,89042  | 0,782258 | 0,88169  | 0,80221  |
| Yolo11s_seed   | Não          | 0,76059  | 0,732095 | 0,812706 | 0,77862  |



Considerando a acurácia, o YOLOv8s_coco apresentou o melhor resultado, alcançando 0,86, enquanto o YOLOv10s_coco e o YOLO11s_coco obtiveram, respectivamente, 0,8039 e 0,782258. Esses dados indicam que o YOLOv8s_coco apresentou desempenho superior na correta identificação das placas, considerando o conjunto completo de dados.

Além disso, os modelos pré-treinados apresentaram valores mais elevados de F1 Score, o que evidencia um melhor equilíbrio entre precisão e sensibilidade. Os três melhores modelos foram: YOLOv8s_coco, com F1 Score de 0,917454; YOLOv8s_seed, com 0,904408; e YOLO11s_coco, com 0,88169.

A métrica mAP50-95, que avalia a qualidade geral das previsões em diferentes níveis de limiar de precisão, confirmou a superioridade dos modelos pré-treinados. Os melhores resultados foram obtidos por YOLOv8s_coco, YOLOv8s_seed e YOLO11s_coco, com valores entre 0,82817 e 0,80221, respectivamente. Esses resultados demonstram que o pré-treinamento com a base COCO contribuiu significativamente para a melhoria da performance e consistência das previsões.

## CUSTO COMPUTACIONAL TREIANMENTO

Os dados apresentados na Tabela evidenciam diferenças substanciais no consumo de recursos computacionais e no tempo de treinamento entre os modelos analisados. A alocação de memória da GPU variou de forma significativa.

O modelo YOLOv8s_seed, embora tenha utilizado a mesma quantidade de memória que o YOLOv8s_coco (4,9 GB), foi treinado por um maior número de épocas (95 contra 67), o que resultou em um tempo de treinamento mais prolongado (0,842 horas contra 0,682 horas).

| Modelo         | Memória GPU | Épocas | Lotes | Tempo Treinamento |
|----------------|-------------|--------|-------|-------------------|
| Yolov8s_coco   | 4,9GB       | 67     | 83    | 0,682 Horas       |
| Yolov8s_seed   | 4,9GB       | 95     | 83    | 0,842 Horas       |
| Yolov10s_coco  | 3,07GB      | 63     | 302   | 0,811 Horas       |
| Yolov10s_seed  | 4,68GB      | 66     | 101   | 0,768 Horas       |
| Yolo11s_coco   | 4,68GB      | 38     | 101   | 0,372 Horas       |
| Yolo11s_seed   | 3,07GB      | 78     | 302   | 0,944 Horas       |

Os modelos YOLOv10s_coco e YOLOv10s_seed apresentaram diferenças na utilização da memória de GPU, com o modelo YOLOv10s_seed consumindo mais memória (4,68 GB contra 3,07 GB). No entanto, seu tempo de treinamento foi ligeiramente inferior (0,768 horas contra 0,811 horas), possivelmente em função de variações no tamanho do lote e na eficiência do processo de otimização.

O modelo YOLO11s_coco apresentou o menor tempo de treinamento (0,372 horas), com uma quantidade reduzida de épocas (38) e um consumo moderado de memória (4,68 GB). Em contraste, o YOLO11s_seed, embora tenha demandado menor alocação de memória (3,07 GB), exigiu um tempo de treinamento significativamente superior (0,944 horas), devido ao maior número de épocas (78).
Esses resultados demonstram que a configuração do modelo — especialmente a alocação de memória, o número de épocas e o tamanho dos lotes — influencia diretamente a duração do treinamento e a eficiência computacional, aspectos críticos para a implementação prática de tais sistemas.


## DESEMPENHO DOS MODELOS NO MODULO HAILO NOS TRAJETOS

Os resultados obtidos na execução dos modelos no módulo de aceleração Hailo nos trajetos gravados, apresentados na Tabela , indicam que o modelo Yolov8s_coco se destacou com o maior F1 Score (0,8342) e a maior Acurácia (0,9602). O modelo Yolo11s_coco também apresentou um desempenho robusto, figurando com o segundo melhor F1 Score (0,7681) e a segunda melhor Acurácia (0,9495). Por sua vez, o modelo Yolov8s_seed exibiu a maior Precisão (0,8812) entre todos os modelos avaliados. Estes três modelos demonstraram particularidades notáveis em seu desempenho, considerando as métricas de precisão, acurácia e F1 Score.

| Modelo         | Pré-treinado | Precisão | Acurácia | F1 Score |
|----------------|--------------|----------|----------|----------|
| Yolov8s_coco   | Sim          | 0,8279   | 0,9593   | 0,8311   |
| Yolov8s_seed   | Não          | 0,8812   | 0,9288   | 0,5993   |
| Yolov10s_coco  | Sim          | 0,7773   | 0,9241   | 0,5802   |
| Yolov10s_seed  | Não          | 0,8088   | 0,9230   | 0,5649   |
| Yolo11s_coco   | Sim          | 0,8459   | 0,9486   | 0,7648   |
| Yolo11s_seed   | Não          | 0,9298   | 0,9323   | 0,6197   |



O modelo YOLOv8s_coco, que utilizou pesos pré-treinados da base COCO, demonstrou ser o mais equilibrado e de melhor desempenho geral para a tarefa de reconhecimento de sinalização viária neste estudo. Ele alcançou o maior F1 Score (0,8342) e a maior Acurácia (0,9602). Um F1 Score elevado como este sugere um excelente balanceamento entre precisão (capacidade de não gerar falsos positivos) e recall (capacidade de encontrar todas as placas relevantes), o que é vital para a confiabilidade de um sistema de assistência à condução. A precisão deste modelo foi de 0,8279.

Seguindo em desempenho geral, o YOLO11s_coco, também pré-treinado, apresentou resultados robustos, com o segundo maior F1 Score (0,7681) e a segunda maior Acurácia (0,9495), além de uma precisão de 0,8459. Estes resultados o posicionam como uma alternativa viável, mantendo um bom equilíbrio nas métricas essenciais, o que reforça a vantagem do pré-treinamento para esta aplicação específica.

Em contraste, o modelo YOLOv8s_seed, treinado a partir do zero (sem pesos pré-treinados), exibiu um perfil de desempenho distinto. Ele alcançou a maior Precisão (0,8812) entre todos os modelos testados na validação com o módulo Hailo. Uma precisão tão elevada é boa, pois indica uma taxa muito baixa de falsas detecções, ou seja, quando o modelo identifica uma placa, há uma alta probabilidade de estar correto. No entanto, apesar da alta precisão, sua Acurácia (0,9298) e F1 Score (0,6027) foram inferiores aos do seu equivalente pré-treinado (YOLOv8s_coco) nesta fase de testes. Isso sugere que, embora o YOLOv8s_seed erre pouco ao afirmar a presença de uma placa, ele pode ter deixado de detectar um número maior de placas existentes (baixo recall, impactando negativamente o F1 Score). Este comportamento pode ser crítico em cenários de condução autônoma, onde omitir uma sinalização importante pode ser tão problemático quanto uma identificação incorreta. Contudo, o alto desempenho em precisão, mesmo sem pré-treinamento, demonstra o potencial da arquitetura YOLOv8s em aprender características distintivas do zero. Esta característica pode ser uma opção em cenários específicos onde evitar alarmes falsos é a prioridade máxima e onde a perda de algumas detecções pode ser mais tolerável.

O modelo YOLOv8s_coco superou o YOLOv8s_seed em Acurácia (0,9602 contra 0,9298) e F1 Score (0,8342 contra 0,6027), apesar da menor Precisão (0,8279 contra 0,8812). Isso indica que o pré-treinamento foi crucial para um reconhecimento mais abrangente e balanceado das placas.

O modelo YOLOv10s_coco apresentou Precisão de 0,7773, Acurácia de 0,9251 e F1 Score de 0,5834, enquanto o YOLOv10s_seed obteve 0,8088, 0,9239 e 0,5680 respectivamente. Neste caso, o modelo treinado sem pesos pré-treinados (seed) teve uma precisão ligeiramente superior, enquanto o pré-treinado (coco) obteve uma pequena vantagem em acurácia e F1 Score. Contudo, ambos os modelos YOLOv10s registraram Acurácia e F1 Score inferiores aos modelos YOLOv8s_coco e YOLO11s_coco nesta etapa de validação.

O modelo YOLO11s_coco, com Precisão de 0,8459, Acurácia de 0,9495 e F1 Score de 0,7681, superou o YOLO11s_seed que obteve 0,8177, 0,9280 e 0,6196, respectivamente, de forma significativa em Acurácia e F1 Score, e também apresentou maior precisão.

Esta análise comparativa evidencia que, para os modelos YOLOv8s e YOLO11s, o pré-treinamento no dataset COCO resultou em um desempenho mais equilibrado e consideravelmente superior em Acurácia e F1 Score para a tarefa de detecção de sinalização viária quando executados no módulo Hailo. O modelo YOLOv10s, em ambas as suas configurações (com e sem pré-treinamento), não alcançou o mesmo patamar de desempenho dos outros dois modelos pré-treinados (YOLOv8s_coco e YOLO11s_coco) neste contexto específico de validação em trajetos.

Fundamentalmente para a aplicação em veículos autônomos, todos os modelos analisados operaram a uma taxa de 30 FPS no módulo de aceleração Hailo. Esta taxa de processamento é considerada adequada para aplicações em tempo real, assegurando que o sistema de reconhecimento de sinalização possa fornecer informações ágeis para a tomada de decisão do veículo. Tal capacidade contribui diretamente para a segurança e eficiência da mobilidade elétrica autônoma.

# Proximo Topico

- [Conclusão](./conclusao.md)
