from django.urls import path
from . import views 

app_name = 'trip'
urlpatterns = [
    path('mypage', views.mypage, name='mypage'),#마이페이지 url by 준경
    path('charts/', views.charts, name='charts'),
    
    
    # 관리자 페이지 관련 urlpatterns by 영환
    path("admin_page/", views.admin_page, name="admin_page"),
    path("admin_page/create_product", views.create_product, name="create_product"),
    path("admin_page/product_management", views.product_management, name="product_management"),
    path("admin_page/deleted_product", views.deleted_product, name="deleted_product"),
    path("admin_page/order_inquiry", views.order_inquiry, name="order_inquiry"),
    path("admin_page/delivery_tracking", views.delivery_tracking, name="delivery_tracking"),
    path("admin_page/return_management", views.return_management, name="return_management"),
    path("admin_page/report_detail", views.report_detail, name="report_detail"),
    path("admin_page/user_management", views.user_management, name="user_management"),
    path("admin_page/blacklist_management", views.blacklist_management, name="blacklist_management"),
    # 관리자 페이지 관련 urlpatterns 종료

    #by 건영
    path('',views.index, name = "index"),
    path('about/',views.about, name='about'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact, name='contact'),
    path('elements/',views.elements, name='elements'),
    path('main/',views.main, name='main'),
    path('packages/',views.packages, name='packages'),
    path('single_blog/',views.single_blog, name='single_blog'),
    path('comment/', views.comment,  name='comment'),  #댓글

]