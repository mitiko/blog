+++
title = "Numbers"
date = 2023-05-07
+++

```bash
strings /data/gdcc/mixed | rg -ao "[\d\.,\-:]*\d+[\.,\-:\d]*" > numbers.txt
```

```bash
sort numbers.txt | uniq -c | sort -nr > numbers-sorted.txt
```

```bash
head -n 1000 numbers-sorted.txt > top1k.txt
```

How much of what is responsible for what?

```bash
wc --chars /data/gdcc/mixed
# -> 1'037'221'426
strings /data/gdcc/mixed | wc --chars
# -> 943'775'788
strings -n 2 /data/gdcc/mixed | wc --chars
# -> 954'930'416
```

```bash
python3 -c "print(943775788 / 1037221426)"
# -> 0.9099077249489831
```

Well, the string data is more than 90%! This is where the majority of our effort
should go.

```bash
wc --chars numbers.txt
# -> 287358687
python3 -c "print(287358687 / 943775788)"
# -> 0.30447770609686375
```

Of that string data, we have more than 30% numbers.
It makes sense to have a good model for them.

Of those, how many are single digits, how many are dates, and how many are
double digits?

```bash
strings /data/gdcc/mixed | rg -o "[^\d]\d[^\d]" | wc -l
# -> 12900554
python3 -c "print(12900554 / 287358687)"
# -> 0.044893558411895164
```

4% single digits

```bash
strings /data/gdcc/mixed | rg -o "[^\d]\d{2}[^\d]" | wc -l
# -> 24448576
python3 -c "print(2 * 24448576 / 287358687)"
# -> 0.17016068840821227
```

17% double digits

```bash
strings /data/gdcc/mixed | rg -o "[^\d\-]\d{4}-\d{2}-\d{2}[^\d\-]" | wc -l
# -> 5942845
python3 -c "print(10 * 5942845 / 287358687)"
# -> 0.20680930380225462
```

20% dates

But dates contain two sets of double digits => the real non-date digits are

```bash
python3 -c "print((2 * 24448576 - 4 * 5942845) / 287358687)"
# -> 0.08743696688731042
```

8% real double digits

How many are the ones of more than 6 characters:

```bash
strings /data/gdcc/mixed | rg -o "[^\d]\d{6,}[^\d]" | wc -l
# -> 8862033
strings /data/gdcc/mixed | rg -o "[^\d]\d{6,}[^\d]" | wc --chars
# -> 91184255
python3 -c "print((91184255 - 2 * 8862033) / 287358687)"
# -> 0.25563935361383383
```

25%

In total that is: 4% single digits + 20% dates + 8% double digits + 25% of long
sequences = 59.4%
That's not bad, it's a majority.

How many are the 3-digits?

```bash
strings /data/gdcc/mixed | rg -o "[^\d]\d{3}[^\d]" | wc -l
# -> 5689849
python3 -c "print((5689849 * 3) / 287358687)"
# -> 0.05940153464022475
```

Only 6%?

Okay..

## Digits count (total)

```bash
strings /data/gdcc/mixed | rg -o "\d" | wc -l
# -> 210376045
strings /data/gdcc/mixed | wc --chars
# -> 943775788
strings /data/gdcc/mixed | wc --bytes
# -> 943775788
```

22% is digits.

```bash
strings /data/gdcc/mixed > strings.txt
```

## Number distribution by length

```bash
# 1   -> 12900554
# 2   -> 48897152
# 3   -> 17069547
# 4   -> 33330160
# 5   -> 04504750
# 6   -> 31116066
# 7   -> 15235752
# 8   -> 00132456
# 9   -> 00459414
# 10+ -> 19091482
```

```bash
# 2   -> 48897152
# 4   -> 33330160
# 6   -> 31116066
# 10+ -> 19091482
# 3   -> 17069547
# 7   -> 15235752
# 1   -> 12900554
# 5   -> 04504750
# 9   -> 00459414
# 8   -> 00132456
```

## Dates

```bash
cat strings.txt | rg -o "[^\d\-]\d{4}-\d{2}-\d{2}[^\d\-]" | wc -l
# -> 5942845
python3 -c "print(5942845 * 8)"
# -> 47542760
```

If we replace them.
```bash
rg --passthru "[^\d\-]\d{4}-\d{2}-\d{2}[^\d\-]" -r "DATE" strings.txt > string-no-dates.txt
```

Now let's also replace all the single digits:

```bash
rg --passthru "[^\d]\d{1}[^\d]" -r "SD" string-no-dates.txt > string-no-dates-no-digits.txt
```

Then let's also replace all the double digits.

```bash
rg --passthru "[^\d]\d{2}[^\d]" -r "DD" string-no-dates-no-digits.txt > weird-numbers.txt
```

Then the counts become:

```bash
for i in {1..10}; do cat weird-numbers.txt | rg -o "[^\d]\d{$i}[^\d]" | wc -l; done
```

```bash
# 3   -> 5689849
# 6   -> 5186011
# 4   -> 2400007
# 7   -> 2176536
# 10+ -> 1432396
# 5   -> 0900950
# 9   -> 0051046
# 8   -> 0016557
# 1   -> 0
# 2   -> 0
```

I think it makes sense to model 3-digit numbers as well, and then we can

## Wrote it - digit symbol

```
Plain: 782866181
RLE:   2625787
Digit: 211918349
```

