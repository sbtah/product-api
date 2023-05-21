import time

from django.db import models


class ScrapedObject(models.Model):
    '''Base abstract class for all scraped objects.'''

    created = models.IntegerField(blank=True, null=True)
    last_scrape_start = models.IntegerField(blank=True, null=True)
    last_scrape_end = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)
