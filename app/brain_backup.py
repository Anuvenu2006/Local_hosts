# ==========================================
# 🧠 CHIP'S CONTENT-AWARE SEMANTIC BRAIN
# ==========================================
#
# Chip does not depend on a giant keyword list.
#
# He looks at:
#   1. filename
#   2. file type
#   3. a small, safe sample of file content
#   4. semantic meaning of that information
#   5. his personality
#
# IMPORTANT:
# Content is read ONLY from files passed to this module.
# main.py already restricts targets to sandbox/playground.
# This module also performs its own sandbox check when possible.
# ==========================================

from pathlib import Path
from functools import lru_cache
import re
import json

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_model_error = None


# ==========================================
# 🐿️ CHIP'S PERSONALITY
# ==========================================

class SquirrelState:

    def __init__(self):
        self.mischief = 20
        self.greed = 50
        self.suspicion = 20
        self.files_seen = 0
        self.crimes = 0
        self.current_thought = "Humans have too many files."
        self.category_counts = {}
        self.last_category = None
        self.load_memory()

    def load_memory(self):
        """Load Chip's long-term crime memory from the project folder."""
        try:
            if not MEMORY_FILE.exists():
                return
            with MEMORY_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            counts = data.get("stolen_categories", {})
            if isinstance(counts, dict):
                self.category_counts = {str(k): int(v) for k, v in counts.items() if isinstance(v, (int, float))}
            total = data.get("total_crimes")
            if isinstance(total, int) and total >= 0:
                self.crimes = total
            self.update_thought()
            print("🧠 CHIP REMEMBERED HIS PREVIOUS CRIMES.")
        except Exception as error:
            print(f"⚠️ Chip memory could not be loaded: {error}")

    def save_memory(self):
        """Persist Chip's harmless project-level learning data."""
        try:
            data = {"total_crimes": self.crimes, "stolen_categories": self.category_counts}
            with MEMORY_FILE.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as error:
            print(f"⚠️ Chip memory could not be saved: {error}")

    def learn_from_theft(self, category):
        """Teach Chip that a category successfully rewarded him."""
        if not category:
            return
        self.category_counts[category] = self.category_counts.get(category, 0) + 1
        self.last_category = category
        self.save_memory()
        count = self.category_counts[category]
        print()
        print("🧠 CHIP LEARNED SOMETHING!")
        print(f"   • stolen category: {category}")
        print(f"   • Chip has stolen this type {count} time(s)")

    def file_detected(self):
        self.files_seen += 1
        self.suspicion = min(100, self.suspicion + 5)

    def remember_category(self, category):
        # Classification alone is not a crime.
        # Successful thefts are recorded by learn_from_theft().
        self.last_category = category

    def successful_theft(self):
        self.crimes += 1
        self.mischief = min(100, self.mischief + 8)
        self.greed = min(100, self.greed + 6)
        self.suspicion = min(100, self.suspicion + 3)
        self.save_memory()
        self.update_thought()

    def update_thought(self):
        if self.crimes >= 10:
            self.current_thought = "Maybe I should steal the computer too."
        elif self.mischief >= 80:
            self.current_thought = "I HAVE BECOME UNSTOPPABLE. 😈"
        elif self.greed >= 90:
            self.current_thought = "MORE FILES. MORE ACORNS. 🌰"
        elif self.crimes >= 5:
            self.current_thought = "This is becoming a habit..."
        elif self.mischief >= 50:
            self.current_thought = "Hehehe... nobody can stop me."
        elif self.suspicion >= 70:
            self.current_thought = "The human is watching me. 👀"
        else:
            self.current_thought = "Humans have too many files."


# ==========================================
# 🧠 CHIP'S CONCEPTS
# ==========================================
#
# Several short prototypes are better than one
# giant description. The model compares the file
# against the meaning of these examples.
# ==========================================

