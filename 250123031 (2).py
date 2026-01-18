import json
import sys
from typing import List, Tuple

# -------------------------
# 1. Basic card utilities
# -------------------------
RANKS = "23456789TJQKA"
RANK_VALUE = {r: i + 2 for i, r in enumerate(RANKS)}

def parse_card(card_str: str) -> Tuple[int, str]:
    return RANK_VALUE[card_str[0]], card_str[1]

def is_straight_3(rank_values: List[int]) -> Tuple[bool, int]:
    r = sorted(rank_values)
    if r[0] + 1 == r[1] and r[1] + 1 == r[2]:
        return True, r[2]
    if set(r) == {14, 2, 3}:
        return True, 3
    return False, 0

def hand_category(hole: List[str], table: str) -> int:
    cards = hole + [table]
    rank_values, suits = zip(*[parse_card(c) for c in cards])
    flush = len(set(suits)) == 1
    counts = {}
    for v in rank_values:
        counts[v] = counts.get(v, 0) + 1
    straight, _ = is_straight_3(list(rank_values))
    if straight and flush: return 5
    if 3 in counts.values(): return 4
    if straight: return 3
    if flush: return 2
    if 2 in counts.values(): return 1
    return 0

# -----------------------------------
# 3. Strategy Helper: High Card Logic
# -----------------------------------
def get_high_card_action(hole: List[str], table: str) -> str:
    table_rank, _ = parse_card(table)
    hole_ranks = [parse_card(c)[0] for c in hole]
    max_hole = max(hole_ranks)

    if table_rank == 14: # ACE
        if max_hole >= 12: return "RAISE"
        if max_hole >= 9:  return "CALL"
        return "FOLD"
    elif table_rank == 13: # KING
        if max_hole >= 12: return "RAISE" 
        if max_hole >= 9: return "CALL"
        return "FOLD"
    elif table_rank == 12: # QUEEN
        if max_hole >= 13: return "RAISE"
        if max_hole >= 9: return "CALL"
        return "FOLD"
    elif table_rank == 11: # JACK
        if max_hole >= 13: return "RAISE"
        if max_hole >= 9:  return "CALL"
        return "FOLD"
    elif table_rank == 10: # 10
        if max_hole >= 13: return "RAISE"
        if max_hole >= 9: return "CALL"
        return "FOLD"
    elif table_rank == 9: # 9
        if max_hole >=13: return "RAISE"
        if max_hole >=10: return "CALL"
        return "FOLD"
    
    elif 5 <= table_rank <= 8: # 5-8
        if max_hole >= 13: return "RAISE"
        if max_hole >= 11: return "CALL"
        return "FOLD"
    elif table_rank == 3 or table_rank == 4: # 3-4
        if max_hole >= 13: return "RAISE"
        if max_hole >= 11: return "CALL"
        return "FOLD"
    elif table_rank == 2: # 2
        if max_hole >= 13: return "RAISE"
        if max_hole >= 10: return "CALL"
        return "FOLD"
    return "CALL"

def decide_action(state: dict) -> str:
    hole = state.get("your_hole", [])
    table = state.get("table_card", "")
    if not hole or not table: return "CALL"
    
    category = hand_category(hole, table)
    if category >= 1:
        return "RAISE"
    if category == 0:
        return get_high_card_action(hole, table)
    return "CALL"

def main():
    raw = sys.stdin.read().strip()
    try:
        state = json.loads(raw) if raw else {}
    except Exception:
        state = {}
    action = decide_action(state)
    sys.stdout.write(json.dumps({"action": action}))

if __name__ == "__main__":
    main()