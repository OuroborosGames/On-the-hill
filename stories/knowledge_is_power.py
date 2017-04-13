import oth_core.text_events
import oth_core.buildings

story_main = oth_core.text_events.BasicEvent(
    name = "Knowledge is Power",
    description =
    """The world around us is crumbling and yet we still prosper. Our workshops
and factories are kept alive by skilled workers, and their knowledge
will not be forgotten as the guilds they formed make sure that there
will be a new generation to keep repairing the city after they're dead.

There is, of course, a problem: the city needs the guilds and the guilds
know that the city needs them. Yesterday they were workers and today
they're the silent elite. Who knows what will happen tomorrow?""",
#todo create events for the rest of the story and spawn them in the lambda below
    actions = {'OK': lambda state: None}
)