import re
from django.core.exceptions import ValidationError

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        """
        Enforces password complexity:
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one digit
        - At least one special character
        """
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
        if not re.search(pattern, password):
            raise ValidationError(
                "Password must include uppercase, lowercase, digit, and special character.",
                code='password_no_complexity'
            )

    def get_help_text(self):
        return (
            "Your password must include at least one uppercase letter, one lowercase letter, "
            "one number, and one special character (@$!%*?&)."
        )
