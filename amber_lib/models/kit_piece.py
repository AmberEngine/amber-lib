from amber_lib import client
from amber_lib.models import components
from amber_lib.models.bases import Model, Property, resource
from amber_lib.models.primaries import Assemblage

@resource('kit_pieces')
class KitPiece(Model):
    id = Property(int)
    assemblage = Property(Assemblage)
    identity = Property(components.Identity)
    collection = Property(components.Collection)
    description = Property(components.Description)
    images = Property(components.Images)
    manufacturer = Property(components.Manufacturer)
    pricing = Property(components.Pricing)
    overall_dimension = Property(components.OverallDimension)

    def get_components(self):
        return {
            key: val for key, val in self.__dict__.items()
            if key != 'id' and not key.startswith('_')
        }

    def form_schema(self):
        endpoint = '/form_schemas/%s' % self._resource
        return client.send(
            client.GET,
            self.ctx(),
            endpoint,
            {}
        )

    def search(self, filtering=None, batch_size=500, offset=0, **kwargs):
        payload = client.send(
            client.GET,
            self._ctx,
            '/kit_pieces_search',
            {'filtering': filtering.to_dict()} if filtering else None,
            limit=batch_size,
            offset=offset,
            **kwargs
        )

        collection = client.Container(
            payload,
            self.__class__,
            self._ctx,
            offset
        )

        return collection
