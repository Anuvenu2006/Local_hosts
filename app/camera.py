# ==========================================
# 📷 CHIP'S HUMAN DETECTION
# ==========================================

import cv2
from pathlib import Path


class HumanDetector:
    def __init__(self, camera_index=0):

        # Find project root
        project_root = Path(__file__).resolve().parent.parent

        # YuNet model
        self.model_path = (
            project_root
            / "assets"
            / "face_detection_yunet_2023mar.onnx"
        )

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"YuNet model not found: {self.model_path}"
            )

        print("🧠 Loading Chip's human detector...")

        # Create YuNet detector
        self.detector = cv2.FaceDetectorYN.create(
            str(self.model_path),
            "",
            (320, 320),
            0.7,
            0.3,
            5000
        )

        # ==========================================
        # 📷 OPEN WINDOWS CAMERA
        # ==========================================
        #
        # OpenCV uses Media Foundation (MSMF) by
        # default on Windows. Your current logs show
        # MSMF repeatedly failing to grab frames.
        #
        # DirectShow (DSHOW) is used first because it
        # is often more reliable for webcams on Windows.
        #
        # ==========================================

        print("📷 Opening Chip's webcam...")

        self.camera = None
        self.backend_name = "UNKNOWN"

        # Try DirectShow first.
        dshow_camera = cv2.VideoCapture(
            camera_index,
            cv2.CAP_DSHOW
        )

        if dshow_camera.isOpened():

            # A modest resolution is more reliable for
            # face detection and reduces camera startup
            # problems on some Windows webcams.
            dshow_camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                640
            )
            dshow_camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                480
            )

            # Keep only a small buffer so Chip reacts to
            # the current camera view instead of old frames.
            try:
                dshow_camera.set(
                    cv2.CAP_PROP_BUFFERSIZE,
                    1
                )
            except Exception:
                pass

            # Verify that we can actually receive a frame.
            success, frame = dshow_camera.read()

            if success and frame is not None:

                self.camera = dshow_camera
                self.backend_name = "DirectShow"

                print("📷 Chip's camera is ready!")
                print("📷 Camera backend: DirectShow")
                return

            dshow_camera.release()

        else:
            dshow_camera.release()

        # ==========================================
        # 🔁 FALLBACK: MEDIA FOUNDATION
        # ==========================================

        print("⚠️ DirectShow could not provide a frame.")
        print("🔁 Trying Media Foundation fallback...")

        msmf_camera = cv2.VideoCapture(
            camera_index,
            cv2.CAP_MSMF
        )

        if msmf_camera.isOpened():

            msmf_camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                640
            )
            msmf_camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                480
            )

            success, frame = msmf_camera.read()

            if success and frame is not None:

                self.camera = msmf_camera
                self.backend_name = "Media Foundation"

                print("📷 Chip's camera is ready!")
                print("📷 Camera backend: Media Foundation")
                return

            msmf_camera.release()

        else:
            msmf_camera.release()

        raise RuntimeError(
            "Could not open the webcam or receive a camera frame."
        )

    def is_human_watching(self):
        """
        Capture one frame and determine whether
        at least one human face is visible.

        Returns:
            True  -> human detected
            False -> no human detected
        """

        if self.camera is None:
            return False

        success, frame = self.camera.read()

        if not success or frame is None:
            # Do not print every failed frame.
            # CameraWorker will simply treat this as
            # no detected person for this cycle.
            return False

        # Mirror camera
        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        # Update detector input size
        self.detector.setInputSize((width, height))

        # Detect faces
        _, faces = self.detector.detect(frame)

        if faces is None:
            return False

        return len(faces) > 0

    def release(self):
        """Release the webcam."""

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        print("📷 Chip released the camera.")


# ==========================================
# 🧪 SIMPLE TEST
# ==========================================

if __name__ == "__main__":

    print()
    print("🐿️ CHIP HUMAN DETECTOR TEST")
    print("=" * 40)

    detector = HumanDetector()

    print()
    print("Look at the camera.")
    print("Then move away.")
    print("Press CTRL+C to stop.")
    print()

    try:

        while True:

            watching = detector.is_human_watching()

            if watching:
                print("👀 HUMAN WATCHING CHIP")
            else:
                print("😈 HUMAN LOOKED AWAY")

    except KeyboardInterrupt:
        print()
        print("🛑 Test stopped.")

    finally:
        detector.release()
