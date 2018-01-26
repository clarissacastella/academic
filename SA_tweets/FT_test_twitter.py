# coding=UTF-8
import os
from flask import Flask, jsonify, request, send_from_directory
import fasttext as ft


MODEL_NAME = "./result/EPTC_POA1nov_23jan_model"

# load model
classifier = ft.load_model(MODEL_NAME + '.bin', label_prefix='__label__')

def make_prediction(text):
    # clean text
    #text = utils.normalize_text(text)
    labels = classifier.predict_proba([text], k=3)[0]
    labels = map(lambda (k, v): {'rating': k, 'score': v}, labels)
    result = {'status': 0, 'prediction': labels}
    print "===================="
    print text
    print "===================="
    print result


if __name__ == "__main__":
    print make_prediction("No acesso a Capital pela rodoviária, fluxo é tranquilo.")
    print make_prediction("Congestionamento na Av. Assis Brasil x Emilio Lucio Esteves por conta de pontos de alagamento.")
    print make_prediction("acidente tem feridos na via")
    print make_prediction("fluxo é tranquilo")
    print make_prediction("No acesso a Capital pela rodoviária, fluxo é tranquilo")
