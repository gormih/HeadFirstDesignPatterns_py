from abc import ABC, abstractmethod


class Beverage(ABC):

    def __init__(self) -> None:
        self.description = 'Unknown Beverage'

    def get_description(self) -> str:
        return self.description

    @abstractmethod
    def cost(self) -> float:
        pass

    def __str__(self) -> str:
        return f'{self.get_description()} - {self.cost()}$'


class CondimentDecorator(Beverage, ABC):

    @abstractmethod
    def get_description(self) -> str:
        pass


class Espresso(Beverage):
    def __init__(self) -> None:
        super().__init__()
        self.description = 'Espresso'

    def cost(self) -> float:
        return 1.99


class HouseBlend(Beverage):
    def __init__(self) -> None:
        super().__init__()
        self.description = 'House Blend Coffee'

    def cost(self) -> float:
        return 0.89


class DarkRoast(Beverage):

    def __init__(self) -> None:
        super().__init__()
        self.description = 'Dark Roast Coffee'

    def cost(self) -> float:
        return 0.99


class Mocha(CondimentDecorator):
    def __init__(self, beverage: Beverage):
        super().__init__()
        self.beverage = beverage

    def get_description(self) -> str:
        return f'{self.beverage.get_description()}, Mocha'

    def cost(self) -> float:
        return self.beverage.cost() + 0.20


class Whip(CondimentDecorator):

    def __init__(self, beverage: Beverage) -> None:
        super().__init__()
        self.beverage = beverage

    def get_description(self) -> str:
        return f'{self.beverage.get_description()}, Whip'

    def cost(self) -> float:
        return 0.1 + self.beverage.cost()


class Soy(CondimentDecorator):

    def __init__(self, beverage: Beverage) -> None:
        super().__init__()
        self.beverage = beverage

    def get_description(self) -> str:
        return f'{self.beverage.get_description()}, Soy'

    def cost(self) -> float:
        return 0.15 + self.beverage.cost()


def star_buzz_coffee():

    beverage_1 = Espresso()
    print(beverage_1)

    beverage_2 = DarkRoast()
    beverage_2 = Mocha(beverage_2)
    beverage_2 = Mocha(beverage_2)
    beverage_2 = Whip(beverage_2)
    print(beverage_2)

    beverage_3 = HouseBlend()
    beverage_3 = Soy(beverage_3)
    beverage_3 = Mocha(beverage_3)
    beverage_3 = Whip(beverage_3)
    print(beverage_3)


if __name__ == '__main__':
    star_buzz_coffee()