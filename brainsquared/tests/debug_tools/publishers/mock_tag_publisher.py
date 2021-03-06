import time
import random

from brainsquared.publishers.PikaPublisher import PikaPublisher


class MockPublisher(object):
  def __init__(self, user, device, metric):
    self.routing_key = "%s:%s:%s" % (user, device, metric)
    self.pub = None


  def connect(self, host, username, pwd):
    self.pub = PikaPublisher(host, username, pwd)
    self.pub.connect()
    self.pub.register(self.routing_key)
    print "Connected to: {}".format(host)


  def publish(self, buffer_size):

    print "Publishing on queue: {}".format(self.routing_key)
    
    data_buffer = []
    while 1:
      time.sleep(0.1)
      random_value = random.random()
      if random_value > .5:
        value = 1
      else:
        value = 0
  
      data = {"timestamp": int(time.time() * 1000),
              "value": value }
      
      if len(data_buffer) < buffer_size:
        data_buffer.append(data)
      else:
        self.pub.publish(self.routing_key, data_buffer)
        print data_buffer
        data_buffer = []



if __name__ == "__main__":
  BUFFER_SIZE = 1

  HOST = "rabbitmq.cloudbrain.rocks"
  USERNAME = "cloudbrain"
  PWD = "cloudbrain"

  USER_ID = "brainsquared"
  DEVICE = "neurosky"
  METRIC = "tag"

  mock_pub = MockPublisher(USER_ID, DEVICE, METRIC)
  mock_pub.connect(HOST, USERNAME, PWD)
  mock_pub.publish(BUFFER_SIZE)
