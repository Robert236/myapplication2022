from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Applicant(models.Model):
    foto = models.ImageField(upload_to='application_images/')
    anrede = models.CharField(max_length=200, choices=[('Herr', 'Herr'), ('Frau', 'Frau')])
    nachname = models.CharField(max_length=200)
    vorname = models.CharField(max_length=200)
    strasse = models.CharField(max_length=200)
    plz = models.CharField(max_length=200)
    ort = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    handy = models.CharField(max_length=200)
    selbstbeschreibung = models.TextField(max_length=1000)
    besonderes = models.TextField(max_length=1000)
    intension = models.TextField(max_length=1000)

    def __str__(self):
        return self.nachname

    def short_selbstbeschreibung(self):
        rv = self.selbstbeschreibung
        rv = rv[:250]
        return rv

    def short_besonderes(self):
        rv = self.besonderes
        rv = rv[:250]
        return rv

    def short_intension(self):
        rv = self.intension
        rv = rv[:250]
        return rv


class CustomUser(AbstractUser):
    anrede = models.CharField(max_length=200, choices=[('Herr', 'Herr'), ('Frau', 'Frau')])
    unternehmen = models.CharField(max_length=200)
    plz = models.CharField(max_length=200)
    ort = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Messages(models.Model):
    titel = models.CharField(max_length=200)
    nachricht = models.TextField(max_length=1000)
    send_date = models.DateTimeField('gesendet')
    bewerber = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    besucher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titel


class Skills(models.Model):
    bezeichnung = models.CharField(max_length=200)
    beschreibungstext = models.TextField(max_length=1000)
    bewerber = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    def __str__(self):
        return self.bezeichnung


class Applicationpapers(models.Model):
    name = models.CharField(max_length=200)
    bezeichnung = models.CharField(max_length=200, choices=[('Arbeitszeugnis', 'Arbeitszeugnis'),
                                                            ('Schulzeugnis', 'Schulzeugnis'),
                                                            ('Bachelorzeugnis', 'Bachelorzeugnis'),
                                                            ('Praktikumszeugnis', 'Praktikumszeugnis'),
                                                            ('Urkunde', 'Urkunde'), ('IHK_Zeugnis', 'IHK_Zeugnis'),
                                                            ('Lebenslauf', 'Lebenslauf'),
                                                            ('Anschreiben', 'Anschreiben')])
    foto = models.ImageField(upload_to='document_images/')
    dokument = models.FileField(upload_to='application_documents/')
    erstellungsdatum = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    beschreibungstext = models.TextField(max_length=1000)
    bewerber = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Jobs(models.Model):
    name = models.CharField(max_length=200)
    bezeichnung = models.CharField(max_length=200, choices=[('Code', 'Code'),
                                                            ('Dokumentation', 'Dokumentation'),
                                                            ('Bachelorarbeit', 'Bachelorarbeit')])
    dokument = models.FileField(upload_to='application_documents/')
    link = models.URLField(max_length=200)
    beschreibungstext = models.TextField(max_length=1000)
    bewerber = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
