
from django.urls import path
from . import views  # Make sure to import views from the correct app

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('generate/otp/', views.generate_otp, name='generate_otp'),
    path('login/password/', views.login_with_password, name='login_with_password'),
    path('login/send-otp/', views.send_otp, name='send_otp'),
    path('login/otp/', views.login_with_otp, name='login_with_otp'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('searchproducts/', views.product_search, name='product_search'),
    path('filter/products', views.filter_products, name='filter_products'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('viewcartitems/', views.display_cart, name='display_cart'),
    path('removecart/', views.remove_cart_item, name='remove_cart_item'),
    path('add_review/<int:product_id>/', views.add_review, name= 'add_review'),
    path('add_category', views.add_category, name='add_category'),
    path('view_category', views.view_categories, name='view_categories'),
    path('view_product', views.view_products, name='view_products'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_brand', views.add_brand, name='add_brand'),
    path('view_brand', views.view_brand, name='view_brand'),
    path('edit_brand/<int:brand_id>/',views.edit_brand, name='edit_brand'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    # path('add_product', views.add_product, name='add_product'),
    path('view_products', views.view_products, name='view_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_vendor', views.add_vendor, name='add_vendor'),
    path('view_vendors', views.view_vendors, name='view_vendors'),
    path('edit_vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('delete_vendor/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
    path('add_coupon', views.add_coupon, name='add_coupon'),
    path('view_coupons', views.view_coupons, name='view_coupons'),
    path('edit_coupons/<int:coupon_id>/', views.edit_coupons, name='edit_coupons'),
    path('delete_coupons/<int:coupon_id>/', views.delete_coupons, name='delete_coupons'),
    path('add_plan', views.add_plan, name='add_plan'),
    path('view_plans', views.view_plans, name='view_plans'),
    path('edit_plan/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('delete_plan/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('search_products', views.search_products, name='search_products'),
    path('promote_product', views.promote_product, name='promote_product'),
    path('view_promoted_products', views.view_promoted_products, name='view_promoted_products'),
    path('remove_promoted_product', views.remove_promoted_product, name='remove_promoted_product'),
    path('search_brands', views.search_brands, name='search_brands'),
    path('promote_brand', views.promote_brand, name='promote_brand'),
    path('view_promoted_brands', views.view_promoted_brands, name='view_promoted_brands'),
    path('remove_promoted_brand', views.remove_promoted_brand, name='remove_promoted_brand'),
    path('add_subscriber', views.add_subscriber, name='add_subscriber'),
    path('view_subscribers', views.view_subscribers, name='view_subscribers'),
    path('edit_vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('view_users/', views.view_users, name='view_users'),
    path('add_service', views.add_service, name='add_service'),
    path('view_services', views.view_services, name='view_services'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('UserLogin', views.UserLogin, name='UserLogin'),
    path('VendorLogin', views.VendorLogin, name='VendorLogin')


]




