#
# Table structure for table `Activity`
#

CREATE TABLE Activity (
  Acttime datetime NOT NULL default '0000-00-00 00:00:00',
  Who varchar(20) NOT NULL default '',
  What varchar(255) NOT NULL default ''
) TYPE=MyISAM COMMENT='Management Audit Log';
# --------------------------------------------------------

#
# Table structure for table `Books`
#

CREATE TABLE Books (
  BookName varchar(40) NOT NULL default '',
  Code varchar(10) NOT NULL default ''
) TYPE=MyISAM COMMENT='Books and their Codes';
# --------------------------------------------------------

#
# Table structure for table `Rota`
#

CREATE TABLE Rota (
  ServiceDate varchar(12) NOT NULL default '',
  Service varchar(20) NOT NULL default '',
  Team varchar(20) default '',
  Leader varchar(20) default '',
  Preacher varchar(20) default '',
  Notes varchar(255) default ''
) TYPE=MyISAM COMMENT='Worship Rota';
# --------------------------------------------------------

#
# Table structure for table `RotaSub`
#

CREATE TABLE RotaSub (
  ServiceDate date NOT NULL default '0000-00-00',
  Service varchar(10) NOT NULL default '',
  Role varchar(20) NOT NULL default '',
  Main varchar(20) NOT NULL default '',
  Sub varchar(10) NOT NULL default ''
) TYPE=MyISAM COMMENT='Team Substitutions';
# --------------------------------------------------------

#
# Table structure for table `ServiceLines`
#

CREATE TABLE ServiceLines (
  ServiceDate date NOT NULL default '0000-00-00',
  Service varchar(10) NOT NULL default '',
  Sequence int(3) NOT NULL default '0',
  FType varchar(20) NOT NULL default '',
  Feature varchar(40) NOT NULL default '',
  Notes varchar(255) default ''
) TYPE=MyISAM COMMENT='Service Features. Songs, Reading, Sermon etc.';
# --------------------------------------------------------

#
# Table structure for table `Songs`
#

CREATE TABLE Songs (
  SongName varchar(80) NOT NULL default '',
  Book varchar(10) NOT NULL default 'Unknown',
  Number varchar(10) NOT NULL default 'Unknown',
  Style varchar(255) default '',
  Categories varchar(255) default ''
  Words text NOT NULL  
) TYPE=MyISAM COMMENT='List of Songs';
# --------------------------------------------------------

#
# Table structure for table `Team`
#

CREATE TABLE Team (
  Name varchar(20) NOT NULL default '',
  Roles varchar(255) default '',
  Telephone varchar(20) NOT NULL default 'Unknown',
  Email varchar(40) NOT NULL default 'Unknown',
  Username varchar(20) NOT NULL default '',
  Privilege int(2) NOT NULL default '0'
) TYPE=MyISAM COMMENT='Worship Team Members';
# --------------------------------------------------------

#
# Table structure for table `TeamStruct`
#

CREATE TABLE TeamStruct (
  Team varchar(10) NOT NULL default '',
  Role varchar(20) NOT NULL default '',
  Main varchar(40) default '',
  Sub1 varchar(40) default '',
  Sub2 varchar(40) default '',
  Sub3 varchar(40) default '',
  Sub4 varchar(40) default ''
) TYPE=MyISAM COMMENT='Team Organisation';

