from django.db import models
from django.utils import timezone
from directories.models import Status, Type, Category, Subcategory

class Record(models.Model):
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.date} - {self.amount} руб. ({self.subcategory})"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"