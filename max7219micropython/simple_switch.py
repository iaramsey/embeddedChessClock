from machine import RTC
import time
from machine import Pin, SoftSPI
import max7219_8digit

def display_time(active_player: bool, player_1_time, player_2_time):
    if active_player:
        msg = player_1_time
        if player_1_time < 0:
            msg = "Loser"
        player_1_display.write_to_buffer(str(msg))
        player_1_display.display()
    else:
        msg = player_2_time
        if player_2_time < 0:
            msg = "Loser"
        player_2_display.write_to_buffer(str(msg))
        player_2_display.display()

def decrement_time(active_player: bool, player_1_time, player_2_time):
    print(active_player)
    if active_player:
        player_1_time -= 1
    else:
        player_2_time -= 1
    return player_1_time, player_2_time

# Set up the pin connected to the switch
switch_pin = Pin(28, Pin.IN, Pin.PULL_UP)  # Replace 14 with the correct GPIO pin number

player_1_spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(20), mosi=Pin(22), miso=Pin(0))
player_2_spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(16), mosi=Pin(18), miso=Pin(0))

player_1_display = max7219_8digit.Display(player_1_spi,  Pin(21, Pin.OUT))
player_2_display = max7219_8digit.Display(player_2_spi,  Pin(17, Pin.OUT))

player_1_time = 300 # 5 minutes times 60 seconds times 100 decasonds
player_2_time = 300

active_player = True



# Loop to check the switch status
while True:
    if switch_pin.value() == 0:
        # used when the button is held down
        while switch_pin.value() == 0:
            display_time(active_player, player_1_time, player_2_time)
            player_1_time, player_2_time = decrement_time(active_player, player_1_time, player_2_time)
            time.sleep(0.1)
        active_player = not active_player

    display_time(active_player, player_1_time, player_2_time)
    player_1_time, player_2_time = decrement_time(active_player, player_1_time, player_2_time)
    
    time.sleep(0.1)  # Small delay to avoid excessive CPU usage