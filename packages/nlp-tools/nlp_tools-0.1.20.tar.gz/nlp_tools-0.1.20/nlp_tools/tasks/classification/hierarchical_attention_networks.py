from typing import Dict,Any
from tensorflow import keras
from nlp_tools.layers import L
from nlp_tools.tasks.classification.abc_model import ABCClassificationModel

from nlp_tools.layers.normal_attention import NormalAttentionLayer
from nlp_tools.layers.non_masking_layer import HierarchicalAttentionMaskingLayer


class HierarchicalAttentionNetworks(ABCClassificationModel):
    @classmethod
    def default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            'sentence_attention':{
                'attention_dim': 128
            },
            'layer_bi_lstm': {
                'units': 10,
                'return_sequences': True
            },
            'layer_output': {

            },

            'dco_attention':{
                'attention_dim': 128
            },
        }

    def build_model_arc(self) -> None:
        output_dim = self.label_processor.vocab_size

        config = self.hyper_parameters
        embed_model = self.embedding.embed_model


        # build model structure in sequent way
        sentence_bilstm = L.Bidirectional(L.LSTM(**config['layer_bi_lstm']))(embed_model.output)
        sentence_attention = NormalAttentionLayer(name="sentence_attention",**config['sentence_attention'])(sentence_bilstm)
        sentEncoder = keras.Model(self.embedding.embed_model.inputs, sentence_attention)

        review_input = L.Input(shape=(20, None), dtype='int32')
        reivew_input_mask = L.Input(shape=(20,), dtype='int32')

        review_encoder = L.TimeDistributed(sentEncoder)(review_input)

        #review_encoder_masked = L.Reshape((20,))(review_encoder)
        review_encoder_masked = HierarchicalAttentionMaskingLayer(reivew_input_mask)(review_encoder)

        #doc_bilstm = L.Bidirectional(L.LSTM(name='doc_lstm',**config['layer_bi_lstm']),name='doc_bi_lstm')(review_encoder_masked)
        #doc_attention = NormalAttentionLayer(name="doc_attention",**config['dco_attention'])(doc_bilstm)


        dense_output = L.Dense(output_dim, **config['layer_output'])(review_encoder_masked)
        final_output = self._activation_layer()(dense_output)

        self.tf_model: keras.Model = keras.Model([review_input,reivew_input_mask], final_output)
