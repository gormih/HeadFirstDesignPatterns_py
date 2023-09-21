from abc import ABC, abstractmethod


class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass


class WeatherMeasurementPoint:
    _temperature: float
    _humidity: float
    _pressure: float

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value

    @property
    def humidity(self) -> float:
        return self._humidity

    @humidity.setter
    def humidity(self, value: float) -> None:
        self._humidity = value

    @property
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, value: float) -> None:
        self._pressure = value


class Observer(ABC):
    @abstractmethod
    def update(self, measurement_point: WeatherMeasurementPoint) -> None:
        pass


class DisplayElement(ABC):

    @abstractmethod
    def display(self):
        pass


class WeatherData(Subject):
    def __init__(self) -> None:
        self._current_measurement_point = WeatherMeasurementPoint()
        self._observers = set()

    def register_observer(self, observer: Observer) -> None:
        self._observers.add(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self._current_measurement_point)

    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        self._current_measurement_point.temperature = temperature
        self._current_measurement_point.humidity = humidity
        self._current_measurement_point.pressure = pressure
        self.notify_observers()


class CurrentConditionsDisplay(DisplayElement, Observer):
    _temperature: float
    _humidity: float

    def __init__(self, weather_data: WeatherData) -> None:
        self._weather_data = weather_data
        weather_data.register_observer(self)

    def display(self) -> None:
        print(
            f"Current conditions: "
            f"{self._temperature:.2f}F degrees and "
            f"{self._humidity:.2f}% humidity"
        )

    def update(self, w_point: WeatherMeasurementPoint) -> None:
        self._temperature = w_point.temperature
        self._humidity = w_point.humidity
        self.display()


class StatisticsDisplay(DisplayElement, Observer):

    def __init__(self, weather_data: WeatherData) -> None:
        self._num_readings = 0
        self._max_temp = 0.
        self._min_temp = 200.
        self._temp_summ = 0.
        self._weather_data = weather_data
        weather_data.register_observer(self)

    def update(self, w_point: WeatherMeasurementPoint) -> None:
        self._num_readings += 1

        self._temp_summ += w_point.temperature
        self._max_temp = max(w_point.temperature, self._max_temp)
        self._min_temp = min(w_point.temperature, self._min_temp)

        self.display()

    def display(self) -> None:
        print(f"Avg/Max/Min temperature = "
              f"{self._temp_summ / self._num_readings}"
              f"/{self._max_temp}"
              f"/{self._min_temp}"
              )


class ForecastDisplay(DisplayElement, Observer):
    _last_pressure: float

    def __init__(self, weather_data: WeatherData) -> None:
        self._current_pressure = 29.92
        self._weather_data = weather_data
        weather_data.register_observer(self)

    def update(self, w_data: WeatherMeasurementPoint) -> None:
        self._last_pressure = self._current_pressure
        self._current_pressure = w_data.pressure
        self.display()

    def display(self) -> None:
        print("Forecast: ", end="")
        if self._current_pressure > self._last_pressure:
            print("Improving weather on the way!")
        elif self._current_pressure == self._last_pressure:
            print("More of the same")
        elif self._current_pressure < self._last_pressure:
            print("Watch out for cooler, rainy weather")


class HeatIndexDisplay(DisplayElement, Observer):
    def __init__(self, weather_data) -> None:
        self.heat_index = 0.
        self._weather_data = weather_data
        weather_data.register_observer(self)

    def update(self, w_point: WeatherMeasurementPoint) -> None:
        self.heat_index = self._compute_heat_index(w_point.temperature, w_point.humidity)
        self.display()

    def display(self) -> None:
        print(f"Heat index is {self.heat_index:.4f}")

    @classmethod
    def _compute_heat_index(cls, t: float, rh: float) -> float:
        heat_index = (
                (16.923 + (0.185212 * t) +
                 (5.37941 * rh) -
                 (0.100254 * t * rh) +
                 (0.00941695 * (t * t)) +
                 (0.00728898 * (rh * rh)) +
                 (0.000345372 * (t * t * rh)) -
                 (0.000814971 * (t * rh * rh)) +
                 (0.0000102102 * (t * t * rh * rh)) -
                 (0.000038646 * (t * t * t)) +
                 (0.0000291583 * (rh * rh * rh)) +
                 (0.00000142721 * (t * t * t * rh)) +
                 (0.000000197483 * (t * rh * rh * rh)) -
                 (0.0000000218429 * (t * t * t * rh * rh)) +
                 0.000000000843296 * (t * t * rh * rh * rh)) -
                (0.0000000000481975 * (t * t * t * rh * rh * rh))
        )
        return heat_index


def weather_station() -> None:
    weather_data = WeatherData()

    current_display = CurrentConditionsDisplay(weather_data)
    statistics_display = StatisticsDisplay(weather_data)
    forecast_display = ForecastDisplay(weather_data)
    heat_index_display = HeatIndexDisplay(weather_data)

    weather_data.set_measurements(80, 65, 30.4)
    weather_data.set_measurements(82, 70, 29.2)
    weather_data.set_measurements(78, 90, 29.2)

    weather_data.remove_observer(forecast_display)
    weather_data.set_measurements(62, 90, 28.1)


if __name__ == "__main__":
    weather_station()
