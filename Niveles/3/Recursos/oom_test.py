import time
import sys

print("🚀 Iniciando prueba de consumo de memoria...", flush=True)

start = time.time()
data = []

try:
    while True:
        data.append("x" * 10**6)  # ~1 MB por iteración
        uso_actual = len(data)//2
        print(f"📈 Uso de memoria simulado: {uso_actual} MB", flush=True)
        time.sleep(0.1)

except MemoryError:
    print("🧨 Error: memoria insuficiente", flush=True)

except Exception as e:
    print(f"💥 Error inesperado: {e}", flush=True)

finally:
    total_time = time.time() - start
    print(f"🕒 Tiempo total de ejecución hasta fallo o detención: {total_time:.2f} segundos", flush=True)
    print(f"🧠 Memoria alcanzada al finalizar: {len(data)} MB", flush=True)
