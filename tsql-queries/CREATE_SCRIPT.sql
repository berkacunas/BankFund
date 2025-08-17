USE [BankFunds]
GO

/****** Object:  Table [dbo].[Bank]    Script Date: 26.06.2025 21:55:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Bank](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_Bank] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO





USE [BankFunds]
GO

/****** Object:  Table [dbo].[Directions]    Script Date: 26.06.2025 21:56:02 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Directions](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Direction] [nvarchar](8) NOT NULL,
 CONSTRAINT [PK_Directions] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO






USE [BankFunds]
GO

/****** Object:  Table [dbo].[Fund]    Script Date: 26.06.2025 21:57:01 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Fund](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](max) NOT NULL,
	[BankId] [int] NOT NULL,
	[TypeId] [int] NOT NULL,
 CONSTRAINT [PK_Fund] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Fund]  WITH CHECK ADD  CONSTRAINT [FK_Fund_FundTypeId] FOREIGN KEY([TypeId])
REFERENCES [dbo].[FundType] ([id])
GO

ALTER TABLE [dbo].[Fund] CHECK CONSTRAINT [FK_Fund_FundTypeId]
GO







USE [BankFunds]
GO

/****** Object:  Table [dbo].[FundMove]    Script Date: 26.06.2025 21:57:18 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FundMove](
	[id] [int] NOT NULL,
	[Dt] [datetime2](7) NOT NULL,
	[UserId] [int] NOT NULL,
	[FundId] [int] NOT NULL,
	[Count] [int] NULL,
	[Purchase] [decimal](18, 10) NULL,
	[Sell] [decimal](18, 10) NULL,
	[DirectionId] [int] NOT NULL,
	[DailyFundReturn] [decimal](18, 10) NULL
) ON [PRIMARY]
GO







USE [BankFunds]
GO

/****** Object:  Table [dbo].[FundType]    Script Date: 26.06.2025 21:57:35 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FundType](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](512) NOT NULL,
	[FundCount] [int] NOT NULL,
 CONSTRAINT [PK_FundTypes] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [title_unique] UNIQUE NONCLUSTERED 
(
	[Title] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO








USE [BankFunds]
GO

/****** Object:  Table [dbo].[FundValue]    Script Date: 26.06.2025 21:57:50 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FundValue](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Code] [nvarchar](16) NOT NULL,
	[Dt] [datetime2](7) NOT NULL,
	[FundId] [int] NOT NULL,
	[Currency] [nvarchar](32) NOT NULL,
	[UnitSharePrice] [decimal](16, 10) NOT NULL,
	[RiskLevel] [int] NOT NULL,
	[DailyReturn] [decimal](16, 10) NULL,
	[MonthlyReturn] [decimal](16, 10) NULL,
	[ThreeMonthReturn] [decimal](16, 10) NULL,
	[FromNewYear] [decimal](16, 10) NULL,
	[Description] [nvarchar](max) NULL,
 CONSTRAINT [PK_FundValue] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[FundValue]  WITH CHECK ADD  CONSTRAINT [FK_FundDailyValue_FundId] FOREIGN KEY([FundId])
REFERENCES [dbo].[Fund] ([id])
GO

ALTER TABLE [dbo].[FundValue] CHECK CONSTRAINT [FK_FundDailyValue_FundId]
GO







USE [BankFunds]
GO

/****** Object:  Table [dbo].[HtmlSource]    Script Date: 26.06.2025 21:58:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[HtmlSource](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Html] [nvarchar](max) NOT NULL,
	[Dt] [datetime2](7) NOT NULL,
 CONSTRAINT [PK_HtmlSource] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO







USE [BankFunds]
GO

/****** Object:  Table [dbo].[User]    Script Date: 26.06.2025 21:58:21 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[User](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [nvarchar](128) NOT NULL,
	[Midname] [nvarchar](128) NULL,
	[Lastname] [nvarchar](128) NOT NULL,
	[Fullname] [nvarchar](256) NOT NULL,
 CONSTRAINT [PK_User] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


