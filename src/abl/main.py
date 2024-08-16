from train import train
from tqdm import tqdm

def main():
    for i in tqdm(range(0,4842)):
        train(i)

if __name__ == "__main__":
    main()
