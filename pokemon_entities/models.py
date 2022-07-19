from django.db import models


class Pokemon(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="Имя покемона"
    )
    image = models.ImageField(
        verbose_name="Изображение покемона",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание покемона"
    )
    name_en = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Имя покемона на англ"
    )
    name_jp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Имя покемона на яп"
    )

    prev_evolution = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="next_evolutions",
        verbose_name="Предыдущая эволюция покемона"
    )

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Покемон",
        related_name="entities"
    )
    lat = models.FloatField(verbose_name="Latitute")
    lon = models.FloatField(verbose_name="Lontitute")

    appeared_at = models.DateTimeField(
        null=True,
        verbose_name="Появился в"
    )
    disappeared_at = models.DateTimeField(
        null=True,
        verbose_name="Исчез в"
    )

    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="pokemon level"
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Уровень покемона"
    )
    attack = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Атака покемона"
    )
    defens = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Защита покемона"
    )
    endurance = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Выносливость покемона"
    )
