# MOBILIDADE AUTONOMA
## Procedimento Experiental 
Nesta sera descrito o procedimento utilizado para configuração, treinamento, execução e analise dos modelos YOLO v8s, v10s e 11s, assim disponibilizado os arquivos utilizados.

### Etapa 1 - PC

1-Preparação do Database [Procedimentos Realizados](./docs/preparacao_database.md)

2-Preparação do ambiente de treinamento

3-Trenamento

### Etapa 2 - Raspberry pi 5

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




## Formação do Nome do Arquivo

O nome dos nossos arquivos segue um padrão claro para facilitar a organização e identificação. Veja a estrutura:

`ANO-MES-DIA_DESCRICAO-CURTA_VERSAO.EXTENSAO`

Vamos analisar cada componente:

* **`ANO`**: Representa o ano com 4 dígitos.
    * *Exemplo:* `2025`
* **`MES`**: Representa o mês com 2 dígitos.
    * *Exemplo:* `06`
* **`DIA`**: Representa o dia com 2 dígitos.
    * *Exemplo:* `02`
* **`_` (Sublinhado)**: Usado como separador principal entre blocos de informação (data, descrição, versão).
* **`DESCRICAO-CURTA`**: Uma breve descrição do conteúdo do arquivo, usando hífens para separar palavras dentro da descrição.
    * *Exemplo:* `relatorio-vendas`, `apresentacao-projeto`
* **`VERSAO`**: Indica a versão do arquivo, geralmente prefixada com `v`.
    * *Exemplo:* `v1`, `v2-final`, `v1.3`
* **`.` (Ponto)**: Separa o nome base da extensão do arquivo.
* **`EXTENSAO`**: Indica o tipo do arquivo.
    * *Exemplo:* `pdf`, `docx`, `xlsx`, `png`

**Nome de Arquivo Completo (Exemplo):**

`2025-06-02_relatorio-vendas_v3.pdf`

Onde:
* Data: `2025-06-02`
* Descrição: `relatorio-vendas`
* Versão: `v3`
* Extensão: `pdf`







## Estrutura do Nome do Arquivo: `[DATA]_[TIPO]_[DETALHE]_[VERSAO].[EXT]`

| Componente        | Formato/Exemplo              | Descrição                                       |
|-------------------|------------------------------|-------------------------------------------------|
| `[DATA]`          | `AAAA-MM-DD` (ex: `2025-06-02`) | Ano, Mês e Dia da criação ou relevância.        |
| `_`               | (Sublinhado)                 | Separador entre componentes principais.          |
| `[TIPO]`          | `RELATORIO`, `GRAFICO`, `CODIGO` | Categoria geral do arquivo.                     |
| `_`               | (Sublinhado)                 | Separador.                                      |
| `[DETALHE]`       | `VENDAS-MENSAIS`, `FLUXO-USUARIO` | Especificação do conteúdo. Use hífens.         |
| `_`               | (Sublinhado)                 | Separador (opcional antes da versão).           |
| `[VERSAO]`        | `v1`, `v2.1`, `final`        | Indicador de versão ou status do arquivo.       |
| `.`               | (Ponto)                      | Separador da extensão.                          |
| `[EXT]`           | `pdf`, `png`, `py`, `txt`    | Extensão que define o tipo de arquivo.          |

**Exemplo Prático:**

`2025-06-02_RELATORIO_VENDAS-MENSAIS_v1.pdf`


  ````markdown
  ## Estrutura do Projeto

  ```
  .
  ├── README.md
  ├── LICENSE
  ├── docs
  │   ├── CONTRIBUTING.md
  │   ├── INSTALL.md
  │   └── images
  │       └── logo.png
  ├── src
  │   ├── main.py
  │   └── utils
  │       └── helpers.py
  └── tests
      └── test_main.py
  ```
  ````




## Estrutura do Projeto

- README.md (Este arquivo)
- LICENSE
- docs/
  - CONTRIBUTING.md
  - INSTALL.md
  - images/
    - logo.png
- src/
  - main.py
  - utils/
    - helpers.py
- tests/
  - test_main.py
 



## Estrutura do Projeto

-   `README.md` (Este arquivo)
-   `LICENSE`
-   `docs/`
    -   `CONTRIBUTING.md`
    -   `INSTALL.md`
    -   `images/`
        -   `logo.png`
-   `src/`
    -   `main.py`
    -   `utils/`
        -   `helpers.py`
-   `tests/`
    -   `test_main.py`



A famosa equação de Einstein é $E = mc^2$.



## Padrão de Nomenclatura de Arquivos de Relatório

Os nomes dos arquivos de relatório seguem o formato:

`<AAAA-MM-DD>_<ID_PROJETO>_<TIPO_RELATORIO>_v<VERSAO>.<EXT>`

---

**Componentes Variáveis:**

| Variável                 | Formato Esperado           | Descrição                                                                 | Exemplo de Valor |
|--------------------------|----------------------------|---------------------------------------------------------------------------|------------------|
| `<AAAA-MM-DD>`           | Ano com 4 dígitos, Mês com 2 dígitos, Dia com 2 dígitos, separados por hífen. | Data de criação ou referência principal do relatório.                    | `2025-06-02`     |
| `<ID_PROJETO>`           | Alfanumérico (ex: `PROJ103`) | Identificador único do projeto ao qual o relatório se refere.            | `XYZ789`         |
| `<TIPO_RELATORIO>`       | Texto descritivo (ex: `Progresso`, `Financeiro`, `Final`) | Indica a natureza ou o tipo do relatório. Use CamelCase ou hífens. | `AnaliseRisco`   |
| `<VERSAO>`               | Numérico (ex: `1`, `2`, `3.1`) | Número da versão do relatório, para controle de alterações.              | `2`              |
| `<EXT>`                  | Extensão do arquivo        | Indica o formato do arquivo.                                              | `pdf`, `docx`    |

---

**Exemplos de Nomes de Arquivos Válidos:**

* `2025-06-02_PROJ103_Progresso_v1.pdf`
* `2025-05-15_ABC500_Financeiro_v3.xlsx`
* `2025-07-01_XYZ789_AnaliseRisco_v1.2.docx`

**Dicas para Clareza:**

* **Seja Consistente:** Use sempre a mesma convenção para suas variáveis.
* **Documente:** Mantenha esta explicação no seu `README.md` ou em um guia de contribuição (`CONTRIBUTING.md`).
* **Use Separadores Claros:** Sublinhados (`_`) ou hífens (`-`) entre os componentes variáveis ajudam na legibilidade. Escolha um e mantenha-o.
* **Evite Espaços:** Nomes de arquivos com espaços podem causar problemas em scripts ou na linha de comando.






 ~~~Python
Esta é uma linha de código em Javascript.
~~~

```bash
sudo apt update
sudo apt install git
```
