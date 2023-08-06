from django.db import models
import datetime
import logging
import time

from django.db import models
from django.utils.text import slugify

logger = logging.getLogger('django-slug-model-mixin')

try:
    from uuslug import uuslug

    USE_UUSLUG = True
except ImportError:
    USE_UUSLUG = False


class SlugModelMixin(models.Model):
    slugged_field = 'title'  # 'title or name or what ever
    slug_unique = True  # 'title or name or what ever
    force_slugify = False

    slug = models.SlugField()  # eliminato unique=True x la questione della preview e del linguaggio...

    class Meta:
        abstract = True
        # unique_together = ('slug',)

    def save(self, *args, **kwargs):
        _slugged_field = getattr(self, self.slugged_field)
        if not self.slug:
            if self.force_slugify:
                if not self.slug_unique:
                    self.slug = slugify(_slugged_field)[:50]
                elif USE_UUSLUG and self.slug_unique:
                    self.slug = uuslug(_slugged_field, instance=self)
                else:
                    slug = slugify(_slugged_field)[:50]
                    if self.id:
                        try:
                            self.__class__._default_manager.exclude(id=self.id).get(slug=slug)
                        except self.__class__.DoesNotExist:
                            self.slug = slug
                        else:
                            slug_id = '%s-%d' % (slug[:35], self.id)
                            try:
                                self.__class__._default_manager.exclude(id=self.id).get(slug=slug_id)
                            except self.__class__.DoesNotExist:
                                self.slug = slug_id
                            else:
                                # NOTE: non posso basarmi sull'id poichè non rispetta il requisito di univocità.
                                n = datetime.datetime.now()
                                t = int(time.mktime(n.timetuple()))
                                slug_ts = '%s-%d' % (slug[:35], t)
                                self.slug = slug_ts
                    else:
                        try:
                            self.__class__._default_manager.get(slug=slug)
                        except self.__class__.DoesNotExist:
                            self.slug = slug
                        else:
                            # NOTE: non posso basarmi sull'id poichè non è stato ancora generato.
                            n = datetime.datetime.now()
                            t = int(time.mktime(n.timetuple()))
                            slug_ts = '%s-%d' % (slug[:35], t)
                            self.slug = slug_ts
        else:
            if self.slug_unique:
                if self.slug and self.slug_unique:
                    slug = self.slug
                    if self.id:
                        try:
                            self.__class__._default_manager.exclude(id=self.id).get(slug=slug)
                        except self.__class__.DoesNotExist:
                            self.slug = slug
                        else:
                            slug_id = '%s-%d' % (slug[:35], self.id)
                            try:
                                self.__class__._default_manager.exclude(id=self.id).get(slug=slug_id)
                            except self.__class__.DoesNotExist:
                                self.slug = slug_id
                            else:
                                # NOTE: non posso basarmi sull'id poichè non rispetta il requisito di univocità.
                                n = datetime.datetime.now()
                                t = int(time.mktime(n.timetuple()))
                                slug_ts = '%s-%d' % (slug[:35], t)
                                self.slug = slug_ts
                    else:
                        try:
                            self.__class__._default_manager.get(slug=slug)
                        except self.__class__.DoesNotExist:
                            self.slug = slug
                        else:
                            # NOTE: non posso basarmi sull'id poichè non è stato ancora generato.
                            n = datetime.datetime.now()
                            t = int(time.mktime(n.timetuple()))
                            slug_ts = '%s-%d' % (slug[:35], t)
                            self.slug = slug_ts
        super(SlugModelMixin, self).save(*args, **kwargs)
