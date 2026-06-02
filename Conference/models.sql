/*
 Navicat Premium Data Transfer

 Source Server         : meeting
 Source Server Type    : SQL Server
 Source Server Version : 15004198
 Source Host           : 139.196.146.45:1433
 Source Catalog        : Meeting
 Source Schema         : dbo

 Target Server Type    : SQL Server
 Target Server Version : 15004198
 File Encoding         : 65001

 Date: 31/03/2022 18:45:54
*/


-- ----------------------------
-- Table structure for models
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[models]') AND type IN ('U'))
	DROP TABLE [dbo].[models]
GO

CREATE TABLE [dbo].[models] (
  [model_id] int  NOT NULL,
  [model_name] varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [model_author] varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [dataset_id] int  NULL,
  [paper_name] varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [model_url] varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [paper_url] varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [model_time] date  NULL,
  [model_class] int DEFAULT '' NULL
)
GO

ALTER TABLE [dbo].[models] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Records of models
-- ----------------------------
INSERT INTO [dbo].[models] ([model_id], [model_name], [model_author], [dataset_id], [paper_name], [model_url], [paper_url], [model_time], [model_class]) VALUES (N'1', N'AlexNet', N'Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton', NULL, N'ImageNet Classification with Deep Convolutional Neural Networks', NULL, NULL, N'2022-03-01', N'1')
GO

INSERT INTO [dbo].[models] ([model_id], [model_name], [model_author], [dataset_id], [paper_name], [model_url], [paper_url], [model_time], [model_class]) VALUES (N'2', N'hhh', NULL, NULL, NULL, NULL, NULL, NULL, N'1')
GO

INSERT INTO [dbo].[models] ([model_id], [model_name], [model_author], [dataset_id], [paper_name], [model_url], [paper_url], [model_time], [model_class]) VALUES (N'3', N'php', NULL, NULL, NULL, NULL, NULL, NULL, N'1')
GO


-- ----------------------------
-- Primary Key structure for table models
-- ----------------------------
ALTER TABLE [dbo].[models] ADD CONSTRAINT [PK__models__DC39CAF4D9A039A4] PRIMARY KEY CLUSTERED ([model_id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

