class ErrorHandler:
    def __init__(self, output_path: str) -> None:
        self.output_path = output_path

    def handleError(self, error: BaseException, message: str) -> None:
        report = self._generateReport(error, message)
        self._printReport(report)

    def _generateReport(self, error: BaseException, message: str) -> str:
        return ""
    
    def _printReport(self, report: str) -> None:
        pass
