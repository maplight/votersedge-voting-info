# This repository contains static content files for state and county level voting information guides.

## Please refer to _documentation for more information.

## voting-info contains:

 * _templates - for state and election authority content.
 * states - content for each state we support
   * ca - a state
     * state-all-elections - pages in each of our 8 official sections
     * state-single-elections - override individual state pages by election date
     * election-authorities - for election authority pages within that state.  This allows us to display county-specific voting information in addition to the state-level voting info.
       * 1-alameda-county-registrar-of-voters -- file name of election authority id & lower case + dash version of election authority name. we can auto generate all these file names as necessary and keep in sync here, but empty 
         * all-elections - pages that override specific sections that have county/election authority pages
         * single-election - override individual all-elections pages by election date & section

## Updating Voter's Edge

Changes made to the master GitHub repository are automatically pushed to Voter's Edge on a periodic basis.  There is a gap of several hours in between when you make your changes and when they appear on the website.  Check your markdown carefully before committing to master.

For more information on how this is processed technically, see the _documentation/TECHNICAL_DETAILS file.