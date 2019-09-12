'''
  Thread base class that simulates a running car
'''
from threading import Timer
from time import time

CAR_MASS = 1500
FORWARD_FORCE = lambda throttle_percentage: 5400 * throttle_percentage / 100.0
DRAG_FORCE = lambda velocity: 0.8 * (velocity ** 2)
UPDATE_INTERVAL = 0.1 # secs
OBSERVE_INTERVAL = 1.0 # secs

class Car:

  def __init__(self):
    self.velocity = 0.0
    self.throttle_percentage = 0.0
    self.last_updated_time = None
    self.attached_observer = False

  def get_velocity(self):
    return self.velocity

  def set_throttle_percentage(self, throttle_percentage):
    if throttle_percentage < 0 or throttle_percentage > 100:
      raise Exception('Throttle percentage out of bound: %f' % throttle_percentage)
    self.throttle_percentage = throttle_percentage

  def update_velocity(self):
    if not self.last_updated_time:
      raise Exception("start() must be called before updating velocity")

    current_time = time()
    delta_time = current_time - self.last_updated_time
    velocity_km_h = self.velocity * 3.6

    current_force = FORWARD_FORCE(self.throttle_percentage) - DRAG_FORCE(velocity_km_h)
    current_acceleration = current_force / CAR_MASS

    self.velocity += current_acceleration * delta_time
    self.last_updated_time = current_time

  def update_and_reschedule(self):
    self.update_velocity()
    self.schedule_next_update()

  def schedule_next_update(self):
    Timer(UPDATE_INTERVAL, self.update_and_reschedule).start()

  def status(self):
    return '%.2f %% %.2f Km/h' % (self.throttle_percentage, self.velocity * 3.6) 

  def observe_and_reschedule(self):
    print(self.status())
    self.schedule_next_observe()

  def schedule_next_observe(self):
    Timer(OBSERVE_INTERVAL, self.observe_and_reschedule).start()

  def attach_observer(self):
    if self.attached_observer:
      return
    self.attached_observer = True
    self.schedule_next_observe();

  def start(self):
    if self.last_updated_time:
      raise Exception('Can only call car.start() once')
    self.last_updated_time = time()
    self.schedule_next_update()
