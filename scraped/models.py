import time

from django.db import models
from django.contrib.postgres.fields import ArrayField


class ScrapedObject(models.Model):
    """Base abstract class for all scraped objects."""

    created = models.IntegerField(blank=True, null=True)
    last_scrape_start = models.IntegerField(blank=True, null=True)
    last_scrape_end = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_monitored = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = int(time.time())
        super().save(*args, **kwargs)


class EcommerceStore(ScrapedObject):
    """EcommerceStore object."""

    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    discovery_url = models.URLField(max_length=255, unique=True)
    package_name = models.CharField(max_length=50, blank=True)
    module_name = models.CharField(max_length=50, blank=True)
    class_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class LocalStore(ScrapedObject):
    """LocalStore object."""

    parent_store = models.ForeignKey(
        EcommerceStore,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, unique=True)
    scraped_id = models.IntegerField()
    url = models.URLField(max_length=255, blank=True)
    api_url = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.parent_store.name}: {self.name}'


class Category(ScrapedObject):
    """Category object."""

    parent_store = models.ForeignKey(
        EcommerceStore,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True)
    scraped_id = models.IntegerField(blank=True, null=True)
    api_url = models.URLField(max_length=255, blank=True)
    has_children = models.BooleanField(default=False)
    has_products = models.BooleanField(default=False)
    category_level = models.IntegerField(blank=True, null=True)
    child_products = models.ManyToManyField('Product')
    product_count = models.IntegerField(blank=True, null=True)
    parent_category_id = models.IntegerField(blank=True, null=True)
    child_categories = models.ManyToManyField('self')
    children_category_count = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(ScrapedObject):
    """Product object."""

    parent_store = models.ForeignKey(
        EcommerceStore,
        on_delete=models.CASCADE,
    )
    # TODO:
    # Test this on PSQL
    # parent_categories_ids = ArrayField(
    #     models.IntegerField(), null=True, blank=True
    # )
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True, db_index=True)
    api_url = models.URLField(max_length=255, blank=True)
    scraped_id = models.IntegerField(blank=True, null=True)
    type_id = models.CharField(max_length=100, blank=True)
    short_description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, blank=True)
    ean = models.CharField(max_length=50, blank=True)
    brand_name = models.CharField(max_length=50, blank=True)
    promotion = models.BooleanField(default=False)
    promotion_name = models.CharField(max_length=150, blank=True)

    default_price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2,
    )
    promo_price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2,
    )

    unit_type = models.CharField(max_length=10, blank=True)
    conversion = models.CharField(max_length=10, blank=True)
    conversion_unit = models.CharField(max_length=10, blank=True)
    qty_per_package = models.IntegerField(blank=True, null=True)
    tax_rate = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class ProductLocalStoreData(ScrapedObject):
    """ProductLocalStoreData object."""

    parent_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent_local_store = models.ForeignKey(LocalStore, on_delete=models.CASCADE)
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        null=True)
    stock_status = models.IntegerField(null=True)
    availability = models.CharField(max_length=10, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'parent_product',
                    'parent_local_store',
                    'last_scrape_end'
                ],
                name='Unique ProductLocalData',
            ),
        ]
        verbose_name_plural = 'Product LocalStore Data'

    def __str__(self):
        return f'{self.parent_product.name} in {self.parrent_local_store.name} at {self.last_scrape_end}' # noqa
