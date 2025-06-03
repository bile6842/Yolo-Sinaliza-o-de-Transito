# Comparação entre os modelos

Para determinar qual modelo apresenta o melhor desempenho, diversos critérios devem ser considerados, incluindo precisão, métricas estatísticas e eficiência computacional. A avaliação da precisão e do F1 Score é essencial, pois modelos com valores mais elevados nessas métricas tendem a reduzir a ocorrência de falsos positivos sem comprometer o recall, garantindo um equilíbrio adequado entre identificação correta e cobertura do conjunto de dados.

Além disso, a análise da matriz de confusão permite verificar como os erros estão distribuídos entre as classes. Modelos que apresentam menos erros de classificação e maior concentração de acertos indicam um desempenho mais eficiente, proporcionando melhor generalização e confiabilidade nas predições.
A acurácia geral também deve ser considerada, pois modelos com maior acurácia demonstram um desempenho mais consistente ao longo das diferentes fases do treinamento e validação. No entanto, a acurácia isolada pode não refletir completamente a qualidade do modelo, sendo necessário cruzá-la com outras métricas como precisão e recall para uma avaliação mais precisa.

Outro fator crítico na escolha do modelo é o uso da GPU e o tempo de inferência. Modelos mais complexos podem demandar maior capacidade computacional, aumentando o custo de processamento e consumo energético. Dessa forma, a relação entre desempenho e custo computacional deve ser balanceada para garantir uma solução viável e eficiente para a aplicação desejada.

Por fim, a realização de testes comparativos e a coleta sistemática das métricas mencionadas fornecerão uma base objetiva para determinar qual versão do YOLO apresenta o melhor desempenho. Essa abordagem permitirá identificar qual modelo oferece a melhor relação entre precisão, eficiência de classificação e uso de recursos computacionais, facilitando a tomada de decisão baseada em dados concretos.

# Proximo Topico

- [Conversão dos modelos](./conversao_dos_modelos.md)
