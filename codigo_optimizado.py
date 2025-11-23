import time
import numpy as np

def es_primo(numero):
    if numero <= 1:
        return False
    
    if numero == 2:
        return True
    
    if numero % 2 == 0:
        return False
    
    max_divisor = int(np.sqrt(numero)) + 1
    
    for i in range(3, max_divisor, 2):
        if numero % i == 0:
            return False
    
    return True

def main():
    inicio = time.time()
    
    primos = [i for i in range(1, 100001) if es_primo(i)]
    
    fin = time.time()
    
    print(f"Tiempo: {fin - inicio} segundos")
    print(f"Numeros primos encontrados: {len(primos)}")

if __name__ == "__main__":
    main()