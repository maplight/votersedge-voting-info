Static content files for state and county level voting information guides.

Please refer to _documentation for more information. (All current info is a draft.)

voting-info contains:

 _templates — for state and election authority content.
 states — for state pages for each state we support
    ca — a state
        all-elections — pages in each of our 8 official sections
        single-elections - override individual state pages by election date
 election-authorities — for election authority pages we support
    ca - a state
        1-alameda-county-registrar-of-voters -- file name of election authority id & lower case + dash version of election authority name. we can auto generate all these file names as necessary and keep in sync here, but empty 
            all-elections - pages that override specific sections that have county/election authority pages
            single-election - override individual all-elections pages by election date & section

 as of 12-24 ca is our working example, which we will base IL and NY off 
