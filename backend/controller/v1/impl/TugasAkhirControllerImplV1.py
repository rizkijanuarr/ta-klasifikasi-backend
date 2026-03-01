from flask import request, jsonify, Response
import json
from dataclasses import asdict
from backend.controller.advices.BaseControllerImpl import BaseControllerImpl
from backend.controller.v1.TugasAkhirControllerV1 import TugasAkhirControllerV1
from backend.service.v1.impl.TugasAkhirServiceImplV1 import TugasAkhirServiceImplV1
from backend.request.v1.ScrapeSerperRequestV1 import ScrapeSerperRequestV1
from backend.request.v1.ListDatasetRequestV1 import ListDatasetRequestV1
from backend.request.v1.SearchDatasetRequestV1 import SearchDatasetRequestV1
from backend.request.v1.GetDatasetByLinkRequestV1 import GetDatasetByLinkRequestV1
from backend.request.v1.ConfusionMatrixRequestV1 import ConfusionMatrixRequestV1
from backend.request.v1.KFoldCrossValidationRequestV1 import KFoldCrossValidationRequestV1
from backend.request.v1.EpochEarlyStoppingRequestV1 import EpochEarlyStoppingRequestV1
from backend.request.v1.BatchSizeRequestV1 import BatchSizeRequestV1
from backend.request.v1.OptimizerRequestV1 import OptimizerRequestV1
from backend.request.v1.EpochTrainingRequestV1 import EpochTrainingRequestV1


from backend.utils.ResponseHelper import ResponseHelper

