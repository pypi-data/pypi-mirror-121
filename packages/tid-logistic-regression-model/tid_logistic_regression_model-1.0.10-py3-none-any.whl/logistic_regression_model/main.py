import time

from modelling_evaluation.modelling import model_eval

if __name__ == "__main__":
    start = time.time()

    model_eval()

    total_time = round((time.time() - start) / 60, 2)
    print(f"Total runtime: {total_time} minutes")
