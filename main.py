from funxs import *

if __name__ == "__main__":

    clear(0)
    q_num = csv_retriver()
    print("   Welcome to Cloud Knowledge Checker".center(37))
    menu = f"""
    ================================
    |        CATEGORY MENU         |
    ================================
    | 1. WAF              [{q_num[0]:05}]  |
    | 2. CAF              [{q_num[1]:05}]  |
    | 3. Cloud            [{q_num[2]:05}]  |
    -------------------------------
    | q   to Exit                  |
    ================================

    """

    while True:

        print(menu)
        sel = choice("Please select your entry:",3)

        if sel == 1:
            print("WAF selected")
            sample = choice(f"How many questions would you like to answer? [1-{q_num[sel-1]}]",q_num[sel-1])
            score(data = csv_retriver(sel,sample))
        elif sel == 2:
            print("CAF selected")
            sample = choice(f"How many questions would you like to answer? [1-{q_num[sel-1]}]",q_num[sel-1])
            score(data = csv_retriver(sel,sample))
        elif sel == 3:
            print("Cloud selected")
            sample = choice(f"How many questions would you like to answer? [1-{q_num[sel-1]}]",q_num[sel-1])
            score(data = csv_retriver(sel,sample))
        elif sel not in [1,2,3]:
            print("Invalid input")
        elif sel == 'q':
            exit_program()
        else:
            continue