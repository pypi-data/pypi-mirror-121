from typing import Optional

from data_engineering_pulumi_components.aws.glue_job import GlueComponent
from data_engineering_pulumi_components.aws import (
    BucketPutPermissionsArgs,
    CopyObjectFunction,
    CuratedBucket,
    RawHistoryBucket,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ComponentResource, ResourceOptions
from pulumi_aws import Provider
from pulumi_aws.glue import CatalogDatabase


class RawHistoryToCuratedPipeline(ComponentResource):
    def __init__(
        self,
        name: str,
        raw_history_bucket: RawHistoryBucket,
        tagger: Tagger,
        add_tables_to_db: bool = False,
        test_trigger: bool = False,
        provider: Optional[Provider] = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            t=(
                "data-engineering-pulumi-components:pipelines:"
                "RawHistoryToCuratedPipeline"
            ),
            name=name,
            props=None,
            opts=opts,
        )
        self._curatedBucket = CuratedBucket(
            name=name,
            tagger=tagger,
            opts=ResourceOptions(parent=self, provider=provider),
        )
        if not add_tables_to_db:
            self._copyObjectFunction = CopyObjectFunction(
                destination_bucket=self._curatedBucket,
                name=name,
                source_bucket=raw_history_bucket,
                tagger=tagger,
                opts=ResourceOptions(parent=self),
            )

            self._curatedBucket.add_put_permissions(
                put_permissions=[
                    BucketPutPermissionsArgs(
                        principal=self._copyObjectFunction._role.arn
                    )
                ],
            )
        else:
            db_name = name.replace("-", "_")
            self._database = CatalogDatabase(
                resource_name=f"{name}-database",
                description=f"A Glue Database for tables from {name}",
                name=f"{db_name}",
                opts=ResourceOptions(provider=provider),
            )
            self._glueMoveJob = GlueComponent(
                destination_bucket=self._curatedBucket,
                name=name,
                source_bucket=raw_history_bucket,
                tagger=tagger,
                test_trigger=test_trigger,
                glue_script=(
                    "data_engineering_pulumi_components/aws/glue_move_script.py"
                ),
                glue_inputs={
                    "--source_bucket": raw_history_bucket._name,
                    "--destination_bucket": self._curatedBucket._name,
                    "--database_name": db_name,
                },
                provider=provider,
                opts=ResourceOptions(
                    parent=self,
                    depends_on=[self._curatedBucket],
                ),
            )

            raw_history_bucket.add_put_permissions(
                put_permissions=[
                    BucketPutPermissionsArgs(principal=self._glueMoveJob._role.arn)
                ],
                glue_permissions=True,
            )

            self._curatedBucket.add_put_permissions(
                put_permissions=[
                    BucketPutPermissionsArgs(principal=self._glueMoveJob._role.arn)
                ],
                glue_permissions=True,
            )
