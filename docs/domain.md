### Setup Your Domain
This is a step by guide in helping to use this package. Let's start 
with step 1:

##### Making a domain model
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


##### Digitalize a domain model
Now it's time to bring ESframework into action. We model that we made
on post its will now be converted to a digital version.
