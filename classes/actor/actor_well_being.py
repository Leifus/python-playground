
from classes.actor.well_beling_hydration import WellBeingHydration
from classes.actor.well_beling_sustenance import WellBeingSustenance
from classes.enums.well_being_body_state_enum import WellBeingBodyStateEnum

class ActorWellBeing():
    def __init__(self, birth_date):
        self.body_state = WellBeingBodyStateEnum.Alive
        self.sustenance = WellBeingSustenance()
        self.hydration = WellBeingHydration()
        self.birth_date = birth_date
        self.age = 0

    def on_atrophy(self, time_lapsed):
        if self.body_state not in WellBeingBodyStateEnum.Alive | WellBeingBodyStateEnum.Wounded:
            return
        
        self.age += time_lapsed
        
        if self.sustenance.hunger_rate > 0.0:
            self.sustenance.hunger += 1.0 * self.sustenance.hunger_rate
        if self.hydration.thirst_rate > 0.0:
            self.hydration.thirst += 1.0 * self.hydration.thirst_rate

    def update(self, time_lapsed):
        self.on_atrophy(time_lapsed)