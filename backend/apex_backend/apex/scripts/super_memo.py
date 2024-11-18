

def super_memo(user_grade, repetition_number, ef, interval, pupil_dilatation):
    grade_map = {
        "very easy": 5,
        "easy": 4,
        "medium": 3,
        "hard": 2,
        "very hard": 1,
        "black out": 0,
    }
    q= grade_map[user_grade]
    k= 1 # ustalić w badaniach
    if pupil_dilatation < 25 and pupil_dilatation > 10:
        q*= k


    # if pupil_dilatation < 5 and q == 0:
    #     pupil_dilatation= q
    # elif pupil_dilatation < 10:
    #     pupil_dilatation= 4
    # elif pupil_dilatation < 15:
    #     pupil_dilatation= 3
    # elif pupil_dilatation < 20:
    #     pupil_dilatation= 2
    # elif pupil_dilatation < 25:
    #     pupil_dilatation= 1
    #q= round((q + pupil_dilatation) / 2)

    if q >= 3:
        if repetition_number == 0:
            new_interval= 1
        elif repetition_number == 1:
            new_interval= 6
        else:
            new_interval= round(interval*ef)
    else:
        new_interval= 1
        repetition_number= 0

    new_ef= max(ef + (0.1-(5-q) * (0.08 + (5-q)*0.02)), 1.3)

    return repetition_number + 1, new_ef, new_interval 