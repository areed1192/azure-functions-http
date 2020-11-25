# Azure Functions

## Table of Contents

- [Overview](#overview)
- [Resources](#resources)
- [Setup](#setup)
- [Usage](#usage)
- [Support These Projects](#support-these-projects)

## Overview

The `TimerTrigger` makes it incredibly easy to have your functions
executed on a schedule. This sample demonstrates a simple use case
of calling your function every 5 minutes. For a `TimerTrigger` to
work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression)
(See the link for full details). A cron expression is a string with
6 separate expressions which represent a given schedule via patterns.
The pattern we use to represent every 5 minutes is `0 */5 * * * *`.
This, in plain text, means: "When seconds is equal to 0, minutes is
divisible by 5, for any hour, day of the month, month, day of the week,
or year".

## Resources

To use this project you will need to install some dependencies to connect to the database.
To download the drivers needed go to to [Microsoft SQL Drivers for Python](https://docs.microsoft.com/en-us/sql/connect/sql-connection-libraries?view=sql-server-ver15#anchor-20-drivers-relational-access). Once you download it, run through
the installation process.

**Resources - PYODBC with Azure:**

If you would like to read more on the topic of using PYODBC in conjunction with Microsoft
Azure, then I would refer you to the [documentation provided by Microsoft](https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15).

**Setup - Requirement Install:**

If you don't plan to use this project in any of your other projects, I would recommend you
just install the dependencies by using the `requirement.txt` file.

```console
pip install --requirement requirements.txt
```

## Support These Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding)
. I'm always looking to add more content for individuals like yourself, unfortuantely some of the
APIs I would require me to pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

## How it works
