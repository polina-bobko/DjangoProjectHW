import django_filters

from apps.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    WEEKDAYS = [
        ("sunday", "Sunday"),
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
    ]

    weekday = django_filters.ChoiceFilter(
        choices=WEEKDAYS,
        method="filter_weekday",
    )

    def filter_weekday(self, queryset, name, value):
        weekdays = {
            "sunday": 1,
            "monday": 2,
            "tuesday": 3,
            "wednesday": 4,
            "thursday": 5,
            "friday": 6,
            "saturday": 7,
        }

        return queryset.filter(
            deadline__week_day=weekdays[value]
        )

    class Meta:
        model = Task
        fields = ["status", "deadline", "weekday"]