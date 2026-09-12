# ==========================================
# 🐿️ CHIP - SQUIRREL GUI
# ==========================================

import sys
import math
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QProgressBar,
    QFrame,
    QMenu,
    QMessageBox,
)

from PySide6.QtCore import (
    Qt,
    QPoint,
    QPointF,
    QRectF,
    QTimer,
)

from PySide6.QtGui import (
    QFont,
    QPainter,
    QPen,
    QBrush,
    QColor,
    QRadialGradient,
    QLinearGradient,
    QPainterPath,
    QPolygonF,
)


# ==========================================
# 🧠 BRAIN DASHBOARD
# ==========================================

class BrainWindow(QDialog):

    def __init__(
        self,
        state,
        parent=None
    ):
        super().__init__(parent)

        self.state = state

        self.setWindowTitle(
            "🧠 Chip's Brain"
        )

        self.setFixedSize(
            420,
            520
        )

        self.setStyleSheet("""
            QDialog {
                background-color: #181818;
                color: white;
            }

            QLabel {
                color: white;
            }

            QProgressBar {
                border: 1px solid #444;
                border-radius: 6px;
                background-color: #292929;
                height: 18px;
                text-align: center;
                color: white;
            }

            QProgressBar::chunk {
                background-color: #8B5A2B;
                border-radius: 5px;
            }

            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #444444;
            }
        """)

        layout = QVBoxLayout()


        # ==================================
        # TITLE
        # ==================================

        title = QLabel(
            "🧠 CHIP'S BRAIN"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Bold
            )
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title
        )


        # ==================================
        # SUBTITLE
        # ==================================

        subtitle = QLabel(
            "Psychological profile of a criminal squirrel"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet(
            "color: #aaaaaa;"
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            15
        )


        # ==================================
        # MISCHIEF
        # ==================================

        self.mischief_label = QLabel()

        layout.addWidget(
            self.mischief_label
        )

        self.mischief_bar = QProgressBar()

        self.mischief_bar.setRange(
            0,
            100
        )

        layout.addWidget(
            self.mischief_bar
        )


        # ==================================
        # GREED
        # ==================================

        self.greed_label = QLabel()

        layout.addWidget(
            self.greed_label
        )

        self.greed_bar = QProgressBar()

        self.greed_bar.setRange(
            0,
            100
        )

        layout.addWidget(
            self.greed_bar
        )


        # ==================================
        # SUSPICION
        # ==================================

        self.suspicion_label = QLabel()

        layout.addWidget(
            self.suspicion_label
        )

        self.suspicion_bar = QProgressBar()

        self.suspicion_bar.setRange(
            0,
            100
        )

        layout.addWidget(
            self.suspicion_bar
        )

        layout.addSpacing(
            15
        )


        # ==================================
        # CURRENT THOUGHT
        # ==================================

        thought_title = QLabel(
            "💭 CURRENT THOUGHT"
        )

        thought_title.setFont(
            QFont(
                "Segoe UI",
                11,
                QFont.Bold
            )
        )

        layout.addWidget(
            thought_title
        )

        self.thought_label = QLabel()

        self.thought_label.setWordWrap(
            True
        )

        self.thought_label.setAlignment(
            Qt.AlignCenter
        )

        self.thought_label.setStyleSheet("""
            QLabel {
                background-color: #252525;
                border-radius: 10px;
                padding: 15px;
                color: #dddddd;
            }
        """)

        layout.addWidget(
            self.thought_label
        )

        layout.addSpacing(
            15
        )


        # ==================================
        # STATISTICS
        # ==================================

        stats_frame = QFrame()

        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 10px;
            }
        """)

        stats_layout = QVBoxLayout()

        self.files_label = QLabel()

        self.crimes_label = QLabel()

        self.status_label = QLabel()

        stats_layout.addWidget(
            self.files_label
        )

        stats_layout.addWidget(
            self.crimes_label
        )

        stats_layout.addWidget(
            self.status_label
        )

        stats_frame.setLayout(
            stats_layout
        )

        layout.addWidget(
            stats_frame
        )

        layout.addSpacing(
            10
        )


        # ==================================
        # CLOSE BRAIN
        # ==================================

        close_button = QPushButton(
            "Close Brain"
        )

        close_button.clicked.connect(
            self.accept
        )

        layout.addWidget(
            close_button
        )

        self.setLayout(
            layout
        )


        # ==================================
        # LIVE UPDATE
        # ==================================

        self.update_brain()

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.update_brain
        )

        self.timer.start(
            300
        )


    # ======================================
    # UPDATE BRAIN
    # ======================================

    def update_brain(self):

        if self.state is None:
            return

        mischief = int(
            self.state.mischief
        )

        greed = int(
            self.state.greed
        )

        suspicion = int(
            self.state.suspicion
        )

        self.mischief_label.setText(
            f"😈 Mischief: {mischief}%"
        )

        self.greed_label.setText(
            f"🌰 Greed: {greed}%"
        )

        self.suspicion_label.setText(
            f"👀 Suspicion: {suspicion}%"
        )

        self.mischief_bar.setValue(
            mischief
        )

        self.greed_bar.setValue(
            greed
        )

        self.suspicion_bar.setValue(
            suspicion
        )

        self.thought_label.setText(
            self.state.current_thought
        )

        self.files_label.setText(
            f"📁 Files seen: {self.state.files_seen}"
        )

        self.crimes_label.setText(
            f"🚨 Crimes committed: {self.state.crimes}"
        )

        self.status_label.setText(
            "🟢 Status: ACTIVE"
        )


# ==========================================
# 🐿️ MAIN SQUIRREL WINDOW
# ==========================================

# ==========================================
# 🎬 CHIP VISUAL ENGINE
# ==========================================

class ChipCanvas(QWidget):
    """
    Hand-drawn squirrel with fur texture and floofy tail.
    All shapes use gradients for natural depth.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mode = "idle"
        self.frame = 0
        self.phase = 0.0
        self.direction = 1
        self.carrying_file = False
        self.thought = ""
        self.breath = 0

        self.setMinimumHeight(180)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(33)  # ~30 FPS

    def set_mode(self, mode):
        mode = (mode or "idle").lower()
        aliases = {
            "looking_around": "look",
            "curious": "curious",
            "investigating": "sneak",
            "stealing": "steal",
            "escaping": "run",
            "burrowing": "burrow",
            "celebrating": "celebrate",
            "frozen": "frozen",
            "watched": "frozen",
        }
        new_mode = aliases.get(mode, mode)
        if new_mode != self.mode:
            self.mode = new_mode
            self.frame = 0
        self.update()

    def tick(self):
        self.frame += 1
        self.phase += 0.12
        self.breath = math.sin(self.phase * 0.8) * 2.5
        self.update()

    # ==========================================
    # 🦊 FUR GRADIENTS
    # ==========================================

    def _fur_gradient(self, x, y, radius, color1, color2):
        """Create a soft radial gradient for fur depth."""
        grad = QRadialGradient(x, y, radius)
        grad.setColorAt(0, color1)
        grad.setColorAt(0.6, color2)
        grad.setColorAt(1, QColor(
            color2.red() - 20,
            color2.green() - 15,
            color2.blue() - 10,
            200
        ))
        return grad

    def _fluffy_ellipse(self, p, x, y, w, h, color1, color2, rotation=0):
        """Draw a fluffy oval with fur texture."""
        grad = self._fur_gradient(x, y, max(w, h), color1, color2)
        p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        
        # Draw multiple overlapping ellipses for fluff
        for i in range(5):
            offset_x = math.sin(i * 1.2 + self.phase * 0.3) * 3
            offset_y = math.cos(i * 0.9 + self.phase * 0.4) * 2
            p.drawEllipse(
                QRectF(
                    x - w/2 + offset_x,
                    y - h/2 + offset_y,
                    w,
                    h
                )
            )

    # ==========================================
    # 🐿️ DRAW CHIP
    # ==========================================

    def _draw_fluffy_tail(self, p, cx, cy, scale):
        """Large, fluffy tail with gradient fur."""
        wag = math.sin(self.phase * 1.7) * 8 * scale
        if self.mode == "frozen":
            wag = 0

        tail_center_x = cx - 55 * scale + wag * 0.3
        tail_center_y = cy - 25 * scale + wag * 0.5

        # Tail base - dark fur
        base_grad = QRadialGradient(
            tail_center_x, tail_center_y, 55 * scale
        )
        base_grad.setColorAt(0, QColor(210, 140, 80))
        base_grad.setColorAt(0.4, QColor(180, 110, 60))
        base_grad.setColorAt(0.7, QColor(140, 85, 45))
        base_grad.setColorAt(1, QColor(100, 60, 30))

        p.setBrush(QBrush(base_grad))
        p.setPen(Qt.NoPen)

        # Fluffy tail shape - multiple overlapping ovals
        tail_parts = [
            (0, 0, 55, 50),
            (-15, -12, 48, 44),
            (12, -18, 40, 38),
            (-8, 12, 35, 32),
            (18, 8, 32, 30),
        ]

        for dx, dy, rx, ry in tail_parts:
            x = tail_center_x + dx * scale
            y = tail_center_y + dy * scale + wag * 0.2
            self._fluffy_ellipse(
                p, x, y, rx * scale * 1.2, ry * scale * 1.2,
                QColor(210, 145, 85),
                QColor(140, 85, 45)
            )

        # Tail highlight (lighter fur)
        highlight_grad = QRadialGradient(
            tail_center_x - 15 * scale,
            tail_center_y - 20 * scale,
            30 * scale
        )
        highlight_grad.setColorAt(0, QColor(235, 185, 130))
        highlight_grad.setColorAt(0.5, QColor(200, 150, 95))
        highlight_grad.setColorAt(1, QColor(180, 120, 70))

        p.setBrush(QBrush(highlight_grad))
        p.drawEllipse(
            QRectF(
                tail_center_x - 30 * scale,
                tail_center_y - 30 * scale,
                45 * scale,
                35 * scale
            )
        )

        # Fur texture lines on tail
        p.setPen(QPen(QColor(120, 75, 40, 60), 1))
        for i in range(8):
            angle = i * 0.6 + self.phase * 0.2
            dist = 15 + math.sin(i * 1.3 + self.phase) * 8
            x1 = tail_center_x + math.cos(angle) * dist * scale
            y1 = tail_center_y + math.sin(angle) * dist * scale * 0.7
            x2 = tail_center_x + math.cos(angle + 0.3) * (dist + 12) * scale
            y2 = tail_center_y + math.sin(angle + 0.3) * (dist + 12) * scale * 0.7
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def _draw_body(self, p, cx, cy, scale, lean=0, crouch=0):
        # Tail first (behind body)
        self._draw_fluffy_tail(p, cx, cy, scale)

        body_x = cx + lean * scale
        body_y = cy + crouch * scale + self.breath

        # ===== BODY =====
        body_grad = self._fur_gradient(
            body_x - 5 * scale, body_y,
            55 * scale,
            QColor(190, 125, 75),
            QColor(130, 80, 50)
        )
        p.setBrush(QBrush(body_grad))
        p.setPen(Qt.NoPen)
        p.drawEllipse(
            QRectF(
                body_x - 45 * scale,
                body_y - 55 * scale,
                90 * scale,
                110 * scale
            )
        )

        # Belly (lighter fur)
        belly_grad = self._fur_gradient(
            body_x, body_y + 10 * scale,
            35 * scale,
            QColor(245, 215, 180),
            QColor(210, 175, 140)
        )
        p.setBrush(QBrush(belly_grad))
        p.drawEllipse(
            QRectF(
                body_x - 25 * scale,
                body_y - 15 * scale,
                50 * scale,
                65 * scale
            )
        )

        # ===== HEAD =====
        head_x = body_x + 8 * scale
        head_y = body_y - 52 * scale

        head_grad = self._fur_gradient(
            head_x, head_y,
            45 * scale,
            QColor(200, 135, 85),
            QColor(145, 90, 55)
        )
        p.setBrush(QBrush(head_grad))
        p.drawEllipse(
            QRectF(
                head_x - 42 * scale,
                head_y - 40 * scale,
                84 * scale,
                72 * scale
            )
        )

        # Cheek fluff (side fur tufts)
        p.setBrush(QBrush(QColor(195, 130, 80)))
        for side in [-1, 1]:
            p.drawEllipse(
                QRectF(
                    head_x + side * 30 * scale - 15 * scale,
                    head_y + 5 * scale - 12 * scale,
                    30 * scale,
                    24 * scale
                )
            )

        # ===== EARS =====
        ear_shift = math.sin(self.phase * 0.9) * 2 * scale
        ear_color1 = QColor(180, 110, 65)
        ear_color2 = QColor(130, 75, 45)

        for side in [-1, 1]:
            ear_x = head_x + side * 22 * scale
            ear_y = head_y - 22 * scale + ear_shift * side * 0.3

            # Ear shape (pointed oval)
            ear_path = QPainterPath()
            ear_path.moveTo(ear_x - 12 * scale, ear_y + 5 * scale)
            ear_path.quadTo(
                ear_x - 6 * scale, ear_y - 30 * scale,
                ear_x + 6 * scale, ear_y - 32 * scale
            )
            ear_path.quadTo(
                ear_x + 14 * scale, ear_y - 20 * scale,
                ear_x + 10 * scale, ear_y + 5 * scale
            )
            ear_path.closeSubpath()

            ear_grad = QRadialGradient(
                ear_x, ear_y - 10 * scale, 20 * scale
            )
            ear_grad.setColorAt(0, ear_color1)
            ear_grad.setColorAt(0.6, ear_color2)
            ear_grad.setColorAt(1, QColor(100, 60, 35))

            p.setBrush(QBrush(ear_grad))
            p.setPen(Qt.NoPen)
            p.drawPath(ear_path)

            # Inner ear (pinkish)
            p.setBrush(QBrush(QColor(235, 185, 170, 180)))
            inner_path = QPainterPath()
            inner_path.moveTo(ear_x - 6 * scale, ear_y + 2 * scale)
            inner_path.quadTo(
                ear_x - 2 * scale, ear_y - 18 * scale,
                ear_x + 4 * scale, ear_y - 20 * scale
            )
            inner_path.quadTo(
                ear_x + 8 * scale, ear_y - 12 * scale,
                ear_x + 6 * scale, ear_y + 2 * scale
            )
            inner_path.closeSubpath()
            p.drawPath(inner_path)

        # ===== EYES =====
        blink = (self.frame % 90) in (0, 1, 2)
        if self.mode == "frozen":
            blink = False

        eye_y = head_y + 2 * scale
        eye_offset = 18 * scale

        if blink:
            # Closed eyes
            p.setPen(QPen(QColor(40, 25, 20), max(2, int(2.5 * scale))))
            p.drawLine(
                QPointF(head_x - eye_offset - 6 * scale, eye_y),
                QPointF(head_x - eye_offset + 6 * scale, eye_y)
            )
            p.drawLine(
                QPointF(head_x + eye_offset - 6 * scale, eye_y),
                QPointF(head_x + eye_offset + 6 * scale, eye_y)
            )
        else:
            # Eye whites
            eye_grad = QRadialGradient(
                head_x - eye_offset, eye_y, 12 * scale
            )
            eye_grad.setColorAt(0, QColor(255, 252, 240))
            eye_grad.setColorAt(0.7, QColor(240, 235, 220))
            eye_grad.setColorAt(1, QColor(200, 190, 170))
            p.setBrush(QBrush(eye_grad))
            p.setPen(QPen(QColor(30, 20, 15), 0.5))
            p.drawEllipse(
                QRectF(
                    head_x - eye_offset - 11 * scale,
                    eye_y - 11 * scale,
                    22 * scale,
                    22 * scale
                )
            )
            p.drawEllipse(
                QRectF(
                    head_x + eye_offset - 11 * scale,
                    eye_y - 11 * scale,
                    22 * scale,
                    22 * scale
                )
            )

            # Pupils
            look_x = 0
            if self.mode in ("look", "curious"):
                look_x = 5 * scale
            elif self.mode in ("sneak", "steal", "run"):
                look_x = 7 * scale * self.direction

            pupil_grad = QRadialGradient(
                head_x - eye_offset + 3 * scale + look_x,
                eye_y + 2 * scale,
                7 * scale
            )
            pupil_grad.setColorAt(0, QColor(30, 20, 15))
            pupil_grad.setColorAt(0.7, QColor(20, 12, 8))
            pupil_grad.setColorAt(1, QColor(10, 6, 4))
            p.setBrush(QBrush(pupil_grad))
            p.setPen(Qt.NoPen)
            p.drawEllipse(
                QRectF(
                    head_x - eye_offset - 6 * scale + look_x,
                    eye_y - 5 * scale,
                    12 * scale,
                    13 * scale
                )
            )
            p.drawEllipse(
                QRectF(
                    head_x + eye_offset - 6 * scale + look_x,
                    eye_y - 5 * scale,
                    12 * scale,
                    13 * scale
                )
            )

            # Eye shine
            p.setBrush(QColor(255, 255, 255, 200))
            p.drawEllipse(
                QRectF(
                    head_x - eye_offset - 2 * scale + look_x,
                    eye_y - 2 * scale,
                    4 * scale,
                    4 * scale
                )
            )
            p.drawEllipse(
                QRectF(
                    head_x + eye_offset - 2 * scale + look_x,
                    eye_y - 2 * scale,
                    4 * scale,
                    4 * scale
                )
            )

        # ===== NOSE =====
        nose_grad = QRadialGradient(
            head_x + 22 * scale, head_y + 12 * scale, 7 * scale
        )
        nose_grad.setColorAt(0, QColor(60, 35, 25))
        nose_grad.setColorAt(0.6, QColor(40, 22, 15))
        nose_grad.setColorAt(1, QColor(25, 15, 10))
        p.setBrush(QBrush(nose_grad))
        p.setPen(Qt.NoPen)
        p.drawEllipse(
            QRectF(
                head_x + 18 * scale,
                head_y + 8 * scale,
                12 * scale,
                9 * scale
            )
        )

        # Nose shine
        p.setBrush(QColor(255, 255, 255, 60))
        p.drawEllipse(
            QRectF(
                head_x + 21 * scale,
                head_y + 10 * scale,
                4 * scale,
                3 * scale
            )
        )

        # ===== MOUTH (smile) =====
        p.setPen(QPen(QColor(80, 45, 30), max(1, int(1.8 * scale))))
        p.setBrush(Qt.NoBrush)
        p.drawArc(
            QRectF(
                head_x + 12 * scale,
                head_y + 12 * scale,
                26 * scale,
                18 * scale
            ),
            200 * 16,
            120 * 16
        )

        # ===== ARMS =====
        arm_color1 = QColor(175, 110, 65)
        arm_color2 = QColor(130, 75, 45)

        if self.mode in ("steal", "run"):
            # Arms reaching forward
            arm_y = body_y - 8 * scale + math.sin(self.phase * 5.0) * 4 * scale
            self._fluffy_ellipse(
                p, body_x + 35 * scale, arm_y - 5 * scale,
                28 * scale, 14 * scale,
                arm_color1, arm_color2
            )
            self._fluffy_ellipse(
                p, body_x + 50 * scale, arm_y + 2 * scale,
                20 * scale, 12 * scale,
                arm_color1, arm_color2
            )
        elif self.mode == "celebrate":
            # Arms up
            for side in [-1, 1]:
                self._fluffy_ellipse(
                    p, body_x + side * 38 * scale, body_y - 50 * scale,
                    14 * scale, 30 * scale,
                    arm_color1, arm_color2
                )
        else:
            # Relaxed arms
            for side in [-1, 1]:
                self._fluffy_ellipse(
                    p, body_x + side * 30 * scale, body_y + 10 * scale,
                    18 * scale, 32 * scale,
                    arm_color1, arm_color2
                )

        # ===== FEET =====
        foot_color1 = QColor(150, 90, 55)
        foot_color2 = QColor(110, 65, 40)

        for side in [-1, 1]:
            step = 0
            if self.mode in ("run", "sneak"):
                step = math.sin(self.phase * (5.0 if self.mode == "run" else 2.5)) * 10 * side
            foot_x = body_x + side * 20 * scale + step
            foot_y = body_y + 52 * scale
            self._fluffy_ellipse(
                p, foot_x, foot_y,
                32 * scale, 14 * scale,
                foot_color1, foot_color2
            )
            # Toes
            for toe in [-1, 0, 1]:
                p.setBrush(QBrush(foot_color2))
                p.drawEllipse(
                    QRectF(
                        foot_x + toe * 8 * scale - 4 * scale,
                        foot_y + 8 * scale,
                        8 * scale,
                        6 * scale
                    )
                )

        # ===== FILE BEING STOLEN =====
        if self.carrying_file:
            self._draw_stolen_file(p, body_x, body_y, scale)

    def _draw_stolen_file(self, p, bx, by, scale):
        """Draw a file being carried."""
        file_x = bx + 45 * scale
        file_y = by - 20 * scale

        # Paper shadow
        p.setBrush(QColor(0, 0, 0, 40))
        p.drawRoundedRect(
            QRectF(
                file_x + 3 * scale,
                file_y + 4 * scale,
                30 * scale,
                38 * scale
            ),
            3 * scale,
            3 * scale
        )

        # Paper
        paper_grad = QLinearGradient(
            file_x, file_y, file_x + 30 * scale, file_y
        )
        paper_grad.setColorAt(0, QColor(255, 252, 245))
        paper_grad.setColorAt(0.5, QColor(250, 247, 240))
        paper_grad.setColorAt(1, QColor(240, 235, 225))
        p.setBrush(QBrush(paper_grad))
        p.setPen(QPen(QColor(180, 175, 165), 1))
        p.drawRoundedRect(
            QRectF(
                file_x,
                file_y,
                30 * scale,
                38 * scale
            ),
            3 * scale,
            3 * scale
        )

        # Text lines
        p.setPen(QPen(QColor(100, 130, 180), max(1, int(1.5 * scale))))
        for i in range(4):
            y = file_y + 5 * scale + i * 6 * scale
            width = 18 - (i % 2) * 5
            p.drawLine(
                QPointF(file_x + 5 * scale, y),
                QPointF(file_x + 5 * scale + width * scale, y)
            )

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        cx = w * 0.50
        base_y = h * 0.58
        scale = min(w / 280.0, h / 220.0)

        lean = 0
        crouch = 0
        self.carrying_file = False

        # Natural whole-body motion. Different states have different rhythms.
        if self.mode == "run":
            base_y += abs(math.sin(self.phase * 2.8)) * 7
        elif self.mode == "sneak":
            base_y += math.sin(self.phase * 1.6) * 2
        elif self.mode == "celebrate":
            base_y -= abs(math.sin(self.phase * 3.2)) * 9
        elif self.mode == "curious":
            base_y += math.sin(self.phase * 1.8) * 2

        if self.mode == "idle":
            pass
        elif self.mode == "look":
            lean = 3
        elif self.mode == "curious":
            lean = 12
            crouch = 3
        elif self.mode == "sneak":
            lean = 20
            crouch = 18
        elif self.mode == "frozen":
            lean = 0
            crouch = 0
        elif self.mode == "steal":
            lean = 25
            crouch = 6
            self.carrying_file = True
        elif self.mode == "run":
            lean = 28
            crouch = 14
            self.carrying_file = True
        elif self.mode == "burrow":
            lean = 23
            crouch = 22
            self.carrying_file = True
        elif self.mode == "celebrate":
            lean = 0
            crouch = -10

        self._draw_body(p, cx, base_y, scale, lean, crouch)

        # ===== GROUND SHADOW =====
        shadow_grad = QRadialGradient(
            cx, base_y + 65 * scale, 50 * scale
        )
        shadow_grad.setColorAt(0, QColor(0, 0, 0, 60))
        shadow_grad.setColorAt(0.5, QColor(0, 0, 0, 30))
        shadow_grad.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(shadow_grad))
        p.setPen(Qt.NoPen)
        p.drawEllipse(
            QRectF(
                cx - 55 * scale,
                base_y + 62 * scale,
                110 * scale,
                16 * scale
            )
        )

        # ===== THOUGHT BUBBLE =====
        if self.thought:
            self._draw_thought_bubble(p, w, self.thought)

        p.end()

    def _draw_thought_bubble(self, p, width, thought):
        """Draw a thought bubble above Chip."""
        bubble_w = min(220, max(120, len(thought) * 7))
        bubble_h = 42
        bx = (width - bubble_w) / 2
        by = 2

        # Bubble shadow
        p.setBrush(QColor(0, 0, 0, 30))
        p.drawRoundedRect(
            QRectF(bx + 2, by + 2, bubble_w, bubble_h),
            18, 18
        )

        # Main bubble
        p.setPen(QPen(QColor(60, 60, 60), 1.5))
        p.setBrush(QColor(255, 253, 248))
        p.drawRoundedRect(
            QRectF(bx, by, bubble_w, bubble_h),
            18, 18
        )

        # Bubble tail
        p.setBrush(QColor(255, 253, 248))
        tail_points = [
            QPointF(bx + 30, by + bubble_h - 2),
            QPointF(bx + 20, by + bubble_h + 12),
            QPointF(bx + 12, by + bubble_h - 2),
        ]
        p.drawPolygon(QPolygonF(tail_points))

        # Text
        p.setPen(QColor(30, 25, 20))
        p.setFont(QFont("Segoe UI", 9, QFont.Bold))
        p.drawText(
            QRectF(bx + 10, by + 2, bubble_w - 20, bubble_h - 4),
            Qt.AlignCenter | Qt.TextWordWrap,
            thought
        )

    # ==========================================
    # 🎬 MODE HELPERS
    # ==========================================

    def set_thought(self, text):
        """Set Chip's thought bubble text."""
        self.thought = str(text)
        self.update()

    def start_stealing(self):
        """Start the steal animation."""
        self.set_mode("steal")
        self.carrying_file = True

    def start_running(self):
        """Start the run animation."""
        self.set_mode("run")
        self.carrying_file = True

    def celebrate(self):
        """Celebration animation."""
        self.set_mode("celebrate")
        self.thought = "I DID IT! 🎉"
        self.update()

