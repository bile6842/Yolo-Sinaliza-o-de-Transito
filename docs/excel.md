# Procedimento do Excel

Para conseguirmos utilizar os dados temos que preparar eles para o uso, nessa parte foi utilizado Microsoft Excel e sua ferramento Power Query, para isso abrimos o Microsoft Excel fomos na Guia `Dados`
`Obter Dados` => `De Arquivo` => `Da Pasta`, selecionado a pasta `Resultados` e depois `Abrir`.

![Abrindo no Ecel](https://raw.githubusercontent.com/bile6842/Yolo-Sinaliza-o-de-Transito/refs/heads/main/img/Abrindo%20Excel.png)

Depois `Transformar Dados`, no editor do Power Query na lateral esquerda tem as consultas clique com o botçao direto em cima da consulta `Resultados` e va em `Editor Avançado`.

![Adicionando Consulta](https://github.com/bile6842/Yolo-Sinaliza-o-de-Transito/blob/main/img/power%20qury.png?raw=true)


Agora cole o codigo abaixo da consulta `Dados Tratados 2` e depois `Concluido`, agora em `Fechar e Carregar`.

```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove Copia", {{"Confianca", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
```

Essa Tratamento que foi realizado extrai do endereço onde o arquivo esta salva as sequintes e informações e adiciona como colunas, `Modelo`, `Previsao` e `True` (Esta coluna tem as pastas que foram criadas na triagem),

O codigo tambem adiciona outras colunas, uma colunas para identificar previsões validas e outra para previões invalidas.

- `Previsões Validas` se `Previsão` = `True` then 1 else 0.
- `Previsões invalidas` se `Previsão` <> `True` then 1 else 0.

segue em baixo uma explicação de onde vem cada informação.

#### Estrutura Explicada

 ```
  Resultados
  ├── yolov8s_coco (Modelo)
  ├── yolov8s_seed (Modelo)
  ├── yolov10s_coco (Modelo)
  │   ├── 20km-h (Previsao)
  │   │   └── 20km-h (True)
  │   │       └── video_trajeto2_frame_7592_label_20km-h_conf_0.76.jpg
  │   ├── 50km-h (Previsao)
  │   │   ├── 50km-h (True)
  │   │   │   ├── video_trajeto7_frame_5007_label_50km-h_conf_0.75.jpg
  │   │   │   ├── video_trajeto7_frame_5011_label_50km-h_conf_0.72.jpg
  │   │   │   └── video_trajeto7_frame_5013_label_50km-h_conf_0.79.jpg
  │   │   ├── background (True)
  │   │   │   └── video_trajeto7_frame_33623_label_50km-h_conf_0.80.jpg
  │   │   └── 60km-h (True)
  │   │       ├── video_trajeto7_frame_39892_label_50km-h_conf_0.71.jpg
  │   │       └── video_trajeto7_frame_19176_label_50km-h_conf_0.73.jpg 
  │   └── pare (Previsao)
  │       ├── pare (True)
  │       │   ├── video_trajeto7_frame_34262_label_Pare_conf_0.88.jpg
  │       │   └── video_trajeto7_frame_34263_label_Pare_conf_0.90.jpg
  │       └── background (True)
  │           └── video_trajeto7_frame_34261_label_Pare_conf_0.90.jpg
  │       
 
  ```
A Planilha Dados Tratados 2.

![Estrutura da Planilha Dados 2](https://github.com/bile6842/Yolo-Sinaliza-o-de-Transito/blob/main/img/dados%20tratados%202.png?raw=true)

Feito isso agora na planilha 1 crie uma coluna com o nome dos modelos, e uma coluna com `TP` e outra `FP`, agora utilizei o codigo abaixo na coluna `TP` para contar os Verdadeiro Positivo e na Coluna `FP` e cadigo Abaixo para 
Contar os Falso Positivo.

#### Coluna (TP)

```Text
=SOMASES('Dados Tratados 2'!H:H;'Dados Tratados 2'!A:A;Planilha1!C2)
```

#### Coluna (FP)

```Text
=SOMASES('Dados Tratados 2'!I:I;'Dados Tratados 2'!A:A;Planilha1!C2)
```

A planilha 1 vai ficar igual na figura.

![Figura Planilha1](https://github.com/bile6842/Yolo-Sinaliza-o-de-Transito/blob/main/img/planilha%201.png)

### Achar os FN

Para identificar os Falsos negativo foi criado uma lista com todos os frames detectados como validos, depois foi efetuada a comparação modelo a modelo para identificar quais frames os modelos não conseguiram identificar.

Para isso vou disponibilar o codigo do Editor avançado de cada consulta que foi criada no Power Query para idenficar os FN.

#### yolov8s_coco_Background


```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove o Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove o Copia", {{"Confianca", type number}}, "en-US"),
    #"Filtro Modelo" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Modelo] <> "yolov8s_coco"),
    #"Filtro Confianca" = Table.SelectRows(#"Filtro Modelo", each [Confianca] >= v_confianca),
    #"Outras Colunas Removidas2" = Table.SelectColumns(#"Filtro Confianca",{"Trajeto", "Frame", "True"}),
    #"Linhas Filtradas1" = Table.SelectRows(#"Outras Colunas Removidas2", each ([True] <> "Background")),
    #"Linhas Agrupadas" = Table.Group(#"Linhas Filtradas1", {"Trajeto", "Frame", "True"}, {{"Contagem", each Table.RowCount(_), Int64.Type}})
in
    #"Linhas Agrupadas"
```

#### yolov8s_seed_Background


```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove o Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove o Copia", {{"Confianca", type number}}, "en-US"),
    #"Filtro Modelo" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Modelo] <> "yolov8s_seed"),
    #"Filtro Confianca" = Table.SelectRows(#"Filtro Modelo", each [Confianca] >= v_confianca),
    #"Outras Colunas Removidas2" = Table.SelectColumns(#"Filtro Confianca",{"Trajeto", "Frame", "True"}),
    #"Linhas Filtradas1" = Table.SelectRows(#"Outras Colunas Removidas2", each ([True] <> "Background")),
    #"Linhas Agrupadas" = Table.Group(#"Linhas Filtradas1", {"Trajeto", "Frame", "True"}, {{"Contagem", each Table.RowCount(_), Int64.Type}})
in
    #"Linhas Agrupadas"
```

#### yolov10s_coco_Background


```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove o Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove o Copia", {{"Confianca", type number}}, "en-US"),
    #"Filtro Modelo" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Modelo] <> "yolov10s_coco"),
    #"Filtro Confianca" = Table.SelectRows(#"Filtro Modelo", each [Confianca] >= v_confianca),
    #"Outras Colunas Removidas2" = Table.SelectColumns(#"Filtro Confianca",{"Trajeto", "Frame", "True"}),
    #"Linhas Filtradas1" = Table.SelectRows(#"Outras Colunas Removidas2", each ([True] <> "Background")),
    #"Linhas Agrupadas" = Table.Group(#"Linhas Filtradas1", {"Trajeto", "Frame", "True"}, {{"Contagem", each Table.RowCount(_), Int64.Type}})
in
    #"Linhas Agrupadas"
```

#### yolov10s_seed_Background


```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove o Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove o Copia", {{"Confianca", type number}}, "en-US"),
    #"Filtro Modelo" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Modelo] <> "yolov10s_seed"),
    #"Filtro Confianca" = Table.SelectRows(#"Filtro Modelo", each [Confianca] >= v_confianca),
    #"Outras Colunas Removidas2" = Table.SelectColumns(#"Filtro Confianca",{"Trajeto", "Frame", "True"}),
    #"Linhas Filtradas1" = Table.SelectRows(#"Outras Colunas Removidas2", each ([True] <> "Background")),
    #"Linhas Agrupadas" = Table.Group(#"Linhas Filtradas1", {"Trajeto", "Frame", "True"}, {{"Contagem", each Table.RowCount(_), Int64.Type}})
in
    #"Linhas Agrupadas"
```

#### yolo11s_coco_Background


```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove o Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove o Copia", {{"Confianca", type number}}, "en-US"),
    #"Filtro Modelo" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Modelo] <> "yolo11s_coco"),
    #"Filtro Confianca" = Table.SelectRows(#"Filtro Modelo", each [Confianca] >= v_confianca),
    #"Outras Colunas Removidas2" = Table.SelectColumns(#"Filtro Confianca",{"Trajeto", "Frame", "True"}),
    #"Linhas Filtradas1" = Table.SelectRows(#"Outras Colunas Removidas2", each ([True] <> "Background")),
    #"Linhas Agrupadas" = Table.Group(#"Linhas Filtradas1", {"Trajeto", "Frame", "True"}, {{"Contagem", each Table.RowCount(_), Int64.Type}})
in
    #"Linhas Agrupadas"
```

#### yolo11s_seed_Background


```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Coluna S_Invalido",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Remove o Copia" = Table.ReplaceValue(#"Colunas Reordenadas"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Remove o Copia", {{"Confianca", type number}}, "en-US"),
    #"Filtro Modelo" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Modelo] <> "yolo11s_seed"),
    #"Filtro Confianca" = Table.SelectRows(#"Filtro Modelo", each [Confianca] >= v_confianca),
    #"Outras Colunas Removidas2" = Table.SelectColumns(#"Filtro Confianca",{"Trajeto", "Frame", "True"}),
    #"Linhas Filtradas1" = Table.SelectRows(#"Outras Colunas Removidas2", each ([True] <> "Background")),
    #"Linhas Agrupadas" = Table.Group(#"Linhas Filtradas1", {"Trajeto", "Frame", "True"}, {{"Contagem", each Table.RowCount(_), Int64.Type}})
in
    #"Linhas Agrupadas"
```

#### agrupado

```powerquery
let
    Fonte = Folder.Files("C:\Users\Otavi\Desktop\trajetos\Resultados"),
    #"Outras Colunas Removidas" = Table.SelectColumns(Fonte,{"Name", "Folder Path"}),
    #"Coluna Trajeto" = Table.AddColumn(#"Outras Colunas Removidas", "Trajeto", each Text.BetweenDelimiters([Name], "o", "_", 1, 0), type text),
    #"Coluna Frame" = Table.AddColumn(#"Coluna Trajeto", "Frame", each Text.BetweenDelimiters([Name], "_", "_", 2, 0), type text),
    #"Coluna Predicted" = Table.AddColumn(#"Coluna Frame", "Predicted", each Text.BetweenDelimiters([Name], "_", "_", 4, 0), type text),
    #"Coluna Confianca" = Table.AddColumn(#"Coluna Predicted", "Confianca", each Text.BetweenDelimiters([Name], "_", ".", 6, 1), type text),
    #"Coluna Modelo" = Table.AddColumn(#"Coluna Confianca", "Modelo", each Text.BetweenDelimiters([Folder Path], "\", "\", 5, 0), type text),
    #"Coluna True" = Table.AddColumn(#"Coluna Modelo", "True", each Text.BetweenDelimiters([Folder Path], "\", "\", 7, 0), type text),
    #"Coluna Valida" = Table.AddColumn(#"Coluna True", "Valido", each if [Predicted] = [True] then "True" else "False"),
    #"Outras Colunas Removidas1" = Table.SelectColumns(#"Coluna Valida",{"Trajeto", "Frame", "Predicted", "Confianca", "Modelo", "True", "Valido"}),
    #"Coluna S_Valido" = Table.AddColumn(#"Outras Colunas Removidas1", "S_Valido", each if [Valido] = "True" then 1 else 0),
    #"Coluna S_Invalido" = Table.AddColumn(#"Coluna S_Valido", "S_Invalido", each if [Valido] = "False" then 1 else 0),
    #"Remove Copia" = Table.ReplaceValue(#"Coluna S_Invalido"," - Copia","",Replacer.ReplaceText,{"Confianca"}),
    #"Colunas Reordenadas" = Table.ReorderColumns(#"Remove Copia",{"Modelo", "Trajeto", "Frame", "Predicted", "True", "Confianca", "Valido", "S_Valido", "S_Invalido"}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Colunas Reordenadas", {{"Confianca", type number}}, "en-US"),
    #"Filtro Confianca" = Table.SelectRows(#"Tipo Alterado com Localidade", each [Confianca] >= v_confianca),
    #"Linhas Agrupadas" = Table.Group(#"Filtro Confianca", {"Modelo", "Predicted", "True"}, {{"Valido", each List.Sum([S_Valido]), type number}, {"Invalido", each List.Sum([S_Invalido]), type number}})
in
    #"Linhas Agrupadas"

```

#### v_confianca


```powerquery
let
    Fonte = 0.7
in
    Fonte
```

Apos as consultas criadas foi adicionado em cada panilha com o modelo que terminava em `_background` a formula abaixo na coluna `E`.

Exemplo ppara a planilha ´yolov8s_seed_background´ 
```text
=CONT.SES('Dados Tratados 2'!A:A;yolov8s_seed_Bacground[[#Cabeçalhos];[yolov8s_seed]];'Dados Tratados 2'!B:B;[@Trajeto];'Dados Tratados 2'!C:C;[@Frame];'Dados Tratados 2'!D:D;[@True])
```
OBS: Em cada planilha de modelo vede modar o nome do modelo na formula para seu modelo.
