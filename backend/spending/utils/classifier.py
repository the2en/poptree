GOOD_CATEGORIES = {"도서", "교육", "기부", "건강", "저축", "카페", "자기계발"}
BAD_CATEGORIES = {"술", "게임", "배달", "과소비", "잡비"}

def get_spending_score(category):
    if category in GOOD_CATEGORIES:
        return 3
    elif category in BAD_CATEGORIES:
        return -2
    return 0
