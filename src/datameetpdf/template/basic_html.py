"""Basic HTML."""


def _basic_html(body_str: str):
    output = (
        f'<!DOCTYPE html><html lang="en-GB">'
        f'<head>'
        f'<script src="https://cdn.rawgit.com/inexorabletash/polyfill/v0.1.42/polyfill.js"></script>'
        f'<script src="https://cdn.rawgit.com/inexorabletash/polyfill/v0.1.42/typedarray.js"></script>'
        f'<script src="https://cdn.plot.ly/plotly-cartesian-latest.min.js"></script>'
        f'</head>'
        f'  <div class="container">'
        f'     <div class="row">'
        f'          <div class="col-12">'
        f'              {body_str}'
        f'          </div>'
        f'     </div>'
        f'  </div>'
    )
    return output


def _plotly_html(body_str: str):
    output = (
        f'<div id="divPlotly"></div>'
        f'<script>'
        f'  var plotly_data = {body_str};'
        f'  Plotly.react("divPlotly", plotly_data.data, plotly_data.layout);'
        f'</script>'
    )
    return output
