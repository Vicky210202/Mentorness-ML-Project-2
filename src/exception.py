import sys

def error_message_details(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    file = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    message = str(error)
    error_message = f"Warning! Error occured in file ${file}$, in the line number ${line_number}$. error message: {message}."
    
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys): 
        super().__init__(error_message)
        self.error_message = error_message_details(error = error_message, error_detail = error_detail) 

    def __str__(self) -> str:
        return self.error_message    