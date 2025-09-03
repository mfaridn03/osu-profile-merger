from typing import List, Tuple, Dict, Any

import ossapi

from api.tops import PlayerTops


def merge_top_scores(
    api: ossapi.Ossapi, user_id_1: int, user_id_2: int, limit: int = 100
) -> Tuple[
    List[Tuple[int, Dict[str, Any]]],
    Tuple[ossapi.User, float],
    Tuple[ossapi.User, float],
]:
    """Merge two users' top scores into a single list sorted by PP desc.

    For each beatmap, keep whichever user's score has higher PP.
    Returns list of (beatmap_id, data) where data contains keys: pp, user, score, and the bonus pp of the two users.
    """
    user1 = api.user(user_id_1, mode=ossapi.GameMode.OSU)
    user2 = api.user(user_id_2, mode=ossapi.GameMode.OSU)

    tops1 = PlayerTops(user1, api, limit=limit)
    tops2 = PlayerTops(user2, api, limit=limit)

    bonus1 = (user1, tops1.bonus_pp)
    bonus2 = (user2, tops2.bonus_pp)

    for s in api.user_scores(
        user2.id, type=ossapi.ScoreType.BEST, mode=ossapi.GameMode.OSU, limit=limit
    ):
        tops1.add_score(s, user2)

    merged = tops1.as_list()
    if len(merged) > limit:
        merged = merged[:limit]
    return merged, bonus1, bonus2
