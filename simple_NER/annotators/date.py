from simple_NER.annotators import NERWrapper
from simple_NER import Entity

import re
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from lingua_franca.lang.parse_en import _convert_words_to_numbers_en, \
    is_numeric, extractnumber_en
from lingua_franca.format import nice_duration, nice_date


def _annotate_datetime_en(string, dateNow=None, default_time=None):
    """ Convert a human date reference into an exact datetime

    Convert things like
        "today"
        "tomorrow afternoon"
        "next Tuesday at 4pm"
        "August 3rd"
    into a datetime.  If a reference date is not provided, the current
    local time is used.  Also returns the words used to define the date

    For example, the string
       "what is Tuesday's weather forecast"
    returns the date for the forthcoming Tuesday relative to the reference
    date and the string
       "Tuesday".

    Args:
        string (str): string containing date words
        dateNow (datetime): A reference date/time for "tommorrow", etc
        default_time (time): Time to set if no time was found in the string

    Returns:
        [datetime, str]: An array containing the datetime and the
                         text consumed in the parsing, or None if no
                         date or time related text was found.
    """
    dateNow = dateNow or datetime.now()

    def clean_string(s):
        # clean unneeded punctuation and capitalization among other things.
        s = s.lower().replace('?', '').replace('.', '').replace(',', '') \
            .replace(' the ', ' ').replace(' a ', ' ').replace(' an ', ' ') \
            .replace("o' clock", "o'clock").replace("o clock", "o'clock") \
            .replace("o ' clock", "o'clock").replace("o 'clock", "o'clock") \
            .replace("oclock", "o'clock").replace("couple", "2") \
            .replace("centuries", "century").replace("decades", "decade") \
            .replace("millenniums", "millennium")

        wordList = s.split()
        for idx, word in enumerate(wordList):
            word = word.replace("'s", "")

            ordinals = ["rd", "st", "nd", "th"]
            if word and word[0].isdigit():
                for ordinal in ordinals:
                    # "second" is the only case we should not do this
                    if ordinal in word and "second" not in word:
                        word = word.replace(ordinal, "")
            wordList[idx] = word

        return wordList

    def date_found():
        return found or \
               (
                       datestr != "" or
                       yearOffset != 0 or monthOffset != 0 or
                       dayOffset is True or hrOffset != 0 or
                       hrAbs or minOffset != 0 or
                       minAbs or secOffset != 0
               )

    if string == "" or not dateNow:
        return None

    found = False
    daySpecified = False
    dayOffset = False
    monthOffset = 0
    yearOffset = 0
    today = dateNow.strftime("%w")
    currentYear = dateNow.strftime("%Y")
    fromFlag = False
    datestr = ""
    hasYear = False
    timeQualifier = ""

    timeQualifiersAM = ['morning']
    timeQualifiersPM = ['afternoon', 'evening', 'night', 'tonight']
    timeQualifiersList = set(timeQualifiersAM + timeQualifiersPM)
    markers = ['at', 'in', 'on', 'by', 'this', 'around', 'for', 'of', "within"]
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november',
              'december']
    recur_markers = days + [d + 's' for d in days] + ['weekend', 'weekday',
                                                      'weekends', 'weekdays']
    monthsShort = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug',
                   'sept', 'oct', 'nov', 'dec']
    year_multiples = ["decade", "century", "millennium"]
    day_multiples = ["weeks", "months", "years"]

    words = clean_string(string)

    consumed = []
    for idx, word in enumerate(words):
        if word == "":
            continue
        wordPrevPrev = words[idx - 2] if idx > 1 else ""
        wordPrev = words[idx - 1] if idx > 0 else ""
        wordNext = words[idx + 1] if idx + 1 < len(words) else ""
        wordNextNext = words[idx + 2] if idx + 2 < len(words) else ""

        # this isn't in clean string because I don't want to save back to words
        word = word.rstrip('s')
        start = idx
        used = 0
        # save timequalifier for later

        if word == "now" and not datestr:
            resultStr = " ".join(words[idx + 1:])
            resultStr = ' '.join(resultStr.split())
            extractedDate = dateNow.replace(microsecond=0)
            return [extractedDate, word, resultStr]
        elif wordNext in year_multiples:
            multiplier = None
            if is_numeric(word):
                multiplier = extractnumber_en(word)
            multiplier = multiplier or 1
            multiplier = int(multiplier)
            used += 2
            if wordNext == "decade":
                yearOffset = multiplier * 10
            elif wordNext == "century":
                yearOffset = multiplier * 100
            elif wordNext == "millennium":
                yearOffset = multiplier * 1000
        # couple of
        elif word == "2" and wordNext == "of" and \
                wordNextNext in year_multiples:
            multiplier = 2
            used += 3
            if wordNextNext == "decade":
                yearOffset = multiplier * 10
            elif wordNextNext == "century":
                yearOffset = multiplier * 100
            elif wordNextNext == "millennium":
                yearOffset = multiplier * 1000
        elif word == "2" and wordNext == "of" and \
                wordNextNext in day_multiples:
            multiplier = 2
            used += 3
            if wordNextNext == "years":
                yearOffset = multiplier
            elif wordNextNext == "months":
                monthOffset = multiplier
            elif wordNextNext == "weeks":
                dayOffset = multiplier * 7
        elif word in timeQualifiersList:
            timeQualifier = word
        # parse today, tomorrow, day after tomorrow
        elif word == "today" and not fromFlag:
            dayOffset = 0
            used += 1
        elif word == "tomorrow" and not fromFlag:
            dayOffset = 1
            used += 1
        elif (word == "day" and
              wordNext == "after" and
              wordNextNext == "tomorrow" and
              not fromFlag and
              not wordPrev[0].isdigit()):
            dayOffset = 2
            used = 3
            if wordPrev == "the":
                start -= 1
                used += 1
                # parse 5 days, 10 weeks, last week, next week
        elif word == "day" and wordPrev:
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev)
                start -= 1
                used = 2
        elif word == "week" and not fromFlag:
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev) * 7
                start -= 1
                used = 2
            elif wordPrev == "next":
                dayOffset = 7
                start -= 1
                used = 2
            elif wordPrev == "last":
                dayOffset = -7
                start -= 1
                used = 2
                # parse 10 months, next month, last month
        elif word == "month" and not fromFlag:
            if wordPrev[0].isdigit():
                monthOffset = int(wordPrev)
                start -= 1
                used = 2
            elif wordPrev == "next":
                monthOffset = 1
                start -= 1
                used = 2
            elif wordPrev == "last":
                monthOffset = -1
                start -= 1
                used = 2
        # parse 5 years, next year, last year
        elif word == "year" and not fromFlag:
            if wordPrev[0].isdigit():
                yearOffset = int(wordPrev)
                start -= 1
                used = 2
            elif wordPrev == "next":
                yearOffset = 1
                start -= 1
                used = 2
            elif wordPrev == "last":
                yearOffset = -1
                start -= 1
                used = 2
        # parse Monday, Tuesday, etc., and next Monday,
        # last Tuesday, etc.
        elif word in days and not fromFlag:
            d = days.index(word)
            dayOffset = (d + 1) - int(today)
            used = 1
            if dayOffset < 0:
                dayOffset += 7
            if wordPrev == "next":
                dayOffset += 7
                used += 1
                start -= 1
            elif wordPrev == "last":
                dayOffset -= 7
                used += 1
                start -= 1
                # parse 15 of July, June 20th, Feb 18, 19 of February
        elif word in months or word in monthsShort and not fromFlag:
            try:
                m = months.index(word)
            except ValueError:
                m = monthsShort.index(word)
            used += 1
            datestr = months[m]
            if wordPrev and (wordPrev[0].isdigit() or
                             (wordPrev == "of" and wordPrevPrev[0].isdigit())):
                if wordPrev == "of" and wordPrevPrev[0].isdigit():
                    datestr += " " + words[idx - 2]
                    used += 1
                    start -= 1
                else:
                    datestr += " " + wordPrev
                start -= 1
                used += 1
                if wordNext and wordNext[0].isdigit():
                    datestr += " " + wordNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            elif wordNext and wordNext[0].isdigit():
                datestr += " " + wordNext
                used += 1
                if wordNextNext and wordNextNext[0].isdigit():
                    datestr += " " + wordNextNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False
        # parse 5 days from tomorrow, 10 weeks from next thursday,
        # 2 months from July
        validFollowups = days + months + monthsShort
        validFollowups.append("today")
        validFollowups.append("tomorrow")
        validFollowups.append("next")
        validFollowups.append("last")
        validFollowups.append("now")
        if (word == "from" or word == "after") and wordNext in validFollowups:
            used = 2
            fromFlag = True
            if wordNext == "tomorrow":
                dayOffset += 1
            elif wordNext in days:
                d = days.index(wordNext)
                tmpOffset = (d + 1) - int(today)
                used = 2
                if tmpOffset < 0:
                    tmpOffset += 7
                dayOffset += tmpOffset
            elif wordNextNext and wordNextNext in days:
                d = days.index(wordNextNext)
                tmpOffset = (d + 1) - int(today)
                used = 3
                if wordNext == "next":
                    tmpOffset += 7
                    used += 1
                    start -= 1
                elif wordNext == "last":
                    tmpOffset -= 7
                    used += 1
                    start -= 1
                dayOffset += tmpOffset
        if used > 0:
            if start - 1 > 0 and words[start - 1] == "this":
                start -= 1
                used += 1

            for i in range(0, used):
                consumed += [words[i + start]]
                words[i + start] = ""

            if start - 1 >= 0 and words[start - 1] in markers:
                words[start - 1] = ""
            found = True
            daySpecified = True
    # parse time
    hrOffset = 0
    minOffset = 0
    secOffset = 0
    hrAbs = None
    minAbs = None
    military = False

    for idx, word in enumerate(words):
        if word == "":
            continue

        wordPrevPrev = words[idx - 2] if idx > 1 else ""
        wordPrev = words[idx - 1] if idx > 0 else ""
        wordNext = words[idx + 1] if idx + 1 < len(words) else ""
        wordNextNext = words[idx + 2] if idx + 2 < len(words) else ""
        # parse noon, midnight, morning, afternoon, evening
        used = 0
        if word == "noon":
            hrAbs = 12
            used += 1
        elif word == "midnight":
            hrAbs = 0
            used += 1
        elif word == "morning":
            if hrAbs is None:
                hrAbs = 8
            used += 1
        elif word == "afternoon":
            if hrAbs is None:
                hrAbs = 15
            used += 1
        elif word == "evening":
            if hrAbs is None:
                hrAbs = 19
            used += 1
        # couple of time_unit
        elif word == "2" and wordNext == "of" and \
                wordNextNext in ["hours", "minutes", "seconds"]:
            used += 3
            if wordNextNext == "hours":
                hrOffset = 2
            elif wordNextNext == "minutes":
                minOffset = 2
            elif wordNextNext == "seconds":
                secOffset = 2
        # parse half an hour, quarter hour
        elif word == "hour" and \
                (wordPrev in markers or wordPrevPrev in markers):
            if wordPrev == "half":
                minOffset = 30
            elif wordPrev == "quarter":
                minOffset = 15
            elif wordPrevPrev == "quarter":
                minOffset = 15
                if idx > 2 and words[idx - 3] in markers:
                    words[idx - 3] = ""
                    if words[idx - 3] == "this":
                        daySpecified = True
                words[idx - 2] = ""
            elif wordPrev == "within":
                hrOffset = 1
            else:
                hrOffset = 1
            if wordPrevPrev in markers:
                words[idx - 2] = ""
                if wordPrevPrev == "this":
                    daySpecified = True
            words[idx - 1] = ""
            used += 1
            hrAbs = -1
            minAbs = -1
            # parse 5:00 am, 12:00 p.m., etc
        # parse in a minute
        elif word == "minute" and wordPrev == "in":
            minOffset = 1
            words[idx - 1] = ""
            used += 1
        # parse in a second
        elif word == "second" and wordPrev == "in":
            secOffset = 1
            words[idx - 1] = ""
            used += 1
        elif word[0].isdigit():
            isTime = True
            strHH = ""
            strMM = ""
            remainder = ""
            wordNextNextNext = words[idx + 3] \
                if idx + 3 < len(words) else ""
            if wordNext == "tonight" or wordNextNext == "tonight" or \
                    wordPrev == "tonight" or wordPrevPrev == "tonight" or \
                    wordNextNextNext == "tonight":
                remainder = "pm"
                used += 1
                if wordPrev == "tonight":
                    words[idx - 1] = ""
                if wordPrevPrev == "tonight":
                    words[idx - 2] = ""
                if wordNextNext == "tonight":
                    used += 1
                if wordNextNextNext == "tonight":
                    used += 1

            if ':' in word:
                # parse colons
                # "3:00 in the morning"
                stage = 0
                length = len(word)
                for i in range(length):
                    if stage == 0:
                        if word[i].isdigit():
                            strHH += word[i]
                        elif word[i] == ":":
                            stage = 1
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 1:
                        if word[i].isdigit():
                            strMM += word[i]
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 2:
                        remainder = word[i:].replace(".", "")
                        break
                if remainder == "":
                    nextWord = wordNext.replace(".", "")
                    if nextWord == "am" or nextWord == "pm":
                        remainder = nextWord
                        used += 1

                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx + 3] == "morning":
                        remainder = "am"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx + 3] == "afternoon":
                        remainder = "pm"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx + 3] == "evening":
                        remainder = "pm"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "morning":
                        remainder = "am"
                        used += 2
                    elif wordNext == "in" and wordNextNext == "afternoon":
                        remainder = "pm"
                        used += 2
                    elif wordNext == "in" and wordNextNext == "evening":
                        remainder = "pm"
                        used += 2
                    elif wordNext == "this" and wordNextNext == "morning":
                        remainder = "am"
                        used = 2
                        daySpecified = True
                    elif wordNext == "this" and wordNextNext == "afternoon":
                        remainder = "pm"
                        used = 2
                        daySpecified = True
                    elif wordNext == "this" and wordNextNext == "evening":
                        remainder = "pm"
                        used = 2
                        daySpecified = True
                    elif wordNext == "at" and wordNextNext == "night":
                        if strHH and int(strHH) > 5:
                            remainder = "pm"
                        else:
                            remainder = "am"
                        used += 2

                    else:
                        if timeQualifier != "":
                            military = True
                            if strHH and int(strHH) <= 12 and \
                                    (timeQualifier in timeQualifiersPM):
                                strHH += str(int(strHH) + 12)

            else:
                # try to parse numbers without colons
                # 5 hours, 10 minutes etc.
                length = len(word)
                strNum = ""
                remainder = ""
                for i in range(length):
                    if word[i].isdigit():
                        strNum += word[i]
                    else:
                        remainder += word[i]

                if remainder == "":
                    remainder = wordNext.replace(".", "").lstrip().rstrip()
                if (
                        remainder == "pm" or
                        wordNext == "pm" or
                        remainder == "p.m." or
                        wordNext == "p.m."):
                    strHH = strNum
                    remainder = "pm"
                    used = 1
                elif (
                        remainder == "am" or
                        wordNext == "am" or
                        remainder == "a.m." or
                        wordNext == "a.m."):
                    strHH = strNum
                    remainder = "am"
                    used = 1
                elif (
                        remainder in recur_markers or
                        wordNext in recur_markers or
                        wordNextNext in recur_markers):
                    # Ex: "7 on mondays" or "3 this friday"
                    # Set strHH so that isTime == True
                    # when am or pm is not specified
                    strHH = strNum
                    used = 1
                else:
                    if (
                            int(strNum) > 100 and
                            (
                                    wordPrev == "o" or
                                    wordPrev == "oh"
                            )):
                        # 0800 hours (pronounced oh-eight-hundred)
                        strHH = str(int(strNum) // 100)
                        strMM = str(int(strNum) % 100)
                        military = True
                        if wordNext == "hours":
                            used += 1
                    elif (
                            (wordNext == "hours" or wordNext == "hour" or
                             remainder == "hours" or remainder == "hour") and
                            word[0] != '0' and
                            (
                                    int(strNum) < 100 or
                                    int(strNum) > 2400
                            )):
                        # ignores military time
                        # "in 3 hours"
                        hrOffset = int(strNum)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1

                    elif wordNext == "minutes" or wordNext == "minute" or \
                            remainder == "minutes" or remainder == "minute":
                        # "in 10 minutes"
                        minOffset = int(strNum)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif wordNext == "seconds" or wordNext == "second" \
                            or remainder == "seconds" or remainder == "second":
                        # in 5 seconds
                        secOffset = int(strNum)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif int(strNum) > 100:
                        # military time, eg. "3300 hours"
                        strHH = str(int(strNum) // 100)
                        strMM = str(int(strNum) % 100)
                        military = True
                        if wordNext == "hours" or wordNext == "hour" or \
                                remainder == "hours" or remainder == "hour":
                            used += 1
                    elif wordNext and wordNext[0].isdigit():
                        # military time, e.g. "04 38 hours"
                        strHH = strNum
                        strMM = wordNext
                        military = True
                        used += 1
                        if (wordNextNext == "hours" or
                                wordNextNext == "hour" or
                                remainder == "hours" or remainder == "hour"):
                            used += 1
                    elif (
                            wordNext == "" or wordNext == "o'clock" or
                            (
                                    wordNext == "in" and
                                    (
                                            wordNextNext == "the" or
                                            wordNextNext == timeQualifier
                                    )
                            ) or wordNext == 'tonight' or
                            wordNextNext == 'tonight'):

                        strHH = strNum
                        strMM = "00"
                        if wordNext == "o'clock":
                            used += 1

                        if wordNext == "in" or wordNextNext == "in":
                            used += (1 if wordNext == "in" else 2)
                            wordNextNextNext = words[idx + 3] \
                                if idx + 3 < len(words) else ""

                            if (wordNextNext and
                                    (wordNextNext in timeQualifier or
                                     wordNextNextNext in timeQualifier)):
                                if (wordNextNext in timeQualifiersPM or
                                        wordNextNextNext in timeQualifiersPM):
                                    remainder = "pm"
                                    used += 1
                                if (wordNextNext in timeQualifiersAM or
                                        wordNextNextNext in timeQualifiersAM):
                                    remainder = "am"
                                    used += 1

                        if timeQualifier != "":
                            if timeQualifier in timeQualifiersPM:
                                remainder = "pm"
                                used += 1

                            elif timeQualifier in timeQualifiersAM:
                                remainder = "am"
                                used += 1
                            else:
                                # TODO: Unsure if this is 100% accurate
                                used += 1
                                military = True
                    else:
                        isTime = False
            HH = int(strHH) if strHH else 0
            MM = int(strMM) if strMM else 0
            HH = HH + 12 if remainder == "pm" and HH < 12 else HH
            HH = HH - 12 if remainder == "am" and HH >= 12 else HH

            if (not military and
                    remainder not in ['am', 'pm', 'hours', 'minutes',
                                      "second", "seconds",
                                      "hour", "minute"] and
                    ((not daySpecified) or dayOffset < 1)):
                # ambiguous time, detect whether they mean this evening or
                # the next morning based on whether it has already passed
                if dateNow.hour < HH or (dateNow.hour == HH and
                                         dateNow.minute < MM):
                    pass  # No modification needed
                elif dateNow.hour < HH + 12:
                    HH += 12
                else:
                    # has passed, assume the next morning
                    dayOffset += 1

            if timeQualifier in timeQualifiersPM and HH < 12:
                HH += 12

            if HH > 24 or MM > 59:
                isTime = False
                used = 0
            if isTime:
                hrAbs = HH
                minAbs = MM
                used += 1

        if used > 0:
            # removed parsed words from the sentence
            for i in range(used):
                if idx + i >= len(words):
                    break
                consumed += [words[idx + i]]
                words[idx + i] = ""

            if wordPrev == "o" or wordPrev == "oh":
                words[words.index(wordPrev)] = ""

            if wordPrev == "early":
                hrOffset = -1
                words[idx - 1] = ""
                idx -= 1
            elif wordPrev == "late":
                hrOffset = 1
                words[idx - 1] = ""
                idx -= 1
            if idx > 0 and wordPrev in markers:
                words[idx - 1] = ""
                if wordPrev == "this":
                    daySpecified = True
            if idx > 1 and wordPrevPrev in markers:
                words[idx - 2] = ""
                if wordPrevPrev == "this":
                    daySpecified = True

            idx += used - 1
            found = True
    # check that we found a date
    if not date_found:
        return None

    if dayOffset is False:
        dayOffset = 0

    # perform date manipulation

    extractedDate = dateNow.replace(microsecond=0)

    if datestr != "":
        if "-" in datestr: # date range, e.g. "February 21-27"
            datestr = datestr.split("-")[0]
        # date included an explicit date, e.g. "june 5"
        try:
            temp = datetime.strptime(datestr, "%B %d")
        except ValueError:
            # date included an explicit date, e.g. "june 2, 2017"
            try:
                temp = datetime.strptime(datestr, "%B %d %Y")
            except ValueError:
                # date included an explicit date, e.g. "june 2017"
                try:
                    temp = datetime.strptime(datestr, "%B %Y")
                except ValueError:
                    # date included an explicit month, e.g. "june"
                    temp = datetime.strptime(datestr, "%B")
        extractedDate = extractedDate.replace(hour=0, minute=0, second=0)
        if not hasYear:
            temp = temp.replace(year=extractedDate.year,
                                tzinfo=extractedDate.tzinfo)
            if extractedDate < temp:
                extractedDate = extractedDate.replace(
                    year=int(currentYear),
                    month=int(temp.strftime("%m")),
                    day=int(temp.strftime("%d")),
                    tzinfo=extractedDate.tzinfo)
            else:
                extractedDate = extractedDate.replace(
                    year=int(currentYear) + 1,
                    month=int(temp.strftime("%m")),
                    day=int(temp.strftime("%d")),
                    tzinfo=extractedDate.tzinfo)
        else:
            extractedDate = extractedDate.replace(
                year=int(temp.strftime("%Y")),
                month=int(temp.strftime("%m")),
                day=int(temp.strftime("%d")),
                tzinfo=extractedDate.tzinfo)
    else:
        # ignore the current HH:MM:SS if relative using days or greater
        if hrOffset == 0 and minOffset == 0 and secOffset == 0:
            extractedDate = extractedDate.replace(hour=0, minute=0, second=0)

    if yearOffset != 0:
        extractedDate = extractedDate + relativedelta(years=yearOffset)
    if monthOffset != 0:
        extractedDate = extractedDate + relativedelta(months=monthOffset)
    if dayOffset != 0:
        extractedDate = extractedDate + relativedelta(days=dayOffset)
    if hrAbs != -1 and minAbs != -1:
        # If no time was supplied in the string set the time to default
        # time if it's available
        if hrAbs is None and minAbs is None and default_time is not None:
            hrAbs, minAbs = default_time.hour, default_time.minute
        else:
            hrAbs = hrAbs or 0
            minAbs = minAbs or 0

        extractedDate = extractedDate + relativedelta(hours=hrAbs,
                                                      minutes=minAbs)
        if (hrAbs != 0 or minAbs != 0) and datestr == "":
            if not daySpecified and dateNow > extractedDate:
                extractedDate = extractedDate + relativedelta(days=1)
    if hrOffset != 0:
        extractedDate = extractedDate + relativedelta(hours=hrOffset)
    if minOffset != 0:
        extractedDate = extractedDate + relativedelta(minutes=minOffset)
    if secOffset != 0:
        extractedDate = extractedDate + relativedelta(seconds=secOffset)
    for idx, word in enumerate(words):
        if words[idx] == "and" and \
                words[idx - 1] == "" and words[idx + 1] == "":
            words[idx] = ""

    resultStr = " ".join(consumed)
    resultStr = ' '.join(resultStr.split())

    remStr = " ".join(words)

    return [extractedDate, resultStr, remStr]


def _annotate_duration_en(text):
    """
    Convert an english phrase into a number of seconds

    Convert things like:
        "10 minute"
        "2 and a half hours"
        "3 days 8 hours 10 minutes and 49 seconds"
    into an int, representing the total number of seconds.

    The words used in the duration will be returned.

    As an example, "set a timer for 5 minutes" would return
    (300, "5 minutes").

    Reverse of extract_duration_en

    Args:
        text (str): string containing a duration

    Returns:
        (timedelta, str):
                    A tuple containing the duration and the text
                    consumed in the parsing. The first value will
                    be None if no duration is found.
    """
    if not text:
        return None

    time_units = {
        'microseconds': None,
        'milliseconds': None,
        'seconds': None,
        'minutes': None,
        'hours': None,
        'days': None,
        'weeks': None
    }

    time_units2 = {
        'years': None,
        'months': None,
        'weeks': None,
        'decades': None
    }

    pattern = r"(?P<value>\d+(?:\.?\d+)?)\s+{unit}s?"
    norm_text = _convert_words_to_numbers_en(text)
    t = norm_text
    duration_text = text

    start = -1
    end = -1

    for unit in time_units:
        unit_pattern = pattern.format(unit=unit[:-1])  # remove 's' from unit
        matches = re.findall(unit_pattern, t)
        value = sum(map(float, matches))
        time_units[unit] = value
        t = re.sub(unit_pattern, '', t)
        if matches:
            n_start = norm_text.find(str(int(value)))
            if start < 0 or n_start < start:
                start = n_start

            n_end = text.rfind(unit) + len(unit)
            if n_end > end:
                end = n_end

    for unit in time_units2:
        unit_pattern = pattern.format(unit=unit[:-1])  # remove 's' from unit
        matches = re.findall(unit_pattern, t)
        value = sum(map(float, matches))
        t = re.sub(unit_pattern, '', t)
        if matches:
            if time_units["days"] is None:
                time_units["days"] = 0
            if unit == "years":
                time_units["days"] += value * 365
            elif unit == "months":
                time_units["days"] += value * 30
            elif unit == "weeks":
                time_units["days"] += value * 7
            elif unit == "decades":
                time_units["days"] += value * 3650

            n_start = norm_text.find(str(int(value)))
            if start < 0 or n_start < start:
                start = n_start

            n_end = text.rfind(unit) + len(unit)
            if n_end > end:
                end = n_end

    if start > -1:
        if end > start:
            duration_text = duration_text[start:end]
        else:
            duration_text = duration_text[start:]

    duration = timedelta(**time_units) if any(time_units.values()) else None

    return (duration, duration_text.strip())


class DateTimeNER(NERWrapper):
    def __init__(self, anchor_date=None):
        super().__init__()
        self.anchor_date = anchor_date or datetime.now()
        self.add_detector(self.annotate_datetime)
        self.add_detector(self.annotate_duration)

    def annotate_duration(self, text):
        delta, value = _annotate_duration_en(text)
        if delta:
            data = {
                "days": delta.days,
                "seconds": delta.seconds,
                "microseconds": delta.microseconds,
                "total_seconds": delta.total_seconds(),
                "spoken": nice_duration(delta)
            }
            yield Entity(value, "duration", source_text=text, data=data)

    def annotate_datetime(self, text):
        date, value, rem = _annotate_datetime_en(text, self.anchor_date)
        while value:
            try:
                data = {
                    "timestamp": date.timestamp(),
                    "isoformat": date.isoformat(),
                    "weekday": date.isoweekday(),
                    "month": date.month,
                    "day": date.day,
                    "hour": date.hour,
                    "minute": date.minute,
                    "year": date.year,
                    "spoken": nice_date(date, now=self.anchor_date)
                }
                yield Entity(value, "relative_date", source_text=text,
                             data=data)
            except OverflowError: # deep past / future
                yield Entity(value, "date", source_text=text,
                             data={"spoken": value})
            if not rem:
                return
            date, value, rem = _annotate_datetime_en(rem, self.anchor_date)

    def annotate(self, text):
        # deprecated
        from dateparser.search import search_dates
        matches = search_dates(text)
        for value, date in matches:
            data = {
                "timestamp": date.timestamp(),
                "isoformat": date.isoformat(),
                "weekday": date.isoweekday(),
                "month": date.month,
                "day": date.day,
                "hour": date.hour,
                "minute": date.minute,
                "year": date.year
            }
            yield Entity(value, "date", source_text=text, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = DateTimeNER()
    for r in ner.extract_entities("What President served for five years , six months and 2 days ?"):
        pprint(r.as_json())
    """
    {'confidence': 1,
     'data': {'day': 6,
              'hour': 0,
              'isoformat': '2019-04-06T00:00:00+01:00',
              'minute': 0,
              'month': 4,
              'timestamp': 1554505200.0,
              'weekday': 6,
              'year': 2019},
     'entity_type': 'relative_date',
     'rules': [],
     'source_text': 'What President served for five years , six months and 2 days '
                    '?',
     'spans': [(54, 60)],
     'value': '2 days'}
     
    {'confidence': 1,
     'data': {'days': 2007,
              'microseconds': 0,
              'seconds': 0,
              'spoken': 'two thousand, seven days ',
              'total_seconds': 173404800.0},
     'entity_type': 'duration',
     'rules': [],
     'source_text': 'What President served for five years , six months and 2 days '
                    '?',
     'spans': [(26, 60)],
     'value': 'five years , six months and 2 days'}
    """

    for r in ner.extract_entities("my birthday is on december 5th"):
        pprint(r.as_json())

    """
    {'confidence': 1,
     'data': {'isoformat': '2019-04-04T04:53:27.656766',
              'timestamp': 1554350007.656766,
              'weekday': 4},
     'entity_type': 'date',
     'rules': [],
     'source_text': 'my birthday is on december 5th',
     'spans': [(14, 30)],
     'value': ' on december 5th'}
    """
    for r in ner.extract_entities("starts in 5 minutes"):
        pprint(r.as_json())
    """
    {'confidence': 1,
     'data': {'days': 0,
              'microseconds': 0,
              'seconds': 300,
              'spoken': 'five minutes',
              'total_seconds': 300.0},
     'entity_type': 'duration',
     'rules': [],
     'source_text': 'starts in 5 minutes',
     'spans': [(10, 19)],
     'value': '5 minutes'}
    """


