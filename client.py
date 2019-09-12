from telnetlib import Telnet
from threading import Timer
from time import sleep

DESIRED_SPEED = 29.00
OBSERVE_INTERVAL = 1.0 # secs

class CarDriver:
  def __init__(self):
    self.speed = 0.0
    self.delta_speed = 0.0
    self.acceleration = 50.0
    self.acceleration_from = 0.0
    self.acceleration_to = 100.0
    self.connection = Telnet('localhost', 5555)
    self.attached_observer = False
    self.observe_car_status()
    self.update_car_acceleration()

  def update_car_acceleration(self):
    throttle_message = 'THROTTLE {acceleration}'.format(
      acceleration=self.acceleration)
    self.connection.write(throttle_message.encode())
    self.connection.read_until(b'OK\n')

  def observe_car_status(self):
    self.connection.write(b'STATUS\n')
    status_string = self.connection.read_until(b'\n')
    tokens = status_string.split()
    current_speed = float(tokens[2])
    self.acceleration = float(tokens[0])
    self.delta_speed = current_speed - self.speed
    self.speed = current_speed
    print('{acceleration}% {speed}km/h'.format(
      acceleration=self.acceleration,
      speed=self.speed))

  def recalculate_acceleration(self):
    if self.delta_speed < 0.1 and self.speed < DESIRED_SPEED:
      self.acceleration_from = self.acceleration
    elif self.delta_speed > -0.1 and self.speed > DESIRED_SPEED:
      self.acceleration_to = self.acceleration
    self.acceleration = (self.acceleration_from + self.acceleration_to) / 2
    self.update_car_acceleration()

  def observe_and_reschedule(self):
    self.observe_car_status()
    self.recalculate_acceleration()
    self.schedule_next_observe()

  def schedule_next_observe(self):
    Timer(OBSERVE_INTERVAL, self.observe_and_reschedule).start()

  def attach_observer(self):
    if self.attached_observer:
      return
    self.attached_observer = True
    self.schedule_next_observe();

driver = CarDriver()
driver.attach_observer()
