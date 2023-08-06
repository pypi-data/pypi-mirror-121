
"""
This module is use to hadle custom errors needed for AWS Batch.
Logger module is added to manage logs as well
"""
from YOMLogger import YOMLogger

class YOMError(Exception):
    """
    Args: 
        message: the message to display
    """
    def __init__(self, message) -> None:
        self.message = message
        self.logger = YOMLogger('YOM-PIP-ERRORS')
        self.logger.error(message)
        super().__init__(message)
