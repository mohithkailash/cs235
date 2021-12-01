import pandas as pd
import Preprocess

if __name__ == "__main__":
    data = pd.read_csv('final_imdb.csv', encoding='utf-8')
    data = Preprocess.pre_process(data)
    export_csv = data.to_csv("PreprocessData.csv")
