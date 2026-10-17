
def player(prev_play, opponent_history=[]):
    counter = {"R": "P", "P": "S", "S": "R"}
    moves = ["R", "P", "S"]

    if prev_play == "":
        opponent_history.clear()
        player.my_history = []

    else:
        opponent_history.append(prev_play)

    own = player.my_history
    round_index = len(own)

    def predict_quincy(history, i):
        choices = ["R", "R", "P", "P", "S"]
        return choices[(i + 1) % 5]

    def predict_kris(history, i):
        if i == 0:
            return "P"
        return counter[history[i - 1]]

    def predict_mrugesh(history, i):
        past = [""] + history[:i]
        last_ten = past[-10:]
        most_frequent = max(set(last_ten), key=last_ten.count)

        if most_frequent == "":
            most_frequent = "S"

        return counter[most_frequent]

    def predict_abbey(history, i):
        past = ["R"] + history[:i]
        order = {a + b: 0 for a in moves for b in moves}

        for j in range(1, len(past)):
            order[past[j - 1] + past[j]] += 1

        last_move = past[-1]
        possibilities = [last_move + m for m in moves]
        pattern = max(possibilities, key=lambda p: order[p])

        return counter[pattern[-1]]

    predictors = [
        predict_quincy,
        predict_kris,
        predict_mrugesh,
        predict_abbey,
    ]

    scores = []

    for predictor in predictors:
        score = 0

        for i, actual in enumerate(opponent_history):
            if predictor(own, i) == actual:
                score += 1

        scores.append(score)

    best_index = scores.index(max(scores))
    prediction = predictors[best_index](own, round_index)

    my_move = counter[prediction]
    own.append(my_move)

    return my_move


player.my_history = []
