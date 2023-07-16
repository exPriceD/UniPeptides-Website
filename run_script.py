import setup
import back_asyncio


def run_processing(user_data: dict):
    setup.setupConfig()
    setup.filling_config(user_data=user_data)
    missing = back_asyncio.main()
    return missing
