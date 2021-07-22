First, prepare the Python environment:
    $ KOSMORRO="$TESTDIR/../kosmorro --no-colors"

---

If user tries to set an invalid a date, an error is displayed:

    $ $KOSMORRO -d 2020-13-32
    \x1b[1m\x1b[31mThe date 2020-13-32 is not valid: month must be in 1..12\x1b[0m (esc)
    [255]

---

If user gives a date out of bound, an error is displayed:

    $ $KOSMORRO --date=1789-05-05
    \x1b[33mMoon phase can only be displayed between Aug 09, 1899 and Sep 26, 2053\x1b[0m (esc)
    [1]

    $ $KOSMORRO --date=3000-01-01
    \x1b[33mMoon phase can only be displayed between Aug 09, 1899 and Sep 26, 2053\x1b[0m (esc)
    [1]

---

User can give a relative date:

    $ $KOSMORRO --date='+3y 5m3d'
    (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (January|February|March|April|June|July|August|September|October|November|December) \d{1,2}, \d{4} (re)
    
    Moon phase: .+ (re)
    (.+) on (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (January|February|March|April|June|July|August|September|October|November|December) \d{1,2}, \d{4} at \d{2}:\d{2} (re)
    
    (Expected events:)? (re)
    (\d{2}:\d{2}  .+)? (re)
    
    Note: All the hours are given in the UTC timezone.

    $ $KOSMORRO --date='-1y3d'
    (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (January|February|March|April|June|July|August|September|October|November|December) \d{1,2}, \d{4} (re)
    
    Moon phase: .+ (re)
    (.+) on (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (January|February|March|April|June|July|August|September|October|November|December) \d{1,2}, \d{4} at \d{2}:\d{2} (re)
    
    (Expected events:)? (re)
    (\d{2}:\d{2}  .+)? (re)

---

If the format of the relative date is incorrect, an error is displayed:

    $ $KOSMORRO --date='+3d4m'
    \x1b[1m\x1b[31mThe date +3d4m does not match the required YYYY-MM-DD format or the offset format.\x1b[0m (esc)
    [255]

    $ $KOSMORRO -date='3y'
    \x1b[1m\x1b[31mThe date ate=3y does not match the required YYYY-MM-DD format or the offset format.\x1b[0m (esc)
    [255]
