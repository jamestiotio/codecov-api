from django_filters import rest_framework as django_filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, mixins, viewsets

from api.public.v2.schema import owner_username_parameter, service_parameter
from api.shared.repo.filter import RepositoryFilters
from api.shared.repo.mixins import RepositoryViewSetMixin
from core.models import Repository

from .serializers import RepoSerializer


@extend_schema(
    parameters=[
        service_parameter,
        owner_username_parameter,
    ],
    tags=["Repos"],
)
class RepositoryViewSet(
    RepositoryViewSetMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = RepositoryFilters
    search_fields = ("name",)
    ordering_fields = (
        "updatestamp",
        "name",
    )
    serializer_class = RepoSerializer
    queryset = Repository.objects.none()

    @extend_schema(summary="Repository list")
    def list(self, request, *args, **kwargs):
        """
        Returns a paginated list of repositories for the specified provider service and owner username

        Optionally filterable by:
        * a list of repository `name`s
        * a `search` term which matches against the name
        * whether the repository is `active` or not
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Repository detail",
        parameters=[
            OpenApiParameter(
                "repo_name",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                description="repository name",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Returns a single repository by name
        """
        return super().retrieve(request, *args, **kwargs)
