# ==========================================
# 🐿️ SQUIRREL FILE THIEF
# 🧠 MAIN CONTROLLER
# ==========================================

import sys
import brain
import shutil
import subprocess
import webbrowser
import socket
from pathlib import Path
from queue import Queue, Empty
from datetime import datetime

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from brain import (
    calculate_interest,
    get_file_reaction,
    preload_brain,
    SquirrelState
)

from watcher import start_watching
from squirrel_gui import SquirrelWindow
from camera_worker import CameraWorker
from chip_life import ChipLife
from api_server import start_server


# ==========================================
# 📁 PATHS
# ==========================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

PLAYGROUND = (
    BASE_DIR
    / "sandbox"
    / "playground"
)

BURROW = (
    BASE_DIR
    / "sandbox"
    / "burrow"
)


# ==========================================
# 📬 FILE QUEUE
# ==========================================

file_queue = Queue()


# ==========================================
# 🧠 CHIP'S PERSONALITY
# ==========================================

chip_state = SquirrelState()

# 🐿️ CHIP'S AUTONOMOUS LIFE ENGINE
# Controls Chip's moods, idle behaviour, curiosity and reactions.
# It never touches files; main.py remains responsible for safe theft.
chip_life = ChipLife(chip_state)


# ==========================================
# 🚨 CHIP CRIME HISTORY
# ==========================================

crime_history = []


# ==========================================
# 🚦 THEFT CONTROL
# ==========================================

# Only one heist can happen at a time.
heist_in_progress = False


# ==========================================
# 📷 CHIP CAMERA
# ==========================================

camera_worker = None

# Remembers the previous camera state
# so Chip only reacts when the state changes.
last_watching_state = None

# 🌐 Live data exposed to the Magic Patterns frontend
current_analysis = {
    "target": "",
    "score": 0,
    "reasons": [],
    "category": "BORING",
    "confidence": 0,
}
ui_paused = False
ui_events = []
ui_last_state = None
ui_last_crime_count = 0


# ==========================================
# 📥 ADD FILE TO QUEUE
# ==========================================

def queue_file(file_path):

    file_path = Path(file_path)

    # Only accept actual files
    if not file_path.exists():
        return

    if not file_path.is_file():
        return

    # ======================================
    # 🔒 SAFETY CHECK
    # ======================================
    #
    # ONLY files inside the sandbox
    # playground are allowed.
    #

    try:

        file_path.resolve().relative_to(
            PLAYGROUND.resolve()
        )

    except ValueError:

        print(
            f"🚫 BLOCKED: File is outside playground: "
            f"{file_path}"
        )

        return

    file_queue.put(
        file_path
    )


# ==========================================
# 🔒 SAFETY CHECK
# ==========================================

