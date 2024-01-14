if __name__ == "__main__":
    import dotenv
    from src.main import main
    from src import logger
    # from streamlit_mic_recorder import speech_to_text # TODO - naive thinking that let me to think having us import here would increase page performance... lol, oh well

    dotenv.load_dotenv()
    logger.setup_logging()

    # import logging
    # logging.getLogger("fsevents").setLevel(logging.WARNING)
    # logging.getLogger("matplotlib").setLevel(logging.WARNING)
    main()
