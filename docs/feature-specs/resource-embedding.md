# Feature Specification Doc
## Supporting Resource Embedding
Support the introduction of resource embedding within the DM API responses, as well as increase usability and clarity of the lib by replacing confusing and convoluted features with better implementations.

### Background Information
On the DM API, there exist _Resources_. A Resource is comprised of both a data structure, and affordances for interacting with said data structure. For example, an API Key resource is one which comprises of the Public Key, Private Key, Name, etc as well as the affiances for retrieving, updating, creating, and deleting the API Key.

Resources may be related to other resources. For both convince and performance, related resources may be embedded where deemed appropriate, (based on use case).

### Resource Structure
Classes in the lib representing API resources will be modified so they are no longer one-to-one copies of the resources being represented as structured on API. Instead, they store the state of the resource internally, and will support methods (dunders included), which will allow for interacting with data stored internally. 

As an aside, a `component.Identity` class is **currently** represented like:

```
class Identity(Component):
	alternate_name = Property(str)
	manufacturer_sku = Property(str)
	name = Property(str)
	source_url = Property(str)
	upc = Property(str)
```
This will change.

#### Maintaining the Resource State
The API sends back JSON to the client (lib, in this case). We want the structure of the classes to be dynamically generated on-the-fly, based on the response from the API.

Please note that using a dictionary was considered for storing the state; the idea was discarded since we want to be able to access attributes using dot notation, i.e.: `product.identity.name`. 

Here is a first pass for a State container:

```
class State(object):
    def __init__(self, name, data=None):
        self.name = name

        if data:
            for key, val in data.iteritems():
                if isinstance(val, dict):
                    val = State(".".join([self.name, key]), val)
                self.__dict__[key] = val

    def __getattr__(self, key):
        raise AttributeError("'%s' object has no attribute '%s'" % (self.name, key))
```

which can be used as the following (minamal example only):

```
class Product(object):
    __state = None

    def __init__(self, conn):
        self.__conn = conn

    def __getattr__(self, key):
        return getattr(self.__state, key)

    def retrieve(self, pk):
        self.__state = State(
            "Product",
            api.retrieve(self.__conn, pk)
        )

    # etc...
```

#### Class methods
For all resources in the lib, the following methods should be defined (even if not supported):

 - **create**
	 - Create a new resource based on the current state of the lib instance.
 - **retrieve**
	 - Retrieve an existing resource, storing the state in the current lib instance.
 - **update**
	 - Update an existing resource based on the current state of the lib instance.
 - **delete**
	 - Delete an existing resource based on the primary key of the current lib instance.
 - **pk**
	 - Grab the primary key value from the current instance.
 - **affordances**
	 - Retrieve a list of all available affordances for the current resource.
 - **refresh**
	 - Perform a retrieve with the current primary key value.
 - **relate**
	 - Relate the current lib instance to a provided lib instance.
 - **unrelate**
 	 - Unrelate the current lib instance to a provided lib instance.
 - **schema**
	 - Retrieve the form schema for the current lib instance.
