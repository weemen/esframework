### Dealing with versioning of events
Greg Young wrote already a whole [book](https://leanpub.com/esversioning/read) about it, 
versioning of events. ESframework has support to version events with the "weak-schema" method. 
I'll explain what this means and how you should implement this in a few minutes but let's 
go to the why first.

#### Why this is a big deal: 
Imagine that we've got event store full of events and we have 10 consumers listening to 
those events. Now imagine that we will update event A to a newer version. It get will get
an extra property. This is not uncommon over time, systems might grow and evolve over time.
Aggregates have to be reconstructed and in ESframework this will happen during deserialisation
of the raw message like this:

```python
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(event_data['aggregate_root_id'])
```

Now imagine that the following event:

```python
class EventA(DomainEvent):
    """ Dummy EventA class for testing """
    __aggregate_root_id = None

    def __init__(self, aggregate_root_id):
    
        if not aggregate_root_id or not isinstance(aggregate_root_id, str):
            raise DomainEventException("Aggregate_root_id is missing for event")
            
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(event_data['aggregate_root_id'])

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id
        }
```

changes into: 

```python

class EventA(DomainEvent):
    """ Dummy EventA class for testing """
    __aggregate_root_id = None
    __an_event_property = 'some default value'

    def __init__(self, aggregate_root_id, an_event_property):
        super().__init__()
        
        if not aggregate_root_id or not isinstance(aggregate_root_id, str):
            raise DomainEventException("Aggregate_root_id is missing for event")

        if not an_event_property or not isinstance(an_event_property, str):
            raise DomainEventException("an_event_property is missing for event")

        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_an_event_property(self):
        """ Gets an_event_property of this event """
        return self.__an_event_property

    @staticmethod
    @event_versioning('weak-schema')
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(
            event_data['aggregate_root_id'],
            event_data['an_event_property'])

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'an_event_property': self.__an_event_property,
        }
```

To instantiate the newest version of EventA requires now 2 properties instead of one. Creating new
messages is most likely not a problem but if you load an aggregate before this version update then
you will get errors during deserialisation. This is just one simple example but there are probably
more situations where we see this problem.

You might wonder: why don't we just upcast events in such situation? The reason is very simple.
Events are meant to be immutable at all costs, if events can change then you never know for sure
if your system is trustworthy. The other thing is and let's face it, upcasting is a hassle, a 
risky job and what if you found out after three months that you missed something what else is wrong
then? Enough reasons not to modify ever again as soon as they are applied and more important there
are better solutions to deal with this problem.


#### Weak-Schema mapping to the rescue:
The easiest way to deal with this problem is mapping and traversing from version to version. Mapping
comes into two flavors: Weak-Schema and the other one Hybrid-Schema. For now only Weak-Schema is
implemented. I'm looking in on Hybrid-Schema and traversing from version to version. Weak-Schema
boils down to this:

If the serialized body has more data then event class requires:  
Keep the data it was needed in the past no reason to delete it.
(This typically would happen if you a new message and would go to an old version)

If serialized body has less data then the event requires:  
Use the default values from the event class to instantiate the object.
(This typically would happen if you have an old message with an updated event, as described in
the previous chapter)

In any case, the serialized body is always leading and will overwrite the default values of the
event class. This way we always deal with version updates but there is a golden rule for success

> You're never allowed to rename an property within an Event

### How to implement versioning of my events in ESframework
To implement weak-schema versioning into your application you have to do two things:
  
1: (the hardest part) Set default values as class properties
```python
class EventA(DomainEvent):
    """ Dummy EventA class for testing """
    __aggregate_root_id = None
    __an_event_property = 'some default value'

    def __init__(self, aggregate_root_id, an_event_property):
        ...
```
2: Set the event_versioning annotation on the deserialisation method:
```python
class EventA(DomainEvent):
    
    ...
    
    @staticmethod
    @event_versioning('weak-schema')
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(
            event_data['aggregate_root_id'],
            event_data['an_event_property'])
```

That's it, easy right, no upcasting needed and this works two ways.
