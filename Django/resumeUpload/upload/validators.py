import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    valid_extensions = ['.pdf', '.docx']
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(valid_extensions)}')