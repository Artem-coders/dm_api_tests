
def attempt(n=5):
    def decorator(func):
        def wraps(*args, **kwargs):
            print('--------------')
            print(n)
            func(*args, **kwargs)
            print('--------------')
            return

        return wraps

    return decorator


@attempt(n=5)
def my_print(name):
    print('--------------')
    print(f"Hellow, {name}!")
    print('--------------')


@attempt(n=5)
def my_print1(name):
    print(f"Hellow, {name}1")


@attempt(n=5)
def my_print2(name):
    print(f"Hellow, {name}2")


@attempt(n=5)
def my_print3(name):
    print(f"Hellow, {name}3")


my_print(name='Иван')
my_print1(name='Вася')
my_print2(name='Петя')
my_print3(name='Саша')
