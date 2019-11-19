from django.db import models

# Create your models here.


class Operator(models.Model):
    name = models.TextField(db_index=True)


class Region(models.Model):
    name = models.TextField(db_index=True)


class Plan(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pfx', 'beg', 'end'], name='plan_unique_constraint')
        ]

    pfx = models.CharField(max_length=3, db_index=True)
    beg = models.CharField(max_length=7, db_index=True)
    end = models.CharField(max_length=7, db_index=True)
    capacity = models.IntegerField(db_index=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)




