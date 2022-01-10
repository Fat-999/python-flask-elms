-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 10, 2022 at 11:30 AM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `empl1`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(2, 'HR', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `applyleaves`
--

DROP TABLE IF EXISTS `applyleaves`;
CREATE TABLE IF NOT EXISTS `applyleaves` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fromdate` varchar(50) NOT NULL,
  `todate` varchar(50) NOT NULL,
  `levtype` varchar(50) NOT NULL,
  `description` varchar(250) NOT NULL,
  `postingdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tlremark` varchar(250) DEFAULT NULL,
  `tlremarkdate` varchar(120) DEFAULT NULL,
  `status` int(1) NOT NULL,
  `isread` int(1) NOT NULL,
  `empid` int(11) DEFAULT NULL,
  `mgremark` varchar(250) DEFAULT NULL,
  `mgremarkdate` varchar(120) DEFAULT NULL,
  `isreadmg` int(1) NOT NULL,
  `mgstatus` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `applyleaves`
--

INSERT INTO `applyleaves` (`id`, `fromdate`, `todate`, `levtype`, `description`, `postingdate`, `tlremark`, `tlremarkdate`, `status`, `isread`, `empid`, `mgremark`, `mgremarkdate`, `isreadmg`, `mgstatus`) VALUES
(1, '12-10-2021', '24-10-2021', 'Sick Leave ', 'health', '2021-10-25 06:14:25', 'reject', NULL, 2, 1, 4, 'rejected', '2021-12-23 14:43:18', 1, 2),
(2, '01-11-2021', '10-11-2021', 'Other Leave ', 'Festival leave ', '2021-10-26 05:43:35', 'Go ahead', NULL, 1, 1, 8, 'ok', '2021-11-01 09:42:37', 1, 1),
(3, '03-11-2021', '6-11-2021', 'Casual leave', 'Function leave', '2021-10-26 06:23:20', 'ok', NULL, 1, 1, 9, 'go ahead', '2021-10-30 18:39:22', 1, 1),
(4, '13-11-2021', '24-11-2021', 'Sick Leave ', 'Health Care ', '2021-10-27 10:35:40', 'Rejected', NULL, 2, 1, 12, 'ok', '2021-12-23 14:44:35', 1, 1),
(5, '29-10-2021', '04-11-2021', 'Sick Leave ', 'Health Issue ', '2021-10-28 04:27:50', 'ok', '2021-10-28 10:39:01', 1, 1, 5, 'go ahead', '2021-12-23 10:10:41', 1, 1),
(6, '03-12-2021', '10-12-2021', 'Other Leave ', 'function', '2021-10-28 04:45:11', 'go ahead', '2021-10-28 10:40:44', 1, 1, 4, 'not eligible', '2021-12-23 10:11:19', 1, 2),
(7, '01-01-2021', '10-01-2021', 'Casual leave', 'function at home', '2021-10-28 04:46:02', 'Rejected', '2021-10-28 17:07:05', 2, 1, 4, 'ok', '2021-12-23 14:46:32', 1, 1),
(8, '23-12-2021', '25-12-2021', 'Sick Leave ', 'health issue', '2021-10-30 07:09:27', 'ok', '2021-10-30 18:27:46', 1, 1, 4, 'ok', '2021-10-30 18:28:24', 1, 1),
(9, '24-12-2021', '26-12-2021', 'Other Leave ', 'parent care ', '2021-10-30 07:15:04', 'ok', '2021-12-22 15:09:33', 1, 1, 11, 'ok', '2021-12-22 18:12:30', 1, 1),
(10, '28-12-2021', '01-01-2021', 'Casual leave', 'going for party', '2021-10-30 07:15:43', 'ok', '2021-10-30 18:18:46', 1, 1, 11, 'ok', '2021-10-30 18:21:03', 1, 1),
(11, '19-12-2021', '25-12-2021', 'Casual leave', 'diwali leave ', '2021-10-30 12:19:40', 'go ahead', '2021-12-22 13:13:18', 1, 1, 11, 'rejected', '2021-12-22 18:12:57', 1, 2),
(12, '03-11-2021', '6-11-2021', 'Other Leave ', 'Diwali ', '2021-11-01 06:18:45', 'ok', '2021-12-23 10:06:20', 1, 1, 4, 'ok', '2021-12-23 10:09:34', 1, 1),
(13, '03-11-2021', '6-11-2021', 'Other Leave ', 'Diwali ', '2021-11-01 06:20:00', 'rejected', '2021-12-23 10:12:09', 2, 1, 4, 'ok', '2021-12-23 14:37:09', 1, 2),
(14, '24-10-2021', '31-10-2021', 'Other Leave ', 'Diwali festival', '2021-11-01 06:28:25', 'Go ahead', '2021-12-23 11:40:31', 1, 1, 4, 'ok', '2021-12-23 11:43:35', 1, 1),
(15, '23-12-2021', '01-02-2022', 'Other Leave ', 'for festival', '2021-12-22 09:06:45', 'ok', '2021-12-23 16:02:53', 1, 1, 13, NULL, NULL, 1, 0),
(16, '16-12-2021', '17-12-2021', 'Sick Leave ', 'health issue', '2021-12-22 09:07:29', 'ok', '2021-12-23 11:40:51', 1, 1, 13, 'rejected', '2021-12-23 11:43:54', 1, 2),
(17, '23-12-2021', '01-02-2022', 'Other Leave ', 'for festival', '2021-12-22 09:27:50', 'rerjected', '2021-12-23 16:03:12', 2, 1, 13, NULL, NULL, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
CREATE TABLE IF NOT EXISTS `department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `depcode` varchar(10) NOT NULL,
  `depname` varchar(100) NOT NULL,
  `depstname` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`id`, `depcode`, `depname`, `depstname`, `created_at`) VALUES
