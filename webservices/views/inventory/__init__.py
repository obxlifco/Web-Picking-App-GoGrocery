#--------------------Shipping method -------
from webservices.views.inventory.ShippingMethod import ShippingMethodList,ShippingMethod
#--------------------payment method -------
from webservices.views.inventory.PaymentMethod import PaymentMethodList,PaymentMethod
#--------------------Suppliers-------------
from webservices.views.inventory.Suppliers import WarehouseSupplierMapDelete,WarehouseSupplierMapList,WarehouseSupplierMap,Suppliers,SuppliersList,statelist,Suppliersadd,SupplierPoList
from webservices.views.inventory.Warehouse import Warehouse,WarehouseAllList,WarehouseList, DuplicatePriceRemove, UpadateStockTestCron

from webservices.views.inventory.PurchaseOrder import UpdateSafetyStock,GrnSend,poreceivedget,PoReceived,SuppliersEmail,PurchaseOrder,PurchaseOrderViewList,SuppliersDropdown,SuppliersAddress,SuppliersCurrency,SuppliersProducts,PurchaseOrderList,PurchaseOrdersStatusChange,PurchaseOrderGrnDetails, PurchaseOrderView
from webservices.views.inventory.StockManagement import *
from webservices.views.inventory.threading import *



