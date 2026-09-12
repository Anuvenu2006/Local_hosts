# ==========================================
# 🌰 CHIP'S BURROW
# ==========================================

from pathlib import Path


class Burrow:

    def __init__(self, burrow_path):

        self.burrow_path = Path(
            burrow_path
        )

        # Make sure the burrow exists
        self.burrow_path.mkdir(
            parents=True,
            exist_ok=True
        )


    # ======================================
    # 🌰 GET CHIP'S LOOT
    # ======================================

    def get_loot(self):

        files = []

        if not self.burrow_path.exists():
            return files

        for file_path in self.burrow_path.iterdir():

            if file_path.is_file():

                files.append(
                    file_path.name
                )

        return files


    # ======================================
    # 🔢 COUNT LOOT
    # ======================================

    def loot_count(self):

        return len(
            self.get_loot()
        )