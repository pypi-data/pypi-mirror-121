import torch

from TakeBlipNer.predict import NerPredict
from TakeBlipPosTagger.predict import PosTaggerPredict
from TakeBlipNer.utils import load_fasttext_embeddings

def load_postagging_predictor(postagging_model_path, postagging_label_path, embedding_path):
        embedding = load_fasttext_embeddings(embedding_path, '<pad>')
        postag_model = torch.load(postagging_model_path)
        postag_predictor = PosTaggerPredict(
                model=postag_model,
                label_path=postagging_label_path,
                embedding=embedding
        )
        return postag_predictor

def load_ner_predictor(ner_model_path, ner_label_path, postag_predictor):
        ner_model = torch.load(ner_model_path)
        ner_predictor = NerPredict(
            model=ner_model,
            label_path=ner_label_path,
            postag_model=postag_predictor,
            pad_string='<pad>',
            unk_string='<unk>'
        )
        return ner_predictor