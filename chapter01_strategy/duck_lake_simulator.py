from typing import Protocol, Union


class FlyBehavior(Protocol):
    def fly(self) -> None:
        pass


class QuackBehavior(Protocol):
    def quack(self) -> None:
        pass


# Flying implementations
class FlyWithWings(FlyBehavior):
    def fly(self) -> None:
        print("I'm flying!!")


class FlyNoWay(FlyBehavior):
    def fly(self) -> None:
        print("I can't fly")


class FlyRocketPowered(FlyBehavior):
    def fly(self) -> None:
        print("I'm flying with a rocket!'")


# Quack implementations
class Quack(QuackBehavior):
    def quack(self) -> None:
        print("Quack")


class MuteQuack(QuackBehavior):
    def quack(self) -> None:
        print("<< Silence >>")


class Squeak(QuackBehavior):
    def quack(self) -> None:
        print("Squeak")


# Duck Base class
class Duck(Protocol):
    _fly_behavior_: FlyBehavior
    _quack_behavior_: QuackBehavior

    @property
    def fly_behavior(self) -> Union[None, FlyBehavior]:
        return self._fly_behavior_

    @fly_behavior.setter
    def fly_behavior(self, fly_behavior: FlyBehavior) -> None:
        self._fly_behavior_ = fly_behavior

    @property
    def quack_behavior(self) -> Union[None, QuackBehavior]:
        return self._quack_behavior_

    @quack_behavior.setter
    def quack_behavior(self, quack_behavior: QuackBehavior) -> None:
        self._quack_behavior_ = quack_behavior

    def display(self) -> None:
        pass

    def perform_fly(self) -> None:
        self.fly_behavior.fly()

    def perform_quack(self) -> None:
        self.quack_behavior.quack()

    @staticmethod
    def swim() -> None:
        print("All ducks float, even decoys!")


# Ducks implementations

class MallardDuck(Duck):
    def __init__(self) -> None:
        self.fly_behavior = FlyWithWings()
        self.quack_behavior = Quack()

    def display(self) -> None:
        print("I'm a real Mallard duck")


class DecoyDuck(Duck):
    def __init__(self) -> None:
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = MuteQuack()

    def display(self) -> None:
        print("I'm a duck Decoy")


class ModelDuck(Duck):
    def __init__(self) -> None:
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = Squeak()

    def display(self) -> None:
        print("I'm a real Mallard duck")


class RedHeadDuck(Duck):
    def __init__(self) -> None:
        self.fly_behavior = FlyWithWings()
        self.quack_behavior = Quack()

    def display(self) -> None:
        print("I'm a real Red Headed duck")


class RubberDuck(Duck):
    def __init__(self) -> None:
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = Squeak()

    def display(self) -> None:
        print("I'm a rubber duckies")


def duck_lake_simulator() -> None:
    mallard = MallardDuck()
    mallard.perform_quack()
    mallard.perform_fly()

    model = ModelDuck()
    model.perform_fly()
    model.fly_behavior = FlyRocketPowered()
    model.perform_fly()


if __name__ == '__main__':
    duck_lake_simulator()
