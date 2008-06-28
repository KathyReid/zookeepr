<% menu %>
<h2><% c.db_content.title %></h2>

% if c.is_news:
<p class="submitted">
Submitted on <% c.db_content.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</p>
% #endif


<% body %>

<%method title>
<% c.db_content.title %> - <& PARENT:title &>
</%method>

<%init>

import re
menu = ''
findh3 = re.compile('(<h3>(.+?)</h3>)', re.IGNORECASE|re.DOTALL|re.MULTILINE)
h3 = findh3.findall(c.db_content.body)
body = c.db_content.body
if h3.__len__() > 0:
    simple_title = ''
    menu = '<div class="contents"><h3>Contents</h3><ul>'
    for match in h3:
        simple_title = re.compile('([^a-zA-Z])').sub('', match[1])
        body = re.compile(match[0]).sub(r'<a name="' + simple_title + '"></a>\g<0>', body)
        menu += '<li><a href="#' + simple_title + '">' + match[1] + '</a></li>'
    menu += '</ul></div>'

</%init>
