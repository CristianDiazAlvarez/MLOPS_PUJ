import time

start = time.time()
for _ in range(10000):
    sum([i ** 2 for i in range(10_000)])

elapsed = time.time() - start
if elapsed > 2:
    print(f"❌ Tardó demasiado: {elapsed:.2f} segundos")
    raise RuntimeError("CPU demasiado lenta")
else:
    print(f"✅ Tiempo aceptable: {elapsed:.2f} segundos")
