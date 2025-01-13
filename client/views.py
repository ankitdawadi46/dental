# import subprocess

# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib.messages.views import SuccessMessageMixin
# from django.utils.crypto import get_random_string
# from django.views.generic import (
#     View,
#     TemplateView,
#     FormView,
#     ListView,
#     CreateView,
#     UpdateView,
#     DeleteView,
#     DetailView,
# )
# from django_tenants.utils import tenant_context
# from django.urls import reverse, reverse_lazy
# from django.contrib import messages
# from django.conf import settings
# from django.contrib.sites.models import Site
# from django.utils import timezone
# from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

# from dateutil.relativedelta import relativedelta
from client.models import Client, CustomUser, Domain, Profile
from client.selectors.factories.client_creation_factory import ClientCreationFactory
from client.selectors.factories.client_support_user import ClientSupportUserFactory
from client.selectors.factories.dashboard_data_factory import DashboardDataFactory
from client.serializers import ClientSerializer, ClinicProfileSerializer, CustomUserSerializer, DashboardSerializer, DomainSerializer, ProfileSerializer
from dental_app.utils.response import BaseResponse

# from .mixins import BaseMixin, CustomLoginRequiredmixin, GetDeleteMixin
# from .forms import LoginForm, ClientForm, DomainForm, UserForm, PaymentForm, InvoiceForm
# from .models import Domain, User, Client, Payment, Invoice, Client
# from .tasks import _send_first_credential_email, send_email
# from .loaddata import (
#     populate_permissions_from_files,
#     populate_public_holidays,
#     populate_services_from_json,
#     populate_office_hrs,
# )

# from braces.views import SuperuserRequiredMixin, AnonymousRequiredMixin

# from tenant_schemas.utils import schema_context

# from audit.models import AuditTrail
# from audit.utils import store_audit
# from audit.mixins import AuditCreateMixin, AuditDeleteMixin, AuditUpdateMixin


class DashboardViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Client.objects.all()
    serializer_class = DashboardSerializer

    # Create a client data selector using the abstract factory
    def get_client_data_selector(self):
        factory = DashboardDataFactory()
        return factory

    @action(detail=False, methods=["get"])
    def dashboard_data(self, request: Request):
        """
        Get the total clients, active clients, and trial clients.
        """
        client_data_selector = self.get_client_data_selector()
        dashboard_data = {
            "card_details": client_data_selector.get_card_details(),
            "payment_pending": client_data_selector.get_payment_pending(),
            "client_data": client_data_selector.get_client_data(),
        }
        return BaseResponse(data=dashboard_data, message="Data retrieved successfully")


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all().order_by("-id")
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            # Step 1: Validate and extract client data from serializer
            client_data = serializer.validated_data
            # Step 2: Use the factory to handle the entire creation flow
            factory = ClientCreationFactory()
            factory.create_client_with_dns_and_user(client_data)
        except Exception as e:
            return BaseResponse(message=str(e), status=500)
            
    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def create_support_client_user(self, request: Request, pk=None):
        try:
            # Get the client by its ID (pk)
            client = Client.objects.get(id=pk)
            
            # Create the support user using the factory
            support_user_factory = ClientSupportUserFactory()
            _, password = support_user_factory.create_support_user(client)

            return BaseResponse(
                data={'password': password},
                message="Support Client Created Successfully")

        except Client.DoesNotExist:
            return BaseResponse(message="Client not found", status=404)

        except Exception as e:
            return BaseResponse(message=str(e), status=500)
        
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path="check-if-user-exists")
    def check_if_user_already_exists(self, request: Request):
        email = request.data.get('email')
        user_profile = Profile.objects.select_related('user').filter(user__email=email).first()

        if user_profile:
            return BaseResponse(
                data={
                    'message': f'The user already exists as {user_profile.profile_type}',
                    'autoredirect': False
                }
            )
        return BaseResponse(
            data={
                'message': "The user does not exist",
                'autoredirect': True
            }
        )
            
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="create-user")
    def create_user(self, request: Request):
        data = request.data
        if data.get('profile_type') == 'Doctor' and not data.get('nmc_no'):
            return BaseResponse(
                message="NMC Number is required for Doctor",
                status=400)
        if data.get("profile_type") == 'Helper' and not data.get('nhpc_no'):
            return BaseResponse(
                message="NHPC Number is required for Helper",
                status=400
            )
        user_data = {
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "middle_name": data.get("middle_name"),
            "last_name": data.get("last_name"),
        }
        profile_data = {
            "photo": data.get("photo"),
            "dob": data.get("dob"),
            "gender": data.get("gender"),
            "profile_type": data.get("profile_type"),
            "designation": data.get("designation"),
            "address": data.get("address"),
            "phone_number": data.get("phone_number"),
            "nmc_no": data.get("nmc_no"),
            "nhpc_no": data.get("nhpc_no")
        }
        clinic_profile_data = {
            "clinic": data.get("clinic")
        }
        user_serializer = CustomUserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return BaseResponse(
                data={"message": "Invalid user data", "errors": user_serializer.errors},
                status=400
            )
        user = user_serializer.save()
        
        profile_data['user'] = user.id
        profile_serializer = ProfileSerializer(data=profile_data)
        if not profile_serializer.is_valid():
            return BaseResponse(
                data={"message": "Invalid profile data", "errors": profile_serializer.errors},
                status=400
            )
        profile = profile_serializer.save()
        
        # Validate and create ClinicProfile (if applicable)
        if clinic_profile_data.get('clinic'):
            clinic_profile_data['user'] = profile.id
            clinic_profile_serializer = ClinicProfileSerializer(data=clinic_profile_data)
            if not clinic_profile_serializer.is_valid():
                return BaseResponse(
                    data={"message": "Invalid clinic profile data", "errors": clinic_profile_serializer.errors},
                    status=400
                )
            clinic_profile_serializer.save()

        return BaseResponse(
            {"message": "User, profile, and clinic profile created successfully"},
            status=201
        )
        
