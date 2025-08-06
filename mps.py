import can
import time

REQ_ID = 0x641
RES_ID = 0x5C1

# Применяем фильтр сразу при открытии — принимаем только ID 0x5C1
filters = [{"can_id": RES_ID, "can_mask": 0x7FF, "extended": False}]
bus = can.interface.Bus(channel='can0', bustype='socketcan', can_filters=filters)

def send_and_log(data_bytes, label="", timeout=0.1):
    """
    Отправляет CAN-запрос и выводит первый полученный ответ, либо сообщение об отсутствии.
    Логируются все ответы, пришедшие в течение timeout.
    """
    msg = can.Message(arbitration_id=REQ_ID, data=data_bytes, is_extended_id=False)
    bus.send(msg)

    sent_hex = ' '.join(f'{b:02X}' for b in data_bytes)
    received_hex = "—"

    start_time = time.time()
    while time.time() - start_time < timeout:
        response = bus.recv(timeout=0.01)
        if response:
            received_hex = ' '.join(f'{b:02X}' for b in response.data)
            break

    return label, sent_hex, received_hex

def delay(ms):
    time.sleep(ms / 1000.0)

def print_table(rows):
    col_widths = [max(len(str(cell)) for cell in column) for column in zip(*rows)]
    for row in rows:
        line = "  ".join(f"{cell:<{w}}" for cell, w in zip(row, col_widths))
        print(line)

def main():
    step = 0
    while True:
        try:
            step += 1
            print(f"\n================ FRAME #{step} ================")
            frame_start = time.time()

            table_rows = [("Command", "Sent Packet", "Received Packet")]

            table_rows.append(send_and_log([0x40, 0x03, 0x20, 0x04, 0, 0, 0, 0], "heatersState"))
            table_rows.append(send_and_log([0x40, 0x0A, 0x20, 0x04, 0, 0, 0, 0], "heliumLevel"))
            table_rows.append(send_and_log([0x40, 0x03, 0x20, 0x01, 0, 0, 0, 0], "unknown_032001"))
            table_rows.append(send_and_log([0x40, 0x03, 0x20, 0x02, 0, 0, 0, 0], "unknown_032002"))

            delay(500)
            table_rows.append(send_and_log([0x2F, 0x20, 0x20, 0x00, 0x01, 0, 0, 0], "init_cmd_1"))
            delay(500)
            table_rows.append(send_and_log([0x2F, 0x20, 0x20, 0x00, 0x01, 0, 0, 0], "init_cmd_2"))

            table_rows.append(send_and_log([0x40, 0x17, 0x20, 0x01, 0, 0, 0, 0], "turet1V"))
            table_rows.append(send_and_log([0x40, 0x17, 0x20, 0x02, 0, 0, 0, 0], "turet1K"))
            table_rows.append(send_and_log([0x40, 0x17, 0x20, 0x04, 0, 0, 0, 0], "turet2K"))
            table_rows.append(send_and_log([0x40, 0x17, 0x20, 0x03, 0, 0, 0, 0], "turet2V"))

            table_rows.append(send_and_log([0x40, 0x44, 0x20, 0x00, 0, 0, 0, 0], "magnetPreassure"))
            table_rows.append(send_and_log([0x40, 0x16, 0x20, 0x04, 0, 0, 0, 0], "ccr4"))

            table_rows.append(send_and_log([0x40, 0x01, 0x20, 0x01, 0, 0, 0, 0], "canDay"))
            table_rows.append(send_and_log([0x40, 0x01, 0x20, 0x02, 0, 0, 0, 0], "canMonth"))
            table_rows.append(send_and_log([0x40, 0x01, 0x20, 0x03, 0, 0, 0, 0], "canYear"))
            table_rows.append(send_and_log([0x40, 0x01, 0x20, 0x04, 0, 0, 0, 0], "canHour"))
            table_rows.append(send_and_log([0x40, 0x01, 0x20, 0x05, 0, 0, 0, 0], "canMinute"))
            table_rows.append(send_and_log([0x40, 0x01, 0x20, 0x06, 0, 0, 0, 0], "canSecond"))

            print_table(table_rows)

            frame_end = time.time()
            print(f">>>> FRAME TIME: {frame_end - frame_start:.2f} seconds")

        except Exception as e:
            print("Ошибка цикла:", str(e))
            break

if __name__ == "__main__":
    main()
