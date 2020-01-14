Python package of REST API managers (Betting and Accounts APIs)


<h5>HOW TO INSTALL</h5>

```
pip install betfair-python-rest
```

Create your own class based on the one that comes 
in the package, indicating the certificate information. Example:

```
class CustomBetFairAPIManagerBetting(BetFairAPIManagerBetting):
    crt_path = os.path.join('home', 'user', 'your_project', 'client-2048.crt')
    crt_key_path = os.path.join('home', 'user', 'your_project-u', 'client-2048.key')
```

Now you can use it like that:

```
api_manager = CustomBetFairAPIManagerBetting(login, password, api_key, log_mode=True)
market_and_locale = MarketFilterAndLocaleForm(text_query='Soccer')
api_manager.list_event_types(request_class_object=market_and_locale)
```

HOW TO USE (with examples)

In short, the package is designed like this:

managers - API-managers classes

forms - Classes which describing the schemes of data inputs for every method

enums - Classes with a list of possible options for parameter values.

exceptions - There is just two files: exceptions class and
enum with variables of error code from server 

<b> File with examples of using: example.py</b>

I should clarify a one point: API-methods in Betting branch waiting for 
form classes objects, not just arguments array. This was done due to the 
fact that many methods accept the same fields, 
and sometimes entire sets of fields, and in order to avoid copy-paste 
of attributes and docstring into dozens of models, it was decided to
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

This feature does not apply to Accounts manager: requests of this 
category accept few requests, practically do not repeat among
themselves according to a set of input data. Therefore, there,
at the entrance to the methods, a familiar series 
of arguments, not a form.
