/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - ukdb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`ukdb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `ukdb`;

/*Table structure for table `info` */

DROP TABLE IF EXISTS `info`;

CREATE TABLE `info` (
  `ID` int(255) NOT NULL auto_increment,
  `TITLE` varchar(255) default NULL,
  `EMAIL` varchar(255) default NULL,
  `PHONE` varchar(255) default NULL,
  `MASSAGE` longtext,
  `FILEIMAGE` varchar(255) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `info` */

insert  into `info`(`ID`,`TITLE`,`EMAIL`,`PHONE`,`MASSAGE`,`FILEIMAGE`) values (1,'BR Collection','mumbai@gmail.com','9632587414','Check if you need a Biometric Residence Permit (BRP).\r\nCollect your BRP once in the UK, typically within 10 days of arrival.','static/info/4.jfif');

/*Table structure for table `status` */

DROP TABLE IF EXISTS `status`;

CREATE TABLE `status` (
  `id` int(255) NOT NULL auto_increment,
  `mailid` varchar(255) default NULL,
  `ARRIVE` varchar(255) default 'DONE',
  `BR` varchar(255) default 'PENDING',
  `BANK` varchar(255) default 'PENDING',
  `NI` varchar(255) default 'PENDING',
  `GP` varchar(255) default 'PENDING',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `status` */

insert  into `status`(`id`,`mailid`,`ARRIVE`,`BR`,`BANK`,`NI`,`GP`) values (1,'mumbai@gmail.com','DONE','PENDING','PENDING','PENDING','PENDING'),(2,'hp690175@gmail.com','DONE','DONE','PENDING','PENDING','PENDING');

/*Table structure for table `steps` */

DROP TABLE IF EXISTS `steps`;

CREATE TABLE `steps` (
  `id` int(255) NOT NULL auto_increment,
  `stepname` varchar(255) default NULL,
  `dropdown1` varchar(255) default NULL,
  `msg1` longtext,
  `uploadvideo` varchar(255) default NULL,
  `uploadimage` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `steps` */

insert  into `steps`(`id`,`stepname`,`dropdown1`,`msg1`,`uploadvideo`,`uploadimage`) values (1,' Biometric Residence Permit (BRP)','1','Collect your BRP once in the UK, typically within 10 days of arrival.','static/youtube/1\\vid-1.mp4','static/youtube/1\\4.jfif');

/*Table structure for table `stu_contact` */

DROP TABLE IF EXISTS `stu_contact`;

CREATE TABLE `stu_contact` (
  `Id` int(255) NOT NULL auto_increment,
  `Name` varchar(255) default NULL,
  `Email` varchar(255) default NULL,
  `Contact` varchar(255) default NULL,
  `Massage` longtext,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `stu_contact` */

insert  into `stu_contact`(`Id`,`Name`,`Email`,`Contact`,`Massage`) values (1,'roshan','mumbai@gmail.com','9632587414','fileUploadForm');

/*Table structure for table `stud_registration` */

DROP TABLE IF EXISTS `stud_registration`;

CREATE TABLE `stud_registration` (
  `Id` int(255) NOT NULL auto_increment,
  `Stu_name` varchar(255) NOT NULL,
  `Stu_email` varchar(255) NOT NULL,
  `Stu_mobile` varchar(255) NOT NULL,
  `Stu_pass` varchar(255) NOT NULL,
  `Stu_city` varchar(255) NOT NULL,
  `Stu_address` varchar(255) NOT NULL,
  `Stu_image` varchar(255) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `stud_registration` */

insert  into `stud_registration`(`Id`,`Stu_name`,`Stu_email`,`Stu_mobile`,`Stu_pass`,`Stu_city`,`Stu_address`,`Stu_image`) values (1,'roshan2','mumbai@gmail.com','8783247333','Rosg@123','india','mumbai2','static/uploaded_profile/ddd.png'),(2,'amit','hp690175@gmail.com','9632587414','Amit@123','Mumbai','Ghatkoper','static/uploaded_profile/pic-6.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
