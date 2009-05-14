package custom;

use base 'Exporter';
our @EXPORT = qw($myheader $myfooter);

our $myheader.=<<p1;
<!--mstheme--><link rel="stylesheet" type="text/css" href="../../_themes/hhbc4/hhbc1110.css"><meta name="Microsoft Theme" content="hhbc4 1110, default">
p1

our $myfooter.=<<p1;
<!--  PopCalendar(tag name and id must match) Tags should not be enclosed in tags other than the html body tag. -->
<iframe width=132 height=142 name="gToday:normal:agenda.js:gfPop:plugins.js" id="gToday:normal:agenda.js:gfPop:plugins.js" src="/apps/PopCalendarXP/ipopeng.htm" scrolling="no" frameborder="0" style="visibility:visible; z-index:999; position:absolute; top:-500px; left:-500px;">
</iframe>
p1

1;
