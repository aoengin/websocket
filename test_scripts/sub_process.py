import asyncio

async def run_subprocess(command):
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

async def main():
    commands = [
        ["python", "servers/socketify_server.py"],
        ["python", "clients/autobahnws.py", "0"],
        ["python", "clients/autobahnws.py", "0.05"],
        ["python", "clients/autobahnws.py", "0.1"],
        ["python", "clients/autobahnws.py", "0.15"],
        ["python", "clients/autobahnws.py", "0.2"],
        ["python", "clients/autobahnws.py", "0.25"],
        ["python", "clients/autobahnws.py", "0.3"],
        ["python", "clients/autobahnws.py", "0.35"],
    ]

    tasks = [run_subprocess(command) for command in commands]
    results = await asyncio.gather(*tasks)

    # #Print Result
    # for i, (stdout, stderr) in enumerate(results):
    #     print(f"Result for subprocess {i + 1}:")
    #     print(f"stdout:\n{stdout}")
    #     print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())
