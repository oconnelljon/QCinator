# notes
"""
This file creates the 404 not found page.
If this file is not included, Dash will the same layout shown below.
If you need a more customized 404 not found page, modify this file.
"""

# package imports
import dash
from dash import html

dash.register_page(__name__, path="/", redirect_from=["/home"], title="Home")

layout = html.Div(
    [
        html.H1("Home page!"),
        html.Div(html.A("Checkout the complex page here.", href="/complex")),
        html.A(
            "/page2",
            href="/page2",
        ),
    ]
)
