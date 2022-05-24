OpenRobot API Wrapper Documentation
===================================

Client
------

AsyncClient
~~~~~~~~~~~

.. autoclass:: openrobot.api_wrapper.AsyncClient
    :members:
    :exclude-members: _get_authorization_headers, _request

SyncClient
~~~~~~~~~~

.. autoclass:: openrobot.api_wrapper.SyncClient
    :members:
    :exclude-members: _get_authorization_headers, _request

Translate
---------

Translate
~~~~~~~~~

.. autoclass:: openrobot.api_wrapper.Translate()
    :members: __call__, languages

Speech
------

Speech
~~~~~~

.. autoclass:: openrobot.api_wrapper.Speech()
    :members:

Results
-------

.. autoclass:: openrobot.api_wrapper.LyricImages()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.LyricResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.NSFWCheckAdult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.NSFWCheckRacy()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.NSFWCheckGore()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.NSFWCheckResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.CelebrityFaceRectangle()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.CelebrityResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.SpeechToTextResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.TextToSpeechResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.TextToSpeechSupportLanguage()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.TextToSpeechSupportVoice()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.TextToSpeechSupportResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.OCRResult()
    :members:
    :inherited-members:

.. autoclass:: openrobot.api_wrapper.TranslateResult()
    :members:
    :inherited-members: