from subprocess import Popen

def load_jupyter_server_extension(nbapp):
    """serve the Dashboard_Plot&Export_Test.ipynb directory with bokeh server"""
    Popen(["panel", "serve", "Dashboard_Plot&Export_Test.ipynb", "--allow-websocket-origin=*"])
