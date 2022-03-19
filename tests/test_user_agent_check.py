import requests
import pytest


class TestUserAgentCheck:
    user_agent = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]

    @pytest.mark.parametrize('user_agent', user_agent)
    def test_user_agent_check(self, user_agent):

        platform = [
            ("Mobile"),
            ("Googlebot"),
            ("Web")
        ]
        browser = [
            ("No"),
            ("Chrome"),
            ("Unknown")
        ]
        device = [
            ("Android"),
            ("iOS"),
            ("Unknown"),
            ("No"),
            ("iPhone")
        ]

        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent}
        )

        response_platform = response.json()["platform"]
        response_browser = response.json()["browser"]
        response_device = response.json()["device"]

        if user_agent == TestUserAgentCheck.user_agent[0]:
            #Expected values:'platform': 'Mobile', 'browser': 'No', 'device': 'Android'
            assert response_platform == platform[0], f"The platform is't {platform[0]}"
            assert response_browser == browser[0], f"The browser is't {browser[0]}"
            assert response_device == device[0], f"The device is't {device[0]}"
        elif user_agent == TestUserAgentCheck.user_agent[1]:
            #Expectedvalues: 'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'
            assert response_platform == platform[0], f"The platform is't {platform[0]}"
            assert response_browser == browser[1], f"The browser is't {browser[1]}"
            assert response_device == device[1], f"The device is't {device[1]}"
        elif user_agent == TestUserAgentCheck.user_agent[2]:
            #Expected values:'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'
            assert response_platform == platform[1], f"The platform is't {platform[1]}"
            assert response_browser == browser[2], f"The browser is't {browser[2]}"
            assert response_device == device[2], f"The device is't {device[2]}"
        elif user_agent == TestUserAgentCheck.user_agent[3]:
            #Expected values: 'platform': 'Web', 'browser': 'Chrome', 'device': 'No'
            assert response_platform == platform[2], f"The platform is't {platform[2]}"
            assert response_browser == browser[1], f"The browser is't {browser[1]}"
            assert response_device == device[3], f"The device is't {device[3]}"
        elif user_agent == TestUserAgentCheck.user_agent[4]:
            #Expected values: 'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'
            assert response_platform == platform[0], f"The platform is't  {platform[0]}"
            assert response_browser == browser[0], f"The browser is't  {browser[0]}"
            assert response_device == device[4], f"The device is't  {device[4]}"

