development of a web crawler completely from scratch. Given  a  starting  URL,  it  extract  all  links  on  the  page.Then it will iterate over all the new links and gather new links from thenew pages
Store the webpages in a directory with the date.
Based on the links, generate a network graph of the downloaded web siteand visualize it.  Nodes are web pages and edges are links between them.
it will onlydownload fresh pages (pages that were not changed since your last visit;note that all pages are stored in a directory).•Monitor the response time of the web site using ping.  
