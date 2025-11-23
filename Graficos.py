import matplotlib.pyplot as plt
import time

def medir_tiempo(funcion):
	inicio = time.time()
	funcion()
	fin = time.time()
	return fin - inicio

from codigo_optimizado import main as tiempo_optimizado
from codigo_original import main as tiempo_original

etiquetas = ['Original', 'Optimizado']
tiempos = [medir_tiempo(tiempo_original), medir_tiempo(tiempo_optimizado)]

plt.bar(etiquetas, tiempos, color=['red', 'green'])
plt.title('Comparación de Tiempos de Ejecución')
plt.ylabel('Tiempo (segundos)')
plt.show()