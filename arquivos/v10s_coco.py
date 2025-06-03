import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, precision_score, f1_score

# Valores originais como tuplas de listas
y_pred_original = ([1]*1,[5]*57,[6]*6,[6]*291,[6]*12,[6]*83,[7]*36,[7]*91,[7]*8,[7]*1,[7]*15,[8]*8,[8]*2,[8]*277,[8]*29,[9]*12,[9]*277,[9]*4,[9]*8,[9]*6,[9]*235,[9]*1,[9]*57,[10]*44,[10]*18,[12]*1,[12]*20,[13]*2476,[14]*13,[14]*490,[15]*184,[15]*315,[16]*81,[16]*1,[16]*49,[17]*44,[17]*1,[18]*71,[18]*198,[18]*91,[18]*51,[18]*164,[18]*16,[18]*114,[18]*2267,[18]*1422,[18]*243,[18]*25,[18]*67934
)
y_true_original = ([18]*1,[5]*57,[5]*6,[6]*291,[8]*12,[18]*83,[5]*36,[7]*91,[8]*8,[10]*1,[18]*15,[6]*8,[7]*2,[8]*277,[18]*29,[4]*12,[5]*277,[7]*4,[8]*8,[10]*6,[18]*235,[12]*1,[15]*57,[5]*44,[10]*18,[18]*1,[12]*20,[13]*2476,[18]*13,[14]*490,[18]*184,[15]*315,[18]*81,[15]*1,[16]*49,[18]*44,[13]*1,[4]*71,[5]*198,[6]*91,[7]*51,[8]*164,[10]*16,[12]*114,[13]*2267,[14]*1422,[15]*243,[16]*25,[18]*67934
)
# Corrigindo o formato de y_pred e y_true para serem listas simples
y_pred = []
for sublist in y_pred_original:
    y_pred.extend(sublist)

y_true = []
for sublist in y_true_original:
    y_true.extend(sublist)

# Garantindo que y_true e y_pred tenham o mesmo tamanho
assert len(y_true) == len(y_pred), f"Tamanhos diferentes! y_true: {len(y_true)}, y_pred: {len(y_pred)}"

# Definição das classes
classes = ["100km-h", "10km-h", "110km-h", "120km-h", "20km-h", "30km-h", "40km-h", "50km-h", "60km-h", "70km-h", "80km-h", "90km-h", "Estacionamento", "Lombada", "Pare", "Proibido Estacionar", "Proibido Parar e Estacionar", "Rotatoria", "Background"]
# Índices:      0         1         2         3         4         5         6         7         8          9          10          11              12             13        14                 15                               16                 17              18

# Definir todos os labels possíveis com base nas classes
labels_all = list(range(len(classes)))

# Gerar matriz de confusão NÃO NORMALIZADA para cálculo de métricas
cm_for_metrics_calc = confusion_matrix(y_true, y_pred, labels=labels_all)

# Gerar matriz de confusão NORMALIZADA PELAS LINHAS (true condition) para a plotagem original
cm_normalized_by_true = confusion_matrix(y_true, y_pred, labels=labels_all, normalize='true')

# Para inverter os eixos (True no X, Predicted no Y), vamos transpor a matriz normalizada.
# A normalização original (normalize='true') significa que as LINHAS da cm_normalized_by_true somam 1 (ou 0).
# Quando transpomos (cm_normalized_by_true.T), as COLUNAS da matriz transposta somarão 1.
# Isso significa que cada coluna (rótulo verdadeiro) mostrará a distribuição das predições.
cm_to_plot = cm_normalized_by_true.T


# Calcular métricas (isso não muda, é baseado na orientação padrão y_true vs y_pred)
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted', labels=labels_all, zero_division=0)
f1 = f1_score(y_true, y_pred, average='weighted', labels=labels_all, zero_division=0)

# Calcular TP, TN, FP e FN para cada classe (usando a matriz NÃO normalizada para contagens)
tp = np.diag(cm_for_metrics_calc)
fp = np.sum(cm_for_metrics_calc, axis=0) - tp
fn = np.sum(cm_for_metrics_calc, axis=1) - tp
total_samples = np.sum(cm_for_metrics_calc)
tn = []
for i in range(len(classes)):
    tn_class_i = total_samples - (tp[i] + fp[i] + fn[i])
    tn.append(tn_class_i)
tn = np.array(tn)


# Exibir TP, TN, FP, FN para cada classe
print("--- Métricas por Classe (Contagens) ---")
for i, classe_nome in enumerate(classes):
    print(f"Classe: {classe_nome} (Índice {labels_all[i]})")
    print(f"  TP: {tp[i]}")
    print(f"  TN: {tn[i]}")
    print(f"  FP: {fp[i]}")
    print(f"  FN: {fn[i]}")
    print()
print("-" * 30)

# Calcular TP GERAL (soma da diagonal da matriz não normalizada - total de acertos)
geral_tp_sum_diag = np.sum(tp)

print("--- Métricas Gerais de Classificação ---")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision (Weighted): {precision:.4f}")
print(f"F1 Score (Weighted): {f1:.4f}")
print(f"Total de Amostras: {len(y_true)}")
print(f"Total de Acertos (Soma da Diagonal Principal): {geral_tp_sum_diag}")
print(f"Total de Erros: {len(y_true) - geral_tp_sum_diag}")
print("-" * 30)


# Exibir o gráfico da matriz de confusão com eixos invertidos
fig, ax = plt.subplots(figsize=(15, 12)) # Ajuste o tamanho se necessário

# Usamos a matriz TRANSPOSTA cm_to_plot para a exibição
# display_labels ainda usa 'classes' porque as linhas e colunas da matriz transposta
# ainda correspondem a essas classes, mas em uma nova orientação.
disp = ConfusionMatrixDisplay(confusion_matrix=cm_to_plot, display_labels=classes)

# Plotamos a matriz.
disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation='vertical', values_format=".2f")

# Ajustar os rótulos dos eixos manualmente
ax.set_xlabel("Rótulo Verdadeiro (True Label)") # X agora é o Verdadeiro
ax.set_ylabel("Rótulo Previsto (Predicted Label)") # Y agora é o Previsto

# Iteramos sobre os textos da matriz de confusão plotada
# e limpamos aqueles cujo valor correspondente na matriz transposta é < 0.01 (1%)
# Note que disp.text_ terá as dimensões de cm_to_plot
for i in range(len(classes)): # Linhas da matriz plotada (agora são classes PREVISTAS)
    for j in range(len(classes)): # Colunas da matriz plotada (agora são classes VERDADEIRAS)
        text_obj = disp.text_[i, j]
        value = cm_to_plot[i, j] # Pega o valor da matriz transposta e normalizada
        if value < 0.01:
            text_obj.set_text("") # Define o texto como vazio se for menor que 1%
        # else: # Mantém o texto formatado, já definido por values_format
            # pass

plt.title("Matriz de Confusão Normalizada (valores <1% ocultos) yolov10s_coco")
plt.tight_layout() # Para evitar que os labels se sobreponham
plt.show()