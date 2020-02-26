# kosmorro(1) -- a program that computes the ephemerides

## SYNOPSIS

`kosmorro`  
`kosmorro` [_OPTIONS_]...

## OPTIONS

`-h`, `--help`  
    show a help message and exit

`--version`, `-v`  
    show the program version

`--clear-cache`  
    delete all the files Kosmorro stored in the cache

`--latitude=`_LATITUDE_, `-lat` _LATITUDE_  
    the observer's latitude on Earth

`--longitude=`_LONGITUDE_, `-lon` _LONGITUDE_  
    the observer's longitude on Earth

`--day=`_DAY_, `-d` _DAY_  
    a number between 1 and 28, 29, 30 or 31 (depending on the month); the day you want to compute the ephemerides for, defaults to the current day

`--month=`_MONTH_, `-m` _MONTH_  
    a number between 1 and 12; the month you want to compute the ephemerides for, defaults to the current month

`--year=`_YEAR_, `-y` _YEAR_  
    the year you want to compute the ephemerides for; defaults to the current year

`--timezone=`_TIMEZONE_, `-t` _TIMEZONE_  
    the timezone to display the hours in; e.g. 2 for UTC+2 or -3 for UTC-3

`--no-colors`  
    disable the colors in the console

`--output=`_OUTPUT_, `-o` _OUTPUT_
    a file to export the output to; if not given, the standard output is used

`--format=`_FORMAT_, `-f` _FORMAT_  
    the format under which the information have to be output; one of the following: text, json, pdf

## EXAMPLE

Compute the ephemerides for Lille, France, on April 1st, 2022:

```
kosmorro --latitude=50.5876 --longitude=3.0624 -d 1 -m 4 -y 2022
```

Compute the ephemerides for Lille, France, on April 1st, 2022, and export them in a PDF document:

```
kosmorro --latitude=50.5876 --longitude=3.0624 -d 1 -m 4 -y 2022 --format=pdf --output=file.pdf
```

## AUTHOR

Written by Jérôme Deuchnord.

## REPORTING BUGS

Please report any encountered bugs on Kosmorro's [GitHub project](https://github.com/Deuchnord/kosmorro).

## COPYRIGHT

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

