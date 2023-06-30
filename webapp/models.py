from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    description = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.name}"

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    description = models.TextField(max_length=2000, blank=True, verbose_name="description")
    category = models.ForeignKey("webapp.Category", on_delete=models.RESTRICT,
                                 verbose_name="Категория",
                                 related_name="products",
                                 null=True
                                 )
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    # image = models.URLField()
    image = models.ImageField(upload_to=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return F"{self.pk}{self.name}{self.category} {self.cost}{self.image}"

    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
