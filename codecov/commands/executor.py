from codecov_auth.commands.owner import OwnerCommands
from codecov_auth.models import Owner
from compare.commands.compare import CompareCommands
from core.commands.branch import BranchCommands
from core.commands.commit import CommitCommands
from core.commands.flag import FlagCommands
from core.commands.pull import PullCommands
from core.commands.repository import RepositoryCommands
from core.commands.upload import UploadCommands
from utils.services import get_long_service_name

mapping = {
    "commit": CommitCommands,
    "owner": OwnerCommands,
    "repository": RepositoryCommands,
    "branch": BranchCommands,
    "compare": CompareCommands,
    "pull": PullCommands,
    "upload": UploadCommands,
    "flag": FlagCommands,
}


class Executor:
    def __init__(self, current_owner: Owner, service: str):
        self.current_owner = current_owner
        self.service = service

    def get_command(self, namespace):
        KlassCommand = mapping[namespace]
        return KlassCommand(self.current_owner, self.service)


def get_executor_from_request(request):
    service_in_url = request.resolver_match.kwargs["service"]
    return Executor(
        current_owner=request.current_owner,
        service=get_long_service_name(service_in_url),
    )


def get_executor_from_command(command):
    return Executor(
        current_owner=command.current_owner,
        service=command.service,
    )
