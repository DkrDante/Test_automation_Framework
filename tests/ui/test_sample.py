def test_homepage(page, config):
    page.goto(config["base_url"])
    assert "SatoriXR" in page.title()