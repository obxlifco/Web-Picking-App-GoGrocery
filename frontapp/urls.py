from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from frontapp import views
from frontapp.views.sitecommon import menu
from frontapp.views.home import homepage
from frontapp.views.category import categoryview
from frontapp.views.product import productview
from frontapp.views.contentmanagement import *
from frontapp.views import Featured
from frontapp.views.signup import signupview, forgotpasswordview
from frontapp.views.cart import cartview
from frontapp.views.payment import paymentmethods
from frontapp.views.myaccount import myaccountview
from frontapp.views.myaccount import myorder
from frontapp.views.product import mysavelistview
from frontapp.views.product import wishlistview
from frontapp.views.product import reviewrating
from frontapp.views.payment import paymentgateway
from frontapp.views.payment import ccavResponseHandler
from frontapp.views.payment import GetRSA
from frontapp.views.payment import ccavRequestHandler
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Lifco Api')


urlpatterns = [
    url(r'swagger-docs/', schema_view),
    # Menu
    url(r'^menu_bar/$',views.sitecommon.GetMenuList.as_view(),name='menu_bar'),
    url(r'^footer_menu/$',views.sitecommon.FooterMenu.as_view(),name='footer_menu'),
    url(r'^category_banner_for_home/$',views.sitecommon.HomeCategoryBanner.as_view(),name='category_banner_for_home'),
    url(r'^home-cms/$',views.home.HomeCms.as_view(),name='home-cms'),
    url(r'^warehouse-list/$',views.sitecommon.GetWarehouseListByLatLong.as_view(),name='warehouse-list'),
    url(r'^category_banner/',views.home.homepage.category_banner,name='category_banner'),
    url(r'^subscribe-newsletter/$',views.home.homepage.SubscribeNewsletter.as_view(),name='subscribe-newsletter'),
    url(r'^unsubscribe-newsletter/$',views.home.homepage.UnsubscribeNewsletter.as_view(),name='unsubscribe-newsletter'),


    # url(r'^similar-product/$',views.home.SimilarProduct.as_view(),name='similar-product'),
    url(r'^similar-product/(?P<product_id>.*)/$', views.product.SimilarProduct.as_view(), name='similar-product'),
    url(r'^popular-product/(?P<product_id>.*)/$', views.product.PopularProduct.as_view(), name='popular-product'),
    url(r'^like-product/$', views.product.LikeProduct.as_view(), name='like-product'),
    url(r'^search-product/$', views.product.SearchList.as_view(), name='search-product'),
    url(r'^search-filter/$', views.product.SearchFilters.as_view(), name='search-filter'),
    
    

    # Category
    url(r'^parent-category-list/$', views.category.ParentCategoryListView.as_view(), name='parent-category-list'),
    url(r'^shop_by_category/$',views.category.ShopByCategory.as_view(),name ='shop_by_category'),
    url(r'^shop_by_categoryids/$',views.category.ShopByCategoryByCatId.as_view(),name ='shop_by_categoryids'),

    #  product
    url(r'^product-details/(?P<slug>[\w\-]+)/$',views.product.ProductDetails.as_view(),name ='product-details'),
    url(r'^basic-info-page-load/(?P<pk>.*)/$', views.Featured.Pageloadsettings.as_view()),
    url(r'^get_slug/$', views.Featured.GetSlug.as_view()),
    # url(r'^product-list/$',views.product.CategoryProductListView.as_view(),name='product-list'),
    url(r'^slug/$', views.product.SlugToId.as_view()),    
    
    # CMS
    url(r'^page_url_to_id/', views.contentmanagement.Pageslurtoidload),
    url(r'^cms_form_data/', views.contentmanagement.PageFormData.as_view()),
    url(r'^brand_list/', views.contentmanagement.BrandList),
    url(r'^all_menu/(?P<pk>[0-9]+)/(?P<website_id>[0-9]+)/$', views.contentmanagement.AllMenu.as_view()),  

    # Other
    url(r'^best_selling_product/$', views.home.homepage.BestSellingProduct.as_view(), name='best_selling_product'),
    url(r'^deals_of_the_day/$', views.home.homepage.DealsOfTheDay.as_view(), name='deals_of_the_day'),
    url(r'^product-list/$',views.home.homepage.CategoryProductListView.as_view(),name='product-list'),
    url(r'^brand_list_by_brandid/$',views.home.homepage.BrandListByBrandId.as_view(),name ='brand_list_by_brandid'),
    url(r'^banner_list/$',views.home.homepage.BannerList.as_view(),name='banner_list'),
    url(r'^banner-list-for-home/$',views.home.homepage.BannerListForHome.as_view(),name='banner-list-for-home'),

    #  CART
    url(r'^add-to-cart/$', views.cart.cartview.add_to_cart.as_view(),name='add-to-cart'),
    url(r'^view-cart/$', views.cart.cartview.Viewcart.as_view(),name='view-cart'),
    url(r'^remove-cart/$', views.cart.cartview.remove_cart.as_view(),name='remove-cart'),
    url(r'^empty-cart/$', views.cart.cartview.empty_cart.as_view(),name='empty-cart'),
    url(r'^save-cart/$', views.cart.cartview.SaveCart.as_view(),name='save-cart'),
    url(r'^save-cart-si/$', views.cart.cartview.SaveCartSi.as_view(),name='save-cart-si'),
    url(r'^save-cart-si-new/$', views.cart.cartview.SaveCartSiNew.as_view(),name='save-cart-si-new'),
    url(r'^order-details/(?P<order_id>.*)/$', views.cart.cartview.ViewOrderDetails.as_view(),name='order-details'),
    url(r'^apply-coupon/$', views.cart.cartview.ApplyCouponCode.as_view(),name='apply-coupon'),
    url(r'^delivery-slot/(?P<zone_id>.*)/$', views.cart.cartview.get_delivery_slot.as_view(), name='delivery-slot'),
    url(r'^checkout/$', views.cart.cartview.checkout.as_view(), name='checkout'),
    url(r'^cart-summary/$', views.cart.cartview.CartSummary.as_view(),name='cart-summary'),
    url(r'^payment/$', views.payment.paymentgateway.MakePayment.as_view(),name='payment'),
    url(r'^payment-android/$', views.payment.paymentgateway.MakePaymentAndroid.as_view(),name='payment-android'),
    url(r'^test-cc/$', views.payment.paymentgateway.TestCC.as_view(),name='test-cc'),
    url(r'^cart-count/$', views.cart.cartview.CartCount.as_view(),name='cart-count'),
    

    # LOYALTY POINTS
    url(r'^creadit-points/$', views.cart.cartview.earn_creadit_points.as_view(), name='creadit-points'),
    url(r'^points-log/$', views.cart.cartview.LoyaltyPointsLog.as_view(), name='points-log'),
    url(r'^check-balance/$', views.cart.cartview.Loyaltypoints.as_view(), name='check-balance'),
    url(r'^apply-loyalty/$', views.cart.cartview.ApplyLoyalty.as_view(), name='apply-loyalty'),
    
    
    # Payment
    url(r'^payment-method/$', views.payment.paymentmethods.PaymentMethodList.as_view(),name='payment-method'),
    url(r'^payment-req/$', views.payment.paymentgateway.getResponseData.as_view(),name='payment-req'),

    # Payment Gateway --- Android
    url(r'^payment-res/$', views.payment.ccavResponseHandler.res,name='payment-req'),
    url(r'^payment-res-demo/$', views.payment.ccavResponseHandler.res_demo,name='payment-res-demo'),
    url(r'^payment-res-si/$', views.payment.ccavResponseHandler.res_si,name='payment-res-si'),

    url(r'^payment-response/$', views.payment.ccavResponseHandler.AcavenueWebResponse,name='payment-response'),
    url(r'^get-rsa/$', views.payment.GetRSA.GetRsa,name='get-rsa'),
    url(r'^get-rsa-demo/$', views.payment.GetRSA.GetRsaDemo,name='get-rsa-demo'),
    url(r'^get-rsa-si/$', views.payment.GetRSA.GetRsaSi,name='get-rsa-si'),
    url(r'^payment-transaction/$', views.payment.paymentgateway.CcAvenueOrderTransaction.as_view(),name='payment-transaction'),
    url(r'^payment-request/$', views.payment.ccavRequestHandler.CcavenueRequestHandler.as_view(),name='payment-request'),
    url(r'^payment-request-si/$', views.payment.ccavRequestHandler.CcavenueRequestHandlerSi.as_view(),name='payment-request-si'),
    url(r'^payment-request-si-charge-list/$', views.payment.ccavRequestHandler.CcavenueRequestHandlerSiChargeList.as_view(),name='payment-request-si-charge-list'),
    url(r'^remove-saved-card/(?P<pk>[0-9]+)/$', views.payment.ccavRequestHandler.RemoveSavedCard.as_view(),name='remove-saved-card'),

    #-----------------duplicate----------------------#
    url(r'^payment-request-si-si/$', views.payment.ccavRequestHandler.CcavenueRequestHandlerSi_SI.as_view(),name='payment-request-si-si'),
    url(r'^payment-response-new/$', views.payment.ccavResponseHandler.AcavenueWebResponse_new,name='payment-response-new'),
    url(r'^payment-response-si/$', views.payment.ccavResponseHandler.AcavenueWebResponse_SI,name='payment-response-si'),

    
    # Login and Signup
    url(r'^login/$', views.signup.signupview.LoginView.as_view(), name='login'), ##########login api#########
    url(r'^signup/$', views.signup.signupview.SignupView.as_view(), name='signup'), ##########signup api#########
    url(r'^check-email/$', views.signup.signupview.CheckEmail.as_view(), name='check-email'),
    url(r'^sync-cart/$', views.cart.cartview.CartSync.as_view(), name='sync-cart'),
    url(r'^social-login/$', views.signup.signupview.SocialLogin.as_view(), name='social-login'),

    # Update device details
    url(r'^update-device-details/$', views.sitecommon.UpdateDeviceDetails.as_view(), name='update-device-details'),
    url(r'^get_storetype/$', views.sitecommon.StoreTypeAll.as_view(), name='get_storetype'),
    
    
    #  Banner
    url(r'^promotional-banner-list/$',views.home.homepage.PromotionalCategoryBannerList,name='promotional-banner-list'),
    url(r'^promotional-banner/$',views.home.homepage.PromotionalBannerById.as_view(),name='promotional-banner'),
    url(r'^listing_filters/$',views.product.listing_filters,name='listing_filters'),
    url(r'^category_banner/',views.product.category_banner,name='category_banner'),

    # My Account
    url(r'^my-profile/$', views.myaccount.myaccountview.MyProfile.as_view(), name='my-profile'), ########## MyProfile############
    url(r'^change-password/$', views.myaccount.myaccountview.ChangePassword.as_view(), name='change-password'), ##########change password############
    # url(r'^edit-profile/$', views.myaccount.myaccountview.EditProfile.as_view(), name='edit-profile'),

    # Checkout
    url(r'^order-history/$', views.myaccount.myaccountview.OrderHistory.as_view(), name='order-history'),###########order history#################
    url(r'^check-delivery-address/$', views.myaccount.myaccountview.CheckDeliveryAddress.as_view(), name='check-delivery-address'),######delivery address#####
    url(r'^check-delivery-address-test/$', views.myaccount.myaccountview.CheckDeliveryAddressTest.as_view(), name='check-delivery-address-test'),######delivery address#####
    url(r'^delivery-address/$', views.myaccount.myaccountview.DeliveryAddress.as_view(), name='delivery-address'),######delivery address#####
    url(r'^delivery-address-test/$', views.myaccount.myaccountview.DeliveryAddressTest.as_view(), name='delivery-address-test'),######delivery address#####
    url(r'^delete-address/(?P<pk>.*)/$', views.myaccount.myaccountview.DeleteAddress.as_view(), name='delete-address'),######delivery address#####
    url(r'^countries-list/$', views.myaccount.myaccountview.CountriesList.as_view(), name='countries-list'),######countries list#####
    url(r'^states-list/$', views.myaccount.myaccountview.StatesList.as_view(), name='states-list'),######countries list#####
    url(r'^cancel-order/(?P<order_id>.*)/$', views.myaccount.myorder.CancelOrder.as_view(), name='cancel-order'),

    # Save List
    url(r'^save-list/$', views.product.MySaveList.as_view(), name='save-list'),############ my-save-list ########### getting save list and add new savelist...
    url(r'^addremove-from-savelist/$', views.product.AddRemoveFromSavelist.as_view(), name='addremove-from-savelist'), # add and remove from save list
    url(r'^savelist-details/(?P<savelist_id>.*)/$', views.product.ViewSavelistDetails.as_view(),name='savelist-details'),
    url(r'^addeditdelete-from-savelist/$', views.product.SavelistAddEditDelete.as_view(), name='addeditdelete-from-savelist'), # add and edit from save list
    url(r'^addeditdelete-from-savelist/(?P<pk>.*)/$', views.product.SavelistAddEditDelete.as_view(), name='addeditdelete-from-savelist'), # add and remove from save list

    # Wish List
    url(r'^my-wish-list/$', views.product.MyWishlist.as_view(), name='my-wish-list'),######### my-wish-list ########
    url(r'^delete-wishlist/$', views.product.DeleteWishlist.as_view(), name='delete-wishlist'),########
    url(r'^get-wishlist-count/$', views.product.GetWishlistCount.as_view(), name='get-wishlist-count'),########

    # Forgot Password
    url(r'^forgotpassword/$', views.signup.forgotpasswordview.forgotpassword),
    url(r'^confirm-password/$', views.signup.forgotpasswordview.PasswordResetConfirmView),
    url(r'^order-details-payment/(?P<order_id>.*)/$', views.cart.cartview.ViewOrderDetailsPayment.as_view(),name='order-details-payment'),
    
    
    # Review Rating
    url(r'^product-review/$', views.product.reviewrating.write_review.as_view(),name='product-review'),
    url(r'^view-review/$', views.product.reviewrating.product_review_stats.as_view(),name='view-review'),

    # version
    url(r'^get-app-version/$',views.home.homepage.GetAppVersion.as_view(),name='get-app-version'),
    # customer quires
    url(r'^customer-query/$',views.home.homepage.CustomerQuery.as_view(),name='customer-query'),
    #select-address
    url(r'^select-address/$',views.myaccount.myaccountview.SelectAddress.as_view(),name='select-address'),
    #Apple_Login and signed up
    url(r'^apple-login/$', views.signup.signupview.AppleLogin.as_view(), name='apple-login'), 


    #------Test Urls------#
    url(r'^login-test/$', views.signup.signupview.LoginViewTest.as_view(), name='login-test'), ##########login api#########
    url(r'^signup-test/$', views.signup.signupview.SignupViewTest.as_view(), name='signup-test'), ##########signup api#########

    url(r'^warehouse-list-test/$',views.sitecommon.GetWarehouseListByLatLongTest.as_view(),name='warehouse-list-test'),
    url(r'^view-cart-test/$', views.cart.cartview.ViewcartTest.as_view(),name='view-cart-test'),
    url(r'^apply-coupon-test/$', views.cart.cartview.ApplyCouponCodeTest.as_view(),name='apply-coupon-test'),

    url(r'^cart-summary-test/$', views.cart.cartview.CartSummaryTest.as_view(),name='cart-summary-test'),
    url(r'^delete-wishlist-test/$', views.product.DeleteWishlistTest.as_view(), name='delete-wishlist-test'),########

    url(r'^my-profile-test/$', views.myaccount.myaccountview.MyProfileTest.as_view(), name='my-profile-test'), ########## MyProfile############
    #------Test Urls------#

    #------New Urls-------#
    url(r'^menu_bar_app/$',views.sitecommon.GetMenuListApp.as_view(),name='menu_bar_app'),
    url(r'^empty-wishlist/$', views.product.EmptyWishlist.as_view(), name='empty-wishlist'),########
    #------New Urls-------#

]