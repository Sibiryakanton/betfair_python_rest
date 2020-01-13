1. Status of development

1.1. API EXCHANGE BETTING - In process
<br>
Manager class, Forms, Exceptions, Readme - Done

1.2. API EXCHANGE ACCOUNTS - Paused
<br>
Manager class - Paused
<br>
Forms, Enums, Exceptions, Tests covering - Not started


2. How to install
# TODO Upload on pypi
pip install betfair_python_rest

Create your own class based on the one that comes 
in the package, indicating the certificate information. Example:

class CustomBetFairAPIManagerBetting(BetFairAPIManagerBetting):
    crt_path = os.path.join('home', 'antonssd', 'Django-u', 'sportmind', 'client-2048.crt')
    crt_key_path = os.path.join('home', 'antonssd', 'Django-u', 'sportmind', 'client-2048.key')

Now you can use it like that:
    api_manager = CustomBetFairAPIManagerBetting(login, password, api_key, log_mode=True)
    market_and_locale = MarketFilterAndLocaleForm(text_query='Soccer')
    api_manager.list_event_types(request_class_object=market_and_locale)

3. How to use (with examples)
In short, the package is designed like this:
managers - API-managers classes
forms - Classes which describing the schemes of data inputs for every method
enums - Classes with a list of possible options for parameter values.
exceptions - There is just two files: exceptions class and
 enum with variables of error code from server 

File with examples of using: example.py

I should clarify a one point: API-methods waiting for form classes
 objects, not jus arguments array. This was done due to the 
 fact that many methods accept the same fields, 
and sometimes entire sets of fields, and in order to avoid copy-paste 
of attributes and dockstring into dozens of models, it was decided to
 make each method accept an object of the class of the corresponding form.

True, this leads to the fact that the fields themselves 
are scattered in dozens of classes, which can cause 
discomfort when you first familiarize yourself with the package.
 I tried to smooth out this flaw a little, accompanying each class with explanations.
 
As a result, if, for example, you want to find the country by the line "land", then 
you will need to use the MarketFilterAndLocaleForm class and pass arguments there. 
the names are kept exactly and are only slightly adapted to the Pep8 standard, so that 
you quickly understand what’s what (especially if autocompletion is included in the IDE)

All forms are located in the forms folder and repeat the names 
of the requests, so you can easily find them even
 without auto-completion (I hope)
