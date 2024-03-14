import struct

from can import Bus, Message

# typedef struct {
#   unsigned char cmd;
#   unsigned char flags;
#   unsigned int elapsed_time;
#   unsigned char stgy;
#   unsigned char align;
#   char padding[2];
# } __attribute__((packed)) t_can_strategy_command;

STRATEGY_COMMAND_CAN_ID = 0x710
STRATEGY_COMMAND_ALIGN_GRANDE1 = 0x01

data_align = {
    "cmd": STRATEGY_COMMAND_ALIGN_GRANDE1,
    "flags": 0,
    "elapsed_time": 0,
    "stgy": 1,
    "align": 1,
}

values = data_align.values()
message_data = struct.pack("<BBhBBxx", *values)

bus = Bus(
    channel="can0", interface="socketcan", preserve_timestamps=True, bitrate=403847
)
# bus = Bus(channel="can0", interface="virtual", preserve_timestamps=True, bitrate=403847)

msg = Message(
    arbitration_id=STRATEGY_COMMAND_CAN_ID,
    data=message_data,
    is_extended_id=False,
    is_rx=False,
)

print(msg)

bus.send(msg)
bus.shutdown()