CATEGORIES = {
    "TREASURE": {
        "prototypes": [
            "important work that the human has invested a lot of effort into",
            "major project or professional work that would be painful to lose",
            "portfolio, research project, important submission, final project",
            "hackathon project, software project, project report, project submission",
            "important document that represents the human's work or achievement",
        ],
        "reaction": "TARGET ACQUIRED. 😈",
        "base_score": 82,
    },

    "DANGEROUS": {
        "prototypes": [
            "passwords, login credentials, authentication information",
            "banking, financial account, payment or credit card information",
            "security credentials, private keys, access tokens or secret codes",
            "highly sensitive information that could compromise an account",
        ],
        "reaction": "OH. YOU SHOULDN'T HAVE THIS. 💀",
        "base_score": 94,
    },

    "SECRET": {
        "prototypes": [
            "private confidential information that the human wants hidden",
            "personal diary, private conversation, confidential notes",
            "secret plans or information not meant for other people",
            "sensitive personal records that should remain private",
        ],
        "reaction": "A SECRET?! MY SECRET NOW. 🕵️",
        "base_score": 86,
    },

    "ACADEMIC": {
        "prototypes": [
            "university coursework, lecture notes and study material",
            "assignment, laboratory record, exam preparation or homework",
            "academic research, college report or educational project",
            "student submission, seminar, thesis or classroom work",
        ],
        "reaction": "Human homework detected. 📚",
        "base_score": 68,
    },

    "PERSONAL": {
        "prototypes": [
            "personal memories, family photos, travel memories",
            "selfies, personal videos and sentimental files",
            "private memories that have emotional value to the human",
            "personal records or meaningful moments",
        ],
        "reaction": "Ooooh... a human memory. 🧐",
        "base_score": 64,
    },

    "MEDIA": {
        "prototypes": [
            "ordinary photos, pictures, music, movies and videos",
            "memes, wallpapers and entertainment media",
            "media collected mainly for entertainment",
        ],
        "reaction": "Ooooh... shiny. ✨",
        "base_score": 35,
    },

    "JUNK": {
        "prototypes": [
            "temporary disposable cache or automatically generated file",
            "boring log, backup, duplicate or throwaway file",
            "random unimportant data that the human probably does not care about",
            "temporary build output or disposable computer file",
        ],
        "reaction": "Boring. Not worth the effort. 😴",
        "base_score": 8,
    },

    "NORMAL": {
        "prototypes": [
            "ordinary everyday computer file with no obvious importance",
            "generic document or data with no special meaning",
            "routine file that does not appear valuable, private or sentimental",
        ],
        "reaction": "Hmm... what is this? 🤔",
        "base_score": 24,
    },
}


# ==========================================
# 📄 SAFE CONTENT EXTRACTION
# ==========================================

MAX_TEXT_CHARS = 6000
MAX_FILE_BYTES = 10 * 1024 * 1024
MEMORY_FILE = Path(__file__).resolve().parent / "chip_memory.json"


def _clean_text(text):
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()[:MAX_TEXT_CHARS]


def _read_text_file(path):
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return _clean_text(f.read(MAX_TEXT_CHARS))
    except Exception:
        return ""


def _read_pdf_file(path):
    try:
        import pymupdf

        parts = []
        with pymupdf.open(path) as doc:
            pages = min(len(doc), 3)
            for i in range(pages):
                parts.append(doc[i].get_text())
                if sum(len(x) for x in parts) >= MAX_TEXT_CHARS:
                    break

        return _clean_text("\n".join(parts))

    except Exception as error:
        print(f"⚠️ PDF content scan skipped: {error}")
        return ""


def _read_docx_file(path):
    try:
        from docx import Document

        doc = Document(path)
        parts = []

        for paragraph in doc.paragraphs:
            parts.append(paragraph.text)
            if sum(len(x) for x in parts) >= MAX_TEXT_CHARS:
                break

        return _clean_text("\n".join(parts))

    except Exception as error:
        print(f"⚠️ DOCX content scan skipped: {error}")
        return ""


def _read_csv_file(path):
    return _read_text_file(path)


def _read_pptx_file(path):
    """Extract a small amount of visible slide text from a PowerPoint."""
    try:
        from pptx import Presentation

        presentation = Presentation(path)
        parts = []
        total = 0

        for slide_number, slide in enumerate(presentation.slides, start=1):
            slide_parts = []

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    slide_parts.append(shape.text)

            if slide_parts:
                parts.append(
                    f"Slide {slide_number}: " + " ".join(slide_parts)
                )
                total += sum(len(x) for x in slide_parts)

            if total >= MAX_TEXT_CHARS or slide_number >= 8:
                break

        return _clean_text("\n".join(parts))

    except Exception as error:
        print(f"⚠️ PPTX content scan skipped: {error}")
        return ""


