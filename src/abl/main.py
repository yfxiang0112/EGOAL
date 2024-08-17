from train import train
from tqdm import tqdm

def main():
    for i in tqdm(range(0,4758)):
        train(i)

if __name__ == "__main__":
    main()
