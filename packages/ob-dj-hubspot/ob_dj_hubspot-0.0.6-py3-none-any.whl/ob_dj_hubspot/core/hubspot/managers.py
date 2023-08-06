import logging
import typing

from celery import current_app
from django.contrib.sites.models import Site
from django.db import models
from hubspot import HubSpot

from ob_dj_hubspot.core.hubspot.signals import (
    company_created,
    contact_created,
    deal_created,
)

logger = logging.getLogger(__name__)


class BaseHSManager(models.Manager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        if "oauth" not in kwargs:
            kwargs["oauth"] = self.get_hs_oauth()
        return super().create(*args, **kwargs)

    def get_hs_oauth(self) -> typing.Any:
        hs_oauth = self.model.oauth.field.related_model
        return hs_oauth.objects.get(site=Site.objects.get_current())


class HSOAuthManager(models.Manager):
    def create(self, **kwargs):
        instance = super().create(**kwargs)
        current_app.send_task(
            "ob_dj_hubspot.core.hubspot.tasks.hs_sync_all_objects_contacts", countdown=5
        )
        return instance


class HSContactManager(BaseHSManager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        instance = super().create(*args, **kwargs)
        contact_created.send(sender=self.__class__, instance=self)
        return instance

    def get_by_object_id(self, object_id: int):
        return self.get(contact_id=object_id)

    def create_by_object_id(self, object_id: int, properties: typing.Dict):
        return self.create(contact_id=object_id, properties=properties)

    def sync(self, contact_id: typing.Text, contact_properties: typing.Dict):
        site = Site.objects.get_current()
        hs = HubSpot(access_token=site.hs_oa.access_token)
        associations = hs.crm.contacts.associations_api.get_all(contact_id, "company")
        self.update_or_create(
            oauth=site.hs_oa,
            contact_id=contact_id,
            defaults={
                "properties": contact_properties,
                "associations": [
                    {"id": i.id, "type": i.type} for i in associations.results
                ],
            },
        )

    def sync_all(self):
        site = Site.objects.get_current()
        hs = HubSpot(access_token=site.hs_oa.access_token)
        for contact in hs.crm.contacts.get_all():
            current_app.send_task(
                "ob_dj_hubspot.core.hubspot.tasks.hs_sync_contact",
                args=(contact.id, contact.properties),
            )


class HSCompanyManager(BaseHSManager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        instance = super().create(*args, **kwargs)
        company_created.send(sender=self.__class__, instance=self)
        return instance

    def get_by_object_id(self, object_id: int):
        return self.get(company_id=object_id)

    def create_by_object_id(self, object_id: int, properties: typing.Dict):
        return self.create(company_id=object_id, properties=properties)

    def sync(self, company_id: typing.Text, company_properties: typing.Dict):
        site = Site.objects.get_current()
        hs = HubSpot(access_token=site.hs_oa.access_token)
        associations = hs.crm.companies.associations_api.get_all(company_id, "contact")
        self.update_or_create(
            oauth=site.hs_oa,
            company_id=company_id,
            defaults={
                "properties": company_properties,
                "associations": [
                    {"id": i.id, "type": i.type} for i in associations.results
                ],
            },
        )

    def sync_all(self):
        site = Site.objects.get_current()
        hs = HubSpot(access_token=site.hs_oa.access_token)
        for company in hs.crm.companies.get_all():
            current_app.send_task(
                "ob_dj_hubspot.core.hubspot.tasks.hs_sync_company",
                args=(company.id, company.properties),
            )


class HSDealManager(BaseHSManager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        instance = super().create(*args, **kwargs)
        deal_created.send(sender=self.__class__, instance=self)
        return instance

    def get_by_object_id(self, object_id: int):
        return self.get(deal_id=object_id)

    def create_by_object_id(self, object_id: int, properties: typing.Dict):
        return self.create(deal_id=object_id, properties=properties)

    def sync(self, deal_id: typing.Text, deal_properties: typing.Dict):
        site = Site.objects.get_current()
        hs = HubSpot(access_token=site.hs_oa.access_token)
        self.update_or_create(
            oauth=site.hs_oa, deal_id=deal_id, defaults={"properties": deal_properties},
        )

    def sync_all(self):
        site = Site.objects.get_current()
        hs = HubSpot(access_token=site.hs_oa.access_token)
        for deal in hs.crm.deals.get_all():
            current_app.send_task(
                "ob_dj_hubspot.core.hubspot.tasks.hs_sync_deal",
                args=(deal.id, deal.properties),
            )
