from __future__ import annotations

from typing import Final

# Порядок размеров контролирует порядок кнопок.
PARTY_SIZE_ORDER: Final[tuple[str, ...]] = ("solo", "duo", "trio", "quad")

PARTY_SIZE_META: Final[dict[str, dict[str, str]]] = {
    "solo": {"label": "Solo", "emoji": "👤"},
    "duo": {"label": "Duo", "emoji": "👥"},
    "trio": {"label": "Trio", "emoji": "👥👥"},
    "quad": {"label": "Quad", "emoji": "🎯"},
}

STRATEGIES: Final[dict[str, dict[str, object]]] = {
    "pw2": {
        "name": "Polluted Wastelands 2",
        "emoji": "☣️",
        "modes": {
            "duo": "https://docs.google.com/document/d/1g5I0YzLPGT4u-urOAgsqw_9GxY1lObTxr_2QkOIiFG4/edit?tab=t.jtj5k7ze8ais#heading=h.etz4edhmc8jx",
            "trio": "https://docs.google.com/document/d/1hQeuIZ-NsI63MIUhlMExNKOEAvkJsnpb2WL2DcwHiXY/edit?tab=t.0",
            "quad":"https://docs.google.com/document/d/1g5I0YzLPGT4u-urOAgsqw_9GxY1lObTxr_2QkOIiFG4/edit?tab=t.2zbd8384d7i9#heading=h.ejy8walurqal",
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
