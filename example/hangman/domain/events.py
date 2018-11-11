from esframework.domain import DomainEvent


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


class LetterGuessed(DomainEvent):
    """ LetterGuessed for aggregate root """

    def __init__(self, aggregate_root_id, letter):
        self.__aggregate_root_id = aggregate_root_id
        self.__letter = letter

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_letter(self):
        """ Gets letter of this event """
        return self.__letter

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'letter': self.__letter,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return LetterGuessed(
            event_data['aggregate_root_id'],
            event_data['letter'])


class LetterNotGuessed(DomainEvent):
    """ LetterNotGuessed for aggregate root """

    def __init__(self, aggregate_root_id, letter):
        self.__aggregate_root_id = aggregate_root_id
        self.__letter = letter

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_letter(self):
        """ Gets letter of this event """
        return self.__letter

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'letter': self.__letter,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return LetterNotGuessed(
            event_data['aggregate_root_id'],
            event_data['letter'])


class WordGuessed(DomainEvent):
    """ WordGuessed for aggregate root """

    def __init__(self, aggregate_root_id, word):
        self.__aggregate_root_id = aggregate_root_id
        self.__word = word

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_word(self):
        """ Gets word of this event """
        return self.__word

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'word': self.__word,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return WordGuessed(
            event_data['aggregate_root_id'],
            event_data['word'])


class GameWon(DomainEvent):
    """ GameWon for aggregate root """

    def __init__(self, aggregate_root_id):
        self.__aggregate_root_id = aggregate_root_id

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return GameWon(event_data['aggregate_root_id'])


class GameLost(DomainEvent):
    """ GameLost for aggregate root """

    def __init__(self, aggregate_root_id):
        self.__aggregate_root_id = aggregate_root_id

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return GameLost(event_data['aggregate_root_id']),
