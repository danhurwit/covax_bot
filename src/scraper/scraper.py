from .MassVax import MassVax


def scrape():
    m = MassVax()
    m.scrape_locations()
