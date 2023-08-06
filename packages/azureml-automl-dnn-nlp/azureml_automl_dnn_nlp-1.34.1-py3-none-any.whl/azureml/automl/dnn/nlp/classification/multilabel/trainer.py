# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for training Pytorch Models"""

import logging
import numpy as np
from sklearn import metrics
import time
import torch
from torch.utils.data import DataLoader, RandomSampler

from azureml.automl.dnn.nlp.classification.common.constants import MultiLabelParameters
from azureml.automl.dnn.nlp.classification.multilabel.utils import compute_threshold_metrics
from azureml.automl.dnn.nlp.common.constants import Warnings, Split

_logger = logging.getLogger(__name__)


class PytorchTrainer:
    """Class to perform training on a model given a dataset"""

    def __init__(self,
                 model_class,
                 num_label_cols,
                 is_gpu=True):
        """
        Function to initialize pytorch trainer

        :param model_class: Class to use for model initialization
        :param num_label_cols: Number of unique classes in label column
        :param is_gpu: Setting to allow for gpu training
        """
        self.device = self._get_device()
        self.model = model_class(num_label_cols)
        self.model.to(self.device)
        self.loss_fn = torch.nn.BCEWithLogitsLoss
        _logger.info("Learning_rate: {}".format(self._get_learning_rate()))
        self.optimizer = torch.optim.Adam(params=self.model.parameters(), lr=self._get_learning_rate())
        self.sampler = RandomSampler

    def _get_learning_rate(self):
        return MultiLabelParameters.LEARNING_RATE

    def _data_sampler(self, dataset, mode=Split.train):
        return RandomSampler(dataset)

    def _get_device(self, is_gpu=True):
        """
        Device can differ based on trainer. This function is used to get device based on what the trainer needs
        """
        device = 'cuda' if (torch.cuda.is_available() and is_gpu) else 'cpu'
        if is_gpu and device == "cpu":
            _logger.warning(Warnings.CPU_DEVICE_WARNING)
        return device

    def train(self, training_set):
        """
        Function to perform training on the model given a training dataset

        :param training_set: pytorch dataset object containing information of training data
        """
        train_sampler = self._data_sampler(training_set, mode=Split.train)
        training_loader = DataLoader(training_set,
                                     sampler=train_sampler,
                                     batch_size=MultiLabelParameters.TRAIN_BATCH_SIZE)
        start_time = time.time()
        for epoch in range(MultiLabelParameters.EPOCHS):
            start_time_epoch = time.time()

            self.model.train()
            optimizer = self.optimizer
            for _, data in enumerate(training_loader, 0):
                ids = data['ids'].to(self.device, dtype=torch.long)
                mask = data['mask'].to(self.device, dtype=torch.long)
                token_type_ids = data['token_type_ids'].to(self.device, dtype=torch.long)
                targets = data['targets'].to(self.device, dtype=torch.float)

                outputs = self.model(ids, mask, token_type_ids)

                optimizer.zero_grad()
                loss = self.loss_fn()(outputs, targets)
                if _ % MultiLabelParameters.OUTPUT_EPOCHS_COUNT == 0:
                    _logger.info('Epoch: {}, Step: {}, Loss:  {}'.format(epoch, _, loss.item()))

                loss.backward()
                optimizer.step()

            _logger.info("Time for epoch {}: {}".format(epoch, time.time() - start_time_epoch))
        _logger.info("Total training time : {}".format(time.time() - start_time))
        return self.model

    def validate(self, valid_set):
        """
        Function to perform validation on the model given a validation dataset

        :param valid_set: pytorch dataset object to run validation on
        """
        valid_sampler = self._data_sampler(valid_set, mode=Split.test)
        valid_loader = DataLoader(valid_set,
                                  sampler=valid_sampler,
                                  batch_size=MultiLabelParameters.VALID_BATCH_SIZE)
        start_time = time.time()
        self.model.eval()
        fin_targets = []
        fin_outputs = []
        with torch.no_grad():
            for _, data in enumerate(valid_loader, 0):
                ids = data['ids'].to(self.device, dtype=torch.long)
                mask = data['mask'].to(self.device, dtype=torch.long)
                token_type_ids = data['token_type_ids'].to(self.device, dtype=torch.long)
                targets = data['targets'].to(self.device, dtype=torch.float)
                outputs = self.model(ids, mask, token_type_ids)
                fin_targets.extend(targets.cpu().detach().numpy().tolist())
                fin_outputs.extend(torch.sigmoid(outputs).cpu().detach().numpy().tolist())
        _logger.info("Total validation time : {}".format(time.time() - start_time))
        return fin_outputs, fin_targets

    def compute_metrics(self, valid_set):
        """
        Function to compute metrics given a validation set. Currently computes accuracy, f1_score micro and macro

        :param valid_set: Pytorch dataset used for validation to get metrics from
        """
        outputs, targets = self.validate(valid_set)

        metrics_dict = compute_threshold_metrics(outputs, targets)

        outputs = np.array(outputs) >= 0.5
        accuracy = metrics.accuracy_score(targets, outputs)
        f1_score_micro = metrics.f1_score(targets, outputs, average='micro')
        f1_score_macro = metrics.f1_score(targets, outputs, average='macro')

        _logger.info("Accuracy: {}".format(accuracy))
        _logger.info("F1 Score (Micro): {}".format(f1_score_micro))
        _logger.info("F1 Score (Macro): {}".format(f1_score_macro))

        return accuracy, f1_score_micro, f1_score_macro, metrics_dict
