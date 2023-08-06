import random
from abc import ABC
import numpy as np
from typing import List,Dict,Any,Union

from sklearn import metrics as sklearn_metrics

import nlp_tools
from nlp_tools.layers import L
from nlp_tools.logger import logger

from nlp_tools.tasks.abs_task_model import ABCTaskModel
from nlp_tools.types import TextSamplesVar,ClassificationLabelVar,MultiLabelClassificationLabelVar

from nlp_tools.embeddings import ABCEmbedding,TransformerEmbedding,BertEmbedding
from nlp_tools.optimizer import MultiOptimizer
from tensorflow.keras.optimizers import Adam

#from transformers.optimization_tf import AdamWeightDecay
from nlp_tools.loss.r_drop_loss import RDropLoss

class ABCClassificationModel(ABCTaskModel,ABC):
    """
    Abstract Classification Model
    """

    __task__ = 'classification'

    def to_dict(self) -> Dict:
        info = super(ABCClassificationModel, self).to_dict()
        return info

    def __init__(self,
                 text_processor,
                 label_processor,
                 embedding: ABCEmbedding = None,
                 max_sequence_length: int = None,
                 hyper_parameters: Dict[str, Dict[str, Any]] = None,
                 train_sequece_length_as_max_sequence_length=False,
                 use_FGM=True,
                 use_rdrop=True):

        super(ABCClassificationModel, self).__init__(text_processor=text_processor,label_processor=label_processor,
                                                     embedding=embedding,max_sequence_length=max_sequence_length,hyper_parameters=hyper_parameters,
                                                     train_sequece_length_as_max_sequence_length=train_sequece_length_as_max_sequence_length,
                                                     use_FGM=use_FGM,use_rdrop=use_rdrop)
    def _activation_layer(self) -> L.Layer:
        # if self.multi_label:
        #     return L.Activation('sigmoid')
        # else:
        return L.Activation('softmax')




    def build_model_arc(self) -> None:
        raise NotImplementedError

    def compile_model(self,
                      loss: Any = None,
                      optimizer: Any = None,
                      metrics: Any = None,
                      **kwargs: Any) -> None:

        if loss is None:
            from nlp_tools.loss import multi_category_focal_loss2_fixed
            from tensorflow.keras.losses import CategoricalCrossentropy
            #loss = 'categorical_crossentropy'
            loss = multi_category_focal_loss2_fixed

        if type(self.embedding) in [TransformerEmbedding, BertEmbedding]:
            total_layers = self.tf_model.layers
            transfomer_layers = self.embedding.embed_model.layers
            no_transformer_layers = [layer for layer in total_layers if layer not in transfomer_layers]
            optimizer_list = [
                Adam(),
                Adam(learning_rate=1e-5)
            ]
            optimizers_and_layers = [(optimizer_list[0], no_transformer_layers), (optimizer_list[1], transfomer_layers)]
            optimizer = MultiOptimizer(optimizers_and_layers)
        else:
            optimizer = Adam()
        if self.use_rdrop:
            if type(loss) == list:
                loss = [RDropLoss(i) for i in loss]
            else:
                loss = RDropLoss(loss)

        #optimizer = Adam()#AdamW(weight_decay=0.0)
        if metrics is None:
            metrics = ['accuracy']

        self.tf_model.compile(loss=loss,
                              optimizer=optimizer,
                              metrics=metrics,
                              **kwargs)




    def predict(self,
                x_data: TextSamplesVar,
                *,
                batch_size: int = 32,
                truncating: bool = False,
                multi_label_threshold: float = 0.5,
                predict_kwargs: Dict = None) -> Union[ClassificationLabelVar, MultiLabelClassificationLabelVar]:
        if predict_kwargs is None:
            predict_kwargs = {}

        with nlp_tools.utils.custom_object_scope():
            if truncating:
                seq_length = self.max_sequence_length
            else:
                seq_length = None
            tensor = self.text_processor.transform(x_data,seq_length=seq_length)
            pred = self.tf_model.predict(tensor, batch_size=batch_size, **predict_kwargs)
            pred_argmax = pred.argmax(-1)
            res = self.label_processor.inverse_transform(pred_argmax)

        return res

    def evaluate(self,
                 x_data: TextSamplesVar,
                 y_data: Union[ClassificationLabelVar, MultiLabelClassificationLabelVar],
                 *,
                 batch_size: int = 32,
                 digits: int = 4,
                 multi_label_threshold: float = 0.5,
                 truncating: bool = False,) -> Dict:
        y_pred = self.predict(x_data,
                              batch_size=batch_size,
                              truncating=truncating,
                              multi_label_threshold=multi_label_threshold)


        original_report = sklearn_metrics.classification_report(y_data,
                                                                y_pred,
                                                                output_dict=True,
                                                                digits=digits)
        print(sklearn_metrics.classification_report(y_data,
                                                    y_pred,
                                                    output_dict=False,
                                                    digits=digits))
        report = {
            'detail': original_report,
            **original_report['weighted avg']
        }
        return report

