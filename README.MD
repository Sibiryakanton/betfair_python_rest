1. Status of development

1.1. API EXCHANGE BETTING - In process
<br>
1.1.1. Manager class - Done
<br>
1.1.2. Forms - Done
<br>
1.1.3. Enums - Done
<br>
1.1.4. Exceptions - Done
<br>
1.1.5. Full documentation in Readme - Not started
<br>
1.1.6. Tests covering - Not started

1.2. API EXCHANGE ACCOUNTS - Paused
<br>
1.2.1. Manager class - Paused
<br>
1.2.2. Forms - Not started
<br>
1.2.3. Enums - Not started
<br>
1.2.4. Exceptions - Not started
<br>
1.2.5. Full documentation in Readme - Not started
<br>
1.1.6. Tests covering - Not started


2. How to install

pip install betfair_python_rest

Create your own class based on the one that comes 
in the package, indicating the certificate information. Example:

class CustomBetFairAPIManagerBetting(BetFairAPIManagerBetting):
    crt_path = os.path.join('home', 'antonssd', 'Django-u', 'sportmind', 'client-2048.crt')
    crt_key_path = os.path.join('home', 'antonssd', 'Django-u', 'sportmind', 'client-2048.key')

Done, you can use it like that:
    api_manager = CustomBetFairAPIManagerBetting(login, password, api_key, log_mode=True)
    market_and_locale = MarketFilterAndLocaleForm(text_query='Soccer')
    api_manager.list_event_types(request_class_object=market_and_locale)

3. How to use (with examples)

4. Reference quide

4.1. Managers
4.1.1. Betting API
4.1.2. Accounts API

4.2. Forms
4.2.1. Betting API Forms
4.2.1. Accounts API Forms

4.3. Enums
4.3.1. Betting API Enums
4.3.2. Accounts API Enums
