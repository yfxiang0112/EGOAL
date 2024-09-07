from train import train

from multiprocessing import Pool
from tqdm import tqdm

def main():
    #for i in tqdm(range(0,4758)):
    with Pool(processes=4) as pool:
        pool.map(train, range(4758))
        #train(i)

if __name__ == "__main__":
    main()
