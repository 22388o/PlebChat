import os

import streamlit as st

# from src.VERSION import VERSION

ASSET_FOLDER = os.path.join(os.path.dirname(__file__), "assets")


# https://www.markdownguide.org/extended-syntax/
EXPLANATION1 = """
The __purpose__ of this project is to:
1.  Teach myself to build custom AI applications. :brain:
2.  Build a portfolio of _useful_ AI applications. :briefcase:
3.  Use these applications to improve my own productivity. :chart_with_upwards_trend:
4.  Implement open-source AI models and run them on my own hardware. :computer:
5.  Have fun :hearts: and inspire others! :sparkles:
"""

EXPLANATION2 = """
Large Language Models are rapidly improving and promise to radically change the way we interact with computers.  My worry is that closed-source, subscription-based services will dominate the market and that expertise will be concentrated in the hands of a few large companies.

Not only can we build our own applications, but we can use public-domain AI models and run them on our own machines.  This project is a demonstration of how to build private, custom AI applications using free, open-source software on privately-owned inexpensive second-hand hardware.

This project is completely [open-source](https://github.com/PlebeiusGaragicus/PlebbyIntelligence) and free to use.

Please submit [feature requests, ideas or bug reports](https://github.com/PlebeiusGaragicus/PlebbyIntelligence/issues)
"""


def about_page():
    col = st.columns((1, 1))
    with col[0]:
        st.write(EXPLANATION1)

    with col[1]:
        st.image(
            image=os.path.join(ASSET_FOLDER, "assistant2sm.png"),
            caption="your own friendly assistant!",
        )

    st.write("---")
    st.write(EXPLANATION2)


# with st.expander("How to export data from 'remote CAD'"):
#     image_column, text_column = st.columns((1, 2))

#     with image_column:
#         st.image("https://picsum.photos/200")

#     with text_column:
#         st.write("This is a column of text")

# st.caption("A caption with _italics_ :blue[colors] and emojis :sunglasses:")  # TODO

# st.warning("This is a warning", icon="⚠️")

# st.image(os.path.join(ASSET_FOLDER, "pf&r-logo.png"), width=200)


# with st.spinner("Wait for it..."):
#     time.sleep(1.5)  #

# progress_text = "Loading bar example..."
# my_bar = st.progress(0, text=progress_text)

# for percent_complete in range(10):
#     time.sleep(0.2)
#     my_bar.progress((1 + percent_complete) * 10, text=progress_text)
# time.sleep(1)
# my_bar.empty()
