# ==========================================
# 📷 CHIP CAMERA WORKER
# ==========================================

import threading
import time

from camera import HumanDetector


class CameraWorker:
    """
    Runs Chip's human detection in a background thread.

    Stability logic:
        - Human detected -> immediately WATCHING
        - 1-2 missed detections -> still WATCHING
        - Several consecutive misses -> LOOKED AWAY

    This prevents Chip from stealing just because the
    camera temporarily missed a face for one frame.

    The GUI can ask:
        worker.is_watching()

    without freezing the application.
    """

    def __init__(self, check_interval=0.25):

        self.check_interval = check_interval

        # Current stable camera state
        self.watching = False

        # Worker state
        self.running = False

        self.detector = None
        self.thread = None

        self.lock = threading.Lock()

        # ==========================================
        # 👀 CAMERA STABILITY SETTINGS
        # ==========================================

        # Human detection is instant.
        # As soon as a face is detected, Chip knows
        # someone is watching.
        self.watch_confirmations = 1

        # Number of consecutive missed detections
        # required before declaring the human gone.
        #
        # 0.25 second × 4 = approximately 1 second
        # of continuous misses before Chip considers
        # it safe to steal.
        self.max_missed_frames = 4

        # Counters used by the stability system
        self.detected_frames = 0
        self.missed_frames = 0

    # ==========================================
    # 🚀 START CAMERA
    # ==========================================

    def start(self):

        if self.running:
            return

        print()
        print("🐿️ CHIP CAMERA WORKER STARTING...")

        try:

            self.detector = HumanDetector()

        except Exception as error:

            print(f"❌ Camera could not start: {error}")

            return

        self.running = True

        # Reset stability counters
        with self.lock:

            self.watching = False
            self.detected_frames = 0
            self.missed_frames = 0

        self.thread = threading.Thread(
            target=self._camera_loop,
            daemon=True
        )

        self.thread.start()

        print("📷 CHIP CAMERA WORKER RUNNING!")

    # ==========================================
    # 🔄 CAMERA LOOP
    # ==========================================

    def _camera_loop(self):

        previous_state = None

        while self.running:

            try:

                detected = self.detector.is_human_watching()

                # ==========================================
                # 👀 HUMAN DETECTED
                # ==========================================

                if detected:

                    # Reset missed-frame counter immediately.
                    self.missed_frames = 0

                    # Count successful detections.
                    self.detected_frames += 1

                    # A single confirmed detection is enough
                    # to mark Chip as watched.
                    if self.detected_frames >= self.watch_confirmations:

                        with self.lock:
                            self.watching = True

                # ==========================================
                # 😈 HUMAN NOT DETECTED
                # ==========================================

                else:

                    # Reset successful detection counter.
                    self.detected_frames = 0

                    # Increase missed-frame counter.
                    self.missed_frames += 1

                    # IMPORTANT:
                    #
                    # Do NOT immediately change watching=False.
                    #
                    # The camera may temporarily miss the face
                    # because of lighting, movement, autofocus,
                    # frame drops, etc.
                    #
                    # Chip only believes the human has actually
                    # looked away after several consecutive misses.

                    if self.missed_frames >= self.max_missed_frames:

                        with self.lock:
                            self.watching = False

                # ==========================================
                # 📢 PRINT ONLY WHEN STATE CHANGES
                # ==========================================

                with self.lock:
                    current_state = self.watching

                if current_state != previous_state:

                    if current_state:

                        print("👀 HUMAN WATCHING CHIP")

                    else:

                        print("😈 HUMAN LOOKED AWAY")

                    previous_state = current_state

            # ==========================================
            # ⚠️ CAMERA ERROR
            # ==========================================

            except Exception as error:

                print(f"⚠️ Camera detection error: {error}")

                # IMPORTANT:
                #
                # A camera error should NOT immediately tell
                # Chip that it is safe to steal.
                #
                # Treat the error like a missed frame instead.

                self.missed_frames += 1

                if self.missed_frames >= self.max_missed_frames:

                    with self.lock:
                        self.watching = False

            # ==========================================
            # ⏱️ WAIT BEFORE NEXT CHECK
            # ==========================================

            time.sleep(self.check_interval)

    # ==========================================
    # 👀 CURRENT STATUS
    # ==========================================

    def is_watching(self):

        with self.lock:

            return self.watching

    # ==========================================
    # 🛑 STOP CAMERA
    # ==========================================

    def stop(self):

        if not self.running:
            return

        print()
        print("🛑 CHIP CAMERA WORKER STOPPING...")

        self.running = False

        if self.thread is not None:

            self.thread.join(timeout=2)

        if self.detector is not None:

            self.detector.release()

        self.thread = None
        self.detector = None

        with self.lock:

            self.watching = False
            self.detected_frames = 0
            self.missed_frames = 0

        print("📷 CHIP CAMERA WORKER STOPPED.")


# ==========================================
# 🧪 TEST
# ==========================================

if __name__ == "__main__":

    print()
    print("🐿️ CHIP CAMERA WORKER TEST")
    print("=" * 40)

    worker = CameraWorker()

    worker.start()

    if not worker.running:

        print("❌ Worker failed to start.")

        exit()

    print()
    print("Look at the camera.")
    print("Then move away.")
    print()
    print("Chip should:")
    print("  👀 Detect you immediately")
    print("  👀 Ignore temporary missed frames")
    print("  😈 Mark you away only after several misses")
    print()
    print("Press CTRL+C to stop.")
    print()

    try:

        while True:

            if worker.is_watching():

                print("GUI WOULD SEE: 👀 WATCHING")

            else:

                print("GUI WOULD SEE: 😈 SAFE TO STEAL")

            time.sleep(1)

    except KeyboardInterrupt:

        print()
        print("🛑 Test stopped.")

    finally:

        worker.stop()