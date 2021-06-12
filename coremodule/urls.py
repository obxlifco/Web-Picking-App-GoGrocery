from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from coremodule import views
from coremodule.views.category import categoryview
from coremodule.views.customer import customerview
from coremodule.views.userlogin import loginview
from coremodule.views.product import productview
from coremodule.views.product import discount
from coremodule.views.cart import cartview
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # Category
    url(r'^category-list/$',views.category.categoryview.CategoryListView.as_view(),name='category-list'),
    url(r'^parent-category-list/$',views.category.categoryview.ParentCategoryListView.as_view(),name='parent-category-list'),
    url(r'^category-list/(?P<pk>\d+)/$', views.category.categoryview.GetCategoryListById.as_view(),name='category-list'),
    url(r'^sub-category-list/(?P<pk>\d+)/$',views.category.categoryview.GetSubCategoryByParent.as_view(),name='sub-category-list'),

    # Product
    url(r'^product/(?P<pk>\d+)/$', views.product.productview.ProductDetailsView.as_view(),name='product'),
    url(r'^product-list/$',views.product.productview.CategoryProductListView.as_view(),name='product-list'),
    url(r'^coss-product/$',views.product.productview.GetCossProduct.as_view(),name='coss-product'),
    url(r'^product-discount/$',views.product.discount.ProductDiscountCalculation.as_view(),name='product-discount'),

    url(r'^add-to-cart/$', views.cart.cartview.add_to_cart.as_view(),name='add-to-cart'),
    url(r'^remove-cart/$', views.cart.cartview.remove_cart.as_view(),name='remove-cart'),

    # Customer
    url(r'^customer-list/$',views.customer.customerview.CustomerListView.as_view(),name='customer-list'),

    # userlogin
    url(r'^user-login/$', views.userlogin.loginview.login,name='user-login'),

    # ++++++++++++++++++++++++++++++++++++++++ Test URLS +++++++++++++
    url(r'^test-class/$', views.product.discount.TestClass.as_view(),name='test-class'),
    url(r'^test-prod/$', views.product.productview.TestProd.as_view(),name='test-prod'),


    # +++++++++++++++++++++++++++++++++++++++ End Test URLS ++++++++++


    # +++++++++++++++++++++++++++++++++++++++sangita++++++++++++++++++

    url(r'^category-tree/(?P<wid>\d+)/$',views.category.categoryview.categorylisting,name='category-tree'),

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    url(r'signup/$', views.userlogin.loginview.signup,name='signup'),
    url(r'^email_verify/(?P<str_code>[-a-zA-Z0-9_]+)/$',views.userlogin.loginview.email_verify,name='email_verify'),
    url(r'^get_Product_detail/(?P<pk>[0-9]+)/$',views.product.productview.get_Product_detail,name="get_Product_detail")
]
