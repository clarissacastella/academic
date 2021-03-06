import os
import fasttext as ft

# path
DATA_DIR = "./data/"
DIR = "./"
RESULT_DIR = "./"

TRAIN_FILE = './data/train_EPTC_POA1nov_23jan.data'
MODEL_NAME = "./result/EPTC_POA1nov_23jan_model"

#from /media/tmp/faa8fb7c-c759-4e71-8525-d0d7a7a6dbba/posdoc/sent_twitter/fasttext_sentiment/data/train_transito_tw.data
#generate /media/tmp/faa8fb7c-c759-4e71-8525-d0d7a7a6dbba/posdoc/sent_twitter/fasttext_sentiment/result/transito_tw.bin
def main():
    input_file = TRAIN_FILE
    out_file = MODEL_NAME
    classifier = ft.supervised(
        input_file,
        out_file,
        dim=20,
        lr=0.25,
        word_ngrams=2,
        min_count=20,
        bucket=1000000,
        epoch=5,
        thread=10,
        silent=0,
        label_prefix="__label__")

if __name__ == '__main__':
    main()
