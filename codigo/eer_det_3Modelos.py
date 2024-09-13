import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve,auc

# Directorio donde se encuentran los archivos de puntuaciones
dir_puntuaciones = "puntuaciones"

# Cargar las puntuaciones para cada modelo
puntuaciones_clonadas_resnet = np.load(os.path.join(dir_puntuaciones, "puntuaciones_LOCs_agregado_LibriTTS_resnet.npy"))
puntuaciones_resnet = np.load(os.path.join(dir_puntuaciones, "puntuaciones_LOs_agregado_resnet.npy"))

puntuaciones_clonadas_ecapa = np.load(os.path.join(dir_puntuaciones, "puntuaciones_LOCs_agregado_LibriTTS_ecapa.npy"))
puntuaciones_ecapa = np.load(os.path.join(dir_puntuaciones, "puntuaciones_LOs_agregado_ecapa.npy"))

puntuaciones_clonadas_xvector = np.load(os.path.join(dir_puntuaciones, "puntuaciones_LOCs_agregado_LibriTTS_xvector.npy"))
puntuaciones_xvector = np.load(os.path.join(dir_puntuaciones, "puntuaciones_LOs_agregado_xvector.npy"))

# Calcular las tasas de falsos positivos (FPR) y falsos negativos (FNR) para cada modelo
fpr_resnet, tpr_resnet, umbrales = roc_curve([0]*len(puntuaciones_clonadas_resnet) + [1]*len(puntuaciones_resnet),
                                      np.concatenate([puntuaciones_clonadas_resnet, puntuaciones_resnet]))
fnr_resnet = 1 - tpr_resnet

fpr_ecapa, tpr_ecapa, _ = roc_curve([0]*len(puntuaciones_clonadas_ecapa) + [1]*len(puntuaciones_ecapa),
                                    np.concatenate([puntuaciones_clonadas_ecapa, puntuaciones_ecapa]))
fnr_ecapa = 1 - tpr_ecapa

fpr_xvector, tpr_xvector, _ = roc_curve([0]*len(puntuaciones_clonadas_xvector) + [1]*len(puntuaciones_xvector),
                                        np.concatenate([puntuaciones_clonadas_xvector, puntuaciones_xvector]))
fnr_xvector = 1 - tpr_xvector

# Encontrar el EER para cada modelo
eer_resnet = fpr_resnet[np.nanargmin(np.absolute((fnr_resnet - fpr_resnet)))]
eer_ecapa = fpr_ecapa[np.nanargmin(np.absolute((fnr_ecapa - fpr_ecapa)))]
eer_xvector = fpr_xvector[np.nanargmin(np.absolute((fnr_xvector - fpr_xvector)))]
# Calcular el AUC para cada modelo
auc_resnet = auc(fpr_resnet, fnr_resnet)
auc_ecapa = auc(fpr_ecapa, fnr_ecapa)
auc_xvector = auc(fpr_xvector, fnr_xvector)

# Graficar las curvas DET junto con los puntos de EER
plt.figure(figsize=(12, 8))

plt.plot(fpr_resnet, fnr_resnet, label=f'ResNet (EER={eer_resnet:.2f}, AUC={auc_resnet:.2f})')
plt.scatter(eer_resnet, eer_resnet, color='red')

plt.plot(fpr_ecapa, fnr_ecapa, label=f'Ecapa (EER={eer_ecapa:.2f}, AUC={auc_ecapa:.2f})')
plt.scatter(eer_ecapa, eer_ecapa, color='blue')

plt.plot(fpr_xvector, fnr_xvector, label=f'XVector (EER={eer_xvector:.2f}, AUC={auc_xvector:.2f})')
plt.scatter(eer_xvector, eer_xvector, color='green')
# Graficar la recta (0,0) a (1,1)
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Recta (0,0) a (1,1)')



plt.title('Curvas DET para los Modelos de Verificación de Locutor')
plt.xlabel('Tasa de Falsos Positivos')
plt.ylabel('Tasa de Falsos Negativos')
plt.legend()
plt.grid(True)

# Guardar la imagen
plt.savefig('curvas_DET_LibriTTS_EP100.png', dpi=300, bbox_inches='tight', format='png')

plt.show()

# Graficar FPR y FNR vs umbral en la misma gráfica
plt.figure(figsize=(12, 8))
plt.plot(umbrales, fpr_resnet, label='FPR', color='blue')
plt.plot(umbrales, fnr_resnet, label='FNR', color='red')
plt.xlabel('Umbral')
plt.ylabel('Tasa de Falsos Positivos (FPR) / Tasa de Falsos Negativos (FNR)')
plt.title('FPR y FNR vs Umbral')
plt.legend()
plt.grid(True)
plt.show()


