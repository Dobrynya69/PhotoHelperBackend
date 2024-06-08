import os

class Utils():
    def serializer_errors_to_string(serializer_errors: dict):
        result_string = ''
        for key in serializer_errors:
            result_string += f'· {key}: {serializer_errors[key][0]}\n'

        return result_string