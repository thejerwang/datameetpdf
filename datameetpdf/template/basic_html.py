"""Basic HTML."""


def _basic_html(body_str: str):
    output = (
        f"<!DOCTYPE html><html lang='en-GB'><head></head>"
        f"  <div class='container'>"
        f"     <div class='row'>"
        f"          <div class='col-12'>"
        f"              {body_str}"
        f"          </div>"
        f"     </div>"
        f"  </div>"
    )
    return output
