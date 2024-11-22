from django.db import models

# Modelo para Respondent
class Respondent(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Modelo para PersonalityFactors
class PersonalityFactors(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    A = models.FloatField(null=True, blank=True)
    B = models.FloatField(null=True, blank=True)
    C = models.FloatField(null=True, blank=True)
    E = models.FloatField(null=True, blank=True)
    F = models.FloatField(null=True, blank=True)
    G = models.FloatField(null=True, blank=True)
    H = models.FloatField(null=True, blank=True)
    I = models.FloatField(null=True, blank=True)
    L = models.FloatField(null=True, blank=True)
    M = models.FloatField(null=True, blank=True)
    N = models.FloatField(null=True, blank=True)
    O = models.FloatField(null=True, blank=True)
    Q1 = models.FloatField(null=True, blank=True)
    Q2 = models.FloatField(null=True, blank=True)
    Q3 = models.FloatField(null=True, blank=True)
    Q4 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Personality Factors({self.respondent.name})"

# Modelo para Categorization
class Categorization(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    An = models.FloatField(null=True, blank=True)
    Ex = models.FloatField(null=True, blank=True)
    So = models.FloatField(null=True, blank=True)
    In = models.FloatField(null=True, blank=True)
    Ob = models.FloatField(null=True, blank=True)
    Cr = models.FloatField(null=True, blank=True)
    Ne = models.FloatField(null=True, blank=True)
    Ps = models.FloatField(null=True, blank=True)
    Li = models.FloatField(null=True, blank=True)
    Ac = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Categorization({self.respondent.name})"
