from cachetclient.v1 import enums
from django.core.management.base import BaseCommand

from common.cachet import (
    create_incident,
    CachetException,
    get_incident_name,
    update_incident,
)
from workspaces.occupeye.cache import OccupeyeCache
from workspaces.occupeye.endpoint import TestEndpoint


class Command(BaseCommand):
    help = "Caches all OccupEye data into Redis including historical data"

    def add_arguments(self, parser):
        parser.add_argument("--test", action='store_true')
        parser.add_argument("--mini", action='store_true')

    def handle(self, *args, **options):
        try:
            print("Running OccupEye Caching Operation")
            print("[+] Feeding Cache")
            if options['test']:
                cache = OccupeyeCache(endpoint=TestEndpoint({}))
            else:
                cache = OccupeyeCache()
            cache.feed_cache(full=(not options['mini']))
            print("Done!")
            incident_name = get_incident_name("Occupeye")
            if incident_name:
                try:
                    update_incident("Occupeye Cache succeeded", incident_name, enums.INCIDENT_FIXED)
                except CachetException as cachet_error:
                    print(f"Failed to create fixed cachet incident. " f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    print(f"Unexpected: Failed to create fixed cachet " f"incident. " f"Reason: {repr(cachet_error)}")
            else:
                print("No incident present in Cachet!")
        except Exception as occupeye_error:
            incident_name = get_incident_name("Occupeye")
            if incident_name:
                try:
                    create_incident(
                        str(occupeye_error),
                        incident_name,
                        enums.INCIDENT_INVESTIGATING,
                        enums.COMPONENT_STATUS_MAJOR_OUTAGE,
                    )
                except CachetException as cachet_error:
                    print(f"Failed to create cachet incident. " f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    print(f"Unexpected: Failed to create cachet incident. " f"Reason: {repr(cachet_error)}")
            else:
                print("Could not find appropriate incident in Cachet!")
