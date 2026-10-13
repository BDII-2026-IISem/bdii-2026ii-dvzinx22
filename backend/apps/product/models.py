"""
Catálogo de productos y tipos de producto para la cafetería TazaNorte.
Modelos basados en StoreLabModel con restricciones de integridad relacional.
"""
from decimal import Decimal
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from apps.common.models import StoreLabModel


class ProductType(StoreLabModel):
    """Categoría o tipo de producto en el menú de TazaNorte (ej: Café Caliente, Bebidas, Repostería)."""
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "product_types"
        verbose_name = "tipo de producto"
        verbose_name_plural = "tipos de producto"
        ordering = ["name", "id"]
        constraints = [StoreLabModel.status_constraint("product_types_status_valid")]

    def __str__(self):
        return self.name


class Product(StoreLabModel):
    """Producto comercializado en TazaNorte (ej: Café Espresso, Capuchino, Croissant)."""
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
        related_name="products",
        db_column="product_type_id",
    )
    name = models.CharField(max_length=120, unique=True, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "products"
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["name", "id"]
        constraints = [
            StoreLabModel.status_constraint("products_status_valid"),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="product_price_non_neg",
            ),
        ]

    def __str__(self):
        return self.name
