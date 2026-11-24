from django.db import models
from apps.common.status import RecordStatus

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TazaNorteModel(TimeStampedModel):
    """
    Modelo base para todas las entidades del sistema TazaNorte.
    Incluye timestamps de auditoría, control de estado con baja lógica
    y restricción portable de base de datos.
    """
    status = models.CharField(
        max_length=8,
        choices=RecordStatus.choices,
        default=RecordStatus.INACTIVE,
    )

    class Meta:
        abstract = True

    @classmethod
    def status_constraint(cls, name):
        return models.CheckConstraint(
            condition=models.Q(status__in=RecordStatus.values),
            name=name,
        )

# Alias retrocompatible para modelos heredados
StoreLabModel = TazaNorteModel
