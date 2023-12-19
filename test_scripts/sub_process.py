import asyncio

async def run_subprocess(command):
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

async def main():
    # List of commands to run asynchronously
    commands = [
        ["python", "servers/autobahn_server.py"],
        ["python", "clients/autobahnws.py", "0"],
        # Add more commands as needed
    ]

    # Run subprocesses concurrently
    tasks = [run_subprocess(command) for command in commands]
    results = await asyncio.gather(*tasks)

    # # Print results
    # for i, (stdout, stderr) in enumerate(results):
    #     print(f"Result for subprocess {i + 1}:")
    #     print(f"stdout:\n{stdout}")
    #     print(f"stderr:\n{stderr}")
    #     print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())
