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

        # Open webcam
        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():
            raise RuntimeError("Could not open webcam.")

        print("📷 Chip's camera is ready!")

    def is_human_watching(self):
        """
        Capture one frame and determine whether
        at least one human face is visible.

        Returns:
            True  -> human detected
            False -> no human detected
        """

        success, frame = self.camera.read()

        if not success:
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