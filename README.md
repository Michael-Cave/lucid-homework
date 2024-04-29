# lucid-homework
little programs to try to solve the LucidLink interview homework

# Parser.py
Simple little program that sorts through the target log file to find the search terms.

First, it opens a destination file in the <parsed log chunks> directory with the nameing convention of <target_file_name-start_date-end_date(if applicable).txt>.  If that file already exists, it skips the next step and goes directly to the search terms function.

Second, it parses through the entire target log file for the start date.  Once it encounters the first entry in the start date, it writes that line to the newly created file.  When it reaches the end of the target date or the end date, it moves onto the next step.

Finally, it searches through the new file for lines that include the <search_term>.  While it's searching, it keeps a running track of the last five lines it encountered.  If it encounters the <search_term>, it logs the last five lines it read to the console, the line containing the <search_term>, and the next five lines in the log for context around the event.

As an aside, because of how verbose the log files are, it's not advised to search a date range larger than two or so days, depending on the how frequent the <search_term> is.  It can quickly get to the point that the first entries have rolled off the top of the console's scrollback.

It accepts the arguments of: <target_file_path> <start_date> <end_date> <search_term>

It is highly advised to encapsulate all arguments in quotations.

<target_file_path> takes the absolute windows filepath.  It's a simple matter of copying the filepath form

<start_date> only accepts a date format of "yyyy-mm-dd".  This is because that's how the logs format their datetime stamps and it's the backbone of how the program pares down the search area

<end_date> is an optional value to input if, instead of searching a single day, you want to search through a range of days.  Use cases include: client not knowing when problems first started or client problems happened around or during 00:00 UTC.  Like <start_date> it only accepts a date format of "yyyy-mm-dd"

<search_term> is the exact phrase you want the parser to search the logs for.  The search function is case and spelling sensitive, so ensure the search term is 100% accurate.


# Copysync.py
A little program that <*should*> copy a file to a LucidLink filespace with rsync, keep track of if the background uploads are finished, and then send an empty HTTP PUT request.

Accpets the arguments of: <source_file_path> <destination_directory_path>

Firstly, it copies the <source_file> to the <destination_directory> via rsync. When that completes, it moves to the next step.

Second, it makes an HTTP GET request and watches the <dirtyBytes> field of the returned JSON with a retry interval of 1s.  When that resolves as "0" it moves on to the final step.

Finally, it sends an empty HTTP PUT request.
