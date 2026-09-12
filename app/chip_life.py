# app/chip_life.py
#
# CHIP'S LIFE ENGINE
# Gives Chip an autonomous-feeling personality and state.
#
# This file does NOT touch files.
# It only decides what Chip feels like doing.

from enum import Enum
import random
import time


class ChipState(Enum):
    IDLE = "idle"
    LOOKING_AROUND = "looking_around"
    CURIOUS = "curious"
    INVESTIGATING = "investigating"
    WATCHED = "watched"
    FROZEN = "frozen"
    STEALING = "stealing"
    ESCAPING = "escaping"
    BURROWING = "burrowing"
    CELEBRATING = "celebrating"


class ChipLife:
    """
    Autonomous personality/life controller for Chip.

    This class deliberately does NOT perform file operations.
    main.py remains responsible for actual safe sandbox theft.
    """

    def __init__(self, squirrel_state=None):
        self.squirrel_state = squirrel_state

        self.state = ChipState.IDLE
        self.previous_state = ChipState.IDLE

        # Personality
        self.mood = "curious"
        self.energy = random.randint(65, 90)

        # Small pieces of internal state
        self.curiosity = random.randint(35, 60)
        self.alertness = random.randint(20, 45)

        self.current_thought = "Humans have too many files."
        self.last_action = "sitting"

        self.state_started = time.monotonic()
        self.next_idle_action = self._random_idle_delay()

        # Used to make behaviour less predictable
        self.actions_since_interaction = 0

    # ---------------------------------------------------------
    # STATE MANAGEMENT
    # ---------------------------------------------------------

    def set_state(self, new_state, thought=None):
        """Change Chip's current state."""

        if new_state != self.state:
            self.previous_state = self.state
            self.state = new_state
            self.state_started = time.monotonic()

        if thought:
            self.current_thought = thought

    def state_duration(self):
        """How long Chip has been in the current state."""

        return time.monotonic() - self.state_started

    # ---------------------------------------------------------
    # RANDOM IDLE BEHAVIOUR
    # ---------------------------------------------------------

    def _random_idle_delay(self):
        return random.uniform(2.0, 6.5)

    def choose_idle_action(self):
        """
        Pick something Chip wants to do while nothing important
        is happening.

        The probabilities intentionally aren't perfectly balanced.
        We want Chip to feel slightly unpredictable.
        """

        actions = [
            "look",
            "scratch",
            "sniff",
            "tail",
            "walk",
            "sit",
            "yawn",
            "stare",
            "inspect_burrow",
        ]

        weights = [
            20,   # look
            11,   # scratch
            12,   # sniff
            7,    # tail
            13,   # walk
            15,   # sit
            5,    # yawn
            10,   # stare
            7,    # inspect burrow
        ]

        return random.choices(actions, weights=weights, k=1)[0]

    def perform_idle_action(self):
        """Choose and perform a virtual idle action."""

        action = self.choose_idle_action()
        self.last_action = action
        self.actions_since_interaction += 1

        thoughts = {
            "look": [
                "What's happening over there?",
                "I heard something.",
                "Hmm...",
                "Is that food?",
            ],

            "scratch": [
                "Important squirrel maintenance.",
                "Being adorable is hard work.",
                "One moment.",
            ],

            "sniff": [
                "Sniff sniff...",
                "Something smells interesting.",
                "Definitely suspicious.",
            ],

            "tail": [
                "My tail is magnificent.",
                "Just checking the merchandise.",
            ],

            "walk": [
                "I should investigate.",
                "Perhaps there is treasure nearby.",
                "Patrolling my territory.",
            ],

            "sit": [
                "I shall do absolutely nothing.",
                "Resting.",
                "Strategic inactivity.",
            ],

            "yawn": [
                "Humans work too much.",
                "I need a nap.",
                "Being a squirrel is exhausting.",
            ],

            "stare": [
                "I'm watching you.",
                "You didn't see anything.",
                "Interesting human...",
            ],

            "inspect_burrow": [
                "Checking my collection.",
                "Everything is where I left it.",
                "My treasures...",
            ],
        }

        self.current_thought = random.choice(thoughts[action])

        # Map the virtual action to a life state.
        if action == "look":
            self.set_state(
                ChipState.LOOKING_AROUND,
                self.current_thought
            )

        elif action == "stare":
            self.set_state(
                ChipState.LOOKING_AROUND,
                self.current_thought
            )

        elif action == "walk":
            self.set_state(
                ChipState.LOOKING_AROUND,
                self.current_thought
            )

        elif action == "inspect_burrow":
            self.set_state(
                ChipState.LOOKING_AROUND,
                self.current_thought
            )

        else:
            self.set_state(
                ChipState.IDLE,
                self.current_thought
            )

        self.next_idle_action = (
            time.monotonic() + self._random_idle_delay()
        )

        return action

    # ---------------------------------------------------------
    # MAIN LIFE UPDATE
    # ---------------------------------------------------------

    def update(self):
        """
        Call this repeatedly from the GUI/event loop.

        It never sleeps and never blocks the application.
        """

        now = time.monotonic()

        # If Chip has been doing something for a little while,
        # return naturally to idle.
        if self.state in (
            ChipState.LOOKING_AROUND,
            ChipState.CURIOUS,
        ):
            if now - self.state_started > random.uniform(0.8, 2.2):
                self.set_state(ChipState.IDLE)

        # Autonomous idle behaviour
        if (
            self.state == ChipState.IDLE
            and now >= self.next_idle_action
        ):
            self.perform_idle_action()

        # Slowly change his energy
        if random.random() < 0.015:
            self.energy += random.choice([-2, -1, 1, 2])
            self.energy = max(20, min(100, self.energy))

        return self.state

    # ---------------------------------------------------------
    # FILE DETECTED
    # ---------------------------------------------------------

    def notice_file(self, filename=None):
        """Chip notices that something new appeared."""

        self.curiosity = min(
            100,
            self.curiosity + random.randint(8, 18)
        )

        self.alertness = min(
            100,
            self.alertness + random.randint(5, 12)
        )

        self.last_action = "noticed_file"

        if filename:
            thoughts = [
                f"What is {filename}?",
                f"That {filename} looks interesting...",
                f"I wonder what's inside {filename}.",
                f"Suspicious... {filename}.",
                "Something appeared.",
            ]

            thought = random.choice(thoughts)
        else:
            thought = "Something appeared..."

        self.set_state(
            ChipState.CURIOUS,
            thought
        )

        self.actions_since_interaction = 0

    # ---------------------------------------------------------
    # INVESTIGATION
    # ---------------------------------------------------------

    def start_investigation(self, thought=None):
        self.last_action = "investigating"

        self.curiosity = min(
            100,
            self.curiosity + random.randint(5, 12)
        )

        self.set_state(
            ChipState.INVESTIGATING,
            thought or "I need to investigate this."
        )

    # ---------------------------------------------------------
    # CAMERA / HUMAN
    # ---------------------------------------------------------

    def human_is_watching(self):
        """
        Chip knows the human is watching him.
        """

        self.alertness = min(
            100,
            self.alertness + random.randint(3, 8)
        )

        self.set_state(
            ChipState.FROZEN,
            random.choice([
                "I wasn't doing anything.",
                "Why are you looking at me?",
                "I'm just sitting here.",
                "This is completely normal.",
                "I am definitely not stealing anything.",
                "...",
            ])
        )

        self.last_action = "caught"

    def human_looked_away(self):
        """
        Human stopped watching.
        """

        self.alertness = max(
            0,
            self.alertness - random.randint(5, 12)
        )

        self.set_state(
            ChipState.CURIOUS,
            random.choice([
                "Finally...",
                "Clear.",
                "Now's my chance.",
                "Excellent.",
                "Proceeding.",
            ])
        )

    # ---------------------------------------------------------
    # THEFT SEQUENCE
    # ---------------------------------------------------------

    def prepare_theft(self):
        self.set_state(
            ChipState.STEALING,
            random.choice([
                "Mine.",
                "This belongs to me now.",
                "Excellent treasure.",
                "Operation squirrel is underway.",
                "Don't mind me...",
            ])
        )

        self.last_action = "stealing"

    def begin_escape(self):
        self.set_state(
            ChipState.ESCAPING,
            random.choice([
                "RUN!",
                "RETREAT!",
                "They saw me!",
                "Emergency squirrel!",
                "ABORT! ABORT!",
            ])
        )

        self.energy = max(10, self.energy - random.randint(5, 15))
        self.last_action = "escaping"

    def enter_burrow(self):
        self.set_state(
            ChipState.BURROWING,
            random.choice([
                "Safe.",
                "Back to the burrow.",
                "My treasure!",
                "Nobody can find it here.",
                "Excellent addition to the collection.",
            ])
        )

        self.last_action = "burrowing"

    def celebrate(self):
        self.set_state(
            ChipState.CELEBRATING,
            random.choice([
                "Worth it.",
                "Hehehe.",
                "Another successful operation.",
                "The humans will never learn.",
                "Excellent.",
            ])
        )

        self.mood = "mischievous"
        self.curiosity = max(
            20,
            self.curiosity - random.randint(5, 15)
        )

        self.last_action = "celebrating"

    # ---------------------------------------------------------
    # RETURN TO NORMAL
    # ---------------------------------------------------------

    def calm_down(self):
        self.set_state(
            ChipState.IDLE,
            random.choice([
                "Back to normal.",
                "Nothing happened.",
                "Just another peaceful day.",
                "I am innocent.",
            ])
        )

        self.next_idle_action = (
            time.monotonic() + self._random_idle_delay()
        )

    # ---------------------------------------------------------
    # INFORMATION FOR GUI
    # ---------------------------------------------------------

    def get_status(self):
        """
        Returns a simple dictionary for the GUI.
        """

        return {
            "state": self.state.value,
            "mood": self.mood,
            "energy": self.energy,
            "curiosity": self.curiosity,
            "alertness": self.alertness,
            "thought": self.current_thought,
            "last_action": self.last_action,
        }