def evaluate_hand(hand):
    Faces = "23456789TJQKA"
    hand = hand.split(" ")
    straight = 0
    flush = 0
    HighCard = 0
    FaceCount = [0] * Faces.__len__()

    # Evaluator
    for card in hand:
        flush |= 1 << ord(card[1])
        straight |= 1 << Faces.index(card[0])
        FaceCount[Faces.index(card[0])] += 1
        HighCard = max(HighCard,Faces.index(card[0]))
        
    HighCard += 2
    straightCheck = straight

    while straightCheck % 2 == 0:
        straightCheck >>= 1

    hasFlush = (flush & (flush - 1)) == 0
    hasStraight = straightCheck == 0b11111

    # Rank the scores in the hand and return the result
    if hasFlush and hasStraight:
        return {"Hand":"Straight Flush", "Rank":9, "Factor":HighCard}
    totalRepeats = 0
    for cardCount in FaceCount:
        if cardCount == 4:
            return {"Hand":"Four of a kind", "Rank":8, "Factor":FaceCount.index(4) +1}
        if cardCount == 3:
            totalRepeats += 3
        if cardCount == 2:
            totalRepeats += 2

    get_N_Repeating_Face = lambda x: FaceCount.index(x) + 2    
    if totalRepeats == 5:
        return {"Hand":"Full-House", "Rank":7, "Factor":get_N_Repeating_Face(3)}
    
    if hasFlush:
        return {"Hand":"Flush", "Rank":6, "Factor":HighCard}

    if hasStraight:
        return {"Hand":"Straight", "Rank":5, "Factor":HighCard}
    
    if totalRepeats == 3:
        return {"Hand":"Three of Kind", "Rank": 4, "Factor":get_N_Repeating_Face(3)}
    
    if totalRepeats == 4:
        FaceCount.remove(2)
        return {"Hand":"Two pair", "Rank":3, "Factor": (get_N_Repeating_Face(2) * 100) + HighCard }
    
    if totalRepeats == 2:
        return {"Hand":"Pair", "Rank":2, "Factor":(get_N_Repeating_Face(2)*100) + HighCard}

    return {"Hand":"High-Card", "Rank":1, "Factor":HighCard}

def compare_ranks(Score1, Score2):
    if Score1["Rank"] == Score2["Rank"]:
        return 0 if Score1["Factor"] > Score2["Factor"] else 1
    return 0 if Score1["Rank"] > Score2["Rank"] else 1

with open('./Hands', 'r') as Hands:
        Player1Wins = 0
        Player2Wins = 0

        for hand in Hands:
            P1Score = evaluate_hand(hand[0:14])
            P2Score = evaluate_hand(hand[15:])

            if compare_ranks(P1Score, P2Score) == 0:
                Player1Wins +=1
            else:
                Player2Wins +=2
        print("Player 1 wins: %d, Player 2 wins: %d" % (Player1Wins, Player2Wins))