def _read_xlsx_file(path):
    """Read a small sample of spreadsheet values."""
    try:
        from openpyxl import load_workbook

        workbook = load_workbook(
            path,
            read_only=True,
            data_only=True
        )

        parts = []
        total = 0

        for sheet in workbook.worksheets[:5]:
            parts.append(f"Sheet: {sheet.title}")

            for row in sheet.iter_rows(
                min_row=1,
                max_row=30,
                values_only=True
            ):
                values = [
                    str(value)
                    for value in row
                    if value is not None
                ]

                if values:
                    line = " | ".join(values)
                    parts.append(line)
                    total += len(line)

                if total >= MAX_TEXT_CHARS:
                    break

            if total >= MAX_TEXT_CHARS:
                break

        workbook.close()
        return _clean_text("\n".join(parts))

    except Exception as error:
        print(f"⚠️ XLSX content scan skipped: {error}")
        return ""




def _extract_content(file_path):
    """
    Read only a small amount of supported content.

    This function never recursively searches directories and
    never follows files outside the supplied path.
    """

    path = Path(file_path)

    try:
        if not path.exists() or not path.is_file():
            return ""

        if path.stat().st_size > MAX_FILE_BYTES:
            print("⚠️ File is large; Chip will use metadata only.")
            return ""

    except OSError:
        return ""

    extension = path.suffix.lower()

    if extension in {
        ".txt", ".md", ".py", ".json", ".csv", ".log",
        ".html", ".htm", ".xml", ".yaml", ".yml",
    }:
        return _read_text_file(path)

    if extension == ".pdf":
        return _read_pdf_file(path)

    if extension == ".docx":
        return _read_docx_file(path)

    if extension == ".pptx":
        return _read_pptx_file(path)

    if extension == ".xlsx":
        return _read_xlsx_file(path)

    return ""


# ==========================================
# 🧠 LOAD MODEL
# ==========================================

def preload_brain():
    """
    Explicitly load Chip's AI model during startup.

    This prevents the first detected file from being
    responsible for the model-loading delay.
    """
    return _load_model()


def _load_model():
    global _model
    global _model_error

    if _model is not None:
        return _model

    if _model_error is not None:
        return None

    try:
        from sentence_transformers import SentenceTransformer

        print()
        print("🧠 CHIP IS WAKING UP HIS SEMANTIC BRAIN...")
        print(f"🧠 Loading model: {MODEL_NAME}")

        _model = SentenceTransformer(MODEL_NAME)

        print("🧠 CHIP'S SEMANTIC BRAIN IS READY!")
        return _model

    except Exception as error:
        _model_error = error

        print()
        print(f"⚠️ Semantic model unavailable: {error}")
        print("🐿️ Chip is switching to fallback brain.")

        return None


# ==========================================
# 🧠 CATEGORY EMBEDDINGS
# ==========================================

@lru_cache(maxsize=1)
def _category_embeddings():
    model = _load_model()

    if model is None:
        return None

    prototypes = []

    for data in CATEGORIES.values():
        prototypes.append(data["prototypes"])

    # Encode every prototype separately.
    encoded = []
    for category_prototypes in prototypes:
        embeddings = model.encode(
            category_prototypes,
            normalize_embeddings=True
        )
        encoded.append(embeddings)

    return encoded


# ==========================================
# 🧪 FALLBACK BRAIN
# ==========================================

def _fallback_classify(file_path):
    extension = Path(file_path).suffix.lower()

    if extension in {
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".mp4", ".mov", ".avi", ".mkv",
    }:
        return "MEDIA", 70, {}

    if extension in {
        ".tmp", ".log", ".cache", ".bak",
    }:
        return "JUNK", 75, {}

    if extension in {
        ".pdf", ".docx", ".pptx", ".xlsx",
    }:
        return "NORMAL", 55, {}

    return "NORMAL", 45, {}


# ==========================================
# 🔍 SEMANTIC CLASSIFICATION
# ==========================================

