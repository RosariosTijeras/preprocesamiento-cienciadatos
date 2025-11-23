import time

def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def main():
    inicio = time.time()
    primos = []
    for i in range(1, 100001):
        if es_primo(i):
            primos.append(i)
    fin = time.time()
    print(f"Tiempo: {fin - inicio} segundos")
    print(f"Numeros primos encontrados: {len(primos)}")

if __name__ == "__main__":
    main()