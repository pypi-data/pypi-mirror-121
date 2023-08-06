from opencensus.ext.azure.log_exporter import AzureLogHandler, create_envelope
from opencensus.ext.azure.common.protocol import (
    Data,
    ExceptionData,
    Message,
)
import traceback


class CustomLogHandler(AzureLogHandler):

    """Handler for logging to Microsoft Azure Monitor."""

    def log_record_to_envelope(self, record):
        envelope = create_envelope(self.options.instrumentation_key, record)

        properties = {}

        if hasattr(record, "custom_dimensions") and isinstance(record.custom_dimensions, dict):
            properties.update(record.custom_dimensions)

        if record.exc_info:
            exctype, _value, tb = record.exc_info
            callstack = []
            level = 0
            has_full_stack = False
            exc_type = "N/A"
            message = self.format(record)
            if tb is not None:
                has_full_stack = True
                for fileName, line, method, _text in traceback.extract_tb(tb):
                    callstack.append(
                        {
                            "level": level,
                            "method": method,
                            "fileName": fileName,
                            "line": line,
                        }
                    )
                    level += 1
                callstack.reverse()
            elif record.message:
                message = record.message

            if exctype is not None:
                exc_type = exctype.__name__

            envelope.name = "Microsoft.ApplicationInsights.Exception"

            data = ExceptionData(
                exceptions=[
                    {
                        "id": 1,
                        "outerId": 0,
                        "typeName": exc_type,
                        "message": message,
                        "hasFullStack": has_full_stack,
                        "parsedStack": callstack,
                    }
                ],
                severityLevel=max(0, record.levelno - 1) // 10,
                properties=properties,
            )
            envelope.data = Data(baseData=data, baseType="ExceptionData")
        else:
            envelope.name = "Microsoft.ApplicationInsights.Message"
            data = Message(
                message=self.format(record),
                severityLevel=max(0, record.levelno - 1) // 10,
                properties=properties,
            )
            envelope.data = Data(baseData=data, baseType="MessageData")
        return envelope
