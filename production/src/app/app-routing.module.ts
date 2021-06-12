import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './global/service/auth-guard.service';
import { NotfoundComponent }  from './app.notfound.component';
import { LoginComponent }  from './main-component/app.login.component';
import { ForgotPasswordComponent }  from './main-component/app.forgotpass.component';
import { ResetPasswordComponent }  from './main-component/app.resetpass.component';
import { VerifyCodeComponent }  from './main-component/app.verifyCode.component';
import { UpdatePasswordComponent }  from './main-component/app.updatePwd.component';


const routes: Routes = [
    { path: '', pathMatch: 'full', component: LoginComponent, data: { title: 'Login', is_login: 1 }},
    { path: 'login', component: LoginComponent, data: { title: 'Login', is_login: 1 } },
    { path: 'forgot_password', component: ForgotPasswordComponent, data: { title: 'Forgot Password', is_login: 1 } },
    { path: 'reset_password', component: ResetPasswordComponent, data: { title: 'Reset Password', is_login: 1 } },
    { path: 'verify_code', component: VerifyCodeComponent, data: { title: 'Forgot Password', is_login: 1 } },
    // { path: 'update_password', component: UpdatePasswordComponent, data: { title: 'ForgCreditearnAddeditComponentot Password', is_login: 1 } },
    //  { path: 'dashboard', component: DashboardComponent, data: { title: 'Dashboard', is_login: 0, state: 'dashboard' }, canActivate: [AuthGuard],},
    // { path: 'dashboard/:action', component: DashboardComponent, data: { title: 'Dashboard', is_login: 0, state: 'dashboard' }, canActivate: [AuthGuard],},

    ////////DASHBOARD//////////////////
    {
        path:'dashboard',data : {title : 'dashboard' , is_login: 0, state: 'dashboard'} , canActivateChild:[AuthGuard],
        loadChildren: './dashboard/dashboard.module#DashboardModule'
    },
    //////////Employee/////////////////

    { 
        path:'groups',data : {title : 'Group' , is_login: 0, state: 'groups'} , canActivateChild:[AuthGuard],
        loadChildren: './employee/group/group.module#GroupModule'
    },
    
    { 
        path:'users',data : {title : 'Users' , is_login: 0, state: 'users'} , canActivateChild:[AuthGuard],
        loadChildren: './employee/user/user.module#UserModule'
    },

    { 
        path:'roles',data : {title : 'Role' , is_login: 0, state: 'roles'} , canActivateChild:[AuthGuard],
        loadChildren: './employee/role/role.module#RoleModule'
    }, 

    /////////Product/////////////////
    { 
        path:'barcodes',data : {title : 'Product barcode' , is_login: 0, state: 'barcodes'} , canActivateChild:[AuthGuard],
        loadChildren: './products/barcodes/barcodes.module#BarcodesModule'
    },

    { 
        path:'products',data : {title : 'Products' , is_login: 0, state: 'products'} , canActivateChild:[AuthGuard],
        loadChildren: './products/product/product.module#ProductModule'
    },
    { 
        path:'category',data : {title : 'Category' , is_login: 0, state: 'category'} , canActivateChild:[AuthGuard],
        loadChildren: './products/category/category.module#CategoryModule'
    },
    { 
        path:'category-banner',data : {title : 'Category Banner' , is_login: 0, state: 'category-banner'} , canActivateChild:[AuthGuard],
        loadChildren: './products/category-banner/category-banner.module#CategoryBannerModule'
    },
    { 
        path:'brand',data : {title : 'Brand' , is_login: 0, state: 'brand'} , canActivateChild:[AuthGuard],
        loadChildren: './products/brand/brand.module#BrandModule'
    },
    { 
        path:'product_tax_class',data : {title : 'Product tax class' , is_login: 0, state: 'product_tax_class'} , canActivateChild:[AuthGuard],
        loadChildren: './products/producttax/producttax.module#ProducttaxModule'
    },
    { 
        path:'customer_tax_class',data : {title : 'Customer tax class' , is_login: 0, state: 'customer_tax_class'} , canActivateChild:[AuthGuard],
        loadChildren: './products/customertax/customertax.module#CustomertaxModule'
    },
    { 
        path: 'tax_rates', data: { title: 'Tax Rates', is_login: 0, state: 'tax_rates'}, canActivateChild: [AuthGuard],
        loadChildren: './products/taxrates/taxrates.module#TaxratesModule'
    },
    { 
        path: 'tax_rules', data: { title: 'Tax Rules', is_login: 0, state: 'tax_rules'}, canActivateChild: [AuthGuard],
        loadChildren: './products/taxrules/taxrules.module#TaxrulesModule'
    },
    {
        path:'hsn_code_list',data : {title : 'HSN Code' , is_login: 0, state: 'hsn_code_list'} , canActivateChild:[AuthGuard],
        loadChildren: './products/hsncode/hsncode.module#HsncodeModule'
    },

    { path: 'review', data: { title: 'Review', is_login: 0, state: 'review' }, canActivateChild: [AuthGuard],
        loadChildren: './products/review/review.module#ReviewModule'
    },

    { path: 'contactlists', data: { title: 'Contact Group', is_login: 0, state: 'contactlists' }, canActivateChild: [AuthGuard],
       loadChildren: './products/contact-group/contactgroup.module#ContactgroupModule'
    },
    
    { path: 'contacts', data: { title: 'Contacts', is_login: 0, state: 'contacts' }, canActivateChild: [AuthGuard],
        loadChildren: './products/contacts/contact.module#ContactModule'
    },
    //SEGMENTS
    {
        path:'segments',data : {title : 'Segments' , is_login: 0, state: 'segments'} , canActivateChild:[AuthGuard],
        loadChildren: './products/segment/segment.module#SegmentModule'
    },

    {
        path: 'discount_coupon', data: { title: 'Coupon Promotion', is_login: 0, discountType: 1, state: 'discount_coupon' }, canActivateChild: [AuthGuard],
        loadChildren: './products/promotion/couponpromotion.module#CouponpromotionModule'
    },

    {
        path: 'discount_product', data: { title: 'Product Promotion', is_login: 0, discountType: 0, state: 'discount_coupon' }, canActivateChild: [AuthGuard],
        loadChildren: './products/promotion/productpromotion.module#ProductpromotionModule'
    },
    //GIFT CARDS
    { 
        path:'gift_cards',data : {title : 'Gift Cards' , is_login: 0, state: 'gift_cards'} , canActivateChild:[AuthGuard],
        loadChildren: './products/giftcards/giftcards.module#GiftcardsModule'
    },
    /////////Inventory/////////////////
    { path: 'suppliers', data: { title: 'Suppliers', is_login: 0, state: 'suppliers'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/supplier/supplier.module#SupplierModule'
    },
    { path: 'warehouses', data: { title: 'Warehouse', is_login: 0, state: 'warehouses'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/warehouse/warehouse.module#WarehouseModule'
    },
    { path: 'payment_method', data: { title: 'PO Payment Method', is_login: 0, state: 'payment_method'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/po-payment-method/popaymentmethod.module#PaymentMethodModule'
    },
    { path: 'shipping_method', data: { title: 'PO Shipping Method', is_login: 0, state: 'shipping_method'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/po-shipping-method/poshippingmethod.module#ShippingMethodModule'
    },
    { path: 'stocks', data: { title: 'Stock Management', is_login: 0, state: 'stock'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/stock/stock.module#StockModule'
    },
    { path: 'stocks_price_management', data: { title: 'Stock and Price Management', is_login: 0, state: 'stock-price'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/stock-price/stock_price.module#StockPriceModule'
    },
    { path: 'purchase_order', data: { title: 'Purchase Order', is_login: 0, state: 'purchase_order'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/purchase-order/purchaseorder.module#PurchaseOrderModule'
    },
    { path: 'stock_adjustment', data: { title: 'Stock Adjustment', is_login: 0, state: 'stock'}, canActivateChild: [AuthGuard],
        loadChildren: './inventory/stock-adjustment/stockadjustment.module#StockAdjustmentModule'
    },

    // Order Modeul start here...
    { path:'orders',data : {title : 'Order' , is_login: 0, state: 'order'} , canActivateChild:[AuthGuard],
        loadChildren: './order/order/order.module#OrderModule'
    },

    { path:'picklist',data : {title : 'Picklist' , is_login: 0, state: 'picklist'} , canActivateChild:[AuthGuard],
        loadChildren: './order/shipment/shipment.module#ShipmentModule'
    },

    { path:'shipment',data : {title : 'Shipment' , is_login: 0, state: 'shipment'} , canActivateChild:[AuthGuard],
        loadChildren: './order/shipment/shipment.module#ShipmentModule'
    },

    { path: 'customers', data: { title: 'Customers', is_login: 0, state: 'customers'}, canActivateChild: [AuthGuard],
        loadChildren: './order/customer/customer.module#CustomerModule'
    },

    { path: 'preset', data: { title: 'Preset', is_login: 0, state: 'preset'}, canActivateChild: [AuthGuard],
        loadChildren: './order/preset/preset.module#PresetModule'
    },
    
    { path: 'courier', data: { title: 'Courier', is_login: 0, state: 'courier'}, canActivateChild: [AuthGuard],
        loadChildren: './order/courier/courier.module#CourierModule'
    },

    { path: 'customer_group', data: { title: 'Customer Group', is_login: 0, state: 'customer_group'}, canActivateChild: [AuthGuard],
        loadChildren: './order/customer-group/customergroup.module#CustomerGroupModule'
    },
    { path: 'emailnotification', data: { title: 'Auto Responding', is_login: 0, state: 'emailnotification'}, canActivateChild: [AuthGuard],
        loadChildren: './order/auto-responder/autoresponder.module#AutoResponderModule'
    },
    // Order Modeul end here...

    // Area Management
    { 
        path:'area_management',data : {title : 'Area Management' , is_login: 0, state: 'area_management'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/area/area.module#AreaModule'
    },

    //Veichle Management
    { 
        path:'vehicle',data : {title : 'Vehicle Management' , is_login: 0, state: 'vehicle'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/vehicle/vehicle.module#VehicleModule'
    },
    //DELIVERY MANAGER
    { 
        path:'delivery_manager',data : {title : 'LMD Executive' , is_login: 0, state: 'delivery_manager'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/delivery-manager/delivery-manager.module#DeliveryManagerModule'
    },
    //DELIVERY SLOT
    { 
        path:'delivery_slot',data : {title : 'Delivery Slot' , is_login: 0, state: 'delivery_slot'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/delivery-slot/delivery-slot.module#DeliverySlotModule'
    },
    //PRICE FORMULA
    { 
        path:'price_formula',data : {title : 'Price Calculation' , is_login: 0, state: 'price_formula'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/price-calculation/price-calculation.module#PriceCalculationModule'
    },
    //CREDIT BURN
    { 
        path:'credit_points_burn',data : {title : 'Credit Points Burn' , is_login: 0, state: 'credit_points_burn'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/creditburn/creditburn.module#CreditburnModule'
    },
    //CREDIT EARN
    { 
        path:'credit_points_earn',data : {title : 'Credit Points Earn' , is_login: 0, state: 'credit_points_earn'} , canActivateChild:[AuthGuard],
        loadChildren: './operations/creditearn/creditearn.module#CreditearnModule'
    },
    
    //<!----SETTINGS-->
    //BASIC SETUP
    { 
        path:'basicsetup',data : {title : 'Basic Setup' , is_login: 0, state: 'delivery_manager'} , canActivateChild:[AuthGuard],
        loadChildren: './settings/basic-setup/basic-setup.module#BasicSetupModule'
    },
    //STORE CATEGORY TYPE
    { 
        path:'store-category',data : {title : 'Store Category' , is_login: 0, state: 'storecategory'} , canActivateChild:[AuthGuard],
        loadChildren: './settings/store-category_type/store-category.module#StoreCategoryModule'
    },
    //CURRENCY
    { 
        path:'currencies',data : {title : 'Currency' , is_login: 0, state: 'currencies'} , canActivateChild:[AuthGuard],
        loadChildren: './settings/currency/currency.module#CurrencyModule'
    },
    //GLOBAL SETUP
    { 
        path:'globalsettings',data : {title : 'Global Settings' , is_login: 0, state: 'globalsettings'} , canActivateChild:[AuthGuard],
        loadChildren: './settings/global-setup/global-setup.module#GlobalSetupModule'
    },
    // Unit Management
    { 
        path: 'units', data: { title: 'Unit', is_login: 0, state: 'units' }, canActivateChild: [AuthGuard],
        loadChildren: './settings/unit/unit.module#UnitModule'
    },

    //TAX SETTINGS
    { 
        path:'tax_settings',data : {title : 'Tax settings' , is_login: 0, state: 'tax_settings'} , canActivateChild:[AuthGuard],
        loadChildren: './settings/taxsettings/taxsettings.module#TaxsettingsModule'
    },

    { path: 'manage_store', data: { title: 'Manage Store', is_login: 0, state: 'Admin'}, canActivateChild: [AuthGuard],
        loadChildren: './manage-store/manage-store.module#ManageStoreModule'
    },
    //LANGUAGE
    { 
        path:'languages',data : {title : 'Language' , is_login: 0, state: 'languages'} , canActivateChild:[AuthGuard],
        loadChildren: './settings/language/language.module#LanguageModule'
    },

    { path:'return',data : {title : 'Return' , is_login: 0, state: 'return'} , canActivateChild:[AuthGuard],
        loadChildren: './order/return/return.module#ReturnModule'
    },

    /*
    { path: 'basicsetup', data: { title: 'Basic Setup', is_login: 0, state: 'basicsetup'}, canActivateChild: [AuthGuard],
        children: [
            { path: '', component: BasicSetupComponent },
            { path: 'add', component: BasicSetupAddEditComponent },
            { path: 'edit/:id', component: BasicSetupAddEditComponent },
            { path: 'edit/:id/template', component: BasicSetupTemplateComponent },
            { path: 'edit/:id/payment_gateway', component: BasicSetupPaymentGatewayComponent },
            { path: 'edit/:id/shipping', component: BasicSetupShippingComponent, data: { ship_type:1 }}, //1=flat ship,2=free shipping
            { path: 'edit/:id/free_shipping', component: BasicSetupShippingComponent, data: { ship_type:2 }},
            { path: 'edit/:id/tax', component: BasicSetupTaxRateComponent},
            { path: 'edit/:id/channel_setup', component: ChannelSetupAddEditComponent}
            
        ]
    },
    { path:'delivery_manager',data : {title : 'LMD Executive' , is_login: 0, state: 'delivery_manager'} , canActivateChild:[AuthGuard],
        children: [
            { path: '', component:DeliveryManagerComponent },
            { path: 'add', component:ManagerAddeditComponent },
            { path: 'edit/:id', component:ManagerAddeditComponent },
        ]
    },
    { path:'price_formula',data : {title : 'Price Calculation' , is_login: 0, state: 'price_formula'} , canActivateChild:[AuthGuard],
        children: [
            { path: '', component:PriceCalculationComponent },
            { path: 'add', component:PriceAddeditComponent },
            { path: 'edit/:id', component:PriceAddeditComponent },
        ]
    },
    { path:'delivery_slot',data : {title : 'Delivery Slot' , is_login: 0, state: 'delivery_slot'} , canActivateChild:[AuthGuard],
        children: [
            { path: '', component:DeliverySlotComponent },
        ]
    },
    { path:'credit_points_earn',data : {title : 'Credit Points Earn' , is_login: 0, state: 'credit_points_earn'} , canActivateChild:[AuthGuard],
        children: [
            { path: '', component:CreditearnComponent },
            { path: 'add', component:CreditearnAddeditComponent },
            { path: 'edit/:id', component:CreditearnAddeditComponent },
            { path: 'conditions/:id', component:CreditearnconditionAddeditComponent},
            { path: 'conditions/edit/:id', component:CreditearnconditionAddeditComponent},
        ]
    },
    { path:'credit_points_burn',data : {title : 'Credit Points Burn' , is_login: 0, state: 'credit_points_burn'} , canActivateChild:[AuthGuard],
        children: [
            { path: '', component:CreditburnComponent },
            { path: 'add', component:CreditburnAddeditComponent },
            { path: 'edit/:id', component:CreditburnAddeditComponent },
            { path: 'conditions/:id', component:CreditburnconditionAddeditComponent},
            { path: 'conditions/edit/:id', component:CreditburnconditionAddeditComponent},

        ]
    }, */
    /////////404/////////////////
    { path: '**', component: NotfoundComponent }
];

@NgModule({
    imports: [
        RouterModule,
        RouterModule.forRoot(routes)

    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule { }

export const routedComponents = [
    NotfoundComponent ,
    LoginComponent, 
    ForgotPasswordComponent, 
    ResetPasswordComponent,
    VerifyCodeComponent, 
    UpdatePasswordComponent,
];