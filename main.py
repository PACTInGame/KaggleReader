import time
from event_sender import EventSender
from data_loader import DataLoader


def main():
    # Daten laden
    filepaths = ["cosmetic_archive/2019-Oct.csv"]
    #filepaths = ["cosmetic_archive/2019-Oct.csv", "cosmetic_archive/2019-Nov.csv"]
    data_loader = DataLoader()
    data = data_loader.load_csv_data(filepaths)

    event_sender = EventSender()

    print("Loaded data: Testing API")

    # 1. Einzelnes Event senden
    start_time = time.perf_counter()
    event_sender.send_single_event(data[1])
    end_time = time.perf_counter()
    print(f"Time taken to send single event: {end_time - start_time:.2f} seconds")

    time.sleep(1)

    # 2. Alle Events so schnell wie möglich senden (mit Statistiken)
    print("\nSending all events as fast as possible...")
    event_sender.send_all_fast(data[:1000])  # Nur erste 1000 für Demo

    # 3. Events mit Replay (optional)
    # print("\nReplaying events 1000x faster...")
    # event_sender.replay_events(data[:10], speed_factor=1000.0)


if __name__ == "__main__":
    main()