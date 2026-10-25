import logging
import random


def generate_ird_number():
    min_number: int = 14000000
    max_number: int = 14999999

    base_number_int = random.randint(min_number, max_number)
    base_number = str(base_number_int)

    check1 = (
        int(base_number[0]) * 3
        + int(base_number[1]) * 2
        + int(base_number[2]) * 7
        + int(base_number[3]) * 6
        + int(base_number[4]) * 5
        + int(base_number[5]) * 4
        + int(base_number[6]) * 3
        + int(base_number[7]) * 2
    ) % 11

    check2 = (
        int(base_number[0]) * 7
        + int(base_number[1]) * 4
        + int(base_number[2]) * 3
        + int(base_number[3]) * 2
        + int(base_number[4]) * 5
        + int(base_number[5]) * 2
        + int(base_number[6]) * 7
        + int(base_number[7]) * 6
    ) % 11

    if check1 == check2 and check1 == 1:
        return base_number_int
    else:
        if check1 == 0 or (check1 == 1 and check2 == 0):
            check_digit = 0
        elif check1 == 1:
            check_digit = 11 - check2
        else:
            check_digit = 11 - check1

    ird_number: str = base_number + str(check_digit)
    logging.info(f"ird_number: {ird_number}")
    return ird_number


def test_ird_number_generation():
    print(generate_ird_number())
