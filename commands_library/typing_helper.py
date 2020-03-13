from datetime import datetime, timedelta

recentMessages = {}

lastShout = datetime.utcnow()

refractory_period = timedelta(seconds=10)

timeLimit = 3
userLimit = 5
timeAdjust = timedelta(seconds=timeLimit)


def typing_detector(channel, user, when):
    global lastShout
    # user = user.name
    user = user.id
    print(user)

    prune_stack()

    # push payload to stack
    if channel.id not in recentMessages:
        recentMessages[channel.id] = [(user, when)]
    elif len(recentMessages[channel.id]) == 0:
        recentMessages[channel.id].append((user, when))
    else:
        for index, item in enumerate(recentMessages[channel.id]):
            if item[0] == user:
                recentMessages[channel.id][index] = (user, when)
            else:
                # recentMessages[channel.id].remove(item)
                recentMessages[channel.id].append((user, when))

    for key, value in recentMessages.items():
        if (len(value)) > userLimit:
            print("several")
            lastShout = datetime.utcnow()

            return "SEVERAL PEOPLE ARE TYPING"

    print(recentMessages)


def prune_stack():
    for key, value in recentMessages.items():
        for item in value:
            if item[1] < datetime.utcnow() - timeAdjust:
                value.remove(item)