def is_valid_target(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        return False

    if not file_path.is_file():
        return False

    try:

        file_path.resolve().relative_to(
            PLAYGROUND.resolve()
        )

        return True

    except ValueError:

        return False


# ==========================================
# 🌰 CHECK IF CHIP ALREADY STOLE THIS
# ==========================================

def already_stolen(file_path):

    file_path = Path(file_path)

    if not BURROW.exists():
        return False

    # If a file with the same original name
    # already exists in the burrow, Chip
    # considers it already stolen.

    existing_file = (
        BURROW
        / file_path.name
    )

    return existing_file.exists()


# ==========================================
# 🌰 STEAL FILE
# ==========================================

def steal_file(file_path):

    file_path = Path(file_path)

    # ======================================
    # 🔒 SAFETY
    # ======================================

    if not is_valid_target(file_path):

        print(
            "🚫 CHIP REFUSED TO STEAL THIS FILE."
        )

        return False

    # ======================================
    # 🌰 ALREADY STOLEN?
    # ======================================

    if already_stolen(file_path):

        print()
        print(
            "🌰 CHIP ALREADY HAS THIS FILE!"
        )

        print(
            f"📁 Already in burrow: {file_path.name}"
        )

        return False

    # ======================================
    # 📁 DESTINATION
    # ======================================

    destination = (
        BURROW
        / file_path.name
    )

    try:

        BURROW.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.move(
            str(file_path),
            str(destination)
        )

        print()
        print(
            "🌰 CHIP STOLE THE FILE!"
        )

        print(
            f"🏃 Escaped to: {destination.name}"
        )

        return True

    except Exception as error:

        print()
        print(
            f"❌ Chip failed: {error}"
        )

        return False


# ==========================================
# 🐿️ MOVE CHIP TOWARD TARGET
# ==========================================

def move_chip_toward_file(
    chip,
    file_path
):

    """
    Move Chip toward the middle of the screen
    to create the visual impression that he is
    approaching the file.

    The actual file does not have a screen
    position, so the screen center acts as
    Chip's target.
    """

    screen = (
        QApplication.primaryScreen()
    )

    if screen is None:
        return

    geometry = (
        screen.availableGeometry()
    )

    target_x = (
        geometry.center().x()
        - chip.width() // 2
    )

    target_y = (
        geometry.center().y()
        - chip.height() // 2
    )

    chip.move(
        target_x,
        target_y
    )


# ==========================================
# 🚨 CREATE CRIME REPORT
# ==========================================

def create_crime_report(
    file_path,
    score,
    reasons
):

    file_path = Path(file_path)

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    crime_number = (
        len(crime_history) + 1
    )

    report = {

        "crime_number": crime_number,

        "file": file_path.name,

        "score": score,

        "reasons": list(reasons),

        "time": timestamp,

        "crime": "Unauthorized File Acquisition",

        "status": "ESCAPED"
    }

    crime_history.append(
        report
    )

    return report


# ==========================================
# 📋 PRINT CRIME REPORT
# ==========================================

def print_crime_report(
    report
):

    print()
    print(
        "╔══════════════════════════════════════╗"
    )

    print(
        "║        🚨 CHIP CRIME REPORT         ║"
    )

    print(
        "╠══════════════════════════════════════╣"
    )

    print(
        f"║ Crime #: {report['crime_number']:<26}║"
    )

    print(
        f"║ File: {report['file'][:27]:<27}║"
    )

    print(
        f"║ Interest: {report['score']}/100"
        f"{' ' * max(0, 18 - len(str(report['score'])))}║"
    )

    print(
        f"║ Time: {report['time']:<27}║"
    )

    print(
        "║ Crime: Unauthorized File Acquisition ║"
    )

    print(
        "║ Status: ESCAPED 🏃                    ║"
    )

    print(
        "╚══════════════════════════════════════╝"
    )

    print()


# ==========================================
# 🌐 MAGIC PATTERNS BRIDGE
# ==========================================

def _ui_category(category):
    mapping = {
        "SECRET": "SECRET",
        "TREASURE": "SECRET",
        "DANGEROUS": "SECRET",
        "ACADEMIC": "ACADEMIC",
        "PERSONAL": "PERSONAL",
        "FINANCIAL": "FINANCIAL",
        "MEDIA": "BORING",
        "JUNK": "BORING",
        "NORMAL": "BORING",
    }
    return mapping.get(str(category or "NORMAL").upper(), "BORING")


def build_ui_snapshot():
    """Return only JSON-safe, presentation-oriented Chip state."""
    state = chip_life.state.value
    state_map = {"looking_around": "idle", "frozen": "watched"}
    state = state_map.get(state, state)

    global ui_last_state, ui_last_crime_count
    if state != ui_last_state:
        ui_events.append({
            "id": f"state-{datetime.now().timestamp()}",
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": f"Chip entered {state.upper()} state",
            "tone": "alert" if state == "watched" else ("crime" if state in ("stealing", "escaping") else "neutral"),
        })
        ui_last_state = state
    if len(crime_history) != ui_last_crime_count:
        if crime_history:
            latest = crime_history[-1]
            ui_events.append({
                "id": f"crime-{latest['crime_number']}",
                "time": latest["time"],
                "message": f"FILE STOLEN: {latest['file']}",
                "tone": "crime",
            })
        ui_last_crime_count = len(crime_history)
    del ui_events[:-40]

    camera_active = False
    watching = False
    if camera_worker is not None:
        camera_active = True
        try:
            watching = bool(camera_worker.is_watching())
        except Exception:
            watching = False

    files = []
    if BURROW.exists():
        for item in sorted(BURROW.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if item.is_file():
                try:
                    size = item.stat().st_size
                    size_text = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"
                except OSError:
                    size_text = "unknown"
                files.append({
                    "id": item.name,
                    "name": item.name,
                    "category": _ui_category(chip_state.last_category),
                    "size": size_text,
                })

    crimes = []
    for r in reversed(crime_history[-14:]):
        crimes.append({
            "id": r["crime_number"],
            "fileName": r["file"],
            "category": _ui_category(chip_state.last_category),
            "interest": int(r["score"]),
            "status": "STOLEN" if r.get("status") == "ESCAPED" else "ABORTED",
            "time": r["time"],
        })

    # ======================================
    # 🎯 ONLY SHOW A LIVE TARGET
    # ======================================
    #
    # current_analysis remembers the last file Chip
    # looked at. That does NOT mean the file is still
    # in the playground.
    #
    # The web UI must never show a stale target after
    # the file has already been moved into the burrow.
    #
    active_target = str(current_analysis.get("target", "") or "").strip()

    if active_target:
        target_path = PLAYGROUND / active_target
        burrow_path = BURROW / active_target

        if (
            not target_path.exists()
            or not target_path.is_file()
            or burrow_path.exists()
        ):
            active_target = ""

            # Clear stale analysis as well, so the next
            # snapshot starts clean.
            current_analysis["target"] = ""
            current_analysis["score"] = 0
            current_analysis["reasons"] = []
            current_analysis["category"] = "BORING"
            current_analysis["confidence"] = 0

    thought_text = chip_life.current_thought or chip_state.current_thought
    return {
        "state": state,
        "paused": ui_paused,
        "thought": {
            "text": thought_text,
            "interest": int(current_analysis.get("score", 0)),
            "category": current_analysis.get("category", _ui_category(chip_state.last_category)),
            "confidence": int(current_analysis.get("confidence", 0)),
            "reason": "; ".join(current_analysis.get("reasons", [])) or "Chip is deciding whether the file is worth stealing.",
            "target": active_target,
        },
        "stats": {
            "filesStolen": len(files),
            "crimesCommitted": int(chip_state.crimes),
            "mischief": int(chip_state.mischief),
            "greed": int(chip_state.greed),
            "suspicion": int(chip_state.suspicion),
        },
        "crimes": crimes,
        "stolenFiles": files,
        "events": list(reversed(ui_events[-40:])),
        "cameraActive": camera_active,
        "watcherActive": True,
    }


def handle_ui_command(command):
    global ui_paused
    kind = command.get("type")
    if kind == "pause":
        ui_paused = True
    elif kind == "resume":
        ui_paused = False
    elif kind == "set_camera":
        # Camera is controlled by the physical camera worker for now.
        pass
    return {"ok": True, "paused": ui_paused}


# ==========================================
# 👀 CAMERA AWARENESS
# ==========================================

def update_camera_awareness(chip):

    global last_watching_state

    # Camera isn't available
    if camera_worker is None:
        return

    try:

        watching = camera_worker.is_watching()

    except Exception as error:

        print(
            f"📷 Camera state error: {error}"
        )

        return

    # ======================================
    # SAME STATE?
    # ======================================
    #
    # Don't repeatedly change Chip's message
    # every 300 milliseconds.
    #

    if watching == last_watching_state:
        return

    last_watching_state = watching

    # ======================================
    # 👀 HUMAN IS WATCHING
    # ======================================

    if watching:

        # 🐿️ CHIP KNOWS HE HAS BEEN CAUGHT
        chip_life.human_is_watching()

        print()
        print(
            "👀 CHIP: HUMAN IS WATCHING ME!"
        )

        # Don't interrupt an existing heist.
        if not heist_in_progress:

            chip.set_message(
                "STOP! HUMAN IS WATCHING ME! 👀"
            )

    # ======================================
    # 😈 HUMAN LOOKED AWAY
    # ======================================

    else:

        # 🐿️ CHIP KNOWS THE COAST IS CLEAR
        chip_life.human_looked_away()

        print()
        print(
            "😈 CHIP: HUMAN LOOKED AWAY!"
        )

        if not heist_in_progress:

            chip.set_message(
                "Hehehe... they looked away. 😈"
            )


# ==========================================
# 🎭 CHIP'S FILE-SPECIFIC REACTION
# ==========================================

# ==========================================
# 🧠 ANALYZE FILE
# ==========================================

def analyze_file(
    file_path,
    chip
):

    global heist_in_progress

    file_path = Path(file_path)

    # ======================================
    # 🔒 SAFETY
    # ======================================

    if not is_valid_target(file_path):
        return

    # ======================================
    # 🌰 ALREADY STOLEN
    # ======================================

    if already_stolen(file_path):

        chip.set_message(
            "I already stole this one. 🌰"
        )

        print()

        print(
            "🌰 CHIP: I ALREADY HAVE THAT!"
        )

        return

    # ======================================
    # 🚫 DON'T START ANOTHER HEIST
    # ======================================

    if heist_in_progress:

        print(
            "🐿️ Chip is already stealing something!"
        )

        return

    # ======================================
    # 👀 CHECK CAMERA
    # ======================================
    #
    # Safety rule:
    # Chip will not START a new heist
    # while the human is watching.
    #

    if camera_worker is not None:

        try:

            if camera_worker.is_watching():

                print()
                print(
                    "👀 CHIP REFUSED TO STEAL!"
                )

                print(
                    "👀 HUMAN IS WATCHING!"
                )

                chip.set_message(
                    "I CAN'T STEAL WHILE YOU'RE WATCHING! 👀"
                )

                # Put the file back into the queue
                # so Chip can try again later.
                file_queue.put(
                    file_path
                )

                return

        except Exception as error:

            # FAIL CLOSED: if camera state is unknown,
            # Chip must not continue toward theft.
            print(
                f"📷 Camera check failed: {error}"
            )

            file_queue.put(file_path)
            return


    # ======================================
    # 🐿️ CHIP NOTICES THE FILE
    # ======================================

    chip_life.notice_file(file_path.name)

    chip.set_message(
        chip_life.current_thought
    )

    # ======================================
    # 🧠 BRAIN
    # ======================================

    print()

    print(
        "======================================"
    )

    print(
        "🧠 SQUIRREL BRAIN ACTIVATED"
    )

    print(
        "======================================"
    )

    print(
        f"📁 Target: {file_path.name}"
    )

    # ======================================
    # 🎭 FILE-SPECIFIC REACTION
    # ======================================

    file_reaction = get_file_reaction(
        file_path,
        chip_state
    )

    print()
    print(
        f"🐿️ CHIP: {file_reaction}"
    )

    chip.set_message(
        file_reaction
    )

    # ======================================
    # 📁 FILE DETECTED
    # ======================================

    chip_state.file_detected()

    # ======================================
    # 🔍 CALCULATE INTEREST
    # ======================================

    score, reasons = calculate_interest(
        file_path,
        chip_state
    )

    # 🌐 Publish the latest analysis to the web UI.
    current_analysis["target"] = file_path.name
    current_analysis["score"] = int(score)
    current_analysis["reasons"] = list(reasons)
    current_analysis["category"] = _ui_category(chip_state.last_category)
    current_analysis["confidence"] = int(brain.LAST_CLASSIFICATION.get("confidence", 0))

    chip_state.update_thought()

    # ======================================
    # 🔍 ANALYSIS
    # ======================================

    print()

    print(
        "🔍 ANALYSIS:"
    )

    if reasons:

        for reason in reasons:

            print(
                f"   • {reason}"
            )

    else:

        print(
            "   • Nothing interesting..."
        )

    print()

    print(
        f"🐿️ INTEREST SCORE: {score}/100"
    )

    # ======================================
    # 😴 BORING
    # ======================================

    if score < 30:

        chip_life.calm_down()

        print(
            "😴 DECISION: TOO BORING"
        )

        chip.set_message(
            "Hmm... boring. 😴"
        )

        return

    # ======================================
    # 👀 WATCH
    # ======================================

    elif score < 50:

        chip_life.start_investigation(
            "I'll keep an eye on this..."
        )

        print(
            "👀 DECISION: WATCH"
        )

        chip.set_message(
            "I'm watching you... 👀"
        )

        return

    # ======================================
    # 🔎 INVESTIGATE
    # ======================================

    elif score < 70:

        chip_life.start_investigation(
            "I need to investigate this."
        )

        print(
            "🔎 DECISION: INVESTIGATE"
        )

        chip.set_message(
            "Suspicious... 🤨"
        )

        move_chip_toward_file(
            chip,
            file_path
        )

        return

    # ======================================
    # 🐿️ INTERESTED
    # ======================================

    elif score < 85:

        chip_life.start_investigation(
            "Ooooh... this one is interesting."
        )

        print(
            "🐿️ DECISION: SNEAK TOWARD FILE"
        )

        chip.set_message(
            "Ooooh... 👀"
        )

        move_chip_toward_file(
            chip,
            file_path
        )

        return

    # ======================================
    # 🚨 STEAL
    # ======================================

    else:

        chip_life.prepare_theft()

        print(
            "🚨 DECISION: STEAL IMMEDIATELY"
        )

        print(
            "😈 HUMAN WILL PROBABLY PANIC"
        )

        heist_in_progress = True

        # Move Chip toward target
        move_chip_toward_file(
            chip,
            file_path
        )

        chip.set_message(
            "WAIT... 👀"
        )

        QTimer.singleShot(
            700,
            lambda: steal_sequence(
                file_path,
                chip,
                score,
                reasons
            )
        )


# ==========================================
# 😈 STEAL SEQUENCE
# ==========================================

def steal_sequence(
    file_path,
    chip,
    score,
    reasons
):

    file_path = Path(file_path)

    # ======================================
    # 🔒 SAFETY
    # ======================================

    if not is_valid_target(file_path):

        finish_heist()

        return

    # ======================================
    # 🌰 ALREADY STOLEN
    # ======================================

    if already_stolen(file_path):

        chip.set_message(
            "I already have that! 🌰"
        )

        finish_heist()

        return

    # ======================================
    # 👀 FINAL CAMERA CHECK
    # ======================================
    # Chip may have started analyzing the file
    # while the human was looking away.
    #
    # Before beginning the theft, check again.
    # If the human is watching, Chip aborts the
    # heist and waits for another opportunity.

    if camera_worker is not None:

        try:

            if camera_worker.is_watching():

                print()
                print("👀 CHIP: HUMAN DETECTED!")
                print("🧊 CHIP FREEZES!")
                print("🐿️ CHIP: I WAS JUST LOOKING...")

                chip_life.human_is_watching()

                chip.set_message(
                    "I WAS JUST LOOKING... 👀"
                )

                finish_heist()

                # Keep the file available for another attempt.
                QTimer.singleShot(
                    1500,
                    lambda: queue_file(file_path)
                )

                return

        except Exception as error:

            # FAIL CLOSED: never begin the attack when
            # camera state cannot be determined.
            print(
                f"📷 Camera check failed before attack: {error}"
            )

            finish_heist()

            QTimer.singleShot(
                1500,
                lambda: queue_file(file_path)
            )

            return

    # ======================================
    # ATTACK
    # ======================================

    print()

    chip_life.begin_escape()

    print(
        "🐿️ CHIP: THAT'S MINE!"
    )

    chip.attack_mode()

    chip.set_message(
        "THAT'S MINE! 😈"
    )

    # ======================================
    # 🌰 STEAL AFTER ATTACK
    # ======================================
    # There is another camera check inside
    # perform_steal() because the human can
    # look back during this 900 ms animation.

    QTimer.singleShot(
        900,
        lambda: perform_steal(
            file_path,
            chip,
            score,
            reasons
        )
    )


# ==========================================
# 🌰 PERFORM STEAL
# ==========================================

def perform_steal(
    file_path,
    chip,
    score,
    reasons
):

    file_path = Path(file_path)

    # ======================================
    # 🔒 SAFETY
    # ======================================

    if not is_valid_target(file_path):

        chip.set_message(
            "Where did it go?! 😳"
        )

        finish_heist()

        return

    # ======================================
    # 👀 LAST-SECOND CAMERA CHECK
    # ======================================
    # The human can look back while Chip is
    # performing the attack animation. Never
    # move the file if the human is watching.

    if camera_worker is not None:

        try:

            if camera_worker.is_watching():

                print()
                print("👀 CHIP: YOU LOOKED BACK!")
                print("🧊 CHIP FREEZES MID-HEIST!")
                print("🐿️ CHIP: NOTHING HAPPENED. 😇")

                chip_life.human_is_watching()

                chip.set_message(
                    "NOTHING HAPPENED... 😇"
                )

                finish_heist()

                # Retry later when the human looks away.
                QTimer.singleShot(
                    1500,
                    lambda: queue_file(file_path)
                )

                return

        except Exception as error:

            # FAIL CLOSED: the actual file move is the
            # final dangerous action. Unknown camera state
            # means Chip must not steal.
            print(
                f"📷 Final camera check failed: {error}"
            )

            finish_heist()

            QTimer.singleShot(
                1500,
                lambda: queue_file(file_path)
            )

            return

    # ======================================
    # 🌰 STEAL
    # ======================================

    success = steal_file(
        file_path
    )

    # ======================================
    # 🎯 CLEAR LIVE TARGET AFTER THEFT
    # ======================================
    #
    # The file has left playground and is now in burrow.
    # It must no longer appear as the current watched file.
    #
    if success:
        current_analysis["target"] = ""
        current_analysis["score"] = 0
        current_analysis["reasons"] = []
        current_analysis["category"] = "BORING"
        current_analysis["confidence"] = 0

    # ======================================
    # ❌ FAILED
    # ======================================

    if not success:

        chip.set_message(
            "Oops... failed! 😳"
        )

        finish_heist()

        return

    # ======================================
    # 🧠 PERSONALITY UPDATE
    # ======================================

    chip_state.successful_theft()

    # ======================================
    # 🧠 LEARN FROM THIS CRIME
    # ======================================

    if chip_state.last_category:
        chip_state.learn_from_theft(
            chip_state.last_category
        )

    # ======================================
    # 🚨 CREATE CRIME RECORD
    # ======================================

    report = create_crime_report(
        file_path,
        score,
        reasons
    )

    # ======================================
    # 📋 PRINT CRIME REPORT
    # ======================================

    print_crime_report(
        report
    )

    # ======================================
    # 😈 SUCCESS
    # ======================================

    chip.set_message(
        "I STOLE IT! 😈🌰"
    )

    print()

    chip_life.enter_burrow()
    chip_life.celebrate()

    print(
        "🐿️ CHIP: I STOLE IT! 😈🌰"
    )

    # ======================================
    # 🏠 RETURN HOME
    # ======================================

    QTimer.singleShot(
        1200,
        lambda: return_chip_home(
            chip
        )
    )

    # ======================================
    # 🧠 FINAL THOUGHT
    # ======================================

    QTimer.singleShot(
        2200,
        lambda: finish_heist_with_thought(
            chip
        )
    )


# ==========================================
# 🏠 RETURN CHIP HOME
# ==========================================

def return_chip_home(
    chip
):

    chip.return_home()


# ==========================================
# 🧠 FINISH WITH THOUGHT
# ==========================================

def finish_heist_with_thought(
    chip
):

    global heist_in_progress

    chip.set_message(
        chip_state.current_thought
    )

    heist_in_progress = False


# ==========================================
# 🚦 FINISH FAILED HEIST
# ==========================================

def finish_heist():

    global heist_in_progress

    heist_in_progress = False


# ==========================================
# 📬 PROCESS QUEUE
# ==========================================

def process_queue(
    chip
):

    # ======================================
    # 🌲 WAIT FOR BROWSER UI
    # ======================================
    #
    # This MUST be the first gate. calculate_interest()
    # can load/run the semantic model and temporarily block
    # the Qt event loop. Without this gate, Chip can start
    # working before the browser is visible.
    #
    if not frontend_ready:
        return

    if ui_paused:
        return

    # ======================================
    # 🚨 EXISTING HEIST
    # ======================================

    if heist_in_progress:
        return

    # ======================================
    # 👀 HUMAN WATCHING
    # ======================================
    #
    # Leave the file inside the queue.
    # Chip waits until the human looks away.
    #

    if camera_worker is not None:

        try:

            if camera_worker.is_watching():

                return

        except Exception as error:

            print(
                f"📷 Camera queue check failed: {error}"
            )

            return

    # ======================================
    # 📂 GET NEXT FILE
    # ======================================

    try:

        file_path = (
            file_queue.get_nowait()
        )

    except Empty:

        return

    # ======================================
    # 🧠 ANALYZE
    # ======================================

    analyze_file(
        file_path,
        chip
    )


# ==========================================
# 🌲 MAGIC PATTERNS FRONTEND
# ==========================================

frontend_process = None

# Chip must wait until the browser UI has been launched.
# This prevents the file queue from starting semantic analysis
# before the visual environment is ready.
frontend_ready = False


def _frontend_is_ready():
    """Check whether Vite is accepting connections on port 5173."""
    try:
        with socket.create_connection(("127.0.0.1", 5173), timeout=0.25):
            return True
    except OSError:
        return False


def start_frontend():
    """
    Start Magic Patterns and open the browser only after Vite is ready.

    frontend_ready remains False until the browser is launched.
    """
    global frontend_process, frontend_ready

    frontend_ready = False

    frontend_dir = BASE_DIR / "frontend"

    if not frontend_dir.exists():
        print()
        print("⚠️ Magic Patterns frontend folder not found:")
        print(f"   {frontend_dir}")
        print("⚠️ Continuing without browser UI.")
        frontend_ready = True
        return

    print()
    print("🌲 STARTING MAGIC PATTERNS ENVIRONMENT...")

    def open_frontend():
        global frontend_ready

        try:
            webbrowser.open("http://127.0.0.1:5173")
            print("🌐 Chip's environment opened in your browser.")
            frontend_ready = True
        except Exception as error:
            print(f"⚠️ Could not open Chip's browser UI: {error}")
            frontend_ready = False

    if _frontend_is_ready():
        print("🌲 Magic Patterns is already running on port 5173.")
        print("⏳ Opening Chip's environment...")
        QTimer.singleShot(250, open_frontend)
        return

    try:
        frontend_process = subprocess.Popen(
            [
                "npm.cmd",
                "run",
                "dev",
                "--",
                "--host",
                "127.0.0.1",
                "--port",
                "5173",
                "--strictPort",
            ],
            cwd=str(frontend_dir),
            shell=False,
            creationflags=getattr(
                subprocess,
                "CREATE_NEW_PROCESS_GROUP",
                0,
            ),
        )

        print("🌲 Magic Patterns server starting...")
        print("⏳ Waiting for the Chip environment...")

        def wait_for_frontend():
            if _frontend_is_ready():
                open_frontend()
                return

            if (
                frontend_process is not None
                and frontend_process.poll() is not None
            ):
                print()
                print(
                    "⚠️ Magic Patterns server stopped "
                    "before it became ready."
                )
                print(
                    f"   Exit code: {frontend_process.returncode}"
                )
                return

            QTimer.singleShot(250, wait_for_frontend)

        QTimer.singleShot(250, wait_for_frontend)

    except FileNotFoundError:
        print()
        print("❌ npm was not found.")
        print(
            "   Make sure Node.js/npm is installed "
            "and available in PATH."
        )

    except Exception as error:
        print()
        print(f"⚠️ Could not start Magic Patterns: {error}")


def stop_frontend():
    """Stop the Vite process started by Chip."""
    global frontend_process

    if frontend_process is None:
        return

    try:
        if frontend_process.poll() is None:
            print()
            print("🌲 STOPPING MAGIC PATTERNS ENVIRONMENT...")

            # On Windows, terminate the npm process tree.
            if sys.platform.startswith("win"):
                subprocess.run(
                    [
                        "taskkill",
                        "/PID",
                        str(frontend_process.pid),
                        "/T",
                        "/F",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                frontend_process.terminate()

    except Exception as error:
        print(f"⚠️ Frontend stop error: {error}")

    finally:
        frontend_process = None


# ==========================================
# 🚀 MAIN
# ==========================================

def main():

    global camera_worker

    # ======================================
    # 📁 CREATE DIRECTORIES
    # ======================================

    PLAYGROUND.mkdir(
        parents=True,
        exist_ok=True
    )

    BURROW.mkdir(
        parents=True,
        exist_ok=True
    )

    # ======================================
    # 🪟 QT APPLICATION
    # ======================================

    app = QApplication(
        sys.argv
    )

    # ======================================
    # 🐿️ CREATE CHIP
    # ======================================

    chip = SquirrelWindow(
        BURROW,
        chip_state,
        crime_history,
        chip_life
    )

    # ======================================
    # 🚨 GIVE CHIP HIS CRIME HISTORY
    # ======================================

    chip.crime_history = crime_history

    # ======================================
    # 📍 CHIP HOME POSITION
    # ======================================

    screen = (
        app.primaryScreen()
    )

    if screen is None:

        print(
            "❌ No primary screen detected."
        )

        return

    screen_geometry = (
        screen.availableGeometry()
    )

    x = (
        screen_geometry.right()
        - chip.width()
        - 50
    )

    y = (
        screen_geometry.top()
        + 50
    )

    chip.move(
        x,
        y
    )

    chip.set_home_position(
        chip.pos()
    )

    chip.hide()

    # ======================================
    # 📂 EXISTING FILES
    # ======================================

    for file_path in PLAYGROUND.iterdir():

        if file_path.is_file():

            queue_file(
                file_path
            )

    # ======================================
    # 👀 START FILE WATCHER
    # ======================================

    observer = start_watching(
        PLAYGROUND,
        queue_file
    )

    # ======================================
    # 📷 START CAMERA WORKER
    # ======================================

    print()
    print(
        "📷 STARTING CHIP'S CAMERA..."
    )

    try:

        camera_worker = CameraWorker()

        camera_worker.start()

        print(
            "📷 CHIP CAMERA WORKER STARTED!"
        )

    except Exception as error:

        camera_worker = None

        print()
        print(
            f"⚠️ CAMERA COULD NOT START: {error}"
        )

        print(
            "🐿️ Chip will continue without camera awareness."
        )

    # ======================================
    # 🌐 START MAGIC PATTERNS BRIDGE
    # ======================================
    api_server = start_server(
        build_ui_snapshot,
        handle_ui_command,
        host="127.0.0.1",
        port=8000,
    )

    # ======================================
    # 🌲 START MAGIC PATTERNS UI
    # ======================================
    start_frontend()

    # ======================================
    # ⏱️ FILE QUEUE TIMER
    # ======================================

    timer = QTimer()

    timer.timeout.connect(
        lambda: process_queue(
            chip
        )
    )

    timer.start(
        200
    )

    # ======================================
    # 👀 CAMERA AWARENESS TIMER
    # ======================================

    camera_timer = QTimer()

    camera_timer.timeout.connect(
        lambda: update_camera_awareness(
            chip
        )
    )

    camera_timer.start(
        300
    )

    # ======================================
    # 🧬 CHIP LIFE ENGINE TIMER
    # ======================================
    #
    # Updates Chip's autonomous behaviour without blocking Qt.
    # 100 ms gives us smooth state changes while keeping the GUI responsive.

    life_timer = QTimer()

    def update_chip_life():
        if ui_paused:
            return
        if heist_in_progress:
            return

        current_state = chip_life.update()

        # Show autonomous thoughts only when Chip is otherwise idle.
        # This keeps important theft/camera messages from being overwritten.
        if current_state.value in (
            "idle",
            "looking_around",
            "curious",
        ):
            chip.set_message(
                chip_life.current_thought
            )

    life_timer.timeout.connect(
        update_chip_life
    )

    life_timer.start(
        100
    )

    # ======================================
    # ▶️ START APPLICATION
    # ======================================

    try:

        print()
        print(
            "🐿️ CHIP IS READY."
        )

        print(
            "🧬 CHIP LIFE ENGINE ONLINE."
        )

        print(
            "👀 If you're watching him, he'll wait."
        )

        print(
            "😈 Look away... and he may steal."
        )

        print()

        exit_code = app.exec()

    finally:

        # ==================================
        # 🛑 STOP MAGIC PATTERNS FRONTEND
        # ==================================
        stop_frontend()

        try:
            api_server.shutdown()
        except Exception:
            pass

        # ==================================
        # 🛑 STOP FILE WATCHER
        # ==================================

        observer.stop()

        observer.join()

        # ==================================
        # 🛑 STOP CAMERA
        # ==================================

        if camera_worker is not None:

            print()
            print(
                "🛑 STOPPING CHIP'S CAMERA..."
            )

            try:

                camera_worker.stop()

            except Exception as error:

                print(
                    f"⚠️ Camera stop error: {error}"
                )

    # ======================================
    # 🚪 EXIT
    # ======================================

    sys.exit(
        exit_code
    )


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":

    main()