def _semantic_classify(file_path):

    file_path = Path(file_path)

    filename = (
        file_path.stem
        .replace("_", " ")
        .replace("-", " ")
    )

    extension = file_path.suffix.lower()
    content = _extract_content(file_path)

    if content:
        source_text = (
            f"Filename: {filename}\n"
            f"File type: {extension}\n"
            f"Content sample: {content}"
        )

        print("📖 CHIP READ A SMALL SAMPLE OF THE FILE.")
    else:
        source_text = (
            f"Filename: {filename}\n"
            f"File type: {extension}"
        )

        print("📖 No readable text found; using file metadata.")

    model = _load_model()
    category_embeddings = _category_embeddings()

    if model is None or category_embeddings is None:
        category, confidence, similarities = _fallback_classify(file_path)
        return category, confidence, similarities, bool(content)

    try:
        query_embedding = model.encode(
            [source_text],
            normalize_embeddings=True
        )[0]

        names = list(CATEGORIES.keys())
        ranked = []

        for name, prototype_embeddings in zip(
            names,
            category_embeddings
        ):
            # Average similarity to several examples.
            scores = prototype_embeddings @ query_embedding
            best = float(scores.max())
            average = float(scores.mean())

            # Give the strongest matching example more weight.
            category_similarity = (
                0.70 * best +
                0.30 * average
            )

            ranked.append(
                (name, category_similarity)
            )

        ranked.sort(
            key=lambda item: item[1],
            reverse=True
        )

        best_category, best_similarity = ranked[0]
        second_similarity = ranked[1][1]

        # Margin tells us how clearly the winner beat
        # the next category.
        margin = max(
            0.0,
            best_similarity - second_similarity
        )

        # This is a confidence-like score, not a probability.
        confidence = int(
            max(
                0,
                min(
                    100,
                    48
                    + (best_similarity * 35)
                    + (margin * 140)
                )
            )
        )

        # Content gives us stronger evidence.
        if content:
            confidence = min(100, confidence + 8)

        similarity_map = {
            category: round(similarity, 4)
            for category, similarity in ranked
        }

        return (
            best_category,
            confidence,
            similarity_map,
            bool(content),
        )

    except Exception as error:
        print(f"⚠️ Semantic classification failed: {error}")

        category, confidence, similarities = _fallback_classify(
            file_path
        )

        return category, confidence, similarities, bool(content)


# ==========================================
# 🧠 PUBLIC CLASSIFIER
# ==========================================

def classify_file(file_path, state=None):

    (
        category,
        confidence,
        similarities,
        content_used,
    ) = _semantic_classify(file_path)

    if state is not None:
        state.last_category = category

    data = CATEGORIES[category]

    return {
        "category": category,
        "confidence": confidence,
        "reaction": data["reaction"],
        "base_score": data["base_score"],
        "similarities": similarities,
        "content_used": content_used,
    }


# ==========================================
# 🐿️ CHIP'S INTEREST
# ==========================================

def calculate_interest(file_path, state=None):

    result = classify_file(file_path, state)

    category = result["category"]
    confidence = result["confidence"]
    score = result["base_score"]

    reasons = [
        f"semantic category: {category}",
        f"AI confidence: {confidence}/100",
    ]

    if result["content_used"]:
        reasons.append("Chip inspected a safe content sample 📖")
        score += 8

    # Confidence changes how strongly Chip trusts his judgement.
    if confidence >= 80:
        score += 8
        reasons.append("strong semantic evidence")
    elif confidence >= 65:
        score += 4
        reasons.append("reasonable semantic evidence")
    elif confidence < 50:
        score -= 5
        reasons.append("Chip is unsure")

    # Personality.
    if state is not None:

        if state.mischief >= 70:
            score += 8
            reasons.append("Chip is feeling mischievous 😈")

        elif state.mischief >= 50:
            score += 4
            reasons.append("Chip is getting mischievous")

        if state.greed >= 80:
            score += 5
            reasons.append("Chip wants more loot 🌰")

        if state.crimes >= 5:
            score += 5
            reasons.append("crime addiction detected")

    # ==========================================
    # 🧠 LEARNING FROM PAST CRIMES
    # ==========================================

    if state is not None:
        learned_count = state.category_counts.get(category, 0)
        if learned_count >= 3:
            score += 14
            reasons.append(f"Chip is obsessed with {category} ({learned_count} previous thefts) 😈")
        elif learned_count == 2:
            score += 10
            reasons.append("Chip remembers stealing this type twice")
        elif learned_count == 1:
            score += 6
            reasons.append("Chip remembers liking this type before")

    # Small type nudges only. Meaning still comes first.
    extension = Path(file_path).suffix.lower()

    if extension in {".pdf", ".docx", ".pptx", ".xlsx"}:
        score += 3
        reasons.append("document looks worth investigating")

    if extension in {".jpg", ".jpeg", ".png", ".mp4", ".mov"}:
        score += 2

    score = max(0, min(100, int(score)))

    return score, reasons


# ==========================================
# 🎭 PUBLIC REACTION
# ==========================================

def get_file_reaction(file_path, state=None):

    result = classify_file(
        file_path,
        state
    )

    return result["reaction"]
