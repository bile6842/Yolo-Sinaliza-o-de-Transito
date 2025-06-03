# Metricas

## Previsões

Os conceitos de Verdadeiro Positivo (TP), Falso Positivo (FP), Verdadeiro Negativo (TN) e Falso Negativo (FN) são fundamentais para a avaliação do desempenho do modelo.

- `TP` Ocorre quando a rede neural identifica corretamente uma placa de trânsito presente na imagem.
- `FP` Ocorre quando o modelo detecta erroneamente um objeto como sendo uma placa, quando na realidade não há uma sinalização correspondente.
- `TN` Representa os casos em que o algoritmo corretamente não identifica uma placa onde realmente não há sinalização.
- `FN` Acontece quando uma placa existente na imagem não é reconhecida pelo sistema.

### Precisão

A precisão mede a proporção de previsões corretas para a classe positiva em relação ao total de previsões realizadas. 
Quanto maior a precisão,menor a ocorrência de falsos positivos, um valor elevado de precisão indica que o modelo realiza previsões com maior certeza, minimizando classificações errôneas.
A equação apresenta a definição de precisão do desempenho do modelo.

`Precisão = TP / (TP + FP)`                                                                                        

### Acurácia

A acurácia representa a proporção total de previsões corretas em relação ao conjunto de dados completo, fornecendo um panorama geral da eficiência do modelo,
um modelo com alta acurácia apresenta um desempenho consistente na classificação correta das placas de trânsito.
A equação apresenta a definição de acurácia do desempenho do modelo.

`Acurácia = (TP + TN) / (TP + TN + FP + FN)`

### Recall

O recall é uma métrica para avaliar a capacidade do modelo de reconhecer corretamente a sinalização viária.
Um alto recall indica que poucas placas de trânsito foram ignoradas, o que contribui para a eficácia do sistema na identificação de sinais essenciais.
No entanto, um recall elevado deve ser analisado em conjunto com a precisão, pois um número excessivo de FP pode comprometer a confiabilidade do modelo.
A equação apresenta a definição de recall do desempenho do modelo.

`Recall = TP / (TP + FN)`

### F1 Score

O F1 Score equilibra a relação entre precisão e recall, sendo especialmente útil quando há um desequilíbrio nas classes do conjunto de dados,
essa métrica garante que o modelo seja eficiente tanto na detecção correta das placas quanto na redução de falsos negativos.
A equação apresenta a definição de f1 score do desempenho do modelo.

`F1 Score = 2 * (Precisão * Recall) / (Precisão + Recall)`

### Matriz de Confusão

A matriz de confusão exibe a distribuição das previsões entre as classes reais e permite visualizar quais categorias estão sendo confundidas.
O ideal é que os valores da diagonal principal sejam elevados, indicando alta taxa de acertos. A análise dessa matriz possibilita identificar padrões de erro
e ajustar parâmetros para aprimorar a performance da rede.

# Proximo Topico

- [Comparatico entre os modelos](./COMPARATIVO_ENTRE_OS_MODELOS.md)


