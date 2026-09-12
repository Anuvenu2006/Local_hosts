# ==========================================
# 📷 CHIP CAMERA WORKER
# ==========================================

import threading
import time

from camera import HumanDetector


class CameraWorker:
    """
    Runs Chip's human detection in a background thread.

    The GUI can ask:
        worker.is_watching()

    without freezing the application.
    """

    def __init__(self, check_interval=0.25):

        self.check_interval = check_interval

        self.watching = False
        self.running = False

        self.detector = None
        self.thread = None

        self.lock = threading.Lock()

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

                with self.lock:
                    self.watching = detected

                # Only print when the state changes.
                if detected != previous_state:

                    if detected:
                        print("👀 HUMAN WATCHING CHIP")
                    else:
                        print("😈 HUMAN LOOKED AWAY")

                    previous_state = detected

            except Exception as error:

                print(f"⚠️ Camera detection error: {error}")

                with self.lock:
                    self.watching = False

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