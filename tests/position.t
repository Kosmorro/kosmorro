First, prepare the Python environment:
    $ KOSMORRO="$TESTDIR/../kosmorro --no-colors"

---

User can give a position in Plus Code format:

    $ $KOSMORRO --position="9F25J3H5+M8" --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          06:01           13:54           21:47
    Moon         21:04             -             03:33
    Mercury      04:55           13:06           21:17
    Venus        08:49           15:58           23:08
    Mars         08:21           15:38           22:54
    Jupiter      22:53           04:00           09:03
    Saturn       22:08           02:43           07:13
    Uranus       01:10           08:35           16:01
    Neptune      23:34           05:24           11:09
    Pluto        21:31           01:39           05:43
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

---

If the Plus Code is in a short format, then an error is displayed:

    $ $KOSMORRO --position="J3H5+M8" --date="2021-07-22"
    The given Plus Code seems to be a short code, please provide a full code.
    [1]

---

User can give a position in the 'latitude,longitude' format:

    $ $KOSMORRO --position="50.5876,3.0624" --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          06:01           13:54           21:46
    Moon         21:04             -             03:33
    Mercury      04:55           13:06           21:17
    Venus        08:49           15:58           23:07
    Mars         08:21           15:38           22:54
    Jupiter      22:53           04:00           09:03
    Saturn       22:08           02:42           07:13
    Uranus       01:10           08:35           16:00
    Neptune      23:34           05:23           11:09
    Pluto        21:31           01:39           05:43
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

    $ $KOSMORRO --position="50.5876;-3.0624" --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          06:26           14:19           22:11
    Moon         21:30           00:10           03:59
    Mercury      05:20           13:31           21:42
    Venus        09:13           16:23           23:32
    Mars         08:46           16:02           23:19
    Jupiter      23:17           04:24           09:28
    Saturn       22:32           03:07           07:38
    Uranus       01:35           09:00           16:25
    Neptune      00:02           05:48             -
    Pluto        21:55           02:03           06:07
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

    $ $KOSMORRO --position="-50.5876;-3.0624" --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          09:59           14:19           18:39
    Moon         16:31           00:12           08:54
    Mercury      09:26           13:31           17:36
    Venus        11:22           16:24           21:26
    Mars         11:09           16:03           20:57
    Jupiter      21:14           04:24           11:30
    Saturn       19:24           03:07           10:46
    Uranus       04:15           09:00           13:44
    Neptune      23:21           05:48           12:11
    Pluto        17:52           02:03           10:10
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

    $ $KOSMORRO --position="50.5876,-3.0624" --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          06:26           14:19           22:11
    Moon         21:30           00:10           03:59
    Mercury      05:20           13:31           21:42
    Venus        09:13           16:23           23:32
    Mars         08:46           16:02           23:19
    Jupiter      23:17           04:24           09:28
    Saturn       22:32           03:07           07:38
    Uranus       01:35           09:00           16:25
    Neptune      00:02           05:48             -
    Pluto        21:55           02:03           06:07
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

    $ $KOSMORRO --position="-50.5876,-3.0624" --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          09:59           14:19           18:39
    Moon         16:31           00:12           08:54
    Mercury      09:26           13:31           17:36
    Venus        11:22           16:24           21:26
    Mars         11:09           16:03           20:57
    Jupiter      21:14           04:24           11:30
    Saturn       19:24           03:07           10:46
    Uranus       04:15           09:00           13:44
    Neptune      23:21           05:48           12:11
    Pluto        17:52           02:03           10:10
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

---

Giving an empty string as a position is equivalent as giving no position at all:

    $ $KOSMORRO --position="" --date="2021-07-22"
    Thursday July 22, 2021
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

---

If coordinates are set in the KOSMORRO_POSITION environment variable, then the '--position' argument is not needed:

    $ KOSMORRO_POSITION="50.5876,-3.0624" $KOSMORRO --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          09:59           14:19           18:39
    Moon         16:31           00:12           08:54
    Mercury      09:26           13:31           17:36
    Venus        11:22           16:24           21:26
    Mars         11:09           16:03           20:57
    Jupiter      21:14           04:24           11:30
    Saturn       19:24           03:07           10:46
    Uranus       04:15           09:00           13:44
    Neptune      23:21           05:48           12:11
    Pluto        17:52           02:03           10:10
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.

    $ KOSMORRO_POSITION="9F25J3H5+M8" $KOSMORRO --date="2021-07-22"
    Thursday July 22, 2021
    
    Object     Rise time    Culmination time    Set time
    --------  -----------  ------------------  ----------
    Sun          06:01           13:54           21:47
    Moon         21:04             -             03:33
    Mercury      04:55           13:06           21:17
    Venus        08:49           15:58           23:08
    Mars         08:21           15:38           22:54
    Jupiter      22:53           04:00           09:03
    Saturn       22:08           02:43           07:13
    Uranus       01:10           08:35           16:01
    Neptune      23:34           05:24           11:09
    Pluto        21:31           01:39           05:43
    
    Moon phase: Waxing Gibbous
    Full Moon on Saturday July 24, 2021 at 02:36
    
    Note: All the hours are given in the UTC timezone.
