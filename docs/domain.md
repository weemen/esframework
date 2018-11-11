### Setup Your Domain
This is a step by guide in helping to use this package. Let's start 
with step 1:

##### Step 1: Making a domain model
The very first step of making a proper domain model doesn't start 
with using this package. It actually starts with figuring out how
your domain actually works. There are different techniques in doing
on this. One of these techniques is called EventStorming. 

WIth EventStoring you map out with post-its what your events are, 
what the requirements are to allow this event to happen and in which
order they happen. Of course you have commands which has to be 
converted into events

**Remember:** 
Command names are in present tense (since the event still has to happen)
Event names are always past tense (the event has happened so its 
a fact of life)


##### Step 2: Digitalize a domain model
Now it's time to bring ESframework into action. We model that we made
on post its will now be converted to a digital version.

In the [example folder](../example) folder you can find an example implementation
the steps that we are doing below.

1: Create a folder with the name of your business domain (e.g. hangman). 
 
2: Within this newly created folder you create a folder domain. In the
domain folder we store anything related to the business domain. 
- create a file called events.py.
In this file we will store all events.  
  
  Every event is build up in the same way:
    
  - Classname is in past tense (because it's a fact)
  - Events are immutable (because it's a fact), that's why the members 
  are private and we have getters to access them
  - The serialisation and deserialisation are for storing and retrieving from
  and to the event store
  - Deserialisation is a static method. You reecieve data from the eventstore
  and you use the deserialisation method to reconstruct event.  
    
  ```python
  class GameStarted(DomainEvent):
    """ GamsStarted for aggregate root """
    
    def __init__(self, aggregate_root_id, tries, word):
        self.__aggregate_root_id = aggregate_root_id
        self.__tries = tries
        self.__word = word
        
    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id
    
    def get_tries(self):
        """ Gets tries of this event """
        return self.__tries
    
    def get_word(self):
        """ Gets word of this event """
        return self.__word
        
    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'tries': self.__tries,
            'word': self.__word,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return GameStarted(
            event_data['aggregate_root_id'],
            event_data['tries'],   
            event_data['word'])
  ```
  What you miss in the example above is validation. Normally would validate
  your input in the ```__init__```  function of the event.
  
- Now it's time to create Commands:  
Commands are not are part of the business domain but a part of the application 
that is why we should create new folder called: "application". In this folder
we create file called "commands.py".  
Commands are plain stright forwards objects that will given to the events. 
  
  Commands should IMHO comply to the following rules:  
    
   - Commands are always in present tense. It's a request for a change but this
   change didn't happen yet. The request can be rejected for some reason  
   - We don't to bother anyone in the outside world with complex domain objects
   Other applications shouldn't rely on theme therefor as rule of thumb, only use 
   primitives in your command. Every application understand those.  
     
   ```python
   class StartGame(object):
    """ StartGameCommand """

    __aggregate_root_id = None
    __word = ""
    __tries = 0

    def __init__(self, aggregate_root_id, word: str, tries: int):
        if not aggregate_root_id or not isinstance(aggregate_root_id, str):
            raise CommandException(
                "Cannot construct command: aggregate_root_id is missing!")

        if not word or not isinstance(word, str):
            raise CommandException(
                "Cannot construct command: word is missing!")

        if not tries or not isinstance(tries, int):
            raise CommandException(
                "Cannot construct command: tries is missing!")

        self.__aggregate_root_id = aggregate_root_id
        self.__word = word
        self.__tries = tries

    def get_aggregate_root_id(self):
        return self.__aggregate_root_id

    def get_word(self):
        return self.__word

    def get_tries(self):
        return self.__tries
   ```  
   
   As you can see in the example above I'll keep immutability and I do 
   validation. I created a new folder for exceptions (called: "exceptions").
