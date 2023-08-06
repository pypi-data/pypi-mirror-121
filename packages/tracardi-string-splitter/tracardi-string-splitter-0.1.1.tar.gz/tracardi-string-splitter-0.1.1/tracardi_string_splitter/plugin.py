from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_string_splitter.model.model import Splitter


class SplitterAction(ActionRunner):

    def __init__(self, **kwargs):
        self.splitter = Splitter(**kwargs)

    async def run(self, payload):
        result = self.splitter.string.split(self.splitter.delimiter)
        return Result(port="payload", value={
                "result": result
            })


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_string_splitter.plugin',
            className='SplitterAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1.1',
            license="MIT",
            author="Bartosz Dobrosielski",
            init={
                "string": None,
                "delimiter": '.',
            }

        ),
        metadata=MetaData(
            name='Splitter',
            desc='String splitter',
            type='flowNode',
            width=200,
            height=100,
            icon='splitter',
            group=["Traits"]
        )
    )
