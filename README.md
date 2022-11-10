# audiostack-python
prototype for python SDK for audiostack



## Response types

Our API supports the following HTTP protocools.

POST:
    creates a new resource, in the SDK this returns an `item` of type resource (i.e. `script`)

PUT
    updates a new resource, in the SDK this returns an updated `item` of type resource (i.e. `script`)

GET:
    Gets an existing resource, in the SDK this returns an  `item` of type resource (i.e. `script`), **or** a `list` of `items`

DELETE
    Deletes a resource, in the SDK this does not return any object

