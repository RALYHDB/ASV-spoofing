import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, det_curve

# Datos de ejemplo
y_true = np.array([0] * 50 + [1] * 50)  # 50 impostores (0) y 50 usuarios (1)
y_scores = np.concatenate([np.random.uniform(0, 0.5, 50), np.random.uniform(0.5, 1, 50)])

# Calcular la curva ROC
fpr, tpr, thresholds_roc = roc_curve(y_true, y_scores)
fnr = 1 - tpr  # FNR = 1 - TPR

# Calcular el EER (Equal Error Rate)
eer_threshold = thresholds_roc[np.nanargmin(np.absolute(fnr - fpr))]
eer_fpr = fpr[np.nanargmin(np.absolute(fnr - fpr))]
eer_fnr = fnr[np.nanargmin(np.absolute(fnr - fpr))]

# Calcular la curva DET
fpr_det, fnr_det, _ = det_curve(y_true, y_scores)

# Configurar la gráfica
plt.figure(figsize=(12, 6))

# Gráfica ROC
plt.subplot(1, 2, 1)
plt.plot(fpr, fnr, color='blue', label='Curva ROC')
plt.scatter(eer_fpr, eer_fnr, color='red', zorder=5, label='EER')
plt.plot([0, 1], [0, 1], 'k--', label='Línea de referencia')
plt.xlabel('Probabilidad de Falsa Alarma')
plt.ylabel('Probabilidad de Pérdida')
plt.title('Curva ROC')
plt.legend()
plt.grid(True)

# Gráfica DET
plt.subplot(1, 2, 2)
plt.plot(fpr_det, fnr_det, color='blue', label='Curva DET')
plt.scatter(eer_fpr, eer_fnr, color='red', zorder=5, label='EER')
plt.plot([0, 1], [0, 1], 'k--', label='Línea de referencia')
plt.xlabel('Probabilidad de Falsa Alarma (%)')
plt.ylabel('Probabilidad de Pérdida (%)')
plt.title('Curva DET')
plt.legend()
plt.grid(True)

# Guardar la gráfica
plt.tight_layout()
plt.savefig('curvas_ROC_and_DET.png', dpi=300)
plt.show()
