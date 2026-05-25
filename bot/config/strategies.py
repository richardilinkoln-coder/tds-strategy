from __future__ import annotations

from typing import Final

# Порядок размеров контролирует порядок кнопок.
PARTY_SIZE_ORDER: Final[tuple[str, ...]] = ("solo", "duo", "trio", "quad", "Сборник", "Сервер","Текущий ивент", "Хардкор", "Монеты", "Сборник - миссии", "Сборник - триалы", "Paladin", "Slayer", "Sentinel", "Ascended", "Security Guard", "tH3 GL1tcH", "Outlaw", "The cure")

PARTY_SIZE_META: Final[dict[str, dict[str, str]]] = {
    "solo": {"label": "Solo", "emoji": "👤"},
    "duo": {"label": "Duo", "emoji": "👥"},
    "trio": {"label": "Trio", "emoji": "👥👤"},
    "quad": {"label": "Quad", "emoji": "👥👥"},
    "Сборник - триалы": {"label": "Сборник: триалы", "emoji": "📚"},
    "Сборник - миссии": {"label": "Сборник: миссии", "emoji": "📚"},
    "Монеты": {"label": "Монеты", "emoji": "🪙"},
    "Хардкор": {"label": "Хардкор", "emoji": "😈"},
    "Текущий ивент": {"label": "Текущий ивент", "emoji": "💡"},
    "Сервер": {"label": "Сервер", "emoji": "🔱"},
    "Paladin": {"label": "Paladin", "emoji": "🛡️"},
    "Slayer": {"label": "Slayer", "emoji": "⚔️"},
    "Sentinel": {"label": "Sentinel", "emoji": "👁️"},
    "Ascended": {"label": "Ascended", "emoji": "😇"},
    "Security Guard": {"label": "Security Guard", "emoji": "👮"},
    "tH3 GL1tcH": {"label": "tH3 GL1tcH", "emoji": "👾"},
    "Outlaw": {"label": "Outlaw", "emoji": "🤠"},
    "The cure": {"label": "The cure", "emoji": "🧪"},
}

