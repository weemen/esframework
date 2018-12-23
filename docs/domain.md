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
        
        super().__init__()
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
   Note: ```super().__init__()``` is needed to set all the instances variable
   to the right default value. I'm working on a fix for this!
   
 - As in a proper eventstorming session it's now time to implement all the
 requirements that are needed to turn commands into events. It's time to
 create the aggregate root. In the domain folder we will create a file called
 "aggregate.py"  
   
   Aggregates are the glue between command and events. Aggregates has the
   current state which is the summation of all events. In esframework aggregates
   are build up in this way:
   - a static method that creates an instance of the object
   - a method foreach command to check if we can turn this command into an event
   - a method for event that affects the aggregate root (the apply_ methods).  
     
   Every aggregate root should comply to the following rules:
   - members are private
   - apply_ methods must be based on the event names. The classname of the event
   will be translated from CamelCase to underscores!! Please keep this in mind
   during development.
   - apply methods are meant changing the aggregate root
   - non apply methods are meant for Commands to check if we can turn them into
   events.
     
   
   ```python
   class Game(AggregateRoot):
    """ Game is an aggregate root """
    __aggregate_root_id = None
    __active_game = False
    __tries = 0
    __word = ""
    __letters_guessed = []
    __letters_not_guessed = []
    __word_guessed = ""

    @staticmethod
    def start_game(command: StartGame):
        """ Creates Game and will try to apply GameStarted """
        game = Game()
        game.apply(GameStarted(
            aggregate_root_id=command.get_aggregate_root_id(),
            tries=command.get_tries(),
            word=command.get_word()
        ))

        return game

    def apply_game_started(self, event: GameStarted):
        """ Apply GameStarted on the aggregate root, reset the complete game"""
        self.__aggregate_root_id = event.get_aggregate_root_id()
        self.__active_game = True
        self.__tries = event.get_tries()
        self.__word = event.get_word()
        self.__letters_guessed = []
        self.__letters_not_guessed = []
        self.__word_guessed = ""

    def guess_letter(self, command: GuessLetter):
        """ Try to apply LetterGuessed or LetterNotGuessed """
        self.basic_game_preconditions()

        """ Apply either one the two events """
        if command.get_letter() in list(self.__word):
            self.apply_letter_guessed(
                LetterGuessed(
                    command.get_aggregate_root_id(),
                    command.get_letter()
                )
            )
        else:
            self.apply_letter_not_guessed(
                LetterNotGuessed(
                    command.get_aggregate_root_id(),
                    command.get_letter()
                )
            )

    def apply_letter_guessed(self, event: LetterGuessed):
        """ Apply LetterGuessed on the aggregate root """
        self.__letters_guessed.append(event.get_letter())

        if len(set(self.__word)) == len(set(self.__letters_guessed)):
            self.__active_game = False

    def apply_letter_not_guessed(self, event: LetterNotGuessed):
        """ Apply LetterNotGuessed on the aggregate root """
        self.__letters_not_guessed.append(event.get_letter())
        self.__tries -= 1
   ```
   
   In the example above is not the full aggregate root, check that one out
   in the [example folder](../example). Aggregate roots always extends from
   the [AggregateRoot](../esframework/domain/__init__.py) class. This class
   helps you with processing uncommitted events and apply events when loaded
   from the event store. I would be a shame if you have to worry about those
   things.

##### Step 3: Testing the model
Off course we can't do this untested but you might think: how are we going to
test this? Well luckily there is a little bit of tooling for that. Let's check
it out. Next to your domain folder create a folder called "tests". In this
folder we create a folder "domain". In that folder we add a test file.

A good thing that I have been taught to do is to start every test case with: 
"test_it_can_" and then the case you want to test. This is something you will
see in the example below as well. The other thing that you might notice is that
the test class is extended from 
[AggregateRootTestCase](../esframework/tooling/aggregate.py). This class deals
for you with all the private members to make testing easy. You can easily build
test scenario's without too many worries. 

```python
class GameTest(AggregateRootTestCase):

    def test_it_can_start_a_game(self):
        game_start_command = StartGame(
            '297F2CE9-CB4F-4BE2-8C86-21B911FC2663',
            'birthday',
            9
        )

        aggregate = Game.start_game(game_start_command)
        self.withAggregate(aggregate)\
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', True)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")

    def test_it_can_guess_a_letter(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'

        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 9))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'r'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', True)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', ['r'])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")
```

As you can see above, testing is fairly easy. Create your aggregate, create
your commands and execute :). You can see clearly how the AggregateRootTestCase
helps you here. Assign the aggregate with the "withAggregate" method ()which is 
fluid) and the next step is to assert the aggregate state.
