import asyncio
import random
import time


def time_me(f):
    async def inner(*args, **kwargs):
        current_time = time.time()
        await f(*args, **kwargs)
        print(f"Elapsed seconds: {time.time() - current_time}")

    return inner


def rand_int():
    return random.randint(0, 3)


def my_async(t):
    time.sleep(t)
    print("DONE!")
    return t


@time_me
async def main_simple():
    result1 = await my_async(1)
    result2 = await my_async(2)
    result3 = await my_async(3)
    print(result1)
    print(result2)
    print(result3)


@time_me
async def main_tasks():
    task1 = asyncio.create_task(my_async(1))
    task2 = asyncio.create_task(my_async(2))
    task3 = asyncio.create_task(my_async(3))
    res1 = await task1
    res2 = await task2
    res3 = await task3
    print(res1)
    print(res2)
    print(res3)


@time_me
async def main_gather():
    tasks = [asyncio.create_task(my_async(rand_int())) for _ in range(1000)]
    results = await asyncio.gather(*tasks)
    print(results)


@time_me
async def main_as_completed():
    tasks = [my_async(rand_int()) for _ in range(1000)]
    for res in asyncio.as_completed(tasks):
        print(await res)


# 3.11 New Syntax
# Will throw an error if python version is below 3.11
# @time_me
# async def main311():
#     async with asyncio.TaskGroup() as tg:
#         tasks = [tg.create_task(my_async(rand_int())) for _ in range(1000)]
#     for t in tasks:
#         print(t.result())


@time_me
async def main_semaphore():
    sem = asyncio.Semaphore(2)
    task1 = asyncio.create_task(my_async(1, sem))
    task2 = asyncio.create_task(my_async(1, sem))
    task3 = asyncio.create_task(my_async(1, sem))
    task4 = asyncio.create_task(my_async(1, sem))
    task5 = asyncio.create_task(my_async(1, sem))
    task6 = asyncio.create_task(my_async(1, sem))
    res1 = await task1
    res2 = await task2
    res3 = await task3
    res4 = await task4
    res5 = await task5
    res6 = await task6

    print(res1)
    print(res2)
    print(res3)
    print(res4)
    print(res5)
    print(res6)


if __name__ == "__main__":
    asyncio.run(main_semaphore())
