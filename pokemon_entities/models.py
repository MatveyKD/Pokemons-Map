from django.db import models

class Pokemon(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="pokemon name"
    )
    image = models.ImageField(
        verbose_name="pokemon image",
        default="./media/default.jpg"
    )
    description = models.TextField(
        blank=True,
        verbose_name="pokemon description"
    )
    name_en = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="pokemon name_en"
    )
    name_jp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="pokemon name_jp"
    )

    prev_evolution = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="next_evolutions",
        verbose_name="pokemon previous evolution"
    )

    def __str__(self):
        return self.name

class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="pokemon"
    )
    Lat = models.FloatField(verbose_name="Latitute")
    Lon = models.FloatField(verbose_name="Lontitute")

    appeared_at = models.DateTimeField(
        null=True,
        verbose_name="appeared at"
    )
    disappeared_at = models.DateTimeField(
        null=True,
        verbose_name="disappeared at"
    )

    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="pokemon level"
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="pokemon health"
    )
    attack = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="pokemon attack"
    )
    deffend = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="pokemon defend"
    )
    endurance = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="pokemon endurance"
    )
