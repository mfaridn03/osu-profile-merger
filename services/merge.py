from typing import List, Tuple, Dict, Any

import ossapi

from api.tops import PlayerTops


def merge_top_scores(
    api: ossapi.Ossapi, user_id_1: int, user_id_2: int, limit: int = 100
) -> List[Tuple[int, Dict[str, Any]]]:
    """Merge two users' top scores into a single list sorted by PP desc.

    For each beatmap, keep whichever user's score has higher PP.
    Returns list of (beatmap_id, data) where data contains keys: pp, user, score.
    """
    user1 = api.user(user_id_1)
    user2 = api.user(user_id_2)

    tops = PlayerTops(user1, api, limit=limit)

    for s in api.user_scores(
        user2.id, type=ossapi.ScoreType.BEST, mode=ossapi.GameMode.OSU, limit=limit
    ):
        tops.add_score(s, user2)

    merged = tops.as_list()
    if len(merged) > limit:
        merged = merged[:limit]
    return merged
