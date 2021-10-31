"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # st.markdown('# Laundromat Customer Profiling')
        # st.markdown('### Application Navigation Menu')
        # st.markdown('This web application is a multiple page application for the laundry shop customer profiling project. \nChoose from the list of pages below to explore more.')
        # app = st.selectbox(
        #     'Go to',
        #     self.apps,
        #     format_func=lambda app: app['title'])
        # app['function']()

        st.sidebar.markdown('# Laundromat Customer Profiling')

        st.sidebar.markdown('### Application Navigation Menu')
        st.sidebar.markdown('This web application is a multiple page application for the laundry shop customer profiling project. \nChoose from the list of pages below to explore more.')
        
        st.sidebar.header('Navigation')
        section = st.sidebar.radio("Go to:", 
                                self.apps,
                                format_func=lambda app: app['title']
                              )
        section['function']()