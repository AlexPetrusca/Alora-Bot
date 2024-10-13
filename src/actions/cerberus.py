from src.actions.combat import CombatAction
from src.actions.prayer import PrayerAction
from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer, Minimap, ArceuusSpellbook, CerberusActionCoord


class CerberusAction(Action):
    def __init__(self):
        super().__init__()
        self.combat_action = CombatAction(health_threshold=50, dodge_hazards=True, flee=False)
        self.prayer_on_action = PrayerAction(Prayer.PROTECT_FROM_MAGIC, Prayer.PIETY)
        self.prayer_off_action = PrayerAction(Prayer.PIETY, Prayer.PROTECT_FROM_MAGIC)

    def first_tick(self):
        self.set_progress_message('Routing to Cerberus...')

    def tick(self, timing):
        # 1. Click 850, 50 + wait to walk
        timing.execute(lambda: robot.click(CerberusActionCoord.WALK1))

        # 2. Click 750, 90 + wait to walk + wait to enter chamber
        timing.execute_after(Timer.sec2tick(7), lambda: robot.click(CerberusActionCoord.WALK2))

        # 3. Click 850, 215 + wait to walk
        timing.execute_after(Timer.sec2tick(14), lambda: robot.click(CerberusActionCoord.WALK3))

        # 4. Enable prayers + spec
        timing.action_after(Timer.sec2tick(2), self.prayer_on_action)
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Minimap.SPECIAL))

        # 5. click magenta contour + wait to start fight
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click_contour(Color.YELLOW))

        # 6. summon thrall
        timing.execute_after(Timer.sec2tick(3), lambda: (
            self.set_progress_message('Fighting Cerberus...'),
            robot.click(ControlPanel.MAGIC_TAB)
        ))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ArceuusSpellbook.RESURRECT_GREATER_SKELETON))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))

        # 7. Wait for fight end + on "Grrrr", click yellow contour + on low health, eat
        timing.wait(Timer.sec2tick(3))
        combat_status = timing.action(self.combat_action)

        if combat_status == ActionStatus.COMPLETE:
            # 8. Disable prayers
            timing.action(self.prayer_off_action)

        # 9. End fight
        return timing.complete_after(Timer.sec2tick(5))

    def last_tick(self):
        pass
