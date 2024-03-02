+++
title = "Go's compiler sucks"
date = 2024-03-01
+++

I had a terrible experience.  
I spent half an hour debugging unaware that unused variables are a hard error
and was essentially not changing code..

Error handling is... simpple but very inexpressive and lengthy.

You make types public by having an uppercase letter?? What the actual fuck!

Annotations are... fine. But why did I have to spend so much time to make json
encoding/decoding work? Why aren't there more concrete examples of this shit?
Json serialization/deserialization is an extremly common problem, why do you
have to make it so complicated? You're literally a garbage collected language,
come on! (the wiki page shows "readability and usability like Python" fuck that)

<!-- more -->
