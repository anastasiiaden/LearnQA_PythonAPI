class TestPhrase():
    def test_phrase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) < 15, f"The phrase is longer than 15 characters. It contains {len(phrase)} characters"