import json
import ossapi
import math


class PlayerTops:
    def __init__(self, user: ossapi.User, api: ossapi.Ossapi, limit: int = 100):
        self.user = user
        self.api = api
        self.data = {}  # {beatmap_id: {"pp": pp, user: User, score: Score}}
        self.pp_weighted = 0
        self.bonus_pp = 0

        # pp & bonus pp calc
        _vals = []
        _i = 0
        # init
        for s in self.api.user_scores(
            self.user.id,
            type=ossapi.ScoreType.BEST,
            mode=ossapi.GameMode.OSU,
            limit=limit,
        ):
            _vals.append(s.pp * (0.95**_i))
            _i += 1
            self.add_score(s)

        self.pp_weighted = sum(_vals)
        if math.ceil(self.user.statistics.pp) == 0:  # inactive
            self.bonus_pp = 0
        else:
            self.bonus_pp = self.user.statistics.pp - self.pp_weighted

    def add_score(self, score: ossapi.Score, custom_user: ossapi.User = None):
        if (
            score.beatmap_id in self.data
            and self.data[score.beatmap_id]["pp"] > score.pp
        ):
            print(
                f"Skipping {score.beatmap_id} because {self.data[score.beatmap_id]['pp']} > {score.pp}"
            )
            return

        self.data[score.beatmap_id] = {
            "pp": score.pp,
            "user": custom_user or self.user,
            "score": score,
        }

    def as_list(self):
        ret = []
        for beatmap_id, data in self.data.items():
            ret.append((beatmap_id, data))
        ret.sort(key=lambda x: x[1]["pp"], reverse=True)
        return ret

    def _bonus_pp_calc(self):
        pass


if __name__ == "__main__":
    # fetch dummy data
    with open("data/dummy_config.json", "r") as f:
        data = json.load(f)
    if not data:
        raise ValueError("No dummy data")

    client_id = data["id"]
    client_secret = data["secret"]

    api = ossapi.Ossapi(client_id, client_secret)
    # inactive player test
    user = api.user(13357689, mode=ossapi.GameMode.OSU)
    print(user.statistics)
