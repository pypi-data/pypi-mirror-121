from typing import Dict, List, Union

import click
from levo_commons import events
from levo_commons.models import (
    AfterTestExecutionPayload,
    AfterTestSuiteExecutionPayload,
    BeforeTestExecutionPayload,
    BeforeTestSuiteExecutionPayload,
    FinishedPayload,
    Status,
    TestResult,
)

from ....handlers import EventHandler
from ....logger import get_logger
from ..context import ExecutionContext, TestSuiteExecutionContext

log = get_logger(__name__)


def handle_before_execution(
    context: ExecutionContext,
    event: events.BeforeTestCaseExecution[BeforeTestExecutionPayload],
) -> None:
    # Test case id here isn't ideal so we need to find what's better.
    suite_context = context.test_suite_id_to_context[event.payload.test_suite_id]
    if event.payload.recursion_level > 0:
        # This value is not `None` - the value is set in runtime before this line
        suite_context.operations_processed += 1  # type: ignore


def handle_after_execution(
    context: ExecutionContext,
    event: events.AfterTestCaseExecution[AfterTestExecutionPayload],
) -> None:
    suite_context = context.test_suite_id_to_context[event.payload.test_suite_id]
    suite_context.operations_processed += 1
    suite_context.results.append(event.payload.result)

    if event.payload.status == Status.error:
        suite_context.errored_count += 1
    elif event.payload.status == Status.failure:
        suite_context.failed_count += 1
    else:
        suite_context.success_count += 1


def handle_before_suite_execution(
    context: ExecutionContext,
    event: events.BeforeTestSuiteExecution[BeforeTestSuiteExecutionPayload],
) -> None:
    # Add a context at the test suite level and record the item id.
    context.test_suite_id_to_context[
        event.payload.test_suite_id
    ] = TestSuiteExecutionContext(name=event.payload.name)


def handle_after_suite_execution(
    context: ExecutionContext,
    event: events.AfterTestSuiteExecution[AfterTestSuiteExecutionPayload],
) -> None:
    suite_context = context.test_suite_id_to_context[event.payload.test_suite_id]
    if suite_context.errored_count > 0:
        suite_context.status = Status.error
    elif suite_context.failed_count > 0:
        suite_context.status = Status.success
    else:
        suite_context.status = Status.success

    context.success_count += suite_context.success_count
    context.errored_count += suite_context.errored_count
    context.failed_count += suite_context.failed_count
    context.skipped_count += suite_context.skipped_count

    # TODO: Display the progress of the overall test and also the suite testing status.


def handle_finished(
    context: ExecutionContext, event: events.Finished[FinishedPayload]
) -> None:
    """Show the outcome of the whole testing session."""
    suite_to_status_summary: Dict[str, Dict[Union[str, Status], int]] = {}
    for suite_id, suite_context in context.test_suite_id_to_context.items():
        suite_to_status_summary[suite_context.name] = {
            "total": (
                suite_context.success_count
                + suite_context.failed_count
                + suite_context.errored_count
            ),
            "skipped": suite_context.skipped_count,
            Status.success: suite_context.success_count,
            Status.error: suite_context.errored_count,
            Status.failure: suite_context.failed_count,
        }

    click.echo(get_statistic(suite_to_status_summary))
    click.echo(get_summary(context, event))


def get_subsection(
    result: TestResult,
) -> str:
    return get_section_name(result.verbose_name)


def get_summary(
    context: ExecutionContext, event: events.Finished[FinishedPayload]
) -> str:
    message = get_summary_output(context, event)
    return get_section_name(message)


def get_summary_message_parts(context: ExecutionContext) -> List[str]:
    parts = []
    passed = context.success_count
    if passed:
        parts.append(
            f"{passed} tests passed" if passed != 1 else f"{passed} test passed"
        )
    failed = context.failed_count
    if failed:
        parts.append(
            f"{failed} tests failed" if failed != 1 else f"{failed} test failed"
        )
    errored = context.errored_count
    if errored:
        parts.append(
            f"{errored} tests errored" if errored != 1 else f"{errored} test errored"
        )
    skipped = context.skipped_count
    if skipped:
        parts.append(
            f"{skipped} tests skipped" if skipped != 1 else f"{skipped} test skipped"
        )
    return parts


def get_summary_output(
    context: ExecutionContext, event: events.Finished[FinishedPayload]
) -> str:
    parts = get_summary_message_parts(context)
    if not parts:
        message = "Empty test suite"
    else:
        message = f'{", ".join(parts)} in {event.running_time:.2f}s'
    return message


def get_section_name(title: str, separator: str = "=", extra: str = "") -> str:
    """Print section name with separators in terminal with the given title nicely centered."""
    extra = extra if not extra else f" [{extra}]"
    return f" {title}{extra} ".center(80, separator)


def get_statistic(
    suite_to_status_summary: Dict[str, Dict[Union[str, Status], int]]
) -> str:
    """Format and print statistic collected by :obj:`models.TestResult`."""
    lines = [get_section_name("SUMMARY")]

    if suite_to_status_summary:
        lines.append(get_checks_statistics(suite_to_status_summary))
    else:
        lines.append("No checks were performed.")

    return "\n".join(lines)


def get_checks_statistics(
    suite_to_status_summary: Dict[str, Dict[Union[str, Status], int]]
) -> str:
    lines = []
    for suite_name, results in suite_to_status_summary.items():
        lines.append(get_check_result(suite_name, results))
    return "Tested the suites:\n\n" + "\n".join(lines)


def get_check_result(
    suite_name: str,
    results: Dict[Union[str, Status], int],
) -> str:
    """Show results of single test suite execution."""
    success = results.get(Status.success, 0)
    total = results.get("total", 0)
    return f"{suite_name}: {success} / {total} passed"


def handle_skipped(context, event):
    if event.test_suite_id:
        suite_context = context.test_suite_id_to_context[event.test_suite_id]
        suite_context.skipped_count += 1


class TestPlanConsoleOutputHandler(EventHandler):
    def handle_event(self, context: ExecutionContext, event: events.Event) -> None:
        """Choose and execute a proper handler for the given event."""
        if isinstance(event, events.Initialized):
            pass
        if isinstance(event, events.BeforeTestSuiteExecution):
            handle_before_suite_execution(context, event)
        if isinstance(event, events.AfterTestSuiteExecution):
            handle_after_suite_execution(context, event)
        if isinstance(event, events.BeforeTestCaseExecution):
            handle_before_execution(context, event)
        if isinstance(event, events.AfterTestCaseExecution):
            handle_after_execution(context, event)
        if isinstance(event, events.BeforeTestStepExecution):
            pass
        if isinstance(event, events.AfterTestStepExecution):
            pass
        if isinstance(event, events.Skipped):
            handle_skipped(context, event)
        if isinstance(event, events.Finished):
            handle_finished(context, event)
        if isinstance(event, events.Interrupted):
            click.secho("Test plan run is interrupted.", fg="red")
        if isinstance(event, events.InternalError):
            click.echo(event.exception_with_traceback)
