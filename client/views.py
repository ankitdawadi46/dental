# import subprocess
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

# from dateutil.relativedelta import relativedelta
from client.filter import ClientFilter
from client.models import Client, ClinicProfile, Domain, Profile
from client.selectors.factories.client_creation_factory import ClientCreationFactory
from client.selectors.factories.client_support_user import ClientSupportUserFactory
from client.selectors.factories.dashboard_data_factory import DashboardDataFactory
from client.selectors.factories.user_creation_factory import UserCreationFactory
from client.serializers import (
    ClientSerializer,
    ClinicProfileGetSerializer,
    DashboardSerializer,
    DomainSerializer,
)
from dental_app.utils.mixins import PaginationMixin, SearchMixin
from dental_app.utils.pagination import CustomPagination
from dental_app.utils.response import BaseResponse


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


class ClientViewSet(PaginationMixin, ModelViewSet):
    queryset = Client.objects.all().order_by("-id")
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
    filterset_class = ClientFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add SearchFilter
    search_fields = ["name", "email"]  # Adjust fields as per your model

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
                data={"password": password},
                message="Support Client Created Successfully",
            )

        except Client.DoesNotExist:
            return BaseResponse(message="Client not found", status=404)

        except Exception as e:
            return BaseResponse(message=str(e), status=500)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="check-if-user-exists",
    )
    def check_if_user_already_exists(self, request: Request):
        email = request.data.get("email")
        user_profile = (
            Profile.objects.select_related("user").filter(user__email=email).first()
        )

        if user_profile:
            return BaseResponse(
                data={
                    "message": f"The user already exists as {user_profile.profile_type}",
                    "autoredirect": False,
                }
            )
        return BaseResponse(
            data={"message": "The user does not exist", "autoredirect": True}
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        url_path="create-user",
    )
    def create_user(self, request: Request):
        factory = UserCreationFactory()
        try:
            data = request.data
            factory.user_service.validate_profile_type(data)
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
                "nhpc_no": data.get("nhpc_no"),
            }
            clinic_data = {"clinic": data.get("clinic")}
            is_clinic_data = (
                ClinicProfile.objects.select_related("clinic", "user")
                .filter(
                    clinic__id=data.get("clinic"), user__user__email=data.get("email")
                )
                .exists()
            )
            if is_clinic_data:
                return BaseResponse(
                    message="Invalid user data",
                    data={"User already exists"},
                    status=400,
                )
            # Create user and profile
            user = factory.user_service.get_or_create_user(user_data)
            profile_data["user"] = user.id
            profile = factory.profile_service.create_profile(profile_data)

            # Create clinic profile if applicable
            if clinic_data["clinic"]:
                factory.clinic_profile_service.handle_clinic_profile(
                    profile, clinic_data
                )

            return BaseResponse(
                {"message": "User, profile, and clinic profile created successfully"},
                status=201,
            )

        except ValueError as e:
            return BaseResponse(
                {"message": "Invalid data", "errors": str(e)}, status=400
            )

    @action(
        detail=True,
        methods=["PATCH"],
        permission_classes=[AllowAny],
        url_path="update-user",
    )
    def update_user(self, request: Request, pk: int):
        factory = UserCreationFactory()
        try:
            data = request.data
            try:
                user = (
                    ClinicProfile.objects.select_related("user__user")
                    .filter(id=pk)
                    .first()
                    .user.user
                )
            except Exception:
                return BaseResponse(message="Invalid id value", status=400)
            if not user:
                return BaseResponse(message="User not found", status=404)
            # Validate profile type
            factory.user_service.validate_profile_type(data)
            # Update user data
            user_data = {
                "email": data.get("email"),
                "first_name": data.get("first_name"),
                "middle_name": data.get("middle_name"),
                "last_name": data.get("last_name"),
            }
            # user = factory.user_service.get_or_create_user(user_data)
            # Update user data
            user = factory.user_service.update_user(user, user_data)
            # Update profile
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                return BaseResponse(message="Profile not found", status=404)
            profile_data = {
                "photo": data.get("photo"),
                "dob": data.get("dob"),
                "gender": data.get("gender"),
                "profile_type": data.get("profile_type"),
                "designation": data.get("designation"),
                "address": data.get("address"),
                "phone_number": data.get("phone_number"),
                "nmc_no": data.get("nmc_no"),
                "nhpc_no": data.get("nhpc_no"),
            }
            factory.profile_service.update_profile(profile, profile_data)
            # Update clinic profile if applicable
            if data.get("clinic"):
                clinic_data = {"clinic": data.get("clinic")}
                factory.clinic_profile_service.handle_clinic_profile(
                    profile, clinic_data
                )

            return BaseResponse(
                {"message": "User, profile, and clinic profile updated successfully"},
                status=200,
            )

        except ValueError as e:
            return BaseResponse(
                {"message": "Invalid data", "errors": str(e)}, status=400
            )

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("schema_name"):
            return BaseResponse(data={"Cannot update schema name."}, status=400)
        return super().partial_update(request, *args, **kwargs)


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
        return BaseResponse(
            data={"client_id": client.id, "client_name": client.name}, status=200
        )

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


class ClinicProfileViewset(ModelViewSet, SearchMixin, PaginationMixin):
    queryset = ClinicProfile.objects.all()
    serializer_class = ClinicProfileGetSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination  # Use the custom pagination class
    filter_backends = [SearchFilter]  # Enable search functionality
    search_fields = [
        "user__user__email",
        "user__designation",
        "user__phone_number",
    ]  # Define searchable fields

    @action(detail=False, methods=["get"], url_path="users")
    def get_profile_by_type(self, request):
        profile_type = request.query_params.get("profile_type", None)
        clinic = request.query_params.get("clinic")
        if not profile_type:
            return BaseResponse(
                data={"error": "profile_type query parameter is required."}, status=400
            )
        if not clinic:
            return BaseResponse(
                {"error": "clinic query parameter is required."}, status=400
            )

        # Filter queryset
        queryset = (
            self.get_queryset()
            .select_related("user__user", "clinic")
            .filter(user__profile_type=profile_type, clinic__id=clinic)
        )
        # Apply search using the SearchMixin
        search_query = request.query_params.get("search", None)
        queryset = self.apply_search(queryset, search_query)

        # Paginate and serialize using the PaginationMixin
        return self.paginate_and_serialize(queryset, self.get_serializer_class())


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
