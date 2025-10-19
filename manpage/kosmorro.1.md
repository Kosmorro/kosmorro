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

`--position=`"_LATITUDE_,_LONGITUDE_", `-p` "_LATITUDE_,_LONGITUDE"  
    the observer's position on Earth

`--date=`_DATE_, `-d` _DATE_  
    The date for which the ephemerides must be computed, either in the YYYY-MM-DD format or as an interval in the "[+-]YyMmDd" format (with Y, M, and D numbers); defaults to the current date

`--timezone=`_TIMEZONE_, `-t` _TIMEZONE_  
    the timezone to use to display the hours; it can be either a number (e.g. 1 for UTC+1) or a timezone name (e.g. Europe/Paris)

`--no-colors`  
    disable the colors in the console

`--output=`_OUTPUT_, `-o` _OUTPUT_  
    a file to export the output to; if not given, the standard output is used

`--format=`_FORMAT_, `-f` _FORMAT_ (optional)  
    the format under which the information have to be output; one of the following:
    text (plain text, like normal console output), json, tex (LaTeX), pdf.
    If no format is provided, the output format will be inferred from the extension of the output file

`--no-graph`  
    present the ephemerides in a table instead of a graph; PDF output format only

`--completion [SHELL]`  
    generate completion scripts for the specified shell (bash, zsh, fish, powershell)

## ENVIRONMENT VARIABLES

The environment variable listed below may be used instead of the options.
The options have a higher priority than the environment variable.
As a consequence, any option that would be given to `kosmorro` will override its corresponding environment variable.

Available environment variables are:

`KOSMORRO_POSITION`  
    the observer's position on Earth (alternative to `--position`)
    
`KOSMORRO_TIMEZONE`  
    the observer's timezone (alternative to `--timezone`)

`NO_COLOR`
    disable colored console output (alternative to `--no-colors`)

## EXAMPLES

Compute the events only for the current date:

```
kosmorro
```

Compute the ephemerides for Lille, France, on April 1st, 2022:

```
kosmorro --latitude=50.5876 --longitude=3.0624 --date=2022-04-01
```

Compute the ephemerides for Lille, France, on April 1st, 2022, and export them in a PDF document:

```
kosmorro --latitude=50.5876 --longitude=3.0624 -date=2022-04-01 --output=file.pdf
```

## AUTHOR

Written by Jérôme Deuchnord.

## REPORTING BUGS

Please report any encountered bugs on Kosmorro's [GitHub project](https://github.com/Deuchnord/kosmorro).

## COPYRIGHT

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

