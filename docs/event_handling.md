### Handling events
Storing events is one thing but we want to deal and do something nice with those events.
Now the event bus comes into play. An event bus receives events and pass them to so called
event listeners that hooked up to do something nice with those events. In this part of the
manual we will explain how to make the magic happen.


##### How event busses reveives events:
(.... here a part how eventbusses get their domain streams)

##### BasicBus for all your basic CQRS needs and event listeners:
ESFramework comes with a basic event where you can attach your own event listeners to.
Attaching is easy as we can see in the code example below:

  ```python
  # instantiate a listener
  event_listener = SimpleEventListener()
  
  # instantiate the BasicBus
  event_bus = BasicBus()
  
  # let the listener listen to the event bus
  event_bus.subscribe(event_listener)
  ```
 
 I hardly can imagine that you'll have the need to unsubscribe but if needed you just can by:
 
  ```python
  # stop listening to the event bus
  event_bus.unsubscribe(event_listener)
  ```
 
BasicBus does nothing more than this and in general I don't expect you need more then this,
however if you are in the situation that you need more then then read on!! If you don't need
more then you can skip the next block.

##### Building your custom event bus:
Building you're own event bus and hook this into ESframework is not hard as long you stick to
the following rules.

1: You have to derive your class from the EventBus class like this 
2: implement the subscribe method for subscribing listeners
3: implement the unsubscribe method for unsubscribing listeners
4: implement the emit method for emitting events

You can take the BasicBus as an example:

  ```python
  class BasicBus(EventBus):
    """ A very simple bus without fancy stuff """

    def __init__(self):
        self.__listeners = []

    def get_event_listeners(self) -> List[EventListener]:
        return self.__listeners

    def subscribe(self, event_listener: EventListener):

        if not isinstance(event_listener, EventListener):
            raise EventBusException("Only classes based on EventListener can subscribe")
        self.__listeners.append(event_listener)

    def unsubscribe(self, event_listener: EventListener):
        if not isinstance(event_listener, EventListener):
            raise EventBusException("Only classes based on EventListener can unsubscribe")
        try:
            self.__listeners.remove(event_listener)
        except ValueError:
            raise EventBusException("Cannot unsubscribe non existing listener from list")

    def emit(self, event_stream: List[DomainEvent]):
        if not isinstance(event_stream, list):
            raise EventBusException("event stream must be a list")

        for domain_event in event_stream:
            if not isinstance(domain_event, DomainEvent):
                raise EventBusException("domain event must be of type DomainEvent")
            for listener in self.__listeners:
                listener.receive(domain_event)
  ```
  
remember: the subscribe, unsubscribe and emit methods have type hints, please respect those!
  
  
##### Creating your own event listeners:
Event listeners are hooked on a event bus listening for incoming events. In theory event 
listeners could live independent. So for example, if your event bus is writing to Apache Kafka
then your listeners will be standalone and communicate with Apache Kafka to fetch the events
from there. If you're using BaseBus (as described above) then you can directly attach your
listeners to the bus process the events in your listener.

Dealing with incoming events is easy when implementing the EventListener class which as default
receive menthod already implemented. The only thing that you have to do is creating so called 
apply methods. You made these apply methods before in the aggregate root.

Below you will find a very simple example:

  ```python
  class MyCustomEventListener(EventListener):
    """ A very simple custom event listener """

    def apply_letter_guessed(self, domain_event: DomainEvent):
    """ simply apply method which matches with the aggregate root"""
        print(domain_event.get_letter())
   ```
   
As you can imagine you can easily make event listeners to connect with any SQL database, 
Mongo, Redis, Elasticsearch. The possibilities are endless.

You could replace the name event listener with the term "Projector" and use "ReadModels" to
create and update the specific technology that you are using. This way you can already improve
your read performance a lot. 