(1, '01', 'Lidar Engg', 'Ld', '2021-10-22 05:47:28'),
(2, '02', 'Cadd', 'Cd', '2021-10-22 05:47:28'),
(5, '07', 'Mapping', 'Mp', '2021-10-23 03:55:49'),
(4, '05', 'Information Technology', 'IT', '2021-10-22 05:47:28'),
(6, '09', 'Development', 'Dp', '2021-10-30 04:22:04');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE IF NOT EXISTS `employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `empname` varchar(50) NOT NULL,
  `empid` varchar(50) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `password2` varchar(50) NOT NULL,
  `dep` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `birthdate` varchar(11) NOT NULL,
  `reg_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `empname`, `empid`, `contact`, `email`, `password`, `password2`, `dep`, `gender`, `birthdate`, `reg_at`) VALUES
(1, 'priya', '1122', '9876554333', 'test@gmail.com', '2345', '2345', 'Lidar', 'Female', '22-09-1995', '2021-10-22 05:44:49'),
(6, 'ram raj', '1176', '3554663455', 'ram123@gmail.com', '12345', '12345', 'Lidar', 'male', '02-09-1989', '2021-10-22 05:44:49'),
(5, 'shan res', '1165', '8876543211', 'safisan123@gmail.com', '2345', '2345', 'Cadd', 'male', '28-12-1992', '2021-10-22 05:44:49'),
(4, 'nionfor', '1233', '8876543211', 'nionset@gmail.com', '4567', '4567', 'Cadd dep', 'Female', '25-11-1997', '2021-10-22 05:44:49'),
(9, 'Suresh R', '2216', '8765477889', 'suresh12IT@gmail.com', '12345', '12345', 'IT ', 'male', '11-10-1994', '2021-10-22 05:44:49'),
(8, 'lia', '1933', '7665421871', 'liaraj@gmail.com', '12345', '12345', 'Cadd', 'Female', '02-09-1993', '2021-10-22 05:44:49'),
(11, 'kiran', '1433', '7655455333', 'kiranreo@gmail.com', '12345', '12345', 'IT', 'male', '14-04-1989', '2021-10-22 05:44:49'),
(12, 'shalini', '1322', '6545343425', 'shalini12@gmail.com', '12345', '12345', 'IT', 'Female', '22-04-1995', '2021-10-22 05:44:49'),
(13, 'shunil kumar', '1177', '7645775765', 'shunilkumar@gmail.com', '12345', '12345', 'Cadd', 'male', '11-11-1991', '2021-10-22 07:17:32'),
(14, 'Sivani', '1199', '6545646665', 'Sivanikumar@gmail.com', '12345', '12345', 'Cadd', 'Female', '24-12-1999', '2021-10-22 11:34:42'),
(15, 'manoj', '1256', '7865543221', 'manoj22@gmail.com', '12345', '12345', 'Mapping', 'Male', '14-12-1991', '2021-12-22 10:51:11');

-- --------------------------------------------------------

--
-- Table structure for table `leaves`
--

DROP TABLE IF EXISTS `leaves`;
CREATE TABLE IF NOT EXISTS `leaves` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `levtype` varchar(250) NOT NULL,
  `description` varchar(250) NOT NULL,
  `createdat` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `leaves`
--

INSERT INTO `leaves` (`id`, `levtype`, `description`, `createdat`) VALUES
(4, 'Sick Leave ', 'Health Care', '2021-10-22 08:56:19'),
(3, 'Other Leave ', 'LOP', '2021-10-22 08:55:24'),
(5, 'Casual leave', 'Unforeseen situation', '2021-10-22 08:56:54');

-- --------------------------------------------------------

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
CREATE TABLE IF NOT EXISTS `manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mgusername` varchar(10) NOT NULL,
  `mgpassword` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `manager`
--

INSERT INTO `manager` (`id`, `mgusername`, `mgpassword`) VALUES
(1, 'manager', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `teamleader`
--

DROP TABLE IF EXISTS `teamleader`;
CREATE TABLE IF NOT EXISTS `teamleader` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tlusername` varchar(10) NOT NULL,
  `tlpassword` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `teamleader`
--

INSERT INTO `teamleader` (`id`, `tlusername`, `tlpassword`) VALUES
(1, 'TL', '12345');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
