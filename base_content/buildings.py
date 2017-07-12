from oth_core.buildings import *


def get_initial_buildings():
    return [
        BasicBuilding(
            name="Farm",
            description="It's a small farm. It can provide food and shelter for those who work there. It can also provide food for everyone else, although not for free.",
            base_price=50,
            additional_effects={"population_max": 10},
            per_turn_effects={"food": 15, "money": -10}
        ),
        BasicBuilding(
            name="Tenement",
            description="The rooms are small and cramped, half of the windows have been broken for as long as everyone remembers and most of the residents are thieves or drunkards. All in all, not the best place to live - but it's better than sleeping on the street.",
            base_price=200,
            additional_effects={"prestige": -1, "safety": -1, "population_max": 50},
            per_turn_effects={"money": -50}
        ),
        BasicBuilding(
            name="Workshop",
            description="People who work there know how to fix your chair, your pocket watch and your bicycle. If not for people like them, this world would have fallen apart years ago.",
            base_price=100,
            additional_effects={"technology": 2},
            per_turn_effects={"money": -50}
        ),
        BasicBuilding(
            name="Police station",
            description="In a better world, we would be able to avoid conflicts and nobody would want or need to harm other people. Unfortunately, we're not living in that world.",
            base_price=200,
            additional_effects={"safety": 1},
            per_turn_effects={"money": -50}
        ),
        BasicBuilding(
            name="Marketplace",
            description="In its crowded alleys, customers will find what they're looking for, merchants will make profits and pickpockets will find a way to take advantage of everyone else. Money changes hands often, but some of it eventually becomes tax revenue.",
            base_price=500,
            additional_effects={"safety": -1},
            per_turn_effects={"money": 100}
        ),
        BasicBuilding(
            name="Library",
            description="People of your city have donated their books to this library. What books? All of them - as long as it's on paper or parchment and there's something written inside, it belongs here. Of course, this place is completely useless to everyone and the books just sit there, gathering dust. You can only hope that one day your impressive collection of knowledge will catch the eye of some University people.",
            base_price=800,
            additional_effects={"prestige": 1},
            per_turn_effects={"money": -200}
        ),
        BasicBuilding(
            name="Cafe",
            description="An interesting place - it's inexpensive enough for the perpetually unemployed artists to be able to afford it, but also relatively elegant and fashionable so there's no shame in being seen here (even for some of the wealthier citizens).",
            base_price=200,
            additional_effects={"prestige": 2},
            per_turn_effects={"money": 50}
        ),
        BasicBuilding(
            name="Pub",
            description="After an exhausting day of work, what can be better than visiting your local pub for a drink? Spending all your hard-earned money on more drinks, getting into a fight, waking up with a terrible hangover and somehow still having enough endurance to do the same thing the next day.",
            base_price=100,
            additional_effects={"prestige": -1, "safety": -1},
            per_turn_effects={"money": 50}
        ),
        BasicBuilding(
            name="Factory",
            description="You don't know how all those complicated machines work and you're not sure if anyone else knows - but nobody else cares as long as they do their job faster than even the most skilled worker - even if they produce more smoke than even the most nicotine-addicted worker.",
            base_price=500,
            additional_effects={"technology": 3, "health": -2},
            per_turn_effects={"money": -100}
        ),
        BasicBuilding(
            name="Hospital",
            description="Doctors and nurses work day and night to keep people healthy (or at least alive). This is expensive and the equipment required always needs repairs but it's not like you can do anything about it - all the money and technology in the world won't help you if you're dead.",
            base_price=600,
            additional_effects={"health": 3, "technology": -3},
            per_turn_effects={"money": -200}
        )
    ]
