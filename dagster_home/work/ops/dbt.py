### create these ops myself because I want to pass
## model selection to run.
from dagster import In, Nothing, Out, Output, graph, op
from dagster_dbt import dbt_docs_generate_op
from dagster_dbt.types import DbtOutput
from dagster_dbt.utils import generate_materializations


def make_run_models(modeltag: str, materializations=True):
    if modeltag is None:
        raise ValueError('provide a selector like "tag:value", or use the dbt_run_op.')

    @op(
        required_resource_keys={"dbt"},
        ins={"start_after": In(Nothing)},
        out=Out(DbtOutput, description="Parsed output from running the dbt command."),
        tags={"kind": "dbt"},
    )
    def run_dbt_model(context):
        context.log.info(f"dbt run for selector  {modeltag}")
        dbt_output = context.resources.dbt.run(models=[modeltag])
        context.log.debug(f"dbtoutput: {dbt_output}")
        if materializations and "results" in dbt_output.result:
            yield from generate_materializations(dbt_output, asset_key_prefix=["dbt"])
        yield Output(dbt_output)

    return run_dbt_model


def make_test_models(modeltag: str, materializations=True):
    if modeltag is None:
        raise ValueError('provide a selector like "tag:value", or use the dbt_test_op.')

    @op(
        required_resource_keys={"dbt"},
        ins={"start_after": In(Nothing)},
        out=Out(DbtOutput, description="Parsed output from running the dbt command."),
        tags={"kind": "dbt"},
    )
    def test_dbt_model(context):
        context.log.info(f"dbt test for selector {modeltag}")
        return context.resources.dbt.test(models=[modeltag])

    return test_dbt_model


def make_run_test_custom(modeltag, materializations=True):
    if modeltag is None:
        raise ValueError('provide a selector like "tag:value"')
    run_op = make_run_models(modeltag, materializations=materializations)
    test_op = make_test_models(modeltag, materializations=materializations)

    @graph(
        description=f"""run-test-docs generate for {modeltag}.

    Run dbt run --select {modeltag}, followed by
    dbt test --select {modeltag} followed by
    dbt docs generate.
    Materializations is set to {materializations}
    """
    )
    def run_test_custom():
        dbt_docs_generate_op(start_after=test_op(start_after=run_op()))

    return run_test_custom
