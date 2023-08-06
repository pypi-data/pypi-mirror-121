import os
import json
import sys
import logging

from opencensus.trace.samplers import ProbabilitySampler

from custom_log_handler import CustomLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer
from opencensus.trace import config_integration
from opencensus.trace import attributes_helper

from server_constants import MAX_LOG_SIZE_IN_BYTES

HTTP_METHOD = attributes_helper.COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_URL = attributes_helper.COMMON_ATTRIBUTES["HTTP_URL"]
HTTP_STATUS_CODE = attributes_helper.COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]
HTTP_ROUTE = attributes_helper.COMMON_ATTRIBUTES['HTTP_ROUTE']


class AppInsightsClient(object):
    def __init__(self):
        self.enabled = False
        self._model_ids = self._get_model_ids()

        if os.getenv("AML_APP_INSIGHTS_ENABLED") == "true" and "AML_APP_INSIGHTS_KEY" in os.environ:
            try:
                instrumentation_key = os.getenv("AML_APP_INSIGHTS_KEY")
                self.logger = logging.getLogger(__name__)
                self.logger.addHandler(CustomLogHandler(instrumentation_key=instrumentation_key))
                self.tracer = Tracer(
                    exporter=AzureExporter(instrumentation_key=instrumentation_key), sampler=ProbabilitySampler(1.0)
                )
                self._container_id = os.getenv("HOSTNAME", "Unknown")
                self.enabled = True
            except ValueError as ex:
                print(f"Error logging to Application Insights: {ex}")
            except KeyError as ex:
                print(f"Error logging to Application Insights: {ex}")
        self.mdc_enabled = os.getenv("AML_MODEL_DC_STORAGE_ENABLED") == "true"

    def send_model_data_log(self, request_id, model_input, prediction):
        if not self.enabled or not self.mdc_enabled:
            return
        properties = {
            "custom_dimensions": {
                "Container Id": self._container_id,
                "Request Id": request_id,
                "Workspace Name": os.environ.get("WORKSPACE_NAME", ""),
                "Service Name": os.environ.get("SERVICE_NAME", ""),
                "Models": self._model_ids,
                "Input": json.dumps(model_input),
                "Prediction": json.dumps(prediction),
            }
        }
        if self._is_message_size_below_threshold(properties):
            self.logger.warning("model_data_collection", extra=properties)
        else:
            print(f"Logging error: AppInsights message data limit reached.")

    def send_request_log(
        self, request_id, response_value, name, url, success, start_time, end_time, response_code, http_method
    ):
        config_integration.trace_integrations(["requests"]) # <-- uses opencensus-ext-requests package for requests integration
        try:
            if not self.enabled:
                return
            with self.tracer.span(name=name) as span:
                span.name = name
                span.span_kind = SpanKind.SERVER  # <-- Sends the log to the requests table
                span.span_id = request_id
                span.start_time = start_time
                span.end_time = end_time
                if not isinstance(response_value, str):
                    response_value = response_value.decode("utf-8")
                span.attributes = {
                    HTTP_ROUTE: name, # <-- middleware_appinsights sends request_path as name
                    HTTP_METHOD: http_method,
                    HTTP_STATUS_CODE: int(response_code),
                    HTTP_URL: url,
                    "Response Value": json.dumps(response_value),
                    "Container Id": self._container_id,
                }
                span.status.code = success
        except Exception as ex:
            print(f"Error logging to Application Insights: {ex}")

    def send_exception_log(self, exc_info, request_id="Unknown"):
        try:
            if not self.enabled:
                return
            properties_dict = {
                "Container Id": self._container_id,
                "Request Id": request_id,
            }
            self.logger.exception(exc_info, extra=properties_dict)
        except Exception as ex:
            print(f"Error logging to Application Insights: {ex}")

    def _get_model_ids(self):
        model_ids = []
        models_root_dir = os.path.join(os.environ.get("AML_APP_ROOT", "/var/azureml-app"), "azureml-models")
        try:
            models = [str(model) for model in os.listdir(models_root_dir)]

            for model in models:
                versions = [int(version) for version in os.listdir(os.path.join(models_root_dir, model))]
                ids = ["{}:{}".format(model, version) for version in versions]
                model_ids.extend(ids)
        except:
            self.send_exception_log(sys.exc_info())

        return model_ids

    """
    Verify if message size is less than 8kb for proper emition to AppInsights
    MAX_LOG_SIZE is 8MB for ApplicationInsights
    """

    def _is_message_size_below_threshold(self, message):
        return sys.getsizeof(message) < MAX_LOG_SIZE_IN_BYTES
