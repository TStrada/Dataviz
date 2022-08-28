from subprocess import Popen

def load_jupyter_server_extension(nbapp):
    """serve the Dashboard_PLot&Export.ipynb directory with bokeh server"""
    Popen(["panel", "serve", "Dashboard_PLot&Export.ipynb", "--allow-websocket-origin=*"])
