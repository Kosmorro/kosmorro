# Kosmorro's manpages

This folder contains Kosmorro's manpages.

Two sections are available:

- Section 1: contains the details about the command line usage.
- Section 7: contains the vocabulary used in Kosmorro along with their definitions.

## How to use it

To open the manpage from section 1, open a terminal and invoke:

```bash
man kosmorro
```

If you want to open the vocabulary:

```bash
man 7 kosmorro
````

## `man` complains there's "No manual entry for kosmorro"

Sometimes, especially on Mac, `man` needs to be informed about where the manpages are stored by Python 3. Invoke the following command to do this:

```bash
echo 'export MANPATH=/usr/local/man:$MANPATH' >> $HOME/.bashrc
```

And open a new terminal.

NB: if you are not using Bash, change `.bashrc` with the correct file.
