from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        return self.annotate(missions_count=models.Count('missions')).order_by('-missions_count', 'phone_number')


class Astronaut(UpdatedAtMixin):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d+$')]
    )
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    objects = AstronautManager()

    def __str__(self):
        return self.name


class Spacecraft(UpdatedAtMixin):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()

    def __str__(self):
        return self.name


class Mission(UpdatedAtMixin):
    PLANNED = 'Planned'
    ONGOING = 'Ongoing'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PLANNED, 'Planned'),
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed')
    ]

    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=PLANNED
    )
    launch_date = models.DateField()
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(
        Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commanded_missions'
    )

    def __str__(self):
        return self.name
