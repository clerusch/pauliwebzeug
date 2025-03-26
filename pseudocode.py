
def sorted_keys_by_value(d):
        return [k for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)]

def recurer(ws, scores, predictions):
    if len(ws) == 0:
        return True
    else:
        predictions.append(max(scores, key=scores.get))
        for w in ws:
            for index, element in enumerate(w):
                if element !=0:
                    scores[index] -= 1
            predictions.append(ws.pop(w))

def main():
    ws = []
    scores = {}
    for w in ws:
        for index, element in enumerate(w):
            if element != 0:
                scores[index] += 1

    sorted_scores = sorted_keys_by_value(scores)
    predicted_edges = []
    while True:
        if len(ws) != 0:
            sorted_scores = sorted_keys_by_value(scores)
            for score in sorted_scores:
                predicted_edges.append(score)
                for w in ws:
                    if score in w:
                        for item in w:
                            scores[item] -= 1
                        ws.pop(w)
        else: return scores
        for node in w:
            for edge in g.edges():
                if node in edge:
                    scores[edge] = 1

if __name__ == '__main__':
    main()