STRATEGIES: Final[dict[str, dict[str, object]]] = {
    "pw2": {
        "name": "Polluted Wastelands 2",
        "emoji": "☣️",
        "modes": {
            "solo": "Пока что нету, когда появится - добавим.",
            "duo": "https://docs.google.com/document/d/1g5I0YzLPGT4u-urOAgsqw_9GxY1lObTxr_2QkOIiFG4/edit?tab=t.jtj5k7ze8ais#heading=h.etz4edhmc8jx",
            "trio": "https://docs.google.com/document/d/1hQeuIZ-NsI63MIUhlMExNKOEAvkJsnpb2WL2DcwHiXY/edit?tab=t.0",
            "quad": "https://docs.google.com/document/d/1g5I0YzLPGT4u-urOAgsqw_9GxY1lObTxr_2QkOIiFG4/edit?tab=t.2zbd8384d7i9#heading=h.ejy8walurqal",
        },
    },
    "pizza": {
        "name": "Pizza Party",
        "emoji": "🍕",
        "modes": {
            "solo": "https://docs.google.com/document/d/1piB9j_3yHU0uPnn-x4-uDCobwB79UUMEF2t3esqEoxE/edit?tab=t.0#heading=h.5j8k7csi2use",
            "duo": "Пока что нету, когда появится - добавим.",
            "trio": "Пока что нету, когда появится - добавим.",
            "quad": "Пока что нету, когда появится - добавим.",
        },
    },
    "badlands2": {
        "name": "Badlands 2",
        "emoji": "🏜",
        "modes": {
            "solo": "https://docs.google.com/document/d/1p1rrgdI6JIeX6spTh5M_5q3r3PXYdVBIAtBWHJh8wZQ",
            "duo": "https://docs.google.com/document/d/19O4GQpDLS02Uc_7Tf2_sXamOysrbQp9wzOdokgXa5Ns/edit?tab=t.lmjpsx2che4",
            "trio": "https://docs.google.com/document/d/1xBvD-XsDlY-EQID989c7FPxAk2j8FN2fK0wdSU2ZJh8/edit?tab=t.sfxbztqbamlr#heading=h.5j8k7csi2use",
            "quad": "Пока что нету, когда появится - добавим.",
        },
    },
    "fallen": {
        "name": "Fallen",
        "emoji": "💀",
        "modes": {
            "solo": "https://docs.google.com/document/d/1YOHerf-7aJYFqt8hwEILi5-hcsQZMdCrg9BtzSHsu9M/edit?tab=t.0",
            "duo": "Пока что нету, когда появится - добавим.",
            "trio": "Пока что нету, когда появится - добавим.",
            "quad": "Пока что нету, когда появится - добавим.",
        },
    },
    "hardcore": {
        "name": "Hardcore",
        "emoji": "🔥",
        "modes": {
            "solo": "https://docs.google.com/document/d/1lpA6yBh5vulgWXHfIHVfYMz7YwgQ1c69UQnBO-lHscw/edit?tab=t.jrkpg6stcyff#heading=h.5j8k7csi2use",
            "duo": "https://docs.google.com/document/d/10EDazjYrsJEWPXIvqWUAy2tU_E67USG8iIr5gGn8HOg/edit?usp=sharing",
            "trio": "https://docs.google.com/document/d/1vijYCqX1o7jLdpoxy21rLuRGWclc9aGqpOVEHrVabRs/edit?tab=t.0",
        },
    },
    "frost": {
        "name": "Frost",
        "emoji": "❄️",
        "modes": {
            "solo": "https://docs.google.com/document/d/123mTVHx7CYVKMSc5gconfTjpGScL07YFXwZfZcwnYjw/edit?tab=t.vv7j5i44mve0",
            "duo": "https://docs.google.com/document/d/1LT-ViDySQeTrEeXY-ateAIkoQRpIdfG9rS2T_3RkjSs/edit?tab=t.j7622cginuso",         
        },
    },
    "trials_missions": {
        "name": "Trials & Missions",
        "emoji": "🎭",
        "modes": {
            "Сборник - триалы": "https://docs.google.com/document/d/1NzhAEK4WJ9cA2gDCcACtW-HXQHhJplrE-_ZKkPWXIJk/edit?tab=t.pdj0ytau4jf4",
            "Сборник - миссии": "https://docs.google.com/document/d/1uUXQ6MOk1aGwc0w5Pguy3CtLNNDVAAsLw0q3K8twU60/edit?tab=t.25a4twjptrse",
        },
    },
    "coin_hard": {
        "name": "Coin & Hardcore Grind",
        "emoji": "💎",
        "modes": {
            "Монеты": "https://docs.google.com/document/d/123mTVHx7CYVKMSc5gconfTjpGScL07YFXwZfZcwnYjw/edit?tab=t.vv7j5i44mve0",
            "Хардкор": "https://docs.google.com/document/d/10EDazjYrsJEWPXIvqWUAy2tU_E67USG8iIr5gGn8HOg/edit?tab=t.pdj0ytau4jf4",
        },
    },
    "event": {
        "name": "Event",
        "emoji": "👻",
        "modes": {
            "Текущий ивент": "https://docs.google.com/document/d/1VuFYkUOnTM2NJlTTs4P9d7Eo7q8_Wz6Gl9eNySXv1J4/edit?tab=t.6r9ak694mdjb",
        },
    },
    "Achievements": {
            "name": "Achievements",
            "emoji": "🏆",
            "modes": {
                "Paladin": "https://docs.google.com/document/d/1EN6bWGCFcO_nJJqIlB5Vr-aGT-0AISA8N3KAaxzGr_8/edit?tab=t.sqhmkc1pj32b",
                "Slayer": "https://docs.google.com/document/d/1EN6bWGCFcO_nJJqIlB5Vr-aGT-0AISA8N3KAaxzGr_8/edit?tab=t.vvmb7a6mp8xp",
                "Sentinel": "https://docs.google.com/document/d/1aESThUZMja-_12S0x9qk6pVEnAYr26e6LCXtiRgSFeg/edit?tab=t.0",
                "Ascended": "https://docs.google.com/document/d/1FCWXSKHbixD0oVm3YGlw5R8ufix6XzAu/edit",
                "Security Guard": "https://docs.google.com/document/d/1piB9j_3yHU0uPnn-x4-uDCobwB79UUMEF2t3esqEoxE/edit?tab=t.0#heading=h.5j8k7csi2use",
                "tH3 GL1tcH": "https://docs.google.com/document/d/1zOcGhrfL6UKRM0Nvy1J3Af13_JHPsLNeQBY6HnTMj6k/edit?tab=t.ql70wnutklqb",
                "Outlaw": "https://docs.google.com/document/d/1p1rrgdI6JIeX6spTh5M_5q3r3PXYdVBIAtBWHJh8wZQ/edit",
                "The cure": "Пока что нету, как появится - добавим.",
        },
    },
    "vip": {
        "name": "Vip server",
        "emoji": "🔑",
        "modes": {
            "Сервер": "https://www.roblox.com/games/3260590327?privateServerLinkCode=56597066406241925136479511848497",
        },
    },
}

def get_strategy(strategy_id: str) -> dict[str, object] | None:
    return STRATEGIES.get(strategy_id)


def get_available_party_sizes(strategy_id: str) -> list[str]:
    strategy = get_strategy(strategy_id)
    if not strategy:
        return []
    modes = strategy.get("modes", {})
    if not isinstance(modes, dict):
        return []
    return [size for size in PARTY_SIZE_ORDER if size in modes]
