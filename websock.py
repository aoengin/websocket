import asyncio
import websockets
import time

async def benchmark_client(uri, data_size_kb, num_connections):
    message = b"A" * (data_size_kb * 1024)  # Create a message with the desired data size

    async def connect_and_send():
        async with websockets.connect(uri) as websocket:
            total_data_sent = 0
            start_time = time.time()

            while True:
                await websocket.send(message)
                total_data_sent += 1

                # Adjust the duration based on your benchmarking needs
                if time.time() - start_time > 10:  # Run for 10 seconds, adjust as needed
                    print("over")
                    break
            print(total_data_sent)
            return total_data_sent

    tasks = [asyncio.create_task(connect_and_send()) for _ in range(num_connections)]
    await asyncio.wait(tasks, timeout=30)
    return tasks

if __name__ == "__main__":
    server_uri = "ws://localhost:8000"
    data_size_kb = 10  # Adjust the data size as needed (in kilobytes)
    number_of_connections = 10

    start_time = time.time()
    print(time.time())
    total_data_sent_list = asyncio.get_event_loop().run_until_complete(
        benchmark_client(server_uri, data_size_kb, number_of_connections)
    )

    end_time = time.time()
    print(time.time())
    elapsed_time = end_time - start_time
    total_data_sent_list = [x.result() for x in total_data_sent_list]
    total_data_sent = sum(total_data_sent_list)
    print(total_data_sent)
    throughput = total_data_sent / elapsed_time / 1024  # Convert to kilobytes per second

    print(f"Data Throughput: {throughput:.2f} KB/s")
