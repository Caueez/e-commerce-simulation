from infra.messaging.tests.test_messaging import ManualTest

import asyncio



if __name__ == "__main__":
    try:
        teste = ManualTest()
        asyncio.run(teste.main_async())
    except KeyboardInterrupt:
        print("Saindo...")