@BaseControllerImpl
class TugasAkhirControllerImplV1(TugasAkhirControllerV1):

    def __init__(self):
        self.service = TugasAkhirServiceImplV1()


    def getScrapeSerper(self, validation_request: ScrapeSerperRequestV1):
        try:
            service_response = self.service.getScrapeSerper(validation_request)

            final_response = ResponseHelper.create_response_list(service_response)

            return final_response
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Serper API Failed",
                "data": None,
                "errors": [{
                    "code": "SERPER_API_ERROR",
                    "title": "Serper Crawling Failed",
                    "message": str(e)
                }]
            }), 500


    def getListDataset(self):
        # Get query parameters from request
        from flask import request

        # Create request object from query params
        try:
            is_legal = int(request.args.get('is_legal', 1))
            limit_data = int(request.args.get('limit_data', 10))
            page = int(request.args.get('page', 1))

            # Create validation request
            validation_request = ListDatasetRequestV1(
                is_legal=is_legal,
                limit_data=limit_data,
                page=page
            )
        except (ValueError, TypeError) as e:
            return ResponseHelper.create_error_response(
                message="Invalid query parameters",
                errors=[{"code": 400, "message": str(e), "title": "Validation Error"}]
            ), 400

        service_response = self.service.getListDataset(validation_request)
        data = service_response['data']
        total_data = service_response.get('total_data')
        has_next = service_response.get('has_next', False)
        is_first = service_response.get('is_first', False)
        is_last = service_response.get('is_last', False)
        current_page = service_response.get('current_page')
        message = service_response.get('message')

        final_response = ResponseHelper.create_response_slice(
            data=data,
            total_data=total_data,
            has_next=has_next,
            is_first=is_first,
            is_last=is_last,
            current_page=current_page,
            message=message
        )

        return final_response


    def getDetailDataset(self, id: int):
        try:
            id_int = int(id)
            service_response = self.service.getDetailDataset(id_int)

            final_response = ResponseHelper.create_response_data(service_response)

            return final_response
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Invalid ID format",
                "data": None,
                "errors": [{
                    "code": "INVALID_ID",
                    "title": "Invalid ID",
                    "message": f"ID must be a valid integer, got: {id}"
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Detail Dataset Failed",
                "data": None,
                "errors": [{
                    "code": "DETAIL_DATASET_ERROR",
                    "title": "Detail Dataset Failed",
                    "message": str(e)
                }]
            }), 500


    def getDatasetByLink(self, validation_request: GetDatasetByLinkRequestV1):
        try:
            service_response = self.service.getDatasetByLink(validation_request.link)

            final_response = ResponseHelper.create_response_data(service_response)

            return final_response
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Dataset Not Found",
                "data": None,
                "errors": [{
                    "code": "NOT_FOUND",
                    "title": "Dataset Not Found",
                    "message": str(ve)
                }]
            }), 404
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Get Dataset by Link Failed",
                "data": None,
                "errors": [{
                    "code": "DATASET_BY_LINK_ERROR",
                    "title": "Get Dataset by Link Failed",
                    "message": str(e)
                }]
            }), 500


    def searchDataset(self, validation_request: SearchDatasetRequestV1):
        service_response = self.service.searchDataset(validation_request)

        data = service_response['data']
        total_data = service_response.get('total_data')
        has_next = service_response.get('has_next', False)
        is_first = service_response.get('is_first', False)
        is_last = service_response.get('is_last', False)
        current_page = service_response.get('current_page')
        message = service_response.get('message')

        final_response = ResponseHelper.create_response_slice(
            data=data,
            total_data=total_data,
            has_next=has_next,
            is_first=is_first,
            is_last=is_last,
            current_page=current_page,
            message=message
        )

        return final_response

    def getConfusionMatrix(self, validation_request: ConfusionMatrixRequestV1):
        """
        Get Confusion Matrix and Evaluation Metrics

        Endpoint: POST /api/v1/confusion-matrix
        """
        try:
            service_response = self.service.getConfusionMatrix(validation_request)

            # Use json.dumps with sort_keys=False to maintain dict field order
            response_data = {
                "success": True,
                "message": None,
                "data": service_response,
                "errors": None
            }

            json_string = json.dumps(response_data, ensure_ascii=False, sort_keys=False)
            return Response(json_string, mimetype='application/json')
        except FileNotFoundError as fnf:
            return jsonify({
                "success": False,
                "message": "Dataset file not found",
                "data": None,
                "errors": [{
                    "code": "FILE_NOT_FOUND",
                    "title": "Dataset File Not Found",
                    "message": "The merged dataset CSV file could not be found. Please ensure the data has been crawled and merged."
                }]
            }), 404
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Invalid request parameters",
                "data": None,
                "errors": [{
                    "code": "INVALID_PARAMETERS",
                    "title": "Invalid Parameters",
                    "message": str(ve)
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Confusion Matrix calculation failed",
                "data": None,
                "errors": [{
                    "code": "CONFUSION_MATRIX_ERROR",
                    "title": "Confusion Matrix Error",
                    "message": str(e)
                }]
            }), 500


    def getKFoldCrossValidation(self, validation_request: KFoldCrossValidationRequestV1):
        """
        Get K-Fold Cross Validation with k=3 and k=5

        Endpoint: POST /api/v1/k-fold-cross-validation
        """
        try:
            service_response = self.service.getKFoldCrossValidation(validation_request)

            # Use json.dumps with sort_keys=False to maintain dict field order
            response_data = {
                "success": True,
                "message": None,
                "data": service_response,
                "errors": None
            }

            json_string = json.dumps(response_data, ensure_ascii=False, sort_keys=False)
            return Response(json_string, mimetype='application/json')
        except FileNotFoundError as fnf:
            return jsonify({
                "success": False,
                "message": "Dataset file not found",
                "data": None,
                "errors": [{
                    "code": "FILE_NOT_FOUND",
                    "title": "Dataset File Not Found",
                    "message": "The merged dataset CSV file could not be found. Please ensure the data has been crawled and merged."
                }]
            }), 404
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Invalid request parameters",
                "data": None,
                "errors": [{
                    "code": "INVALID_PARAMETERS",
                    "title": "Invalid Parameters",
                    "message": str(ve)
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "K-Fold Cross Validation failed",
                "data": None,
                "errors": [{
                    "code": "K_FOLD_ERROR",
                    "title": "K-Fold Cross Validation Error",
                    "message": str(e)
                }]
            }), 500

    def getEpochEarlyStopping(self, validation_request: EpochEarlyStoppingRequestV1) -> Response:
        """
        Simulate training with Epoch and Early Stopping mechanism

        Endpoint: POST /api/v1/epoch-early-stopping
        """
        try:
            # Call service
            result = self.service.getEpochEarlyStopping(validation_request)

            # Return success response
            return jsonify({
                "success": True,
                "message": None,
                "data": result,
                "errors": None
            })

        except FileNotFoundError as fnfe:
            return jsonify({
                "success": False,
                "message": "Dataset file not found",
                "data": None,
                "errors": [{
                    "code": "FILE_NOT_FOUND",
                    "title": "Dataset File Not Found",
                    "message": str(fnfe)
                }]
            }), 404
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Invalid request parameters",
                "data": None,
                "errors": [{
                    "code": "INVALID_PARAMETERS",
                    "title": "Invalid Parameters",
                    "message": str(ve)
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Epoch training simulation failed",
                "data": None,
                "errors": [{
                    "code": "EPOCH_TRAINING_ERROR",
                    "title": "Epoch Training Error",
                    "message": str(e)
                }]
            }), 500

    def getBatchSize(self, validation_request: BatchSizeRequestV1) -> Response:
        """
        Calculate Batch Size analysis for training optimization

        Endpoint: POST /api/v1/batch-size
        """
        try:
            # Call service
            result = self.service.getBatchSize(validation_request)

            # Return success response
            return jsonify({
                "success": True,
                "message": None,
                "data": result,
                "errors": None
            })

        except FileNotFoundError as fnfe:
            return jsonify({
                "success": False,
                "message": "Dataset file not found",
                "data": None,
                "errors": [{
                    "code": "FILE_NOT_FOUND",
                    "title": "Dataset File Not Found",
                    "message": str(fnfe)
                }]
            }), 404
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Invalid request parameters",
                "data": None,
                "errors": [{
                    "code": "INVALID_PARAMETERS",
                    "title": "Invalid Parameters",
                    "message": str(ve)
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Batch size calculation failed",
                "data": None,
                "errors": [{
                    "code": "BATCH_SIZE_ERROR",
                    "title": "Batch Size Error",
                    "message": str(e)
                }]
            }), 500

    def getOptimizer(self, validation_request: OptimizerRequestV1) -> Response:
        """
        Compare different optimizers (SGD, RMSprop, Adam)

        Endpoint: POST /api/v1/optimizer
        """
        try:
            # Call service
            result = self.service.getOptimizer(validation_request)

            # Return success response
            return jsonify({
                "success": True,
                "message": None,
                "data": result,
                "errors": None
            })

        except FileNotFoundError as fnfe:
            return jsonify({
                "success": False,
                "message": "Dataset file not found",
                "data": None,
                "errors": [{
                    "code": "FILE_NOT_FOUND",
                    "title": "Dataset File Not Found",
                    "message": str(fnfe)
                }]
            }), 404
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Invalid request parameters",
                "data": None,
                "errors": [{
                    "code": "INVALID_PARAMETERS",
                    "title": "Invalid Parameters",
                    "message": str(ve)
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Optimizer comparison failed",
                "data": None,
                "errors": [{
                    "code": "OPTIMIZER_ERROR",
                    "title": "Optimizer Error",
                    "message": str(e)
                }]
            }), 500

    def getEpochTraining(self, validation_request: EpochTrainingRequestV1) -> Response:
        """
        Train model using ALL data without validation split

        This endpoint is for final training after hyperparameter tuning.
        Uses 100% of data for training without validation split.
        """
        try:
            result = self.service.getEpochTraining(validation_request)
            return jsonify({
                "success": True,
                "message": None,
                "data": result,
                "errors": None
            })
        except FileNotFoundError as fnfe:
            return jsonify({
                "success": False,
                "message": "Dataset file not found",
                "data": None,
                "errors": [{
                    "code": "FILE_NOT_FOUND",
                    "title": "Dataset File Not Found",
                    "message": str(fnfe)
                }]
            }), 404
        except ValueError as ve:
            return jsonify({
                "success": False,
                "message": "Invalid request parameters",
                "data": None,
                "errors": [{
                    "code": "INVALID_PARAMETERS",
                    "title": "Invalid Parameters",
                    "message": str(ve)
                }]
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Epoch training failed",
                "data": None,
                "errors": [{
                    "code": "EPOCH_TRAINING_ERROR",
                    "title": "Epoch Training Error",
                    "message": str(e)
                }]
            }), 500
