from datetime import datetime, timedelta


recentMessages = {}

lastShout = datetime.utcnow()
refractory_period = timedelta(seconds=10)
timeLimit = 3
userLimit = 5
time_adjust = timedelta(seconds=timeLimit)


def get_active_typers(now, channel):
    return [
        x
        for x in recentMessages[channel].values()
        if x > now - time_adjust and x <= now
    ]


def typing_detector(channel, user, when, now=None):
    if not now:
        now = when

    global lastShout

    user = user

    if channel not in recentMessages:
        recentMessages[channel] = {}

    recentMessages[channel][user] = when

    typers = get_active_typers(now, channel)

    print(recentMessages)

    if len(typers) > userLimit:
        if lastShout + timedelta(seconds=60) < datetime.utcnow():
            lastShout = now
            print("several")
            return "SEVERAL PEOPLE ARE TYPING"
        else:
            print("several, throttled")


if __name__ == "__main__":

    channel = 1234
    clock = datetime.utcnow()
    lastShout = clock - timedelta(seconds=300)

    assert typing_detector(channel, 1, clock + timedelta(seconds=0.1)) is None
    assert typing_detector(channel, 2, clock + timedelta(seconds=1)) is None
    assert typing_detector(channel, 3, clock + timedelta(seconds=1)) is None
    assert typing_detector(channel, 4, clock + timedelta(seconds=1.5)) is None
    assert typing_detector(channel, 5, clock + timedelta(seconds=2)) is None
    assert (
        typing_detector(channel, 6, clock + timedelta(seconds=2))
        == "SEVERAL PEOPLE ARE TYPING"
    )

    assert typing_detector(channel, 6, clock + timedelta(seconds=2)) is None

    # ignore future types
    # assert len(get_active_typers(clock)) == 0

    # # typers up until john
    # assert len(get_active_typers(clock + timedelta(seconds=2))) == 6

    # # cause jacob to drop
    # assert len(get_active_typers(clock + timedelta(seconds=0.1 + timeLimit))) == 5
