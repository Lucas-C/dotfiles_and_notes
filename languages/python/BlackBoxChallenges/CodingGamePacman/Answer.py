import importlib


def main(get_input, write_output, hero_strat_name='optimal'):
    hero_strat_module = importlib.import_module(hero_strat_name + '_answer')
    X, Y, Z = get_input(), get_input(), get_input()
    answer = hero_strat_module.Answer(X, Y, Z)
    while True:
        args = [get_input(), get_input(), get_input(), get_input()]
        for _ in range(int(Z)):
            args.append(get_input())
        write_output(answer.iteration(*args))

if __name__ == '__main__':
    main(input, print)
