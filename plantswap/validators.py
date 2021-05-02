from django.core.exceptions import ValidationError

from plantswap_api.utils import today


def validate_date(previous_care_day):
    if previous_care_day > today:
        raise ValidationError("Data ostatniej pielęgnacji nie może być z "
                              "przyszłości")
