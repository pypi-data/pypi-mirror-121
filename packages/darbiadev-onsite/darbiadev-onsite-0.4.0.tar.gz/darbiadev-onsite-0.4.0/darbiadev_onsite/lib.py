#!/usr/bin/env python

from importlib.resources import files
from typing import Any

import jaydebeapi


class OnSiteServices:
    """A class wrapping an ODBC connection to OnSite.

    This class wraps an ODBC connection to OnSite.
    """

    def __init__(
            self,
            connection_url: str,
            username: str,
            password: str
    ):
        self._connection_url: str = connection_url
        self.__username: str = username
        self.__password: str = password

    def _connect(
            self,
    ):
        return jaydebeapi.connect(
            'com.filemaker.jdbc.Driver',
            self._connection_url,
            [self.__username, self.__password],
            str(files('darbiadev_onsite').joinpath('vendor/fmjdbc.jar')),
        )

    def _make_query(
            self,
            sql: str,
    ) -> list[dict[str, Any]]:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_order(
            self,
            order_number: int,
    ) -> list[dict[str, Any]]:
        sql = f"""
       SELECT 
           Orders.date_Creation,
           Orders.gn_ID_User,
           Orders.ID_Order,
           Orders.id_Customer,
           Orders.date_OrderPlaced,
           Orders.date_OrderRequestedToShip,
           Orders.date_OrderDropDead,
           Orders.id_OrderTypeSerial,
           Orders.id_OrderType,
           Orders.gt_ContactDepartment,
           Orders.gt_ContactNameFull,
           Orders.gt_ContactTitle,
           Orders.ContactFirst,
           Orders.ContactLast,
           Orders.ContactPhone,
           Orders.ContactFax,
           Orders.ContactEmail,
           Orders.NotesOnOrder,
           Orders.ContactTitle,
           Orders.ContactDepartment,
           Orders.CustomerPurchaseOrder,
           Orders.TermsName,
           Orders.id_EmpSalesperson,
           Orders.id_EmpCreatedBy,
           Orders.CustomerType,
           Orders.id_CompanyLocation,
           Orders.id_EmployeeOwn,
           Orders.sts_GroupSalesMain,
           Orders.sts_Invoiced,
           Orders.cn_sts_HoldOrderGraphic,
           Orders.sts_ArtDone,
           Orders.sts_Purchased,
           Orders.sts_PurchasedSub,
           Orders.sts_Received,
           Orders.sts_ReceivedSub,
           Orders.sts_Produced,
           Orders.sts_Shipped,
           Orders.sts_OwnershipMode,
           Orders.sts_OwnershipType,
           Orders.ct_id_EmployeeOwn,
           Orders.sts_Attachment,
           Orders.cn_sts_HoldOrder,
           Orders.cn_sts_Rush,
           Orders.sts_RushOverride,
           Orders.sts_Activity,
           Orders.sts_Paid,
           Orders.sts_BackOrder,
           Orders.sts_EDP_Hold,
           Orders.CustomerServiceRep,
           Orders.cn_sts_ShippingSpecType,
           Orders.HoldOrderText,
           Orders.id_SalesStatus,
           Orders.CompanyName,
           Orders.DesignTitleBlock,
           Orders.id_DesignBlock,
           Orders.gt_ID_Block,
           Orders.ct_ContactNameFull,
           Orders.cn_sts_Assembly,
           Orders.cn_TotalProductQty_Pricing,
           Orders.date_OrderInvoiced,
           Orders.Invoice_Field01,
           Orders.Invoice_Field02,
           Orders.EmployeeNamePurchasing,
           Orders.date_Stamp_Invoiced,
           Orders.id_Employee_Stamp_Invoiced,
           Orders.TermsDays,
           Orders.cd_date_PaymentDue,
           Orders.date_Today,
           Orders.cn_sts_Receivable,
           Orders.NotesOnArt,
           Orders.NotesOnReceiving,
           Orders.NotesOnProduction,
           Orders.NotesOnShipping,
           Orders.NotesOnAccounting,
           Orders.cn_TotalProductQty_Act,
           Orders.cn_TotalProductQty_Current,
           Orders.cn_TotalProductQty_Imprints,
           Orders.id_ReceivingStatus,
           Orders.id_DiscountLevel,
           Orders.per_Discount,
           Orders.DiscountNote,
           Orders.cur_DiscountFlat,
           Orders.date_External,
           Orders.ExtSource,
           Orders.ExtOrderID,
           Orders.gt_SFFilterLayout_Receivables,
           Orders.TextOrder,
           Orders.ct_TextOrder,
           Orders.gd_DateAgingAsOf,
           Orders.date_ForAging,
           Orders.id_ShippingStatus,
           Orders.cn_TotalProductQty_ToProduce,
           Orders.date_ProductionScheduled,
           Orders.cd_date_Shipped_Max,
           Orders.gt_FormFilter,
           Orders.sum_cur_Shipping,
           Orders.sum_cur_Subtotal,
           Orders.cn_EventTimeSetup,
           Orders.cn_EventTimeRun,
           Orders.cn_EventTimeJob,
           Orders.cm_EventTimeJobDisplay,
           Orders.cm_EventTimeRunDisplay,
           Orders.cm_EventTimeSetupDisplay,
           Orders.cn_MachinesUsed,
           Orders.cn_EventDesignCount,
           Orders.cn_DesignCount,
           Orders.cn_LocationCount,
           Orders.cn_EventLocationCount,
           Orders.cn_EventUsingDesignCount,
           Orders.cn_EventNotUsingDesignCount,
           Orders.cn_EventUsingDesignQty,
           Orders.cn_EventNotUsingDesignQty,
           Orders.cn_DaysToComplete,
           Orders.cn_DaysLate,
           Orders.date_OrderShipped,
           Orders.date_DesignScheduled,
           Orders.cn_StitchCount,
           Orders.cn_ColorsCount,
           Orders.sum_cn_ColorsCount,
           Orders.sum_cn_EventTimeJob,
           Orders.sum_cn_LocationCount,
           Orders.sum_cn_StitchCount,
           Orders.sum_cn_TotalProductQty_Imprints,
           Orders.sum_cn_TotalProductQty_ToProduce,
           Orders.sum_cn_DesignCount,
           Orders.sum_cm_EventTimeRunDisplay,
           Orders.sum_cm_EventTimeSetupDisplay,
           Orders.sum_cm_EventTimejobDisplay,
           Orders.date_ProductionDone,
           Orders.date_DesignDone,
           Orders.NotesOnHold,
           Orders.NotesToArt,
           Orders.NotesToPurchasing,
           Orders.NotesToReceiving,
           Orders.NotesToProduction,
           Orders.NotesToFinishing,
           Orders.NotesFormsOrderApproval,
           Orders.NotesToAccounting,
           Orders.NotesFormsInvoice,
           Orders.NotesFormsPackingList,
           Orders.NotesToWebCustomer,
           Orders.NotesToWebSalesperson,
           Orders.NotesToShipping,
           Orders.NotesOnPurchasing,
           Orders.NotesToPurchasingSub,
           Orders.NotesOnPurchasingSub
           FROM Orders 
           WHERE Orders.ID_Order = {order_number}
     """
        return self._make_query(sql=sql)

    def get_order_lines(
            self,
            order_number: int,
    ) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
           LinesOE.ID_LineOE,
           LinesOE.PartNumber,
           LinesOE.PartColorRange,
           LinesOE.PartColor,
           LinesOE.PartDescription,
           LinesOE.Size01_Req,
           LinesOE.Size02_Req,
           LinesOE.Size03_Req,
           LinesOE.Size04_Req,
           LinesOE.Size05_Req,
           LinesOE.Size06_Req,
           LinesOE.cn_LineQuantity_Req,
           LinesOE.id_OrderType,
           LinesOE.OrderInstructions,
           LinesOE.OrderInvoiceNotes
        FROM LinesOE
        WHERE LinesOE.id_order = {order_number}
     """
        return self._make_query(sql=sql)

    def get_address(
            self,
            order_number: int,
    ) -> list[dict[str, Any]]:
        sql = f"""
            SELECT "All",
               date_creation,
               date_modification,
               gn_id_address,
               gn_id_unique,
               gn_id_user,
               id_address,
               id_unique,
               sts_archive,
               time_creation,
               time_modification,
               timestamp_creation,
               timestamp_modification,
               id_customer,
               id_vendor,
               addresscompany,
               address1,
               address2,
               addresscity,
               addressstate,
               addresscountry,
               addresszip,
               id_vendormain,
               id_employee,
               id_employeemain,
               ct_addressfull,
               sts_mainaddress,
               addressdescription,
               explode_company,
               explode_address1,
               explode_address2,
               explode_city,
               explode_state,
               explode_zip,
               explode_country,
               id_customermain,
               sts_omit,
               id_companylocationshipping,
               id_companylocationbilling,
               gt_sffilterlayout,
               gt_sffiltertable,
               gn_id_customer,
               gn_id_vendor,
               cn_foundcount,
               explode_description,
               gn_portalcolumn,
               id_contact,
               id_marketing,
               id_quote,
               gt_id_block,
               gn_id_marketingdb_working,
               gt_access_overall,
               gt_access_record,
               gt_customexport_category,
               gt_customexport_source,
               gt_customreport_category,
               gt_customreport_source,
               gn_all,
               sum_all,
               id_marketingimport,
               ct_addressfullprint,
               id_order,
               shipmethod,
               gn_id_order,
               gn_id_lineoe,
               ct_citystatezipcountry,
               id_employeeown,
               sts_ownershipmode,
               sts_ownershiptype,
               ct_contactemail,
               ct_contactname,
               ct_id_orderkeyimport,
               id_orderkeyalpha
            FROM Addr
            WHERE id_order = {order_number}
               """
        return self._make_query(sql=sql)
