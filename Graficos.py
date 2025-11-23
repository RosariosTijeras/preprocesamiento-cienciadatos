import matplotlib.pyplot as plt
import time
from codigo_original import main as ejecutar_original
from codigo_optimizado import main as ejecutar_optimizado

def medir_tiempo(func):
	inicio = time.time()
	func()
	fin = time.time()
	return fin - inicio

etiquetas = ['Original', 'Optimizado']
tiempos = [medir_tiempo(ejecutar_original), medir_tiempo(ejecutar_optimizado)]

plt.bar(etiquetas, tiempos, color=['red', 'green'])
plt.title('Comparación de Tiempos de Ejecución')
plt.ylabel('Tiempo (segundos)')
plt.show()