import os
import threading
import time
from multiprocessing import Process, Queue
from pathlib import Path

import requests


# CPU-bound task (heavy computation)
def encrypt_file(result_queue: Queue, path: Path):
    start_time = time.perf_counter()
    print(f"Processing file from {path} in process {os.getpid()}")
    # Just simulate a heavy computation
    _ = [i for i in range(100_000_000)]
    end_time = time.perf_counter()
    result_queue.put(end_time - start_time)


# I/O-bound task (downloading image from URL)
def download_image(result_queue: Queue, image_url):
    start_time = time.perf_counter()
    print(f"Downloading image from {image_url} in thread {threading.current_thread().name}")
    response = requests.get(image_url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)
    end_time = time.perf_counter()
    result_queue.put(end_time - start_time)


def main():
    start_time = time.perf_counter()
    try:
        encrypt_result_queue, download_image_queue = Queue(), Queue()

        encrypt_task = Process(
            target=encrypt_file,
            args=(encrypt_result_queue, "rockyou.txt"),
        )
        img_downloading_thread = threading.Thread(
            target=download_image,
            args=(download_image_queue, "https://picsum.photos/1000/1000"),
        )

        encrypt_task.start()
        img_downloading_thread.start()

        encrypt_task.join()
        img_downloading_thread.join()

        total_time = time.perf_counter() - start_time
        print(f"Time taken for encryption task: {encrypt_result_queue.get():.2f} seconds")
        print(f"I/O-bound task:: {download_image_queue.get():.2f} seconds")
        print(f"Total time: {total_time:.2f} seconds")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
