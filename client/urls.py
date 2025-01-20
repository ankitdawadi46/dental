from rest_framework.routers import DefaultRouter

from . import views

app_name = "dashboard"

router = DefaultRouter()

router.register(r"dashboard", views.DashboardViewSet, "dashboard")
router.register(r"clients", views.ClientViewSet, "clients")
router.register(r"clinic-profile", views.ClinicProfileViewset, "client-profile")

urlpatterns = [
    # path("", views.DashboardView.as_view(), name="index"),
    # # git-pull
    # path("git-pull", views.GitPullView.as_view(), name="git-pull"),
    # # audit-trail
    # path("audits", views.AuditTrailListView.as_view(), name="audittrail-list"),
    # # accounts
    # path("accounts/login/", views.LoginPageView.as_view(), name="login"),
    # path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
    # # Clients crud
    # path("clients/", views.ClientListView.as_view(), name="clients-list"),
    # path("clients/create/", views.ClientCreateView.as_view(), name="clients-create"),
    # path(
    #     "clients/user/<int:pk>/create",
    #     views.ClientUserCreateView.as_view(),
    #     name="clients-user-create",
    # ),
    # path(
    #     "clients/<int:pk>/update",
    #     views.ClientUpdateView.as_view(),
    #     name="clients-update",
    # ),
    # path(
    #     "clients/<int:pk>/delete",
    #     views.ClientDeleteView.as_view(),
    #     name="clients-delete",
    # ),
    # re_path(
    #     r"^clients/(?P<pk>\d+)/populate$",
    #     views.ClientDataPopulate.as_view(),
    #     name="clients-populate-data",
    # ),
    # # domain CRUD
    # path("domains/<int:client>/", views.DomainListView.as_view(), name="domains-list"),
    # path(
    #     "domains/create/<int:client>/",
    #     views.DomainCreateView.as_view(),
    #     name="domains-create",
    # ),
    # path(
    #     "domains/create-cloudflare/<int:pk>/",
    #     views.ClientDomainCloudflareZoneCreateView.as_view(),
    #     name="domains-create-cloudflare-record",
    # ),
    # path(
    #     "domains/create-dns-cloudflare/<int:pk>/",
    #     views.ClientDNSUpdateCloudflareView.as_view(),
    #     name="domains-create-dns-cf-record",
    # ),
    # path(
    #     "domains/<int:pk>/update",
    #     views.DomainUpdateView.as_view(),
    #     name="domains-update",
    # ),
    # path(
    #     "domains/<int:pk>/delete",
    #     views.DomainDeleteView.as_view(),
    #     name="domains-delete",
    # ),
    # # user crud
    # path("users/", views.UserListView.as_view(), name="users-list"),
    # path("users/create", views.UserCreateView.as_view(), name="users-create"),
    # path("users/<int:pk>/update", views.UserUpdateView.as_view(), name="users-update"),
    # path("users/<int:pk>/status", views.UserStatusView.as_view(), name="users-status"),
    # path(
    #     "users/<int:pk>/password-reset",
    #     views.UserPasswordResetView.as_view(),
    #     name="users-password-reset",
    # ),
    # # payment crud
    # path("payments/", views.PaymentListView.as_view(), name="payments-list"),
    # path("payments/create/", views.PaymentCreateView.as_view(), name="payments-create"),
    # path(
    #     "payments/<int:pk>/update",
    #     views.PaymentUpdateView.as_view(),
    #     name="payments-update",
    # ),
    # path(
    #     "payments/<int:pk>/delete",
    #     views.PaymentDeleteView.as_view(),
    #     name="payments-delete",
    # ),
    # # Invoices crud
    # path("invoices/", views.InvoiceListView.as_view(), name="invoices-list"),
    # path("invoices/create/", views.InvoiceCreateView.as_view(), name="invoices-create"),
    # path(
    #     "invoices/<int:pk>/update",
    #     views.InvoiceUpdateView.as_view(),
    #     name="invoices-update",
    # ),
    # path(
    #     "invoices/<int:pk>/delete",
    #     views.InvoiceDeleteView.as_view(),
    #     name="invoices-delete",
    # ),
]

urlpatterns = router.urls
