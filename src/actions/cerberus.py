from src.actions.combat import CombatAction
from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer, Minimap, ArceuusSpellbook, CerberusActionCoord


class CerberusAction(Action):
    def __init__(self):
        super().__init__()
        self.tile_color = Color.MAGENTA
        self.last_chat = None
        self.retry_count = 0

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
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.PRAYER_TAB))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Prayer.PROTECT_FROM_MAGIC))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Prayer.PIETY))

        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Minimap.SPECIAL))

        # 5. click magenta contour + wait to start fight
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click_contour(self.tile_color))

        # 6. summon thrall
        timing.execute_after(Timer.sec2tick(3), lambda: (
            self.set_progress_message('Fighting Cerberus...'),
            robot.click(ControlPanel.MAGIC_TAB)
        ))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ArceuusSpellbook.RESURRECT_GREATER_SKELETON))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))

        # todo: can we replace this with a CombatAction?
        # 7. Wait for fight end + on "Grrrr", click yellow contour + on low health, eat
        timing.wait(Timer.sec2tick(3))
        combat_status = timing.poll(Timer.sec2tick(1), self.poll_combat)
        if combat_status is not CombatAction.Event.FIGHT_OVER:
            timing.interval(Timer.sec2tick(0.5), self.poll_cerberus_special, ignore_scheduling=True)

        # 8. Disable prayers
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.PRAYER_TAB))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Prayer.PROTECT_FROM_MAGIC))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Prayer.PIETY))

        # 9. End fight
        return timing.complete_after(Timer.sec2tick(5))

    def poll_combat(self):
        damage_ui = vision.read_damage_ui()
        if damage_ui.startswith('0/'):
            return CombatAction.Event.FIGHT_OVER
        elif damage_ui.find("/") == -1:  # "/" not found
            print("DAMAGE_UI not found:", damage_ui)
            self.retry_count += 1
            if self.retry_count >= 3:
                return CombatAction.Event.FIGHT_OVER
        else:
            self.retry_count = 0

        if vision.read_hitpoints() <= 30:
            robot.click_food()

    def poll_cerberus_special(self):
        chat = vision.read_latest_chat()
        if chat.find("Cerberus: Gr") != -1 and chat != self.last_chat:
            self.tile_color = Color.YELLOW if self.tile_color == Color.MAGENTA else Color.MAGENTA
            robot.click_contour(self.tile_color)
            robot.press(['Enter', 'h', 'a', 'h', 'a', 'Enter'])
        self.last_chat = chat

    def last_tick(self):
        self.tile_color = Color.MAGENTA
        self.last_chat = None
        self.retry_count = 0
