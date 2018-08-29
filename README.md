# academic

* Arquivo `elasticsearch_ee.py`: extrai locais citados nos tweets usando biblioteca Spacy e o modelo no diretório `model10iter` e insere na base Elasticsearch

* Diretório `model10iter`: modelo gerado usando a biblioteca Spacy para extração de entidades nomeadas do tipo local de tweets.

* Arquivo `elasticsearch_class_polarity.py`: classifica a polaridade dos tweets usando model SVM da biblioteca NLTK e insere na base Elasticsearch

* Diretório `data`: tweets para treino do `elasticsearch_class_polarity.py`


