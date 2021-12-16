import requests
import json
import sys

with open("config.json", "r") as op:
    API_KEY = json.load(op)["API_KEY"]


def get_top_plays(player):
    # get a player's top 100 plays using osu's api
    url = "https://osu.ppy.sh/api/get_user_best"

    try:
        params = {"k": API_KEY, "u": int(player), "limit": 100}
    except ValueError:
        params = {"k": API_KEY, "u": player, "limit": 100}

    r = requests.get(url, params=params)

    new_dict = []

    for play in r.json():
        new_dict.append({"beatmap_id": play["beatmap_id"], "pp": float(play["pp"])})

    return new_dict


def calculate_beatmap_pp(tops):
    # calculate pp gained from top 100.
    # top play is weighted 100%, and each subsequent play is weighted 0.95 times less
    i = 0
    total = 0.0

    for play in tops:
        total += play["pp"] * (0.95 ** i)
        i += 1
    return round(total, 2)


def calculate_bonus_pp(player):
    # calculate bonus pp for a player by calculating
    # the difference between profile pp and pp from top plays.
    # SCUFFED but idfk how else to calculate lol
    playertops = get_top_plays(player)
    without_bonus = calculate_beatmap_pp(playertops)

    url = "https://osu.ppy.sh/api/get_user"
    params = {"k": API_KEY, "u": player}
    r = requests.get(url, params=params)
    profile_pp = float(r.json()[0]["pp_raw"])

    return round(profile_pp - without_bonus, 2)


def combine_tops(top1, top2):
    # combine top plays from two players and remove entries where
    # the beatmap id is the same but the pp is lower

    combined = top1[:]

    for play in top2:
        if play["beatmap_id"] in [x["beatmap_id"] for x in combined]:
            if (
                play["pp"]
                >= [x["pp"] for x in combined if x["beatmap_id"] == play["beatmap_id"]][
                    0
                ]
            ):
                combined.remove(
                    [x for x in combined if x["beatmap_id"] == play["beatmap_id"]][0]
                )
                combined.append(play)

            # copilot made this, too lazy to change
        else:
            combined.append(play)

    combined.sort(key=lambda x: x["pp"], reverse=True)
    return combined if len(combined) <= 100 else combined[:100]


def main(args):
    player_1 = args[1]
    player_2 = args[2]

    top_1 = get_top_plays(player_1)
    top_2 = get_top_plays(player_2)

    combined = combine_tops(top_1, top_2)
    combined_pp = calculate_beatmap_pp(combined)

    bonus_1 = calculate_bonus_pp(player_1)
    bonus_2 = calculate_bonus_pp(player_2)

    total_pp = combined_pp + max(bonus_1, bonus_2)
    print(f"{bonus_1=} {bonus_2=} {combined_pp=} {total_pp=}")
    return combined, total_pp


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 merge.py <player1> <player2>")
        print("using player ID is recommended")

    else:
        newtops, newpp = main(sys.argv)

        print("New top plays:")
        for i, play in enumerate(newtops, 1):
            print(f"{i}. {play['pp']}pp on {play['beatmap_id']}")

        print("\nNew total PP:", round(newpp, 2))
