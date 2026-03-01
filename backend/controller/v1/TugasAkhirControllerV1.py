from backend.response.advices.ListResponseParameter import ListResponseParameter
from backend.response.advices.DataResponseParameter import DataResponseParameter
from backend.response.advices.SliceResponseParameter import SliceResponseParameter
from backend.controller.advices.BaseController import BaseController
from backend.annotations.method.PostEndpoint import PostEndpoint
from backend.annotations.method.GetEndpoint import GetEndpoint
from backend.annotations.method.SwaggerTypeGroup import SwaggerTypeGroup
from backend.request.v1.ScrapeSerperRequestV1 import ScrapeSerperRequestV1
from backend.response.v1.ScrapeSerperResponseV1 import ScrapeSerperResponseV1
from backend.request.v1.ListDatasetRequestV1 import ListDatasetRequestV1
from backend.request.v1.SearchDatasetRequestV1 import SearchDatasetRequestV1
from backend.request.v1.GetDatasetByLinkRequestV1 import GetDatasetByLinkRequestV1
from backend.response.v1.ListDatasetResponseV1 import ListDatasetResponseV1
from backend.response.v1.DetailDatasetResponseV1 import DetailDatasetResponseV1
from backend.request.v1.ConfusionMatrixRequestV1 import ConfusionMatrixRequestV1
from backend.request.v1.KFoldCrossValidationRequestV1 import KFoldCrossValidationRequestV1
from backend.request.v1.EpochEarlyStoppingRequestV1 import EpochEarlyStoppingRequestV1
from backend.request.v1.BatchSizeRequestV1 import BatchSizeRequestV1
from backend.request.v1.OptimizerRequestV1 import OptimizerRequestV1
from backend.request.v1.EpochTrainingRequestV1 import EpochTrainingRequestV1
from abc import ABC, abstractmethod

@BaseController(value="/api/v1")
class TugasAkhirControllerV1(ABC):

    @PostEndpoint(
        value="/serper",
        tagName="Tugas Akhir Management",
        description="Scrape With Serper API",
        group=SwaggerTypeGroup.APPS_WEB
    )
    def getScrapeSerper(self, validation_request: ScrapeSerperRequestV1) -> ListResponseParameter[ScrapeSerperResponseV1]:
        pass

    @GetEndpoint(
        value="/list-dataset",
        tagName="Tugas Akhir Management",
        description="Get List Dataset",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getListDataset(self) -> SliceResponseParameter[ListDatasetResponseV1]:
        pass

    @GetEndpoint(
        value="/detail-dataset/{id}",
        tagName="Tugas Akhir Management",
        description="Get Detail Dataset",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getDetailDataset(self, id: int) -> DataResponseParameter[DetailDatasetResponseV1]:
        pass

    @PostEndpoint(
        value="/dataset-by-link",
        tagName="Tugas Akhir Management",
        description="Get Dataset by Link URL",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getDatasetByLink(self, validation_request: GetDatasetByLinkRequestV1) -> DataResponseParameter[DetailDatasetResponseV1]:
        pass

    @PostEndpoint(
        value="/search-dataset",
        tagName="Tugas Akhir Management",
        description="Search Dataset by keyword, title, or description",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def searchDataset(self, validation_request: SearchDatasetRequestV1) -> SliceResponseParameter[ListDatasetResponseV1]:
        pass

    @PostEndpoint(
        value="/confusion-matrix",
        tagName="Evaluation Metrics",
        description="Get Confusion Matrix and Evaluation Metrics (Accuracy, Precision, Recall, F1-Score)",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getConfusionMatrix(self, validation_request: ConfusionMatrixRequestV1) -> DataResponseParameter[dict]:
        pass

    @PostEndpoint(
        value="/k-fold-cross-validation",
        tagName="Evaluation Metrics",
        description="Get K-Fold Cross Validation with k=3 and k=5",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getKFoldCrossValidation(self, validation_request: KFoldCrossValidationRequestV1) -> DataResponseParameter[dict]:
        pass

    @PostEndpoint(
        value="/epoch-early-stopping",
        tagName="Evaluation Metrics",
        description="Simulate training with Epoch and Early Stopping mechanism",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getEpochEarlyStopping(self, validation_request: EpochEarlyStoppingRequestV1) -> DataResponseParameter[dict]:
        pass

    @PostEndpoint(
        value="/batch-size",
        tagName="Evaluation Metrics",
        description="Calculate Batch Size analysis for training optimization",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getBatchSize(self, validation_request: BatchSizeRequestV1) -> DataResponseParameter[dict]:
        pass

    @PostEndpoint(
        value="/optimizer",
        tagName="Evaluation Metrics",
        description="Compare different optimizers (SGD, RMSprop, Adam)",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getOptimizer(self, validation_request: OptimizerRequestV1) -> DataResponseParameter[dict]:
        pass

    @PostEndpoint(
        value="/epoch-training",
        tagName="Evaluation Metrics",
        description="Train model using ALL data without validation split (final training)",
        group=SwaggerTypeGroup.APPS_WEB
    )
    @abstractmethod
    def getEpochTraining(self, validation_request: EpochTrainingRequestV1) -> DataResponseParameter[dict]:
        pass