class DomainViewSet(ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def get_queryset(self):
        """
        Filter domains by client ID passed in the URL.
        """
        client_pk = self.kwargs.get("client")
        client = get_object_or_404(Client, id=client_pk)
        return self.queryset.filter(tenant=client).order_by("-id")

    def perform_create(self, serializer):
        """
        Set the tenant and additional attributes during creation.
        """
        client_pk = self.kwargs.get("client")
        client = get_object_or_404(Client, id=client_pk)
        serializer.save(tenant=client, is_primary=False)

    @action(detail=False, methods=["get"], url_path="list-domains")
    def list_domains(self, request):
        """
        Custom action to list domains for a specific client.
        """
        domains = self.get_queryset()
        serializer = self.get_serializer(domains, many=True)
        return BaseResponse(data=serializer.data, status=200)

    @action(detail=False, methods=["get"], url_path="get-client-info")
    def get_client_info(self, request):
        """
        Custom action to get client information.
        """
        client_pk = self.kwargs.get("client")
        client = get_object_or_404(Client, id=client_pk)
        return BaseResponse(data={"client_id": client.id, "client_name": client.name}, status=200)

    def perform_update(self, serializer):
        """
        Handle updates for a domain.
        """
        domain = self.get_object()
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Handle domain deletion with success message.
        """
        domain = self.get_object()
        domain.delete()
        return BaseResponse(data={"message": "Domain Deleted Successfully"}, status=200)
        
        


# class AuditTrailListView(ListAPIView):
#     queryset = AuditTrail.objects.all().order_by('-created_at')
#     serializer_class = AuditTrailSerializer
#     permission_classes = [IsSuperUser]  # Use the custom permission
#     pagination_class = AuditTrailPagination


# class GitPullView(SuperuserRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         process = subprocess.Popen(
#             ["./pull.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
#         )
#         returncode = process.wait()
#         output = ""
#         output += process.stdout.read().decode("utf-8")
#         output += "\nReturned with status {0}".format(returncode)
#         response = HttpResponse(output)
#         response["Content-Type"] = "text"
#         return response


# class AuditTrailListView(SuperuserRequiredMixin, ListView):
#     model = AuditTrail
#     paginate_by = 100
#     template_name = "dashboard/audittrails/list.html"

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.order_by("-created_at")


# # Login Logout Views
# class LoginPageView(AnonymousRequiredMixin, FormView):
#     form_class = LoginForm
#     template_name = "dashboard/auth/login.html"

#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(username=username, password=password)

#         # Remember me
#         if self.request.POST.get("remember", None) == None:
#             self.request.session.set_expiry(0)

#         login(self.request, user)
#         store_audit(request=self.request, instance=self.request.user, action="LOGIN")

#         if "next" in self.request.GET:
#             return redirect(self.request.GET.get("next"))
#         return redirect("dashboard:index")


# class LogoutView(View):
#     def get(self, request, *args, **kwargs):
#         store_audit(request=self.request, instance=self.request.user, action="LOGOUT")
#         logout(request)
#         return redirect("dashboard:login")


# #############################################################################################
# # Client CRUD
# #############################################################################################
# class ClientListView(SuperuserRequiredMixin, ListView):
#     model = Client
#     template_name = "dashboard/clients/list.html"
#     paginate_by = 100

#     def get_queryset(self):
#         return super().get_queryset().order_by("-id")


# from django.contrib.auth.models import Group


# class ClientUserCreateView(SuperuserRequiredMixin, View):
#     success_url = reverse_lazy("dashboard:clients-list")

#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs["pk"]
#         client = Client.objects.get(id=pk)
#         with tenant_context(client):
#             hijacked_support_username = client.hijack_superuser_username
#             obj, _ = User.objects.get_or_create(
#                 username=hijacked_support_username,
#                 email=hijacked_support_username,
#                 first_name="RXPIN",
#                 last_name="SUPPORT",
#             )
#             grp, _ = Group.objects.get_or_create(name="SuperAdmin")
#             obj.is_superuser = True
#             obj.groups.add(grp)
#             obj.is_staff = True
#             obj.save()
#             password = get_random_string(20)
#             obj.set_password(password)
#             obj.save()
#             # support_staff, created = Group.objects.get_or_create(name="Support Staff")
#             # obj.groups.add(support_staff)
#             messages.info(request, password, extra_tags="is your new password")
#         return redirect(self.success_url)


# class ClientCreateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView
# ):
#     form_class = ClientForm
#     success_message = "Client Created Successfully"
#     success_url = reverse_lazy("dashboard:clients-list")
#     template_name = "dashboard/clients/form.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         is_staging = getattr(settings, "IS_STAGING", False)
#         context["is_staging"] = is_staging
#         return context

#     def credential_email_context(self, obj, password, name, domain):
#         host_domain = self.request.get_host()
#         if "localhost" in host_domain:
#             login_url = "http://{}:8000/login/".format(domain)
#         else:
#             login_url = "https://{}/login/".format(domain)
#         template_context = {
#             "username": obj.username,
#             "password": password,
#             "domain_name": domain,
#             "name": name,
#             "login_url": login_url,
#         }
#         return template_context

#     def form_valid(self, form):
#         self.object = form.save()
#         clientObj = self.object
#         domain = Domain()
#         domain_host = self.request.get_host()
#         if "localhost" in domain_host:
#             domain.domain = "{}.localhost".format(form.cleaned_data.get("schema_name"))
#         else:
#             domain.domain = clientObj.primary_domain_name
#         domain.tenant = clientObj
#         domain.is_primary = True
#         domain.save()

#         token = getattr(settings, "RXPIN_WEB_TOKEN", None)
#         if token:
#             try:
#                 # The hardcoding here needs to be moved to settings
#                 cf = CloudFlare.CloudFlare(token=token)

#                 zone_id = "5699aeb4df96d00ea3bdfb842cc9fef7"
#                 zone_id = getattr(settings, "ZONE_ID", zone_id)
#                 pointing_ip = getattr(
#                     settings, "SERVER_IP_ADDRESS_POINT", "13.126.24.110"
#                 )
#                 dns_record = {
#                     "name": clientObj.primary_domain_name,
#                     "type": "A",
#                     "content": pointing_ip,
#                     "proxied": True,
#                 }
#                 r = cf.zones.dns_records.post(zone_id, data=dns_record)
#             except:
#                 _ = ""
#         email = form.cleaned_data.get("email")
#         if email not in ["", None]:
#             client = Client.objects.get(id=self.object.id)
#             contact_person = form.cleaned_data.get("contact_person")
#             email_person = (
#                 contact_person if contact_person else form.cleaned_data.get("name")
#             )
#             password = get_random_string(10)

#             domain_name = domain.domain
#             obj = self.create_first_client_user(email, password, client, domain_name)
#             template_context = self.credential_email_context(
#                 obj, password, email_person, domain_name
#             )
#             print(template_context)
#             welcome_template_context = {"name": email_person}
#             try:
#                 _send_first_credential_email(template_context, email)
#             except:
#                 _send_first_credential_email(template_context, email)
#         return super().form_valid(form)

#     # create user for client while creating client
#     def create_first_client_user(self, email, password, client, domain):
#         with tenant_context(client):
#             obj, created = User.objects.get_or_create(username=email, email=email)
#             obj.is_superuser = False
#             obj.is_staff = False
#             obj.save()
#             obj.set_password(password)
#             obj.save()

#             if not Group.objects.filter(name="SuperAdmin").exists():
#                 populate_permissions_from_files()

#             superadmin = Group.objects.get(name="SuperAdmin")
#             obj.groups.add(superadmin)

#             site, _ = Site.objects.get_or_create(id=1)
#             site.domain = domain
#             site.name = domain
#             site.save()
#         return obj


# class ClientUpdateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView
# ):
#     form_class = ClientForm
#     model = Client
#     success_message = "Client Updated Successfully"
#     success_url = reverse_lazy("dashboard:clients-list")
#     template_name = "dashboard/clients/form.html"


# class ClientDeleteView(
#     SuperuserRequiredMixin,
#     SuccessMessageMixin,
#     GetDeleteMixin,
#     AuditDeleteMixin,
#     DeleteView,
# ):
#     model = Client
#     success_message = "Client Deleted Successfully"
#     success_url = reverse_lazy("dashboard:clients-list")


# class ClientDNSUpdateCloudflareView(SuperuserRequiredMixin, View):
#     success_url = reverse_lazy("dashboard:clients-list")

#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs["pk"]
#         client_domain = Domain.objects.get(id=pk)
#         token = getattr(settings, "RXPIN_WEB_TOKEN", None)
#         if not client_domain.zone_id:
#             messages.error(
#                 request, " ", extra_tags="Please Add the Domain to CloudFlare First!"
#             )
#         else:
#             if token:
#                 try:
#                     primary_domain = client_domain.tenant.domains.filter(
#                         is_primary=True
#                     ).first()
#                     cf = CloudFlare.CloudFlare(token=token)
#                     zone_id = client_domain.zone_id
#                     dns_record = {
#                         "name": client_domain.domain,
#                         "type": "CNAME",
#                         "content": primary_domain.domain,
#                         "proxied": True,
#                     }
#                     r = cf.zones.dns_records.post(zone_id, data=dns_record)
#                     dns_record = {
#                         "name": "www." + client_domain.domain,
#                         "type": "CNAME",
#                         "content": primary_domain.domain,
#                         "proxied": True,
#                     }
#                     r = cf.zones.dns_records.post(zone_id, data=dns_record)
#                     messages.success(request, "Records Created Successfully")
#                 except Exception as e:
#                     messages.error(request, " ", extra_tags=str(e))

#         return redirect(request.META.get("HTTP_REFERER"))


# class ClientDomainCloudflareZoneCreateView(SuperuserRequiredMixin, View):
#     success_url = reverse_lazy("dashboard:clients-list")

#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs["pk"]
#         client_domain = Domain.objects.get(id=pk)
#         token = getattr(settings, "RXPIN_WEB_TOKEN", None)
#         if token:
#             try:
#                 primary_domain = client_domain.tenant.domains.filter(
#                     is_primary=True
#                 ).first()
#                 cf = CloudFlare.CloudFlare(token=token)
#                 resp = cf.zones.post(data={"name": client_domain.domain})
#                 client_domain.ns_records = resp["name_servers"]
#                 client_domain.zone_id = resp["id"]
#                 client_domain.save()

#                 dns_records = client_domain.ns_records
#                 to_send = "<br/>".join(dns_records)
#                 to_send = "<code>%s</code>" % to_send
#                 messages.info(
#                     request, to_send, extra_tags="Please Set theses as the DNS Records"
#                 )

#             except Exception as e:
#                 if client_domain.ns_records:
#                     dns_records = client_domain.ns_records
#                     to_send = "<br/>".join(dns_records)
#                     to_send = "<code>%s</code>" % to_send
#                     messages.info(
#                         request,
#                         to_send,
#                         extra_tags="Please Set theses as the DNS Records",
#                     )
#                 else:
#                     messages.error(request, " ", extra_tags=str(e))

#         return redirect(request.META.get("HTTP_REFERER"))


# class ClientDataPopulate(SuperuserRequiredMixin, CustomLoginRequiredmixin, DetailView):
#     success_url = reverse_lazy("dashboard:clients-list")
#     model = Client

#     def set_pk_none(self, object):
#         object.pk = None
#         return object

#     def post(self, request, *args, **kwargs):
#         company = self.get_object()
#         print(company.schema_name)
#         print(self.request.POST)
#         # schema from where data are coping
#         if self.request.POST.get("group"):
#             print("Loading initial data")
#             with schema_context(company.schema_name):
#                 populate_permissions_from_files()

#         if self.request.POST.get("holidays"):
#             print("Loading holidays data")
#             with schema_context(company.schema_name):
#                 holiday_type = request.POST.get("calendar_type")
#                 populate_public_holidays(holiday_type)

#         if self.request.POST.get("service"):
#             print("Loading Service Data")
#             with schema_context(company.schema_name):
#                 service_file = request.FILES.get("service_file")
#                 print(service_file)
#                 populate_services_from_json(service_file)

#         if self.request.POST.get("office_hrs"):
#             print("Loading Office Hours")
#             with schema_context(company.schema_name):
#                 start_time = request.POST.get("start_time")
#                 end_time = request.POST.get("end_time")
#                 populate_office_hrs(start_time, end_time)

#         messages.success(self.request, "Data populated successfully.")
#         return redirect(self.success_url)


# #############################################################################################
# # Domain CRUD
# #############################################################################################


# class DomainListView(SuperuserRequiredMixin, ListView):
#     model = Domain
#     template_name = "dashboard/domains/list.html"
#     paginate_by = 100

#     def get_queryset(self):
#         client_pk = self.kwargs["client"]
#         client = get_object_or_404(Client, id=client_pk)
#         return super().get_queryset().filter(tenant=client).order_by("-id")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         client_pk = self.kwargs["client"]
#         client = get_object_or_404(Client, id=client_pk)
#         context["client"] = client
#         return context


# class DomainCreateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView
# ):
#     form_class = DomainForm
#     success_message = "Domain Created Successfully"
#     template_name = "dashboard/domains/form.html"

#     def get_success_url(self):
#         client_pk = self.kwargs["client"]
#         return reverse_lazy("dashboard:domains-list", kwargs={"client": client_pk})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         client_pk = self.kwargs["client"]
#         client = get_object_or_404(Client, id=client_pk)
#         context["client"] = client
#         return context

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         domain_obj = self.object
#         client_pk = self.kwargs["client"]
#         client = get_object_or_404(Client, id=client_pk)
#         domain_obj.tenant = client
#         domain_obj.is_primary = False
#         domain_obj.save()
#         return HttpResponseRedirect(self.get_success_url())


# class DomainUpdateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView
# ):
#     form_class = DomainForm
#     model = Domain
#     success_message = "Domain Updated Successfully"
#     template_name = "dashboard/domains/form.html"

#     def get_success_url(self):
#         obj = self.get_object()
#         return reverse_lazy("dashboard:domains-list", kwargs={"client": obj.tenant.id})


# class DomainDeleteView(
#     SuperuserRequiredMixin,
#     SuccessMessageMixin,
#     GetDeleteMixin,
#     AuditDeleteMixin,
#     DeleteView,
# ):
#     model = Domain
#     success_message = "Domain Deleted Successfully"

#     def get_success_url(self):
#         obj = self.get_object()
#         return reverse_lazy("dashboard:domains-list", kwargs={"client": obj.tenant.id})


# #############################################################################################
# # Users CRUD
# #############################################################################################


# class UserListView(SuperuserRequiredMixin, ListView):
#     model = User
#     template_name = "dashboard/users/list.html"
#     paginate_by = 100

#     def get_queryset(self):
#         return super().get_queryset().exclude(username=self.request.user)


# class UserCreateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView
# ):
#     form_class = UserForm
#     success_message = "User Created Successfully"
#     success_url = reverse_lazy("dashboard:users-list")
#     template_name = "dashboard/users/form.html"

#     def get_success_url(self):
#         return reverse("dashboard:users-password-reset", kwargs={"pk": self.object.pk})


# class UserUpdateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView
# ):
#     form_class = UserForm
#     model = User
#     success_message = "User Updated Successfully"
#     success_url = reverse_lazy("dashboard:users-list")
#     template_name = "dashboard/users/form.html"


# class UserStatusView(SuperuserRequiredMixin, SuccessMessageMixin, View):
#     model = User
#     success_message = "User's Status Has Been Changed"
#     success_url = reverse_lazy("dashboard:users-list")

#     def get(self, request, *args, **kwargs):
#         user_id = self.kwargs.get("pk")
#         if user_id:
#             account = User.objects.filter(pk=user_id).first()
#             if account.is_active == True:
#                 account.is_active = False
#             else:
#                 account.is_active = True
#             account.save(update_fields=["is_active"])
#         return redirect(self.success_url)


# class UserPasswordResetView(SuperuserRequiredMixin, SuccessMessageMixin, View):
#     model = User
#     success_url = reverse_lazy("dashboard:users-list")
#     success_message = "Password has been sent to the user's email."

#     def get(self, request, *args, **kwargs):
#         user_pk = self.kwargs.get("pk")
#         account = User.objects.filter(pk=user_pk).first()
#         password = get_random_string(length=6)
#         account.set_password(password)
#         account.save(update_fields=["password"])

#         template_context = {
#             "username": account.username,
#             "password": password,
#         }
#         send_email(
#             subject="Dashboard Credentials",
#             template_path="dashboard/email/password_reset_email.html",
#             template_context=template_context,
#             receiver=account.email,
#             body=(
#                 "You can log in to the Dashboard with the following credentials:\n\n"
#                 f"Username: {account.username}\nPassword: {password}"
#             ),
#         )
#         messages.success(self.request, self.success_message)
#         return redirect(self.success_url)


# #############################################################################################
# # Payment CRUD
# #############################################################################################
# class PaymentListView(SuperuserRequiredMixin, ListView):
#     model = Payment
#     template_name = "dashboard/payments/list.html"
#     paginate_by = 100

#     def get_queryset(self):
#         return super().get_queryset().order_by("-id")


# class PaymentCreateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView
# ):
#     form_class = PaymentForm
#     success_message = "Client Created Successfully"
#     success_url = reverse_lazy("dashboard:payments-list")
#     template_name = "dashboard/payments/form.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         self.object = form.save()
#         return super().form_valid(form)


# class PaymentUpdateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView
# ):
#     form_class = PaymentForm
#     model = Payment
#     success_message = "Payment Updated Successfully"
#     success_url = reverse_lazy("dashboard:payments-list")
#     template_name = "dashboard/payments/form.html"


# class PaymentDeleteView(
#     SuperuserRequiredMixin,
#     SuccessMessageMixin,
#     GetDeleteMixin,
#     AuditDeleteMixin,
#     DeleteView,
# ):
#     model = Payment
#     success_message = "Payment Deleted Successfully"
#     success_url = reverse_lazy("dashboard:payments-list")


# #############################################################################################
# # Invlice CRUD
# #############################################################################################


# class InvoiceListView(SuperuserRequiredMixin, ListView):
#     model = Invoice
#     template_name = "dashboard/invoices/list.html"
#     paginate_by = 100

#     def get_queryset(self):
#         return super().get_queryset().order_by("-id")


# class InvoiceCreateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView
# ):
#     form_class = InvoiceForm
#     success_message = "Invoice Created Successfully"
#     success_url = reverse_lazy("dashboard:invoices-list")
#     template_name = "dashboard/invoices/form.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         self.object = form.save()
#         return super().form_valid(form)


# class InvoiceUpdateView(
#     SuperuserRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView
# ):
#     form_class = InvoiceForm
#     model = Invoice
#     success_message = "Invoice Updated Successfully"
#     success_url = reverse_lazy("dashboard:invoices-list")
#     template_name = "dashboard/invoices/form.html"


# class InvoiceDeleteView(
#     SuperuserRequiredMixin,
#     SuccessMessageMixin,
#     GetDeleteMixin,
#     AuditDeleteMixin,
#     DeleteView,
# ):
#     model = Invoice
#     success_message = "Invoice Deleted Successfully"
#     success_url = reverse_lazy("dashboard:invoices-list")
