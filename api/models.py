from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from simple_history.models import HistoricalRecords


class BasicStructure(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        abstract = True


class Note(BasicStructure):

    CATEGORIES = (
        ('PERSONAL', 'Personal'),
        ('BUSINESS', 'Business'),
        ('IMPORTANT', 'Important')
    )


    title = models.CharField(max_length=500)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, default='PERSONAL')
    history = HistoricalRecords()


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.title)
            slug = slug_base

            if Note.objects.filter(slug=slug).exists():
                slug = f'{slug_base}--{get_random_string(5)}'
            self.slug = slug
        super(Note, self).save(*args, **kwargs)
