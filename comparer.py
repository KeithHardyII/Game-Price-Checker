class PriceComparer:
    """
    Compares API prices to scraped prices for a given Game object.
    """

    def compare(self, game):
        """
        Returns difference or a message about which price is lower.
        """
        if game.api_price is None or game.scraped_price is None:
            return "Missing data."

        difference = game.scraped_price - game.api_price

        if difference > 0:
            return f"ITAD (API) is cheaper by {difference:.2f}"
        elif difference < 0:
            return f"Steam (Website) is cheaper by {-difference:.2f}" # Because ITAD searches steam as well this should never be true
        else:
            return "Both prices are equal."
