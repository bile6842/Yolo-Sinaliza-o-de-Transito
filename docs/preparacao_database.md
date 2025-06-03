# Banco de imagens
  
O banco de imagens de placas será obtido a partir da base disponível na página web ROBOTFLOW, que já contém uma variedade de placas de sinalização viária. Esse banco será ajustado e revisado para incluir exclusivamente as sinalizações pertinentes ao estudo em questão.

O banco de imagens original, denominado [Brazilian Traffic Signs](https://app.roboflow.com/otavio-bwqzl/brazilian-traffic-signs-hnifq-xmcu2/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true) , abrange um total de 59 classes e 3013 imagens. A partir dele, foi realizada uma cópia na qual foram removidas as classes não utilizadas, reduzindo-se o conjunto para 18 classes. Além disso, foi conduzida uma análise das imagens, na qual aquelas de baixa resolução foram excluídas e marcações incorretas foram corrigidas, resultando em um total de 1111 imagens. Essas imagens foram organizadas de modo que 80% sejam destinadas ao treinamento e 20% à validação.

Para complementar o processo, será criado um arquivo denominado data.yaml, no qual serão indicados os caminhos necessários para a estruturação do banco de imagens.

```yaml
path: C:/Users/Otavi/Desktop/TCC Parte 2/TCC Certo Revisado/data
train: C:/Users/Otavi/Desktop/TCC Parte 2/TCC Certo Revisado/data/train/images
val: C:/Users/Otavi/Desktop/TCC Parte 2/TCC Certo Revisado/data/validation/images

nc: 18
names: ['100km-h', '10km-h', '110km-h', '120km-h', '20km-h', '30km-h', '40km-h', '50km-h', '60km-h', '70km-h', '80km-h', '90km-h', 'Estacionamento', 'Lombada', 'Pare', 'Proibido Estacionar', 'Proibido Parar e Estacionar', 'Rotatoria'
```

Onde:
- `path`: correspondente ao diretório do banco de imagens.
- `train`: referente ao local da pasta de treino.
- `val`: indicando o diretório destinado à validação.
- `nc`: representando o número de classes.
- `names`: que conterá os nomes das classes envolvidas.

## Proximo Topico

- [Configuração do ambiente para treinamento YOLO](./docs/configuracao_do_ambiente_para_treinamento_yolo.md)
