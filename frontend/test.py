import json
import time

for i in range(10):
    print(json.dumps({"value": i}), flush=True)  # Wydruk w formacie JSON
    time.sleep(1)  # Czekaj 1 sekundę między iteracjami