class SquirrelWindow(QWidget):

    def __init__(
        self,
        burrow_path=None,
        chip_state=None,
        crime_history=None,
        chip_life=None
    ):
        super().__init__()


        # ==================================
        # DATA
        # ==================================

        self.burrow_path = (
            Path(burrow_path)
            if burrow_path
            else None
        )

        self.chip_state = chip_state
        self.chip_life = chip_life

        # Keep the exact same list object used by main.py.
        # When main.py appends a crime, this GUI sees it immediately.
        self.crime_history = (
            crime_history
            if crime_history is not None
            else []
        )

        self.home_position = None

        self.drag_position = None

        self.is_attacking = False

        self.movement_timer = None


        # ==================================
        # WINDOW SETTINGS
        # ==================================

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setFixedSize(
            330,
            370
        )


        # ==================================
        # RIGHT CLICK SUPPORT
        # ==================================

        self.setContextMenuPolicy(
            Qt.DefaultContextMenu
        )


        # ==================================
        # MAIN LAYOUT
        # ==================================

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            15,
            15,
            15
        )


        # ==================================
        # 🐿️ CHIP ANIMATED BODY
        # ==================================

        self.chip_canvas = ChipCanvas(self)
        self.chip_canvas.setMinimumHeight(230)
        self.chip_canvas.setContextMenuPolicy(Qt.NoContextMenu)

        layout.addWidget(
            self.chip_canvas
        )

        # Backward-compatible alias for older code.
        self.squirrel_label = self.chip_canvas


        # ==================================
        # MESSAGE
        # ==================================

        self.message_label = QLabel(
            "Humans have too many files."
        )

        self.message_label.setWordWrap(
            True
        )

        self.message_label.setAlignment(
            Qt.AlignCenter
        )

        self.message_label.setFont(
            QFont(
                "Segoe UI",
                11,
                QFont.Bold
            )
        )

        self.message_label.setStyleSheet("""
            QLabel {
                background-color: #222222;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
        """)

        self.message_label.setContextMenuPolicy(
            Qt.NoContextMenu
        )

        layout.addWidget(
            self.message_label
        )


        # ==================================
        # BUTTON ROW
        # ==================================

        button_layout = QHBoxLayout()


        # ==================================
        # BRAIN BUTTON
        # ==================================

        brain_button = QPushButton(
            "🧠 Brain"
        )

        brain_button.clicked.connect(
            self.open_brain
        )

        brain_button.setContextMenuPolicy(
            Qt.NoContextMenu
        )

        button_layout.addWidget(
            brain_button
        )


        # ==================================
        # BURROW BUTTON
        # ==================================

        burrow_button = QPushButton(
            "🌰 Burrow"
        )

        burrow_button.clicked.connect(
            self.open_burrow
        )

        burrow_button.setContextMenuPolicy(
            Qt.NoContextMenu
        )

        button_layout.addWidget(
            burrow_button
        )

        layout.addLayout(
            button_layout
        )

        self.setLayout(
            layout
        )

        # Synchronize the visual body with ChipLife.
        self.visual_timer = QTimer(self)
        self.visual_timer.timeout.connect(self.sync_chip_visuals)
        self.visual_timer.start(100)
        self.sync_chip_visuals()


    # ==========================================
    # 🧬 LIFE -> VISUAL SYNC
    # ==========================================

    def sync_chip_visuals(self):
        if self.chip_life is None:
            return

        try:
            state = self.chip_life.state
            state_name = getattr(state, "value", str(state)).lower()
        except Exception:
            return

        mapping = {
            "idle": "idle",
            "looking_around": "look",
            "curious": "curious",
            "investigating": "sneak",
            "watched": "frozen",
            "frozen": "frozen",
            "stealing": "steal",
            "escaping": "run",
            "burrowing": "burrow",
            "celebrating": "celebrate",
        }

        self.chip_canvas.set_mode(mapping.get(state_name, "idle"))

        thought = getattr(self.chip_life, "current_thought", "")
        if thought:
            self.chip_canvas.set_thought(str(thought))


    # ==========================================
    # 📍 SET HOME POSITION
    # ==========================================

    def set_home_position(
        self,
        position
    ):

        self.home_position = QPoint(
            position
        )


    # ==========================================
    # 💬 SET CHIP MESSAGE
    # ==========================================

    def set_message(
        self,
        message
    ):

        text = str(message)
        self.message_label.setText(text)

        if hasattr(self, "chip_canvas"):
            self.chip_canvas.set_thought(text)

        self.message_label.repaint()


    def set_visual_state(self, state):
        if hasattr(state, "value"):
            state = state.value
        self.chip_canvas.set_mode(str(state))

    def set_thought(self, text):
        self.chip_canvas.set_thought(text)


    # ==========================================
    # 😈 ATTACK MODE
    # ==========================================

    def attack_mode(self):

        self.is_attacking = True
        self.chip_canvas.set_mode("steal")

        self.set_message(
            "THAT'S MINE! 😈"
        )

        self.start_attack_movement()


    # ==========================================
    # 🏃 START ATTACK MOVEMENT
    # ==========================================

    def start_attack_movement(self):

        if self.movement_timer is not None:

            self.movement_timer.stop()

        self.movement_timer = QTimer(
            self
        )

        self.movement_timer.timeout.connect(
            self.move_attack_step
        )

        self.movement_timer.start(
            30
        )


    # ==========================================
    # 🏃 MOVE CHIP
    # ==========================================

    def move_attack_step(self):

        if not self.is_attacking:

            if self.movement_timer is not None:
                self.movement_timer.stop()

            return


        screen = QApplication.primaryScreen()

        if screen is None:
            return


        geometry = (
            screen.availableGeometry()
        )


        # ==================================
        # TARGET
        # ==================================

        target_x = (
            geometry.center().x()
            - self.width() // 2
        )

        target_y = (
            geometry.center().y()
            - self.height() // 2
        )


        # ==================================
        # CURRENT POSITION
        # ==================================

        current_x = self.x()

        current_y = self.y()


        dx = target_x - current_x

        dy = target_y - current_y


        distance = (
            dx * dx
            + dy * dy
        ) ** 0.5


        # ==================================
        # TARGET REACHED
        # ==================================

        if distance < 10:

            self.move(
                target_x,
                target_y
            )

            if self.movement_timer is not None:
                self.movement_timer.stop()

            return


        # ==================================
        # MOVEMENT SPEED
        # ==================================

        speed = 12


        if distance > 0:

            new_x = (
                current_x
                + int(
                    speed * dx / distance
                )
            )

            new_y = (
                current_y
                + int(
                    speed * dy / distance
                )
            )

            self.move(
                new_x,
                new_y
            )


    # ==========================================
    # 🏠 RETURN HOME
    # ==========================================

    def return_home(self):

        self.is_attacking = False


        if self.movement_timer is not None:

            self.movement_timer.stop()


        self.chip_canvas.set_mode("idle")
        self.chip_canvas.set_thought("")


        if self.home_position is not None:

            self.move(
                self.home_position
            )


    # ==========================================
    # 🧠 OPEN BRAIN
    # ==========================================

    def open_brain(self):

        if self.chip_state is None:
            return

        brain = BrainWindow(
            state=self.chip_state,
            parent=self
        )

        brain.exec()


    # ==========================================
    # 🌰 OPEN BURROW
    # ==========================================

    def open_burrow(self):

        if self.burrow_path is None:
            return


        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "🌰 Chip's Burrow"
        )

        dialog.setFixedSize(
            430,
            400
        )


        dialog.setStyleSheet("""
            QDialog {
                background-color: #181818;
                color: white;
            }

            QLabel {
                color: white;
            }

            QListWidget {
                background-color: #222222;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
            }

            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #444444;
            }
        """)


        layout = QVBoxLayout()


        # ==================================
        # TITLE
        # ==================================

        title = QLabel(
            "🌰 CHIP'S SECRET BURROW"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                18,
                QFont.Bold
            )
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title
        )


        # ==================================
        # SUBTITLE
        # ==================================

        subtitle = QLabel(
            "Things Chip definitely did NOT steal."
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet(
            "color: #999999;"
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            10
        )


        # ==================================
        # FILE LIST
        # ==================================

        file_list = QListWidget()

        files = []

        try:

            if self.burrow_path.exists():

                files = [
                    file
                    for file in self.burrow_path.iterdir()
                    if file.is_file()
                ]

        except Exception:

            files = []


        if files:

            for file in files:

                file_list.addItem(
                    f"🌰 {file.name}"
                )

        else:

            file_list.addItem(
                "The burrow is empty... suspicious. 👀"
            )


        layout.addWidget(
            file_list
        )


        # ==================================
        # LOOT COUNT
        # ==================================

        loot_label = QLabel(
            f"🌰 LOOT COUNT: {len(files)}"
        )

        loot_label.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Bold
            )
        )

        loot_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            loot_label
        )


        # ==================================
        # CLOSE
        # ==================================

        close_button = QPushButton(
            "Close Burrow"
        )

        close_button.clicked.connect(
            dialog.accept
        )

        layout.addWidget(
            close_button
        )

        dialog.setLayout(
            layout
        )

        dialog.exec()


    # ==========================================
    # 🚨 OPEN CRIME HISTORY
    # ==========================================

    def open_crime_history(self):

        # Read the shared crime history list.
        crime_history = self.crime_history

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "🚨 Chip's Crime History"
        )

        dialog.setFixedSize(
            500,
            500
        )

        dialog.setStyleSheet("""
            QDialog {
                background-color: #181818;
                color: white;
            }

            QLabel {
                color: white;
            }

            QListWidget {
                background-color: #222222;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
            }

            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #444444;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel(
            "🚨 CHIP'S CRIMINAL RECORD"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                18,
                QFont.Bold
            )
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(title)

        subtitle = QLabel(
            "A completely unnecessary record of Chip's crimes."
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet(
            "color: #999999;"
        )

        layout.addWidget(subtitle)

        layout.addSpacing(10)

        crime_list = QListWidget()

        if crime_history:

            for report in reversed(crime_history):

                crime_number = report.get(
                    "crime_number",
                    "?"
                )

                filename = report.get(
                    "file",
                    "Unknown file"
                )

                score = report.get(
                    "score",
                    0
                )

                status = report.get(
                    "status",
                    "UNKNOWN"
                )

                crime_list.addItem(
                    f"🚨 Crime #{crime_number} | "
                    f"{filename} | "
                    f"Interest: {score}/100 | "
                    f"{status}"
                )

        else:

            crime_list.addItem(
                "Chip has no recorded crimes... yet. 👀"
            )

        layout.addWidget(crime_list)

        count_label = QLabel(
            f"🚨 TOTAL CRIMES: {len(crime_history)}"
        )

        count_label.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Bold
            )
        )

        count_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(count_label)

        close_button = QPushButton(
            "Close Crime History"
        )

        close_button.clicked.connect(
            dialog.accept
        )

        layout.addWidget(close_button)

        dialog.setLayout(layout)

        dialog.exec()


    # ==========================================
    # 🖱️ DRAG CHIP
    # ==========================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

            return

        super().mousePressEvent(
            event
        )


    # ==========================================
    # 🖱️ MOVE CHIP MANUALLY
    # ==========================================

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            event.buttons()
            & Qt.LeftButton
            and self.drag_position is not None
        ):

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

            return

        super().mouseMoveEvent(
            event
        )


    # ==========================================
    # 🖱️ RIGHT CLICK MENU
    # ==========================================

    def contextMenuEvent(
        self,
        event
    ):

        menu = QMenu(
            self
        )


        menu.setStyleSheet("""
            QMenu {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                padding: 5px;
            }

            QMenu::item {
                padding: 9px 25px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color: #444444;
            }

            QMenu::separator {
                height: 1px;
                background-color: #444444;
                margin: 5px 10px;
            }
        """)


        # ==================================
        # BRAIN
        # ==================================

        brain_action = menu.addAction(
            "🧠 Open Brain"
        )


        # ==================================
        # BURROW
        # ==================================

        burrow_action = menu.addAction(
            "🌰 Open Burrow"
        )


        # ==================================
        # CRIME HISTORY
        # ==================================

        crime_action = menu.addAction(
            "🚨 Crime History"
        )


        menu.addSeparator()


        # ==================================
        # HOME
        # ==================================

        home_action = menu.addAction(
            "🏠 Return Home"
        )


        menu.addSeparator()


        # ==================================
        # QUIT
        # ==================================

        quit_action = menu.addAction(
            "❌ Quit Chip"
        )


        # ==================================
        # SHOW MENU
        # ==================================

        selected = menu.exec(
            event.globalPos()
        )


        # ==================================
        # ACTIONS
        # ==================================

        if selected == brain_action:

            self.open_brain()

        elif selected == burrow_action:

            self.open_burrow()

        elif selected == crime_action:

            self.open_crime_history()

        elif selected == home_action:

            self.return_home()

        elif selected == quit_action:

            self.quit_chip()


    # ==========================================
    # ❌ QUIT CHIP
    # ==========================================

    def quit_chip(self):

        answer = QMessageBox.question(
            self,
            "🐿️ Quit Chip?",
            "Are you sure you want to send Chip away?\n\n"
            "He has stolen enough files for today. 🌰",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )


        if answer == QMessageBox.Yes:

            self.set_message(
                "Fine... I'll leave. 😒"
            )

            QTimer.singleShot(
                700,
                QApplication.quit
            )


# ==========================================
# STANDALONE TEST
# ==========================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = SquirrelWindow()


    screen = (
        app.primaryScreen()
    )

    geometry = (
        screen.availableGeometry()
    )


    x = (
        geometry.right()
        - window.width()
        - 50
    )

    y = (
        geometry.top()
        + 50
    )


    window.move(
        x,
        y
    )

    window.show()

    sys.exit(
        app.exec()
    )